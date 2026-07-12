# Vulkan buffer and synchronization capabilities

> **Source baseline:** llama.cpp commit [`e3546c7948e3af463d0b401e6421d5a4c2faf565`](https://github.com/ggml-org/llama.cpp/commit/e3546c7948e3af463d0b401e6421d5a4c2faf565)
>
> This page records only behavior verified directly in the pinned Vulkan backend. Exact host/device `set_tensor`, `get_tensor`, and direct-copy branches remain a follow-up rather than being inferred from Vulkan API conventions.

## Five-minute explanation

The pinned Vulkan backend exposes two important but different capabilities:

- its ordinary device buffer type does **not** report `is_host`, so generic GGML code must treat device-buffer tensor pointers as not CPU-dereferenceable;
- the Vulkan device advertises asynchronous graph execution, a separate host-buffer type, and backend events.

This means “Vulkan supports host buffers” does not mean the main Vulkan device buffer is host-visible. It means the backend can provide a distinct host-buffer type for transfer-oriented storage while device tensors remain governed by Vulkan memory and queue ordering.

## Verified

### Device-buffer host visibility

`ggml_backend_vk_buffer_type_interface` leaves `.is_host` as `NULL`. GGML's generic capability helper interprets a missing callback as false. Therefore the ordinary Vulkan device buffer is not host-visible through the GGML buffer contract.

### Device capabilities

`ggml_backend_vk_device_get_props()` reports:

- `async = true`;
- `host_buffer = true`;
- `buffer_from_host_ptr = false`;
- `events = true`.

The backend also returns `ggml_backend_vk_host_buffer_type()` from its device host-buffer query. Host-buffer support is therefore explicit and separate from the default device-buffer type.

### Queue and synchronization model

The implementation maintains compute and transfer queues, command pools, submissions, semaphores, and event state. Queue submission is protected against simultaneous submission to the same underlying queue.

Backend synchronization calls `ggml_vk_synchronize(ctx)` and then graph cleanup. Event state uses Vulkan events for command-side waits and a timeline semaphore for host synchronization; the source comment explains that polling only a Vulkan event would not guarantee command-buffer completion.

### Graph execution

The Vulkan backend batches graph work into command buffers and may submit after node-count, FLOP, almost-ready, or end-of-graph thresholds. Internal hazard tracking detects overlapping unsynchronized tensor regions and inserts buffer synchronization when at least one overlapping access is a write.

## Interpretation

- Vulkan's scheduler-visible asynchronous capability means work may be submitted without global host completion; it does not make buffer-level reads or writes automatically asynchronous.
- A distinct Vulkan host buffer can reduce or specialize staging costs, but it should not be described as zero-copy until the pinned allocation and transfer branches are traced.
- `events = true` provides a mechanism for dependency ordering and completion, but the exact scheduler copy path depends on the backend's copy callbacks and the source/destination buffer pair.
- Internal graph hazard tracking is separate from cross-backend scheduler ordering. One protects Vulkan command-buffer accesses; the other coordinates split copies and backend execution.

## Historical

These findings apply only to the pinned revision. Vulkan memory-type selection, host-buffer implementation, event handling, and transfer callbacks may differ in later llama.cpp revisions.

## Open questions

- What Vulkan memory properties are selected for the ordinary device buffer and dedicated host buffer on discrete versus integrated GPUs?
- Do pinned host-buffer `set_tensor` and `get_tensor` operations use direct mapped memory, explicit flush/invalidate, or staging copies?
- Which source buffers are accepted by Vulkan's blocking `cpy_tensor` callback, if present?
- Does the backend implement scheduler-level `cpy_tensor_async` for Vulkan-to-Vulkan or host-to-Vulkan pairs at this revision?
- Which operations wait a fence before returning, and which only enqueue work?
- How does Android Vulkan behavior differ across unified-memory SoCs and vendor drivers?

## Pinned source map

| Concern | Pinned source |
|---|---|
| Default Vulkan buffer type and absent `is_host` callback | [`ggml-vulkan.cpp`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-vulkan/ggml-vulkan.cpp#L285-L297) |
| Vulkan buffer ownership fields | [`vk_buffer_struct`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-vulkan/ggml-vulkan.cpp#L1027-L1046) |
| Event and timeline-semaphore rationale | [`vk_event`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-vulkan/ggml-vulkan.cpp#L1063-L1076) |
| Backend synchronization wrapper | [`ggml_backend_vk_synchronize()`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-vulkan/ggml-vulkan.cpp#L15703-L15710) |
| Vulkan device capabilities and host-buffer query | [`ggml_backend_vk_device_get_props()`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-vulkan/ggml-vulkan.cpp#L17130-L17172) |

## Next investigation

Trace the concrete Vulkan device-buffer and host-buffer interfaces from allocation through `set_tensor`, `get_tensor`, copy callbacks, queue submission, fence waits, and return-time completion. Then add exact Vulkan rows to the source-buffer × destination-buffer matrix.
