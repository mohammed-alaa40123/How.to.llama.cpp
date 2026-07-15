# Cross-backend synchronous tensor-set contract

- Run time: 2026-07-15 23:49 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Pinned source: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: compare the generic tensor-set wrapper and two accelerator backends to classify the 24 remaining OpenCL waits

## Verified

The pinned generic wrapper `ggml_backend_tensor_set()` validates the tensor, resolves the owning buffer, and directly calls `buf->iface.set_tensor(...)`. It performs no synchronization of its own. Completion behavior is therefore delegated to each buffer backend.

The pinned CUDA buffer implementation enqueues the host-to-device copy on `cudaStreamPerThread` and immediately calls `cudaStreamSynchronize(cudaStreamPerThread)` before returning. Its 2-D set path follows the same enqueue-then-stream-synchronize structure.

The pinned SYCL buffer implementation first waits all device queues, then submits the host-to-device copy to the default queue and calls `.wait()` on the returned operation before returning. On non-Windows builds it copies mmap-backed input into a temporary host buffer, waits for the device copy, and only then frees that host buffer.

| Layer | Pinned behavior | Return point |
|---|---|---|
| Generic `ggml_backend_tensor_set()` | Direct dispatch to buffer interface | Whatever the backend callback guarantees |
| CUDA `ggml_backend_cuda_buffer_set_tensor()` | `cudaMemcpyAsync(...)` followed by `cudaStreamSynchronize(...)` | Copy complete |
| SYCL `ggml_backend_sycl_buffer_set_tensor()` | queue copy followed by `.wait()` | Copy complete |
| OpenCL `ggml_backend_opencl_buffer_set_tensor()` | blocking upload plus explicit waits for conversion/expansion kernels | Converted persistent representation complete |

The public header distinguishes ordinary tensor-set functions from explicitly asynchronous tensor-set functions, but does not state the ordinary function's device-completion guarantee in prose.

## Interpretation

The pinned implementations establish a strong **de facto synchronous tensor-set contract**:

```text
ggml_backend_tensor_set() returns
        ↓
backend-specific upload and required representation conversion are complete
        ↓
the destination tensor is ready for immediate backend use
```

This is implementation evidence, not a normative documented promise. Nevertheless, removing the remaining OpenCL conversion waits would make OpenCL observably weaker than CUDA and SYCL: OpenCL could return while persistent quantized auxiliary buffers were still being materialized.

The 24 remaining OpenCL waits should therefore be classified as **required by the pinned de facto synchronous return contract**:

- 21 waits before `clReleaseMemObject(data_device)` are not needed for temporary-object lifetime, but are still completion barriers for the converted destination representation before return.
- 3 return-boundary expansion waits ensure persistent MoE scale/min buffers are complete before return.

The event-ownership repair remains independent. Retaining these waits requires releasing their command events; the generated 46-release patch is still the behavior-preserving first change.

## Historical

The previous run narrowed the three lexical `nested_scope_exit` records to return-boundary expansion-completion waits. This run supplies the missing cross-backend evidence and resolves the broader 21/3 synchronization classification for the pinned baseline.

## Open questions

- Should the de facto synchronous behavior be documented explicitly in `ggml-backend.h` upstream?
- Does current upstream retain the same CUDA, SYCL, and OpenCL behavior, or has the contract changed since the pinned revision?
- Should the OpenCL classifier rename the three records to `return_boundary_expansion_completion` and annotate all 24 as `required_by_sync_set_contract`?
- Should the generated 46-release patch be rebased and submitted upstream before any synchronization optimization?

## Validation

- Read the complete project startup context before editing.
- Inspected pinned `ggml/src/ggml-backend.cpp` around `ggml_backend_tensor_set()`.
- Inspected pinned CUDA `ggml_backend_cuda_buffer_set_tensor()` and its stream synchronization.
- Inspected pinned SYCL `ggml_backend_sycl_buffer_set_tensor()` and its queue waits.
- Reconciled this evidence with the previously audited OpenCL 21 temporary-input-release and 3 return-boundary expansion waits.

## Next priority

Rebase the generated behavior-preserving 46-event release patch against current upstream, determine whether the leak still exists, and prepare an upstream-ready patch or issue. Keep synchronization unchanged unless the public contract is intentionally revised.
