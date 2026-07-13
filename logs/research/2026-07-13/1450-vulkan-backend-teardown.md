# Vulkan backend teardown increment

- Run time: 2026-07-13 14:50 Africa/Cairo
- Scope: exact backend free chain, queue completion, context-owned resource release, scheduler event/buffer independence, and backend-before-scheduler classification
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Added `docs/architecture/vulkan-backend-teardown.md` and linked it under Architecture navigation.

## Verified

- `ggml_backend_vk_free()` calls `ggml_vk_cleanup()` before deleting the Vulkan backend context and generic backend wrapper.
- `ggml_vk_cleanup()` resets the current unsubmitted compute context, then calls `ggml_vk_synchronize()` before destroying context-owned Vulkan resources.
- Cleanup destroys graph-local binary/timeline semaphores, temporary buffers, context events, fences, descriptor pools, compute command pools, and transfer semaphore/pool state after synchronization.
- Scheduler Vulkan events own a timeline semaphore and reusable/submitted Vulkan events; their free callback uses persistent backend-device registry state rather than the deleted backend context.
- Scheduler Vulkan buffers own a buffer-local context with a shared `vk_device` and `vk_buffer`; their free callback does not dereference the deleted backend context.
- Vulkan backend-device wrappers are stored in a function-static registry vector.
- Ordinary pinned Vulkan backend-before-scheduler destruction is therefore verified safe for the resources inspected.

## Interpretation

- Vulkan backend free provides an explicit completion boundary comparable to the pinned Metal path and stronger than the pinned CUDA-family path.
- Event and buffer lifetime safety depends on retained device-level ownership, not on the continued existence of the individual backend wrapper.
- Backend cleanup protects backend-owned submissions; it does not synchronize unrelated application Vulkan work.

## Historical

- Queue topology, transfer policy, event implementation, command-pool ownership, and registry lifetime are revision-sensitive.

## Open questions

- The optional performance query pool is created/replaced during graph compute, but no explicit `destroyQueryPool(ctx->query_pool)` appeared in the inspected cleanup body.
- Immediate context-destruction validation tests remain to be located or added.
- Persistent Vulkan device/process-exit teardown still needs a separate audit.

## Sources inspected

Repository context:

- complete `README.md`;
- `docs/reference/project-state.md`;
- `docs/reference/research-log.md`;
- `docs/reference/research-ledger.md`;
- latest detailed note `logs/research/2026-07-13/1352-vulkan-command-lifetime.md`;
- current `mkdocs.yml`.

Pinned upstream source:

- `ggml/src/ggml-vulkan/ggml-vulkan.cpp`;
- prior generic scheduler, context teardown, CPU, CUDA, Metal, and Vulkan command-lifetime audits.

No new external secondary source passed the verification bar, so the research ledger was unchanged.

## Validation

- Connector-side inspection confirmed the explicit cleanup synchronization boundary, context-owned destruction order, scheduler event/device independence, buffer-local shared-device ownership, and static registry lifetime.
- New page, navigation entry, README TODO update, project-state update, research-log update, and this detailed note were written through the repository API.
- Local command validation remains blocked because the execution environment cannot resolve `github.com` and has no usable checkout.
- GitHub Actions and Pages checks are performed after this note; exact results or blockers are recorded in project state and README TODOs.

## Next priority

Audit the pinned SYCL backend teardown and classify backend-before-scheduler destruction.
