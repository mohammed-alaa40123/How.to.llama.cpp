# OpenCL process-lifetime queue/context ownership resolution

- Run time: 2026-07-15 09:10 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: use the source-bearing pinned artifact to resolve `shared_context`, `backend_ctx->queue`, backend-wrapper references, scheduler events, and deterministic release behavior

## Artifact and validation

GitHub Actions run `29392658206` succeeded and uploaded artifact `8333854723`, containing:

- `opencl-lifecycle-pinned-e3546c7.json`;
- `ggml-opencl-pinned-e3546c7.cpp`;
- `opencl-lifecycle-pinned-e3546c7.sha256`.

The downloaded source was 1,168,071 bytes. The report and source hashes recomputed locally matched the manifest values:

- report: `31b708767b506629ef1bdf9aebfa18c54d56554cd15745f1be77d35eac0d26ba`;
- source: `8e2f6fdd532de1b78dbfe14d14921df05d1b37c5b73d415d620a787f635fde6d`.

The manifest currently records workflow-relative `build/reports/...` paths. Hashes match, but `sha256sum -c` from the artifact root requires path adjustment; a future small workflow cleanup can emit basenames.

## Verified

- OpenCL registration creates one `shared_context` with all selected device IDs.
- The same `cl_context` handle is copied into each supported `ggml_backend_opencl_device_context::context`.
- Device contexts are stored in static vector `g_ggml_backend_opencl_dev_ctxs`.
- The source comment immediately above that vector says the devices live as long as the process, so their contexts do too.
- `ggml_cl_init()` lazily allocates one `ggml_backend_opencl_context` per device and stores its raw pointer in `dev_ctx->backend_ctx`.
- That context receives the device context's shared `cl_context` and creates one `backend_ctx->queue`.
- `ggml_backend_opencl_device_init()` increments `backend_ctx->ref_count` for each backend wrapper.
- Backend free calls `ggml_cl_free()`, which invokes `backend_ctx->free()`.
- `backend_ctx->free()` calls `clFinish(queue)` before decrementing the wrapper reference count.
- On the final wrapper reference it releases pooled KV/dequant image and sub-buffer views, but it does not delete `backend_ctx`, release the command queue, or release the OpenCL context.
- The backend capability table advertises `events = false`, and event record/wait callbacks are null. Therefore there is no scheduler-owned OpenCL event object whose deleter can outlive a wrapper.
- Buffer wrappers own `cl_mem` references locally; their deleters do not require the deleted `ggml_backend` wrapper object.
- The complete pinned translation unit contains no direct `clReleaseCommandQueue()` or `clReleaseContext()` call.

## Interpretation

Pinned OpenCL backend-wrapper destruction is structurally supported: each wrapper free completes its shared per-device queue before dropping its reference, while the queue, context, programs, kernels, and device backend context remain in process-lifetime static state. Buffer destruction after wrapper destruction does not depend on the wrapper itself.

This is not deterministic cleanup. OpenCL queue/context handles and the lazily allocated per-device backend context are not explicitly destroyed in the pinned translation unit. Process or ICD teardown is relied upon for final reclamation. Repeated dynamic-library load/unload or registry teardown inside one process remains unproven.

## Historical

Previous runs could locate the two direct creation calls but not declarations or final owners because the report preserved only three-line windows. Preserving the complete pinned source resolved the ownership chain in one source-level pass.

## Open questions

- Does the optional Adreno binary-kernel loader retain and close its dynamic-library handle?
- Which enqueue-then-release groups rely only on OpenCL command-retention semantics?
- Should upstream add explicit registry/process-exit teardown for per-device queues, contexts, programs, kernels, and backend contexts?
- Are repeated registration/unregistration or shared-library unload scenarios supported?

## Documentation changes

Updated:

- `.github/workflows/opencl-lifecycle-report.yml` to preserve source and checksums;
- `docs/architecture/opencl-build-and-buffer-lifetimes.md` with the resolved ownership chain;
- `docs/architecture/backend-teardown-comparison.md` with the stronger pinned classification;
- `docs/reference/project-state.md` with artifact and next-task state.

The research ledger is unchanged because no external source was added or reclassified; the evidence remains the already-ledgered pinned llama.cpp source.

## Classification

> **Backend-wrapper order supported; deterministic process-exit release omitted.**

## Next priority

Resolve the optional Adreno dynamic-library handle and kernel-destruction ordering, then classify retention-only enqueue/release groups. In parallel, implement the first CPU repack ASan/LSan destruction fixture.
