# Scheduler core teardown and lifetime dependencies

- Run time: 2026-07-13 09:49 Africa/Cairo
- Scope: pinned generic scheduler free order, event and graph-buffer deleter chains, borrowed object dependencies, and the limit of the generic backend-order conclusion
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Added `docs/architecture/scheduler-teardown-core.md` and linked it under Architecture navigation.

## Verified

- `ggml_backend_sched_new()` stores borrowed backend pointers and buffer-type pointers.
- Parallel schedulers create events through each backend device.
- `ggml_backend_sched_free()` frees events first, the graph allocator second, and scheduler host metadata last.
- The scheduler free function does not explicitly synchronize.
- `ggml_backend_event_free()` dereferences `event->device` and calls the concrete device event destructor.
- `ggml_gallocr_free()` releases unique virtual buffers and allocator state.
- Virtual-buffer destruction reaches `ggml_backend_buffer_free()`, which calls the concrete `free_buffer` callback before deleting the generic buffer wrapper.
- The generic scheduler never frees the backend wrappers stored in `sched->backends`.

## Interpretation

- A valid scheduler teardown needs more than a live scheduler pointer: the event device, buffer types, allocator state, and callback dependencies must remain usable.
- Synchronization is the clearest queued-work completion boundary but does not fix invalid ownership order.
- Backend-before-scheduler destruction is safe only when concrete backend contracts keep event and buffer-deleter dependencies alive independently of the backend wrapper.

## Historical

- Event ownership, copy-slot count, graph allocator structure, and destruction order are revision-sensitive.

## Open questions

- Does each pinned backend keep its device object alive independently of backend instances?
- Do event destructors wait for, cancel, or assume completion?
- Do buffer destructors require a live stream, command queue, allocator, or backend context?
- Does backend wrapper free synchronize or invalidate scheduler-owned resources?
- Are immediate-destruction-after-async-submission tests present?

## Sources inspected

Repository context:

- complete `README.md`;
- `docs/reference/project-state.md`;
- `docs/reference/research-log.md`;
- `docs/reference/research-ledger.md`;
- latest detailed note `logs/research/2026-07-13/0915-interactive-slug-validator-fix.md`;
- current `mkdocs.yml`.

Pinned upstream source:

- `ggml/src/ggml-backend.cpp`;
- `ggml/src/ggml-alloc.c`.

No new external secondary source was introduced, so the research ledger was unchanged.

## Validation

- Connector-side re-fetch of pinned source confirmed the scheduler free sequence and event/device dispatch.
- Connector-side re-fetch confirmed graph allocator ownership and backend-buffer callback destruction.
- The new page and navigation were written successfully through the repository API.
- Local checkout and command validation remain blocked because this environment cannot resolve `github.com`.
- Combined status lookup returned no statuses for the increment commit, so push-triggered workflow state remains unverified.
- Site-specific search returned no indexed result, and direct Pages opening was rejected by the safe-URL gate; live HTTP and rendered-page verification remain blocked.

## Next priority

Trace concrete CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL `free`, `event_free`, `free_buffer`, synchronization, and queued-work behavior. Classify backend-before-scheduler destruction as verified safe, conditional, or unsafe for the pinned revision.
