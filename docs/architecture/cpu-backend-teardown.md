# CPU backend teardown and scheduler-order classification

This page completes one concrete slice of the backend teardown audit: the ordinary CPU backend at the pinned llama.cpp revision. It answers whether destroying the CPU backend wrapper before the scheduler is safe, and why this conclusion must not be generalized to asynchronous accelerators.

## Scope and truth labels

- **Pinned baseline:** llama.cpp [`e3546c7948e3af463d0b401e6421d5a4c2faf565`](https://github.com/ggml-org/llama.cpp/commit/e3546c7948e3af463d0b401e6421d5a4c2faf565).
- **Verified:** directly established by pinned source.
- **Interpretation:** a reasoned consequence of the verified call and ownership structure.
- **Historical:** revision-sensitive behavior.
- **Open question:** not resolved by this CPU-only slice.

## Five-minute explanation

The ordinary CPU backend is structurally simpler than CUDA, Metal, Vulkan, or SYCL:

- graph execution calls `ggml_graph_compute()` directly and returns only after the CPU computation finishes;
- the backend interface has no asynchronous tensor methods, no synchronize callback, and no event record/wait callbacks;
- the CPU device advertises `async = false` and `events = false`;
- the CPU device object is static registry storage, independent of an individual backend wrapper;
- freeing the backend wrapper deletes only its per-backend work buffer and context.

Therefore the scheduler has no CPU events to destroy, no queued CPU stream work to drain, and no event object that depends on the deleted CPU backend context. Scheduler-owned CPU graph-allocation buffers are released through their buffer callbacks, not through the deleted backend wrapper.

**Verified classification:** for the ordinary pinned CPU backend, backend-before-scheduler destruction is safe.

## Exact backend free path

```text
ggml_backend_free(cpu_backend)
    └── ggml_backend_cpu_free(cpu_backend)
            ├── delete[] cpu_ctx->work_data
            ├── delete cpu_ctx
            └── delete backend wrapper
```

The CPU backend destructor does not synchronize because the interface exposes no synchronize callback and CPU graph execution is synchronous.

Pinned source:

- [`ggml_backend_cpu_free()` and CPU interface table](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-cpu/ggml-cpu.cpp#L120-L125)
- [`ggml_backend_cpu_graph_compute()`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-cpu/ggml-cpu.cpp#L172-L193)

## No queued-work contract is required

The CPU interface table sets these entries to `NULL`:

```text
set_tensor_async
get_tensor_async
set_tensor_2d_async
get_tensor_2d_async
cpy_tensor_async
synchronize
event_record
event_wait
```

The generic `ggml_backend_synchronize()` wrapper returns immediately when the backend has no synchronize callback. This is not an implicit wait; it reflects that the ordinary CPU backend does not submit work to an asynchronous device queue.

**Verified:** `ggml_backend_graph_compute_async()` still calls the CPU graph-compute callback, but that callback executes `ggml_graph_compute()` synchronously before returning.

Pinned source:

- [CPU interface table](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-cpu/ggml-cpu.cpp#L195-L212)
- [`ggml_backend_synchronize()` and graph-compute wrappers](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-backend.cpp#L416-L454)

## Device and event lifetime

The CPU device reports:

```text
async  = false
events = false
```

Its `event_new`, `event_free`, and `event_synchronize` entries are null. The registry returns a function-local static CPU device and static device context.

```text
static CPU device context
static CPU device object
        │
        ├── outlives individual CPU backend wrappers
        └── owns no scheduler event objects because events are unsupported
```

**Verified:** the scheduler cannot create CPU events through this device, so CPU scheduler teardown never enters a CPU `event_free` callback.

Pinned source:

- [CPU device capabilities and interface](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-cpu/ggml-cpu.cpp#L391-L499)
- [Static CPU device storage](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-cpu/ggml-cpu.cpp#L512-L527)

## Scheduler buffer destruction

The scheduler graph allocator owns CPU backend buffers, but generic buffer destruction calls each buffer's `free_buffer` callback and then deletes the generic buffer wrapper. It does not call back into the deleted CPU backend wrapper.

```text
scheduler free
    └── graph allocator free
            └── backend buffer free
                    ├── buffer-specific free_buffer
                    └── delete generic buffer wrapper
```

**Interpretation:** ordinary CPU scheduler buffers remain independently destructible after the per-backend CPU context is deleted because their allocation and destruction state is carried by the buffer and process-lifetime buffer type, not by `ggml_backend_cpu_context`.

Pinned source:

- [`ggml_backend_buffer_free()`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-backend.cpp#L109-L118)
- [CPU backend obtains its device from the registry](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-cpu/ggml-cpu.cpp#L219-L248)

## Safety classification

| Dependency | CPU result | Classification |
|---|---|---|
| Queued graph work | `ggml_graph_compute()` completes before return | Safe |
| Backend synchronize callback | None required or provided | Safe |
| Scheduler events | Unsupported; none created | Safe |
| Device lifetime | Static registry object | Safe |
| Backend wrapper free | Deletes only per-backend work/context/wrapper | Safe |
| Scheduler buffer free | Buffer callback path does not require CPU backend context | Safe |
| Backend-before-scheduler order | No remaining scheduler dependency on deleted CPU wrapper | **Verified safe** |

## Truth-labelled conclusion

### Verified

- Ordinary CPU graph execution is synchronous.
- The CPU backend has no synchronize or event callbacks.
- The CPU device advertises no asynchronous execution and no event support.
- The CPU device and its context are static registry objects.
- CPU backend free deletes only the backend work allocation, backend context, and wrapper.

### Interpretation

- The pinned `llama_context` reverse member order is safe for the ordinary CPU backend because scheduler teardown has no remaining dependency on the deleted CPU backend context.
- This conclusion covers the standard CPU backend only; optional CPU-adjacent buffer types such as AMX, KleidiAI, repack, HBM, or vendor libraries require their own buffer-deleter audit where used.

### Historical

- CPU async support, event support, buffer implementations, and registry lifetime may change in later revisions.

### Open questions

- Do all optional CPU extra-buffer implementations preserve the same backend-independent destruction property?
- Are there sanitizer tests that construct a CPU scheduler, free its backend wrapper first, and then free the scheduler?
- Which accelerator backends preserve device and allocator state independently of their backend wrappers?

## Next audit slice

Audit CUDA teardown: backend-context destruction, stream synchronization, event destruction, device and buffer-type lifetime, `cudaFree` behavior, CUDA graph resources, and whether scheduler buffers remain valid after the CUDA backend wrapper is deleted.
