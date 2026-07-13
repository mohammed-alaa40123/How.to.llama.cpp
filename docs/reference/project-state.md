# Project state

_Last updated: 2026-07-13 09:49 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream reference used for the graph/MoE chapter: `6b4dc2116a92c5c8f2782bfe51fabe5ee66fb5ef`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Foundations deepening — interactive system map plus file-by-file subsystem synthesis**

## Completed

- MkDocs Material site, strict documentation CI, Pages deployment, health checks, source indexing, and durable run context.
- Canonical GGUF, model placement, model/context, graph/MoE, scheduler, memory-lifetime, and system-ownership pages.
- Pass A pages for public API, model/GGUF loading, runtime context/memory, scheduler, and concrete context-memory implementations.
- Exact pinned declaration and reverse-destruction map for `llama_model` and `llama_context`, including partial construction, RAII, model mappings/buffers, output and memory resources, backends, scheduler, and application teardown.
- Exact pinned generic scheduler teardown path, including event destruction, graph allocator and backend-buffer destruction, host metadata release, and borrowed lifetime dependencies.

## Latest concrete findings

- `ggml_backend_sched_free()` destroys scheduler events first, graph-allocation resources second, and host scheduler metadata last.
- The generic scheduler free path does not call `ggml_backend_sched_synchronize()`.
- Event free dispatches through `event->device->iface.event_free`, so the event's device and backend-specific event state must remain valid.
- Graph allocator free reaches `ggml_backend_buffer_free()`, which invokes concrete `free_buffer` callbacks for scheduler-owned buffer chunks.
- The scheduler borrows backend, device, and buffer-type relationships; generic code does not prove that destroying owning backend wrappers before `sched` is safe for every concrete backend.

## In progress

- Concrete backend teardown audit for CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL.
- Architecture-specific graph-builder downcasts to concrete memory-context types and exact state tensors read/written.
- Runtime evidence for synchronization, event waits, page faults, memory updates, and teardown.

## Immediate next task

Trace concrete backend teardown dependencies:

```text
backend wrapper free
→ implicit or explicit synchronization
→ device lifetime
→ event_free requirements
→ scheduler buffer free_buffer requirements
→ allocator/queue/stream dependencies
→ classify backend-before-scheduler ordering
```

Required deliverables:

1. per-backend `free`, `event_free`, `free_buffer`, and synchronization call chains;
2. device and buffer-type ownership/lifetime;
3. queued-work behavior during destruction;
4. a safety classification for the pinned context member order;
5. runtime or test evidence where available;
6. truth labels and durable context updates.

## Publication and verification state

- New page: `docs/architecture/scheduler-teardown-core.md`.
- Page commit: `d954c67d1558fb7db3b86f2e1c7fceed8e505c2f`.
- Navigation commit: `52fe517f9b62a2070c96e0c066fec3d3cb09cd53`.
- README/TODO commit: `600587c3f56c4814a56dd12dae03d64f2938ab8a`.
- Connector-side source inspection confirmed the pinned scheduler free order, event dispatch through the device, graph allocator ownership, and backend-buffer callback chain.
- Combined-status lookup for `600587c3f56c4814a56dd12dae03d64f2938ab8a` returned no statuses, so push-triggered Documentation CI, Pages deployment, and hourly-context validation remain unverified rather than failed.
- Site-specific search returned no indexed project or scheduler-teardown page. Direct opening of the Pages root and new route was rejected by the safe-URL gate because the exact URLs were absent from search results.
- No new external secondary source was introduced; the research ledger remains unchanged.

## Known blockers and caveats

- **Local validation blocker:** this environment cannot resolve `github.com`, so a checkout and local validators, tests, script checks, and strict MkDocs build cannot run.
- **CI visibility blocker:** the connected combined-status endpoint returned an empty status list and does not expose the push-triggered workflow run state.
- **Pages verification blocker:** search returned no indexed result and direct open was blocked by the safe-URL gate; live HTTP status and rendered content remain unverified.
- The generic scheduler call chain is verified, but backend-before-scheduler safety remains an open question until concrete deleters and synchronization behavior are traced.
- Mapping, allocation, physical residency, data validity, queued completion, ownership, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
