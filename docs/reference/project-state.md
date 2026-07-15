# Project state

_Last updated: 2026-07-15 09:51 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream reference used for the graph/MoE chapter: `6b4dc2116a92c5c8f2782bfe51fabe5ee66fb5ef`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Foundations deepening — interactive system map plus file-by-file subsystem synthesis**

## Completed

- MkDocs Material site, strict documentation CI, Pages deployment, health checks, source indexing, and durable run context.
- Canonical GGUF, model placement, model/context, graph/MoE, scheduler, memory-lifetime, and system-ownership pages.
- Pass A pages for the public API/minimal example, model/GGUF loader, runtime context/memory, backend scheduler, and concrete context-memory implementations.
- Exact pinned declaration and reverse-destruction map for `llama_model` and `llama_context`.
- Generic scheduler plus ordinary CPU, CUDA, Metal, Vulkan, SYCL, RPC, and CANN teardown audits.
- Cross-backend teardown comparison matrix and reusable teardown audit method.
- Pinned OpenCL build composition, exact lifecycle inventory, source-backed queue/context ownership, and Adreno binary-library lifetime classification.
- Line-aware generated source indexing with pinned file and symbol links.
- Guided end-to-end inference atlas with clickable reading paths.
- Bounded CPU repack, AMX, KleidiAI, and SpacemiT IME extra-buffer lifetime audits.
- Cross-implementation CPU optional-buffer comparison and portable destruction-test matrix.
- Implementation-ready CPU optional-buffer destruction-harness specification with admission, correctness, lifetime-ordering, and sanitizer assertions.
- Documentation CI validation commands split into named steps with verbose unittest output.
- Python unit tests split into source-index, boundary, unsupported-syntax, function-try-block, OpenCL lifecycle, and interactive-link suites, followed by a full discovery guard.
- Source-index exact-line support for attributes, trailing returns, bounded constraints, operators, qualified special members, parenthesized initializer lists, and delegating constructors.
- Negative boundary tests plus bounded telemetry for braced/multiline constructor initializers and constructor function-try-blocks.
- Bounded OpenCL lifecycle-call extractor for direct queue/context creation and retention plus completion/wait and queue/context/program/kernel/event/buffer releases.
- C/C++ comment and quoted-literal masking for lifecycle extraction while preserving exact source offsets and line numbers.
- Function-try initializer-line guard preventing `try : member(...) {` from becoming a false ordinary-function symbol.
- Optional bounded original-source context for every lifecycle record, with exact clamped line ranges and backward-compatible default output.
- GitHub-hosted pinned OpenCL workflow that verifies the exact baseline checkout and preserves the complete source, generated report, and SHA-256 manifest.
- Verified OpenCL backend-wrapper order: queue completion occurs before wrapper reference drop, while the actual device/backend context remains process-lifetime.
- Verified OpenCL scheduler events are unsupported and buffer deleters use buffer-local `cl_mem` ownership rather than the destroyed wrapper.
- Resolved optional Adreno binary-library lifetime: the raw loader handle is not retained or closed, so the library, exported lookup function, and accepted binary-kernel path remain process-lifetime.

## Latest concrete findings

- Workflow run `29392658206` succeeded and uploaded artifact `8333854723`, expiring on 2026-08-14.
- The artifact contains the exact pinned source, the 558-call JSON report, and a two-entry SHA-256 manifest.
- Recomputed hashes matched the manifest: report `31b708767b506629ef1bdf9aebfa18c54d56554cd15745f1be77d35eac0d26ba`; source `8e2f6fdd532de1b78dbfe14d14921df05d1b37c5b73d415d620a787f635fde6d`.
- Device registration creates one `shared_context` and copies it into each supported `ggml_backend_opencl_device_context`.
- Device contexts are held by static `g_ggml_backend_opencl_dev_ctxs`; the source explicitly states those devices and contexts live as long as the process.
- `ggml_cl_init()` lazily allocates one `ggml_backend_opencl_context` per device, stores it in `dev_ctx->backend_ctx`, copies the shared context, and creates one command queue.
- Backend-wrapper initialization increments `ref_count`; wrapper free calls `clFinish(queue)` and decrements it.
- Final-wrapper cleanup releases pooled image/sub-buffer views but does not delete the per-device backend context or release the command queue/context.
- Backend capabilities advertise `events = false`, and event callbacks are null; there is no scheduler-owned OpenCL event deleter that can outlive the wrapper.
- Buffer-local `cl_mem` deleters do not require the deleted `ggml_backend` wrapper.
- Under `GGML_OPENCL_USE_ADRENO_BIN_KERNELS`, `kernel_lib_handle` is a block-local raw handle. `libdl.h` provides a deleter, but the loader neither owns nor closes the handle.
- Only `get_adreno_bin_kernel_func` is retained in the process-lifetime backend context. A successfully loaded library and a loaded library with a missing symbol both remain mapped until process teardown.
- Five pinned paths consume library-provided bytes through `clCreateProgramWithBinary()`, create a kernel, and release the temporary program reference.
- Pinned classification is now **backend-wrapper order supported; deterministic process-exit release omitted; Adreno binary library process-lifetime by leaked handle**.

## In progress

- Classification of enqueue-then-release groups that rely on OpenCL retention semantics rather than explicit waits.
- Determining whether repeated OpenCL registration, registry teardown, or shared-library unload is supported.
- Fixing checksum-manifest paths to use artifact-root basenames for direct `sha256sum -c` verification.
- Regeneration of the pinned source inventory with line-aware records, pinned source links, and unsupported-syntax counts.
- Implementation of the first CPU repack backend-free-before-buffer-free test fixture under ASan/LSan.
- CPU extra-buffer destruction tests for KleidiAI, AMX, and SpacemiT plus TSan and hardware-specific cleanup coverage.
- Shared generated metadata for the static inference atlas and interactive workflow.
- Runtime overlays for page faults, scheduler copies, event waits, KV/recurrent growth, and backend queues.
- CANN reset semantics, RPC completion, CUDA all-stream coverage, SYCL all-queue coverage, and Vulkan query-pool ownership.

## Immediate next task

```text
Inspect preserved pinned OpenCL source
  → classify temporary cl_mem release immediately after enqueue
  → separate retention-only-safe paths from host-storage lifetime hazards
  → document any site requiring an explicit wait or event
  → update OpenCL teardown page and comparison matrix
```

In parallel or if blocked, implement the admitted CPU repack `MUL_MAT` fixture with reference comparison, CPU backend-wrapper free, repack-buffer free, and ASan/LSan repetition.

## Publication and verification state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`.
- Added detailed note `logs/research/2026-07-15/0951-opencl-adreno-library-lifetime.md`.
- Pinned lifecycle/source workflow run `29392658206` completed successfully for the source-preservation increment.
- The generated artifact was downloaded and its report/source hashes were verified.
- Documentation CI and the pinned OpenCL workflow for the final durable-state head must be checked before the run closes.
- Full local checkout validation remains unavailable because direct GitHub DNS resolution is blocked in this runtime.
- Public Pages verification remains blocked for branch-only content until PR #1 merges.

## Known blockers and caveats

- **Deterministic-release gap:** the pinned translation unit intentionally keeps device/backend contexts process-lifetime and contains no explicit queue/context release or per-device backend-context deletion path.
- **Adreno library lifetime:** the optional binary-kernel loader loses its raw `dl_handle`. This prevents early unload but omits deterministic release and also retains invalid-symbol loads until process exit.
- **Checksum usability caveat:** the manifest hashes are correct, but entries include `build/reports/...` paths, so direct `sha256sum -c` from the artifact root needs path adjustment.
- **Local validation blocker:** direct cloning fails with `Could not resolve host: github.com`; GitHub-hosted Actions are the authoritative validation path for this branch.
- **Pages verification blocker:** branch-added content cannot deploy until PR #1 merges; live response verification remains unavailable independently of strict-build success.
- **Lifecycle-extractor caveat:** selected direct APIs and bounded context are navigation evidence only; wrapper constructors, ownership, error paths, macro wrappers, disabled code, raw strings, and semantic ordering still require human source review.
- **Source-index caveat:** same-line standard attributes, trailing-return definitions, bounded same-line constraints, bounded operators, qualified out-of-class special members, and bounded parenthesized member/delegating constructor initializer lists are recognized. Braced and multiline constructor initializers and constructor function-try-blocks remain intentionally omitted from navigation but are counted as bounded candidates.
- **Telemetry caveat:** unsupported-syntax counts are prioritization signals, not parser-completeness metrics.
- **Harness caveat:** a skipped hardware-gated path is not evidence that the lifetime ordering passed.
- **SpacemiT caveat:** buffer lifetime is distinct from thread-local TCM leases and process-level pool-manager lifetime.
- Mapping, allocation, residency, validity, command completion, ownership, reset, thread-local leases, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.