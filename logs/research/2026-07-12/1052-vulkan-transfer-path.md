# Vulkan transfer path and compatibility matrix

- Run time: 2026-07-12 10:52 Africa/Cairo
- Scope: complete the pinned Vulkan buffer transfer trace from allocation through blocking and scheduler-level asynchronous copies
- Baseline: `ggml-org/llama.cpp@e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Verified

### Allocation and host visibility

- `ggml_vk_create_buffer_device()` selects ordered Vulkan memory-property candidates based on `prefer_host_memory`, UMA detection, `disable_host_visible_vidmem`, and `allow_sysmem_fallback`.
- Host-visible selected allocations are mapped into `vk_buffer::ptr`.
- The default Vulkan GGML buffer type still leaves `.is_host = NULL`, so the generic GGML contract treats its tensor pointer as opaque.
- The dedicated Vulkan host-buffer type uses `ggml_vk_host_malloc()`, wraps the pointer with CPU buffer operations, inherits CPU `is_host`, and replaces the free callback with Vulkan host unregistration/free.
- Failed Vulkan host registration falls back to an ordinary CPU buffer.

### Blocking buffer operations

- `ggml_backend_vk_buffer_set_tensor()` delegates to `ggml_vk_buffer_write()`.
- Host-visible coherent destinations receive direct `memcpy()` writes.
- Non-host-visible destinations use coherent staging, a transfer command, queue submission, and `waitForFences()` before return.
- `ggml_backend_vk_buffer_get_tensor()` waits before exposing bytes to the caller.
- Host-visible UMA reads insert a shader/transfer-write to host-read barrier, submit, wait for a fence, then `memcpy()` from mapped memory.
- Other reads copy through coherent staging, wait for a fence, and then execute the deferred CPU copy.
- Blocking `cpy_tensor` accepts Vulkan sources.
- Same-device Vulkan copies record `vkCmdCopyBuffer` and wait for a fence.
- Cross-device Vulkan copies stage through source-device host-visible memory and then execute a blocking destination write.

### Backend asynchronous operations

- Backend set/get callbacks support the default Vulkan device buffer and dedicated Vulkan host-buffer type.
- Registered Vulkan host pointers can be copied through an open compute or transfer command context without immediate synchronization.
- Ordinary unregistered host pointers use `ctx->sync_staging` and call `ggml_vk_synchronize()` before the callback returns.
- Thus the backend `async` callback has pointer-dependent completion behavior.

### Scheduler asynchronous copy

- Destination must be the default Vulkan device-buffer type.
- Same-device Vulkan-device sources are accepted and recorded as `vkCmdCopyBuffer` in the destination compute context.
- Cross-device Vulkan sources return `false`.
- Host-visible sources are accepted only when `ggml_vk_host_get()` proves that the source pointer belongs to a Vulkan-registered host allocation.
- Ordinary CPU and CPU_Mapped/mmap pointers return `false`.
- A successful callback means queued work, not host-visible completion.

### Synchronization

- `ggml_vk_synchronize()` submits pending transfer work, ends/submits compute work, joins transfer and compute queues with a timeline semaphore when required, submits a fence, waits for it, and performs deferred output CPU copies.
- Backend synchronization therefore establishes both device completion and CPU output-copy completion.

## Interpretation

- Vulkan registration is the actual host-transfer fast-path capability; generic host visibility alone is insufficient for scheduler overlap.
- Internal Vulkan mapping and GGML `is_host` are deliberately separate contracts.
- Cross-device Vulkan support is compatibility-oriented and synchronizing, not a peer asynchronous transfer path.
- UMA may remove a transfer stage but does not remove the barrier and fence required before host reads.
- CPU_Mapped/mmap-to-Vulkan avoids generic full-tensor heap staging, but it still takes a synchronized blocking Vulkan set path and can include file-backed page faults.

## Historical

- These findings are pinned to `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- Later revisions may alter memory preference lists, host-buffer device ownership, staging reuse, transfer queues, event integration, and cross-device support.

## Open questions

- Actual memory heaps chosen by Android vendor drivers for each preference list.
- Fence latency and transfer/compute overlap on Qualcomm, ARM, Imagination, Samsung, and Mesa implementations.
- Whether later llama.cpp revisions provide device-specific host-buffer types.
- Whether later revisions add direct cross-device Vulkan transfer.

## Artifacts changed

- `docs/lifecycle/vulkan-buffer-capabilities.md`
- `docs/lifecycle/buffer-compatibility.md`
- `README.md`
- `docs/reference/project-state.md`
- `docs/reference/research-log.md`
- `logs/research/2026-07-12/1052-vulkan-transfer-path.md`

## Validation

- Connector-side source reads verified exact pinned branches for allocation, writes, reads, blocking copies, host-buffer allocation, backend async set/get, scheduler async copy, and synchronization.
- Local clone failed because the execution environment could not resolve `github.com`; local `mkdocs build --strict` could not run.
- GitHub Actions and Pages status must be checked through the repository interfaces and recorded separately.

## Next step

- Trace SYCL host, shared/USM, and device allocations; blocking set/get/direct copy; scheduler async-copy acceptance; queue/event ordering; and return-time completion.
