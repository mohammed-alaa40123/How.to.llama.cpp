# Project state

_Last updated: 2026-07-13 12:49 Africa/Cairo_

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
- Pinned CUDA backend teardown dependency audit and conditional safety classification.
- Pinned Metal backend teardown audit and verified-safe backend-before-scheduler classification.

## Latest concrete findings

- `ggml_backend_metal_free()` explicitly calls `ggml_metal_synchronize()` before releasing the Metal context and backend wrapper.
- Synchronization waits for `cmd_buf_last`, checks graph and extra command-buffer status, and releases completed extra command buffers.
- `ggml_metal_free()` then releases retained graph/extra command buffers, dynamic pipelines, the encoding block, the dispatch queue, and the context-owned copy event.
- The Metal command queue is device-owned rather than backend-context-owned in the pinned design.
- Scheduler Metal events own independent `MTLSharedEvent` objects; their free path does not require a live `ggml_metal` context.
- Scheduler shared/private/mapped buffers own buffer-local contexts and use static device state for residency-set removal and `MTLBuffer` release.
- Mapped Metal buffers release wrapper views but do not own the underlying mapped host bytes.
- Backend-before-scheduler destruction is verified safe for the ordinary pinned Metal backend because backend free establishes queued-work completion and later scheduler deleters retain valid device-level dependencies.

## In progress

- Vulkan teardown audit: queues, fences/events, command pools/buffers, allocator-backed buffers, synchronization, and scheduler ordering.
- Remaining concrete backend teardown audits for SYCL, RPC, CANN, and OpenCL.
- Optional CPU extra-buffer teardown audit.
- CUDA concurrent-stream synchronization coverage.
- Architecture-specific graph-builder downcasts and exact state tensors.
- Runtime evidence for synchronization, event waits, page faults, memory updates, and teardown.

## Immediate next task

Trace Vulkan teardown dependencies:

```text
Vulkan backend wrapper free
→ queue/device synchronization
→ command-buffer and command-pool release
→ fence/semaphore/event destruction
→ allocator-backed buffer release
→ scheduler event and buffer lifetime
→ classify backend-before-scheduler ordering
```

Required deliverables:

1. exact Vulkan backend/context free chain;
2. queue, command-buffer, fence/semaphore, and synchronization behavior;
3. buffer, allocator, and buffer-type ownership;
4. queued-work requirements during resource release;
5. safety classification for the pinned context member order;
6. truth labels and durable context updates.

## Publication and verification state

- New page: `docs/architecture/metal-backend-teardown.md`.
- Page commit: `f74a3ca31ba9a61022f114c176a22063912aa022`.
- Navigation commit: `322a5bc8920fde2ce7ca24dca5e05c74120e7559`.
- README/TODO commit: `20c7404071f02da542632954ab9349b5cc4f50b7`.
- Detailed-note commit: `ca5fcac1460e8490c681804f1e98322f8b5ebcb4`.
- Research-log commit: `21caccb2a9721244c0e876ad8b089e360fd59941`.
- Connector-side source inspection confirmed the explicit Metal backend-free synchronization path, command-buffer/context release sequence, scheduler event independence, shared/private/mapped buffer ownership, residency-set cleanup, and static device/registry lifetime.
- The new page was re-fetched from `main` and contains the expected verified-safe classification, teardown graph, truth labels, and source map.
- Commit-scoped workflow lookup for `21caccb2a9721244c0e876ad8b089e360fd59941` returned `workflow_runs: []`; Documentation CI, Pages deployment, and hourly-context validation are unverified rather than confirmed failed.
- Site-specific searches for the project root and `architecture/metal-backend-teardown/` returned no indexed results. The available web safety gate therefore rejected direct opening of both Pages URLs, so live HTTP status and rendered content remain unverified.
- No new external secondary source passed the verification bar; the research ledger remains unchanged.

## Known blockers and caveats

- **Local validation blocker:** the execution environment has no usable repository checkout, so `validate_project_context.py`, interactive-link tests, unit tests, strict MkDocs build, and `check_site.sh` could not run locally.
- **CI visibility blocker:** the available commit workflow endpoint returned an empty run list and is limited to a subset of workflow triggers, so push-triggered results cannot be confirmed through it.
- **Pages verification blocker:** search returned no indexed root or Metal teardown route, and the web safety gate only permits direct opening of URLs already present in search results or user content.
- The Metal safety classification covers ordinary resources at the pinned revision, not future queue ownership, plugin unload ordering, or alternative device lifecycle designs.
- Mapping, allocation, physical residency, data validity, queued completion, ownership, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
