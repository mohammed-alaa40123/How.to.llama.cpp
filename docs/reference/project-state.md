# Project state

_Last updated: 2026-07-13 13:52 Africa/Cairo_

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

## Latest concrete findings

- `vk_command_pool` stores a Vulkan pool, stable command-buffer records, and a borrowed queue pointer; pools exist per `(context, queue)` and `(device, queue)` pairing.
- `ggml_vk_command_pool_cleanup()` resets a command pool only under the explicit source precondition that its command buffers are already complete.
- Synchronous Vulkan buffer read, same-device copy, and GPU memset helpers submit work with a device fence, wait indefinitely for that fence, reset it, and only then recycle command-pool state.
- Deferred host copies in the read path occur after the fence completion boundary.
- Context synchronization primitives are pooled: binary semaphores, timeline semaphores, and Vulkan events are created on demand and selected through reusable indices.
- `ggml_backend_vk_graph_compute()` is submission-oriented; return from graph computation is not by itself proof of device completion.
- The complete Vulkan backend-before-scheduler destruction classification remains open pending the exact final free chain and scheduler event/buffer ownership audit.

## In progress

- Vulkan final free-chain audit: backend synchronization, context/device queue completion, command/descriptor/query pool release, semaphore/event destruction, allocator-backed buffers, and scheduler ordering.
- Remaining concrete backend teardown audits for SYCL, RPC, CANN, and OpenCL.
- Optional CPU extra-buffer teardown audit.
- CUDA concurrent-stream synchronization coverage.
- Architecture-specific graph-builder downcasts and exact state tensors.
- Runtime evidence for synchronization, event waits, page faults, memory updates, and teardown.

## Immediate next task

Finish the pinned Vulkan teardown classification:

```text
Vulkan backend wrapper free
→ final queue/device synchronization
→ context command/descriptor/query pools
→ fences, semaphores, and events
→ allocator-backed buffer release
→ scheduler event and buffer lifetime
→ classify backend-before-scheduler ordering
```

Required deliverables:

1. exact Vulkan backend/context free chain;
2. final compute and transfer queue completion behavior;
3. destruction order for command, descriptor, and query pools plus fences/semaphores/events;
4. buffer, device, and buffer-type ownership;
5. safety classification for the pinned context member order;
6. truth labels and durable context updates.

## Publication and verification state

- New page: `docs/architecture/vulkan-command-lifetime.md`.
- Page commit: `a7301fcf2432dc26b768acc85e6269830e448b8a`.
- Navigation commit: `d95410622cb9539237ef1013e29554311ed28486`.
- Connector-side source inspection confirmed the command-pool topology, explicit completion precondition for pool reset, pooled synchronization objects, and fence-based completion sequence used by synchronous read/copy/memset helpers.
- No new external secondary source was introduced; the research ledger remains unchanged.
- GitHub Actions and Pages checks are performed after durable context updates; exact results or blockers are recorded below and in README TODOs.

## Known blockers and caveats

- **Local validation blocker:** the execution environment cannot resolve `github.com` and has no usable repository checkout, so `validate_project_context.py`, interactive-link tests, unit tests, strict MkDocs build, and `check_site.sh` could not run locally.
- **Vulkan scope caveat:** this increment maps command and completion lifetimes but does not yet prove the final backend-free destruction order.
- Mapping, allocation, residency, validity, command completion, ownership, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
