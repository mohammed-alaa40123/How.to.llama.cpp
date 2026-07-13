# Project state

_Last updated: 2026-07-13 10:50 Africa/Cairo_

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
- Exact pinned declaration and reverse-destruction map for `llama_model` and `llama_context`.
- Exact pinned generic scheduler teardown path.
- Ordinary pinned CPU backend teardown classification.

## Latest concrete findings

- CPU graph execution calls `ggml_graph_compute()` directly and completes before the backend callback returns.
- The ordinary CPU backend interface has no async tensor-copy methods, synchronize callback, or event record/wait callbacks.
- The CPU device advertises `async = false` and `events = false`; its event callbacks are null.
- The CPU device and device context are static registry objects, independent of individual backend wrappers.
- `ggml_backend_cpu_free()` deletes only the per-backend work allocation, CPU context, and backend wrapper.
- Scheduler-owned ordinary CPU buffers are destroyed through buffer callbacks rather than through the deleted CPU backend context.
- Backend-before-scheduler destruction is therefore **verified safe for the ordinary pinned CPU backend**.

## In progress

- CUDA teardown audit: streams, events, `cudaFree`, graph resources, device and buffer-type lifetime.
- Remaining concrete backend teardown audits for Metal, Vulkan, SYCL, RPC, CANN, and OpenCL.
- Optional CPU extra-buffer teardown audit.
- Architecture-specific graph-builder downcasts and exact state tensors.
- Runtime evidence for synchronization, event waits, page faults, memory updates, and teardown.

## Immediate next task

Trace CUDA teardown dependencies:

```text
CUDA backend wrapper free
→ stream and graph-resource destruction
→ implicit or explicit synchronization
→ scheduler event_free
→ scheduler buffer cudaFree/free_buffer
→ device and buffer-type lifetime
→ classify backend-before-scheduler ordering
```

Required deliverables:

1. exact CUDA backend free and context-destructor chain;
2. stream/event/graph-resource synchronization behavior;
3. buffer and buffer-type ownership;
4. queued-work requirements during `cudaFree` and event destruction;
5. safety classification for the pinned context member order;
6. truth labels and durable context updates.

## Publication and verification state

- New page: `docs/architecture/cpu-backend-teardown.md`.
- Page commit: `9f8a58354d6f24d2cef2494ab14a4b14ac1fc347`.
- Navigation commit: `a59a922df471b6caa5720900ebc479755ce62e68`.
- README/TODO commit: `b1e59e34dc8f74ecf79e1a766590970fc4f6212a`.
- Connector-side source inspection confirmed synchronous CPU graph execution, null async/synchronize/event callbacks, static CPU device lifetime, and the narrow backend-free ownership boundary.
- No new external secondary source was introduced; the research ledger remains unchanged.
- Latest push-triggered workflow and Pages verification are checked after the final context commits; exact results or blockers are recorded below and in the README TODOs.

## Known blockers and caveats

- **Local validation blocker:** this environment has no usable checkout and cannot run the repository's local validation commands.
- **CI visibility caveat:** the connected commit-status endpoint may return no statuses for push-triggered Actions; an empty result means unverified, not failed.
- **Pages visibility caveat:** direct site verification may be blocked if the Pages URL is not indexed or retrievable through the available web path.
- The CPU conclusion covers the ordinary CPU backend only. AMX, KleidiAI, repack, HBM, BLAS, and other optional CPU-adjacent buffer implementations require separate review.
- Mapping, allocation, physical residency, data validity, queued completion, ownership, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
