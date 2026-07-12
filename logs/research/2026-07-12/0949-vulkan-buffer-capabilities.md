# Vulkan buffer capability boundary

- Run time: 2026-07-12 09:49 Africa/Cairo
- Scope: establish the pinned Vulkan backend's buffer host-visibility, device capability, event, queue, and synchronization boundary without guessing untraced transfer branches

## Verified

- The ordinary Vulkan buffer type leaves `.is_host` unset, so GGML treats Vulkan device-buffer pointers as not host-visible.
- The Vulkan device advertises asynchronous execution, a dedicated host-buffer type, and events, but does not advertise wrapping arbitrary host pointers.
- The backend keeps compute and transfer queues, command pools, submissions, semaphores, and event state.
- Vulkan event state combines command-side Vulkan events with a timeline semaphore for host synchronization.
- Backend synchronization calls `ggml_vk_synchronize()` and then graph cleanup.
- Graph execution batches command buffers and inserts internal synchronization when overlapping unsynchronized tensor regions include a write.

## Interpretation

- Dedicated Vulkan host-buffer support is distinct from device-buffer host visibility.
- Scheduler-visible asynchronous capability does not prove buffer-level set/get completion behavior.
- Vulkan graph hazard tracking and cross-backend scheduler ordering solve different synchronization problems.

## Historical

- These findings apply to llama.cpp commit `e3546c7948e3af463d0b401e6421d5a4c2faf565`; later Vulkan memory and event paths may differ.

## Open questions

- Exact device and host memory-property selection on discrete and integrated GPUs.
- Exact `set_tensor`, `get_tensor`, blocking copy, and scheduler async-copy branches.
- Fence-wait versus enqueue-only return points.
- Android Vulkan behavior across unified-memory SoCs and vendor drivers.

## Artifacts changed

- `docs/lifecycle/vulkan-buffer-capabilities.md`
- `mkdocs.yml`
- `README.md`
- `docs/reference/project-state.md`
- `docs/reference/research-log.md`
- `logs/research/2026-07-12/0949-vulkan-buffer-capabilities.md`

## Validation

- Connector-side source reads confirmed the pinned symbols and page source links.
- Strict MkDocs and live Pages rendering remain delegated to GitHub Actions because no local checkout is available in this run.

## Next step

- Trace the concrete Vulkan device-buffer and host-buffer interfaces through allocation, set/get, copy callbacks, queue submission, and fence completion, then add exact matrix rows.
