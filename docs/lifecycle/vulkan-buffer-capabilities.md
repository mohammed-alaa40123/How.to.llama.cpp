# Vulkan buffer transfers and synchronization

> **Source baseline:** llama.cpp commit [`e3546c7948e3af463d0b401e6421d5a4c2faf565`](https://github.com/ggml-org/llama.cpp/commit/e3546c7948e3af463d0b401e6421d5a4c2faf565)
>
> This page distinguishes the ordinary blocking buffer interface from the backend-level asynchronous callbacks used by the scheduler. Function names containing `async` do not by themselves prove that a call returns before completion.

## Five-minute explanation

The pinned Vulkan backend has three materially different transfer paths:

1. **Blocking buffer operations.** `set_tensor`, `get_tensor`, and blocking Vulkan-to-Vulkan `cpy_tensor` wait for a Vulkan fence before returning whenever a queue copy is required.
2. **Accepted backend asynchronous copies.** Same-device Vulkan-to-Vulkan copies and copies from registered Vulkan host memory can be recorded into a compute or transfer command context and return before host completion.
3. **Asynchronous API fallback.** If ordinary host memory is not registered as a Vulkan host allocation, backend `set_tensor_async` and `get_tensor_async` create or reuse coherent staging memory and call `ggml_vk_synchronize()` before returning. The API entry point is asynchronous in name, but this branch is synchronizing.

The device-memory allocator is also adaptive. On UMA devices it prefers memory that is device-local, host-visible, and host-coherent; on discrete devices it may prefer device-local memory, ReBAR-style host-visible device memory, or system-memory fallback depending on runtime flags and available memory types. GGML still leaves the ordinary Vulkan buffer type's `is_host` callback unset, so generic GGML code must not dereference its synthetic tensor pointer directly.

## Memory types and ownership

### Verified

`ggml_vk_create_buffer_device()` chooses memory properties according to device and configuration:

| Condition | Preferred flags | Fallback |
|---|---|---|
| `prefer_host_memory` | host-visible + host-coherent | device-local |
| UMA device | device-local + host-visible + host-coherent | device-local, then host-visible + host-coherent |
| host-visible VRAM disabled, system fallback allowed | device-local | host-visible + host-coherent |
| host-visible VRAM disabled, no system fallback | device-local | none |
| ordinary discrete path with system fallback | device-local + host-visible + host-coherent | device-local, then host-visible + host-coherent |
| ordinary discrete path without system fallback | device-local + host-visible + host-coherent | device-local |

Any chosen host-visible allocation is mapped and stored in `vk_buffer::ptr`. However, the default Vulkan GGML buffer type still leaves `.is_host = NULL`. This separates internal Vulkan mapping capability from the generic GGML promise that `tensor->data` is a directly dereferenceable process pointer.

The dedicated Vulkan host-buffer type uses `ggml_vk_host_malloc()`, wraps the returned registered pointer with the CPU buffer interface, reports the CPU buffer's `is_host` capability, and replaces only the free callback so Vulkan unregisters/frees the allocation. If pinned allocation fails, it falls back to an ordinary CPU buffer.

### Interpretation

- A mapped Vulkan allocation is not automatically a generic host buffer. The backend may use its internal mapping for direct writes or UMA reads while preserving an opaque GGML device-buffer contract.
- The dedicated host buffer is CPU-addressable and Vulkan-registered when allocation succeeds. This registration is what enables scheduler-level host-to-Vulkan asynchronous copies without an extra staging allocation.
- The current host-buffer type is tied to Vulkan device 0; the source includes a TODO noting that a device-specific host-buffer type would require llama.cpp changes.

## Blocking `set_tensor`

### Verified

`ggml_backend_vk_buffer_set_tensor()` delegates to `ggml_vk_buffer_write()`.

- If the destination allocation is host-visible and coherent, the implementation writes directly with `memcpy()` and returns.
- Otherwise it creates a temporary transfer command context, records a copy from a coherent host staging buffer, submits it with a device fence, waits indefinitely for that fence, resets it, and cleans command pools before returning.

For non-host-visible destinations, ordinary unregistered host input therefore follows:

```text
host pointer
  -> coherent mapped sync-staging buffer
  -> vkCmdCopyBuffer to Vulkan destination
  -> queue submit
  -> waitForFences
  -> return
```

### Completion guarantee

The blocking buffer call is complete on return. Either the bytes were copied directly into coherent mapped memory or the transfer fence has completed.

## Blocking `get_tensor`

### Verified

`ggml_backend_vk_buffer_get_tensor()` delegates to `ggml_vk_buffer_read()`.

- On UMA, when the allocation is host-visible, it records a barrier from shader/transfer writes to host reads, submits, waits for a fence, and only then copies from mapped memory into the caller's pointer.
- Otherwise it records a copy into coherent staging memory, submits it, waits for a fence, and then performs the deferred CPU `memcpy()` into the destination pointer.

Even the mapped UMA read waits for prior GPU writes before CPU access. Host visibility does not remove the completion barrier.

## Blocking Vulkan-to-Vulkan `cpy_tensor`

### Verified

The destination buffer callback accepts the source only when `ggml_backend_buffer_is_vk(src->buffer)` is true.

- **Same device:** record `vkCmdCopyBuffer`, submit on the transfer queue, wait for a fence, reset the fence, and return `true`.
- **Different Vulkan devices:** allocate/reuse source-device coherent staging, perform a blocking source-device copy into staging, then perform the destination buffer's blocking write. This is a two-stage host-mediated copy and returns `true` only after both stages complete.
- **Non-Vulkan source:** return `false`, allowing the generic tensor-copy decision tree to select a host-visible branch or full host staging.

### Interpretation

The blocking Vulkan callback is broader than the asynchronous callback: it supports cross-device Vulkan copies, but only by serializing through host-visible staging.

## Backend `set_tensor_async` and `get_tensor_async`

### Verified

Both callbacks require the tensor buffer type to be either the backend's default Vulkan device type or the dedicated Vulkan host-buffer type.

For writes:

- If the input pointer belongs to a Vulkan-registered host allocation, the backend records a direct buffer copy in the transfer or compute context and returns without synchronizing.
- If the input is ordinary unregistered host memory, it copies into `ctx->sync_staging`, records the Vulkan copy, and calls `ggml_vk_synchronize(ctx)` before returning.

For reads:

- If the output pointer belongs to registered Vulkan host memory, the backend records the copy and returns without synchronizing.
- If it is ordinary host memory, it records a copy into `ctx->sync_staging`, registers a deferred CPU copy, and calls `ggml_vk_synchronize(ctx)`; synchronization waits for GPU completion and then executes the deferred CPU copy.

### Interpretation

The asynchronous interface has a conditional completion contract:

| Host pointer kind | Queue work recorded? | Synchronizes before return? |
|---|---:|---:|
| Vulkan-registered host allocation | Yes | No |
| Ordinary unregistered host pointer | Yes, through backend staging | Yes |

This is why backend capability flags or callback names are insufficient evidence for overlap. Pointer provenance decides whether the pinned implementation can preserve asynchronous behavior.

## Scheduler-level `cpy_tensor_async`

### Verified

`ggml_backend_vk_cpy_tensor_async()` accepts only these destination/source combinations:

| Source | Destination | Accepted? | Mechanism | Completion on return |
|---|---|---:|---|---|
| Vulkan device buffer, same Vulkan device | Vulkan default device buffer | Yes | `vkCmdCopyBuffer` in destination compute context | queued, not host-complete |
| Vulkan device buffer, different device | Vulkan default device buffer | No | generic fallback handles it | not applicable |
| Vulkan registered host buffer | Vulkan default device buffer | Yes | copy from registered Vulkan buffer in transfer/compute context | queued, not host-complete |
| Ordinary CPU or CPU_Mapped pointer | Vulkan default device buffer | No | generic synchronized fallback | not applicable |
| Any source | Vulkan host-buffer destination | No | destination must be default Vulkan device type | not applicable |
| Zero-sized tensor | any accepted destination | Yes | no work | complete trivially |

The host-source branch first checks generic host visibility and then calls `ggml_vk_host_get()` to prove that the pointer belongs to a Vulkan-registered allocation. An ordinary CPU or mmap pointer therefore returns `false` even though it is host-visible.

### Scheduler consequence

When this callback returns `false`, the generic scheduler path synchronizes the source and destination backends before invoking blocking tensor copy. CPU/mmap-to-Vulkan avoids the emergency full-size heap allocation because the source is host-visible, but the Vulkan destination `set_tensor` path is blocking and may stage plus wait for a fence.

## Backend synchronization

### Verified

`ggml_vk_synchronize()`:

1. submits any pending transfer context;
2. ends and submits the compute context when present;
3. if transfer and compute queues need joining, submits a timeline-semaphore wait to the compute queue;
4. submits a fence signal;
5. waits for the fence;
6. executes deferred output `memcpy()` operations;
7. resets retained contexts and pending state.

Backend synchronization therefore establishes both device command completion and completion of deferred CPU-visible output copies.

## Runtime validation points

For Android or desktop Vulkan traces, record:

```text
vulkan_device_name, vendor_id, uma,
prefer_host_memory, disable_host_visible_vidmem, allow_sysmem_fallback,
selected_memory_property_flags,
source_buffer_type, destination_buffer_type,
source_registered_with_vulkan,
async_copy_accepted,
transfer_queue_used,
sync_staging_bytes,
fence_wait_us,
copy_submit_us, copy_total_us,
minor_fault_delta, major_fault_delta, rss_delta
```

The most important Android experiment is to compare integrated-GPU drivers where default device memory is host-visible/coherent against drivers that force staging. The GGML `is_host` result remains false in both cases, so instrumentation must inspect Vulkan memory flags rather than infer them from the GGML buffer name.

## Truth-labelled findings

### Verified

- Default Vulkan buffers leave GGML `is_host` unset even when the selected Vulkan memory type is internally mapped.
- Dedicated Vulkan host buffers use registered host allocation and report host visibility.
- Blocking Vulkan set/get/device-copy paths establish completion before returning.
- Same-device Vulkan-to-Vulkan scheduler copies are accepted asynchronously.
- Registered Vulkan-host-to-device scheduler copies are accepted asynchronously.
- Cross-device Vulkan and ordinary CPU/mmap sources are rejected by the scheduler async-copy callback.
- Backend async set/get callbacks synchronize on the ordinary-host staging branch.

### Interpretation

- Registered host buffers are the pinned backend's real overlap-enabling host-transfer mechanism.
- UMA reduces staging and transfer cost but does not eliminate command ordering or host-read barriers.
- Cross-device support in the blocking callback is a compatibility path, not an overlapping peer-copy path.

### Historical

These findings apply to pinned commit `e3546c7948e3af463d0b401e6421d5a4c2faf565`. Later Vulkan revisions may change memory preferences, host registration, transfer-queue use, staging reuse, and scheduler copy acceptance.

### Open question

- How Qualcomm, ARM, Imagination, Samsung, and Mesa Android Vulkan drivers map these preference lists to actual memory heaps.
- Whether later llama.cpp revisions provide device-specific host-buffer types or direct cross-device Vulkan transfers.
- Runtime evidence for overlap, staging pressure, and fence latency during prompt processing and one-token decode.

## Pinned source map

| Concern | Pinned source |
|---|---|
| Device-buffer memory-property selection | [`ggml_vk_create_buffer_device()`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-vulkan/ggml-vulkan.cpp#L3253-L3290) |
| Blocking write/read and fence waits | [`ggml_vk_buffer_write_2d()` and `ggml_vk_buffer_read_2d()`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-vulkan/ggml-vulkan.cpp#L7934-L8111) |
| Blocking same-device and cross-device copy | [`ggml_vk_buffer_copy()`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-vulkan/ggml-vulkan.cpp#L8113-L8145) |
| Device buffer interface and direct-copy acceptance | [`ggml_backend_vk_buffer_cpy_tensor()`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-vulkan/ggml-vulkan.cpp#L15216-L15309) |
| Dedicated Vulkan host-buffer allocation | [`ggml_backend_vk_host_buffer_type_alloc_buffer()`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-vulkan/ggml-vulkan.cpp#L15360-L15427) |
| Backend async set/get branches | [`ggml_backend_vk_set_tensor_2d_async()` and `get_tensor_2d_async()`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-vulkan/ggml-vulkan.cpp#L15455-L15578) |
| Scheduler asynchronous copy acceptance | [`ggml_backend_vk_cpy_tensor_async()`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-vulkan/ggml-vulkan.cpp#L15580-L15640) |
| Fence and deferred-copy synchronization | [`ggml_vk_synchronize()`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-vulkan/ggml-vulkan.cpp#L15642-L15712) |

## Next investigation

Trace SYCL host, USM, and device-buffer behavior with the same distinction between blocking buffer operations, backend asynchronous callbacks, and scheduler-level copy acceptance.
