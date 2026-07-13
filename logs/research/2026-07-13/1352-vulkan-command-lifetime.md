# Vulkan command and synchronization lifetime increment

- Run time: 2026-07-13 13:52 Africa/Cairo
- Scope: command-pool topology, command-buffer reuse, fences, semaphores, events, synchronous transfer completion, and the remaining teardown gap
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Added `docs/architecture/vulkan-command-lifetime.md` and linked it under Architecture navigation.

## Verified

- `vk_command_pool` stores a Vulkan command pool, stable command-buffer records, and a borrowed queue pointer.
- The pinned source says command pools exist per `(context, queue)` and per `(device, queue)` pairing.
- `ggml_vk_command_pool_cleanup()` calls `resetCommandPool()` only under the explicit precondition that its command buffers are complete, then marks tracked records reusable.
- Synchronous buffer read, same-device copy, and GPU memset helpers record into temporary contexts, submit with the device fence, wait with `UINT64_MAX`, reset the fence, and only then clean reusable command pools.
- Deferred host copies in the read path execute after the fence wait.
- Binary semaphores, timeline semaphores, and Vulkan events are pooled in the backend context and selected through reusable indices.
- `ggml_backend_vk_graph_compute()` is organized around transfer and compute command submission, so return from graph compute is not itself a universal host completion boundary.

## Interpretation

- Command-pool reset is a reuse operation after completion, not a synchronization primitive.
- Fence waits are the clearest host completion boundary in the inspected synchronous helper paths.
- Timeline semaphores and events may establish device ordering without proving host completion.
- The final backend free chain must separately account for context-owned and device-owned pools and synchronization objects.

## Historical

- Queue sharing, pool topology, batching, and synchronization object reuse are revision-sensitive.

## Open questions

- Which exact pinned function performs final backend synchronization?
- Does final synchronization cover both compute and transfer queues and all timeline-semaphore work?
- What is the destruction order for context command pools, descriptor/query pools, semaphores, events, and buffers?
- Do scheduler-owned Vulkan events and buffers retain valid device state after backend-wrapper deletion?
- Is backend-before-scheduler destruction safe, conditional, or unsafe for the pinned Vulkan backend?

## Sources inspected

Repository context:

- complete `README.md`;
- `docs/reference/project-state.md`;
- `docs/reference/research-log.md`;
- `docs/reference/research-ledger.md`;
- latest detailed note `logs/research/2026-07-13/1249-metal-backend-teardown.md`;
- current `mkdocs.yml`.

Pinned upstream source:

- `ggml/src/ggml-vulkan/ggml-vulkan.cpp`;
- prior generic scheduler, context teardown, and backend teardown audits.

No new external secondary source passed the verification bar, so the research ledger was unchanged.

## Validation

- Connector-side inspection confirmed the command-pool topology, pooled synchronization state, explicit completion precondition for command-pool reset, and fence-based synchronous helper sequence.
- New page, navigation entry, project-state update, research-log update, README TODO update, and this detailed note were written through the repository API.
- Local command validation remains blocked because the environment cannot resolve `github.com` and has no usable checkout.
- GitHub Actions and Pages checks are performed after this note; exact results or blockers are recorded in project state and README TODOs.

## Next priority

Finish the exact Vulkan backend/context free chain and classify backend-before-scheduler destruction.
