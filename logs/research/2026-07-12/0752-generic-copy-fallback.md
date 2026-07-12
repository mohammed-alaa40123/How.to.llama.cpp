# Generic tensor-copy fallback and staging

- Run time: 2026-07-12 07:52 Africa/Cairo
- Upstream baseline: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: generic fallback after rejected backend asynchronous copy, including host-visible branches, destination-buffer direct copy, full host staging, completion, and representative CUDA/Metal paths

## Verified

- `ggml_backend_tensor_copy_async()` first calls the destination backend's optional `cpy_tensor_async` callback.
- If the callback is absent or returns `false`, GGML synchronizes both source and destination backends before calling the blocking `ggml_backend_tensor_copy()` helper.
- The blocking helper uses the source tensor pointer directly when the source buffer is host-visible.
- It uses the destination tensor pointer directly when only the destination buffer is host-visible.
- If neither side is host-visible, the destination buffer receives an opportunity to perform a direct blocking `cpy_tensor` operation.
- If direct copy is also rejected, GGML allocates `ggml_nbytes(src)`, reads the entire source into that host allocation, writes the allocation into the destination, and frees it.
- CPU/mmap and CUDA-host sources are outside the pinned CUDA device-to-device asynchronous callback, but both are host-visible and therefore avoid the generic full-size heap allocation.
- The generic fallback returns only after source/destination queue drains and the blocking buffer copy returns.

## Interpretation

- An async-copy rejection is a correctness-preserving serialization point, not a harmless function-call substitution.
- Synchronizing both backends can remove overlap on both sides of a scheduler split boundary.
- CPU/mmap-to-accelerator copies can combine page-fault latency, queue-drain latency, and host-to-device transfer latency.
- Avoiding the generic `malloc()` branch does not imply zero-copy or asynchronous behavior.
- Unsupported device-to-device pairs can create transient RSS and allocator pressure by staging the complete tensor through pageable host memory.

## Historical

- These findings apply to the pinned baseline. Newer scheduler or backend revisions may add specialized async paths, reusable staging pools, or different event/ownership rules.

## Open questions

- Exact destination-buffer `cpy_tensor` support matrix across CPU, CUDA, Metal, Vulkan, SYCL, RPC, and Android backends.
- Whether later revisions reuse staging allocations.
- Measured page faults, queue stalls, transfer overlap, and temporary RSS in representative prefill and one-token decode runs.

## Artifact

- `docs/lifecycle/generic-copy-fallback.md`
- `mkdocs.yml`

## Evidence

- `ggml/src/ggml-backend.cpp`: `ggml_backend_tensor_copy_async`, `ggml_backend_tensor_copy`, `ggml_backend_buffer_copy_tensor`, tensor set/get dispatch, and synchronization wrapper.
- Existing CUDA, Metal, and scheduler documentation for concrete async acceptance/rejection behavior.

## Validation

- Connector-side pinned source reads confirmed the exact generic call chain and branch order.
- Connector-side repository reads verify publication and navigation.
- Local clone/build remains blocked by DNS resolution of `github.com`; GitHub Actions and Pages are checked separately.

## Next step

- Trace concrete buffer-level `set_tensor`, `get_tensor`, and `cpy_tensor` implementations and build a backend buffer-pair compatibility matrix.