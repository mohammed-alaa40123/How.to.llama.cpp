# CUDA asynchronous tensor-copy branches

- Run time: 2026-07-12 05:50 Africa/Cairo
- Upstream baseline: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: exact acceptance, transfer, ordering, and fallback branches in `ggml_backend_cuda_cpy_tensor_async()`

## Verified

- Tensor views resolve eligibility through their owning `view_src->buffer`.
- Both backend objects must be CUDA backends.
- Both resolved buffers must be CUDA device buffers; CPU/mmap and CUDA host buffers are rejected.
- Each backend context's device must match its tensor buffer's device.
- A same-backend copy queues `cudaMemcpyAsync(..., cudaMemcpyDeviceToDevice, source_stream)` and relies on same-stream order.
- Different backend objects on one CUDA device queue D2D copy on the source stream, record a lazily created source-context event, and make the destination stream wait.
- Different CUDA devices use `cudaMemcpyPeerAsync()` when peer copy is enabled.
- `GGML_CUDA_NO_PEER_COPY` rejects cross-device copies with `false`.
- Every accepted branch copies `ggml_nbytes(dst)` and returns `true` without host synchronization.
- Every unsupported branch returns `false` so the generic scheduler can use its synchronized copy fallback.

## Interpretation

- The callback is a device-resident fast path, not a universal host/device asynchronous transfer API.
- A successful return means transfer commands and dependencies were queued; it does not establish host visibility.
- A false return is capability negotiation rather than a copy failure, but it may introduce a synchronization bubble in the fallback path.
- CUDA host buffers are intentionally outside this callback's accepted set despite belonging to the CUDA backend family.

## Open questions

- Exact generic fallback route for each CPU/mmap/CUDA-host to CUDA-device combination.
- Measured overlap and contention for same-device and peer copies during prefill and one-token decode.
- Whether later revisions changed the single source-context `copy_event`, stream selection, or peer-copy capability gating.
- Metal command-buffer and event semantics compared with CUDA source-stream/event/destination-wait ordering.

## Artifact

- `docs/lifecycle/cuda-async-copy.md`
- `mkdocs.yml`

## Evidence

- `ggml/src/ggml-cuda/ggml-cuda.cu`
  - `ggml_backend_cuda_cpy_tensor_async()` lines 2332-2385 at the pinned revision
  - `ggml_backend_cuda_synchronize()` lines 2387-2393
  - CUDA interface registration around lines 4321-4333
- Existing scheduler fallback analysis in `docs/lifecycle/backend-scheduler-execution.md`

## Validation

- Connector-side pinned source reads verified every documented callback branch.
- Connector-side repository reads will verify the page, navigation, state, README, and logs after publication.
- Local clone and `mkdocs build --strict` remain blocked because this execution environment cannot resolve `github.com`.
- GitHub Actions and Pages status are checked separately at the end of this run.

## Next step

- Trace the pinned Metal backend's graph submission, buffer copies, event/shared-event ordering, and host synchronization boundary, then compare it with CUDA.
