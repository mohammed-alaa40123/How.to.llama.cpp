# Project state

_Last updated: 2026-07-13 14:50 Africa/Cairo_

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
- Pinned Vulkan command-pool, command-buffer, fence, semaphore, event, and synchronous-helper completion-boundary map.
- Pinned Vulkan backend free-chain audit and verified-safe ordinary backend-before-scheduler classification.

## Latest concrete findings

- `ggml_backend_vk_free()` calls `ggml_vk_cleanup()` before deleting the Vulkan backend context and wrapper.
- `ggml_vk_cleanup()` discards unsubmitted compute recording, explicitly calls `ggml_vk_synchronize()` for submitted work, and only then destroys context-owned temporary buffers, events, fences, descriptor pools, command pools, and transfer synchronization state.
- Vulkan scheduler events are device-owned resources: their free callback resolves the persistent registry device, destroys the event-owned timeline semaphore and `VkEvent` objects, and does not dereference the deleted backend context.
- Vulkan scheduler buffers own a buffer-local context containing a shared `vk_device` and `vk_buffer`; their deleter does not require the deleted backend context.
- The backend-device registry stores function-static device wrappers, so scheduler event destruction remains valid after individual backend-wrapper deletion.
- Backend-before-scheduler destruction is verified safe for the ordinary pinned Vulkan resources inspected in this audit.
- A possible cleanup gap remains: the performance query pool is created/replaced during graph compute, but no explicit `destroyQueryPool(ctx->query_pool)` appeared in the inspected backend cleanup body.

## In progress

- Remaining concrete backend teardown audits for SYCL, RPC, CANN, and OpenCL.
- Optional CPU extra-buffer teardown audit.
- CUDA concurrent-stream synchronization coverage.
- Vulkan performance-query-pool ownership and process-exit device teardown.
- Architecture-specific graph-builder downcasts and exact state tensors.
- Runtime evidence for synchronization, event waits, page faults, memory updates, and teardown.

## Immediate next task

Audit the pinned SYCL backend teardown:

```text
SYCL backend wrapper free
→ queue wait/completion behavior
→ context and stream/queue ownership
→ scheduler event implementation
→ USM/device/host buffer destruction
→ static registry/device lifetime
→ classify backend-before-scheduler ordering
```

Required deliverables:

1. exact SYCL backend/context free chain;
2. queue completion behavior during free;
3. event and buffer ownership after backend-wrapper deletion;
4. static device/buffer-type lifetime;
5. safety classification for the pinned context member order;
6. truth labels and durable context updates.

## Publication and verification state

- New page: `docs/architecture/vulkan-backend-teardown.md`.
- Page commit: `00d82b68637722e84fd68bdd4d1d82b9d94226a8`.
- Navigation commit: `69b0fed03e807d4fd913720258e477c10e660a8f`.
- README/TODO commit: `66c2769d6a702e5e77dafaef408c146ca3b4fc85`.
- Detailed note commit: `73d5357941624060547018dbfcc8a18ca06b8de6`.
- Connector-side re-fetch confirmed that the new page is present on `main` with the expected classification, source links, Mermaid teardown map, and truth-labelled sections.
- Commit-scoped workflow lookup for `73d5357941624060547018dbfcc8a18ca06b8de6` returned `workflow_runs: []`; Documentation CI, Pages deployment, and hourly-context validation are unverified rather than confirmed failed.
- Searches for the Pages root and new route returned no indexed results. The available web safety gate then rejected direct opening of both URLs, so live HTTP status and rendered content remain unverified.
- No new external secondary source was introduced; the research ledger remains unchanged.

## Known blockers and caveats

- **Local validation blocker:** the execution environment cannot resolve `github.com` and has no usable repository checkout, so `validate_project_context.py`, interactive-link tests, unit tests, strict MkDocs build, and `check_site.sh` could not run locally.
- **CI visibility blocker:** the available commit-scoped workflow endpoint returned an empty run list and does not expose push-triggered results reliably.
- **Pages verification blocker:** public search did not index the Pages root or new route, and the web safety gate rejected direct opening; HTTP response and expected rendered content could not be inspected.
- **Vulkan query-pool caveat:** the inspected cleanup path does not explicitly destroy the optional performance query pool; ownership or leak behavior needs a focused follow-up.
- Mapping, allocation, residency, validity, command completion, ownership, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
