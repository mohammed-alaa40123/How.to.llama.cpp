# CPU and CUDA backend execution semantics

- Run time: 2026-07-12 04:51 Africa/Cairo
- Upstream baseline: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: concrete CPU and CUDA graph submission, copies, events, synchronization, and host-visible completion

## Verified

- The CPU backend stores a thread count, optional `ggml_threadpool_t`, reusable work memory, and abort settings.
- `ggml_backend_cpu_graph_compute()` plans the graph and returns the result of `ggml_graph_compute()` directly, so the scheduler call does not return while CPU graph work remains in flight.
- The pinned CPU backend leaves asynchronous tensor-copy, synchronize, event-record, and event-wait callbacks unset.
- CUDA graph compute queues kernels or launches a captured CUDA graph on the backend stream and returns without a trailing stream synchronization.
- CUDA implements scheduler events with `cudaEventRecord` and `cudaStreamWaitEvent`.
- The CUDA interface supplies asynchronous tensor operations, peer-copy, synchronize, graph-compute, and event callbacks.
- CUDA ordinary buffer set/get/copy paths use asynchronous CUDA primitives followed by immediate `cudaStreamSynchronize`, making those buffer-interface calls synchronous to the caller.
- CUDA device capabilities advertise asynchronous operation and conditionally advertise event support depending on peer-copy build configuration.

## Interpretation

- CPU threadpool parallelism is internal parallelism inside a blocking backend callback; it is not scheduler-level asynchronous submission.
- `ggml_backend_graph_compute_async()` means “do not force generic global synchronization,” not “every backend returns before execution completes.”
- CUDA event waits are device-side stream dependencies, whereas CUDA synchronization is the host completion boundary.
- The presence of an API named `Async` or a call to `cudaMemcpyAsync` is insufficient evidence of caller-visible asynchrony when the implementation immediately synchronizes.

## Open questions

- Exact accepted source/destination cases in `ggml_backend_cuda_cpy_tensor_async()`.
- Observable prompt/decode overlap on discrete PCIe GPUs, UMA systems, and multi-GPU configurations.
- Metal command-buffer and event semantics compared with CUDA streams.
- Later PRs that changed peer-copy capability, event ordering, or CUDA graph reuse.

## Artifact

- `docs/lifecycle/cpu-cuda-backend-semantics.md`
- `mkdocs.yml`

## Evidence

- `ggml/src/ggml-cpu/ggml-cpu.cpp`
  - `ggml_backend_cpu_context`
  - `ggml_backend_cpu_graph_compute()`
  - `ggml_backend_cpu_i`
- `ggml/src/ggml-cuda/ggml-cuda.cu`
  - CUDA buffer set/get/copy functions
  - `ggml_backend_cuda_graph_compute()`
  - `ggml_backend_cuda_event_record()`
  - `ggml_backend_cuda_event_wait()`
  - `ggml_backend_cuda_interface`
  - CUDA device capability declaration

## Validation

- Connector-side source reads verified the pinned CPU and CUDA implementations and the new documentation file on `main`.
- Local clone and `mkdocs build --strict` remain blocked because the execution environment cannot resolve `github.com`.
- GitHub Actions and the Pages endpoint are checked separately at the end of this run; unresolved results remain explicit TODOs.

## Next step

- Trace `ggml_backend_cuda_cpy_tensor_async()` branch by branch, then compare CUDA with Metal or Vulkan.