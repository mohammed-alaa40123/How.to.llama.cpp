# Scheduler core teardown and lifetime dependencies

This page traces the pinned core teardown path for `ggml_backend_sched_t`. It deliberately stops before claiming that every concrete accelerator backend is safe: the generic scheduler code proves which objects are released and which interfaces are called, while backend-specific synchronization and allocator behavior require separate audits.

## Scope and truth labels

- **Pinned baseline:** llama.cpp [`e3546c7948e3af463d0b401e6421d5a4c2faf565`](https://github.com/ggml-org/llama.cpp/commit/e3546c7948e3af463d0b401e6421d5a4c2faf565).
- **Verified:** directly established by the pinned source.
- **Interpretation:** a reasoned consequence that still depends on backend contracts.
- **Historical:** behavior that is revision-sensitive.
- **Open question:** not resolved by the generic scheduler implementation alone.

## Five-minute explanation

The scheduler is not only a graph planner. It owns three important classes of resources:

1. backend events used as copy-slot reuse fences;
2. graph-allocation buffers created through backend buffer types;
3. host-side graph, hash-table, split, and assignment metadata.

`ggml_backend_sched_free()` releases them in that order: events first, graph allocator second, then the scheduler's host allocations. It does **not** call `ggml_backend_sched_synchronize()` first.

That detail matters because the scheduler stores borrowed backend, device, and buffer-type pointers. Event destruction dispatches through `event->device->iface.event_free`; graph-allocation destruction dispatches through each backend buffer's `free_buffer` callback. Therefore scheduler destruction still needs the objects and callback state behind those borrowed pointers to remain usable.

## Construction establishes borrowed relationships

`ggml_backend_sched_new()` copies caller-provided backend pointers into `sched->backends` and obtains or copies the corresponding buffer types into `sched->bufts`. In parallel mode it creates one event per backend and copy slot through the backend's device. Finally it creates a graph allocator from the buffer-type array.

```text
caller-owned backend wrapper
        │
        ├── borrowed by sched->backends[b]
        ├── exposes device
        │       └── creates sched->events[b][c]
        └── supplies buffer type
                └── borrowed by sched->galloc
```

**Verified:** the generic scheduler does not take ownership of the backend wrappers. It stores their pointers but never calls `ggml_backend_free()` during scheduler teardown.

Pinned source:

- [`ggml_backend_sched_new()`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-backend.cpp#L1729-L1796)

## Exact free order

At the pinned revision, `ggml_backend_sched_free()` performs this sequence:

```text
for each backend b
    for each copy slot c
        ggml_backend_event_free(events[b][c])

 ggml_gallocr_free(galloc)
 ggml_free(ctx)
 ggml_hash_set_free(hash_set)
 free(splits)
 free(hv_tensor_backend_ids)
 free(hv_tensor_copies)
 free(node_backend_ids)
 free(leaf_backend_ids)
 free(prev_node_backend_ids)
 free(prev_leaf_backend_ids)
 free(context_buffer)
 free(graph.nodes)
 free(graph.leafs)
 free(sched)
```

**Verified:** there is no explicit scheduler synchronization at the beginning of this function.

Pinned source:

- [`ggml_backend_sched_free()`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-backend.cpp#L1798-L1821)

## Event destruction still dispatches through the device

The generic event free wrapper is small but lifetime-critical:

```text
ggml_backend_event_free(event)
    └── event->device->iface.event_free(event->device, event)
```

**Verified:** event destruction dereferences the device pointer stored in the event and invokes the device's backend-specific event destructor.

This means that destroying a backend wrapper before the scheduler is safe only if the device object and its event-destruction state remain valid independently of that wrapper. The generic code does not prove that contract for every backend.

Pinned source:

- [`ggml_backend_event_free()`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-backend.cpp#L533-L538)

## Graph allocator destruction reaches backend buffer callbacks

The graph allocator stores borrowed buffer-type pointers and owns virtual buffers allocated from those types. During `ggml_gallocr_free()` it releases each unique virtual buffer. Each virtual buffer releases its backend buffer chunks, and generic backend-buffer destruction calls the concrete `free_buffer` callback before deleting the wrapper.

```text
ggml_gallocr_free
    └── ggml_vbuffer_free
            └── ggml_backend_buffer_free(chunk)
                    ├── chunk->iface.free_buffer(chunk)
                    └── delete chunk wrapper
```

**Verified:** scheduler teardown can execute backend-specific memory deallocation code after entering `ggml_gallocr_free()`.

Pinned source:

- [`ggml_gallocr_free()`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-alloc.c#L539-L580)
- [`ggml_backend_buffer_free()`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-backend.cpp#L109-L118)

## What the generic code proves

### Verified

- Scheduler events are destroyed before graph-allocation buffers.
- The graph allocator owns backend buffer chunks but borrows buffer-type objects.
- Scheduler host metadata is freed only after events and graph buffers.
- The scheduler does not own or free the backend wrappers in `sched->backends`.
- `ggml_backend_sched_free()` does not explicitly synchronize queued work.
- Event and buffer destruction invoke backend-specific callbacks.

### Interpretation

- A safe teardown boundary requires more than keeping the `ggml_backend_sched` struct alive. Device objects, buffer types, allocator state, queues, and any callback context used by event or buffer deleters must also remain valid.
- Calling `ggml_backend_sched_synchronize()` before destruction is the clearest application-level completion boundary, but synchronization alone does not repair an invalid object-lifetime order.
- If a concrete backend's wrapper destructor invalidates device-event state or allocator state used by scheduler-owned resources, freeing that wrapper before `sched` is a lifetime hazard.

### Historical

- The number of copy slots, event ownership, graph allocator structure, and destruction order are revision-sensitive.
- Newer scheduler-copy work must be documented separately rather than retroactively changing the pinned conclusion.

### Open questions

- Does each pinned backend keep its device object alive independently of individual backend wrappers?
- Do concrete event destructors wait for, cancel, or assume completion of recorded work?
- Do concrete buffer destructors require a live stream, command queue, allocator, or backend context?
- Does backend-wrapper destruction implicitly synchronize or invalidate resources still owned by the scheduler?
- Are there tests that destroy a context immediately after asynchronous graph submission?

## Current conclusion on `llama_context` member order

The pinned `llama_context` declaration causes owning backend wrappers to be destroyed before the scheduler smart pointer during reverse member destruction.

**Verified conclusion:** the generic scheduler teardown path still invokes device and backend-buffer callbacks after backend-wrapper destruction begins.

**Open conclusion:** the generic code alone cannot validate that ordering for all concrete backends. The ordering is safe only where the concrete backend guarantees that event devices, buffer types, allocation contexts, and deleter dependencies outlive the individual backend wrapper.

Until the concrete backend audit is complete, portable application code should synchronize outstanding work and explicitly destroy/reset the scheduler before releasing owning backend wrappers whenever the API and object structure permit it.

## Next audit slice

Trace concrete `free`, `event_free`, `free_buffer`, and synchronization implementations for CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL. Record for each backend:

- what object owns the device and buffer type;
- whether backend free synchronizes;
- what event free requires;
- what buffer free requires;
- whether queued work may still reference scheduler buffers;
- whether backend-before-scheduler destruction is verified safe, conditionally safe, or unsafe.
