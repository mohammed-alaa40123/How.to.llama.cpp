# Project state

_Last updated: 2026-07-13 16:49 Africa/Cairo_

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
- Pinned Vulkan command-lifetime map and verified-safe ordinary backend teardown classification.
- Pinned SYCL backend teardown audit and conditional queued-work classification.
- Pinned RPC backend teardown audit and distributed completion classification.

## Latest concrete findings

- `ggml_backend_rpc_free()` deletes only endpoint/device/name metadata and the generic wrapper; it neither owns a socket nor synchronizes remote work.
- Scheduler RPC buffers retain their own `std::shared_ptr<socket_t>` and remote handle, so later remote-release commands remain possible after backend-wrapper deletion.
- Client graph compute is request-only: it sends the command and receives no completion response.
- RPC synchronize is a no-op.
- The server processes commands serially per connection, but graph handlers call the selected concrete backend without a following generic synchronize.
- The server frees explicitly released buffers and releases all remaining session buffers when the connection handler exits.
- Backend-before-scheduler destruction is structurally safe for ordinary pinned RPC client objects, while remote completion remains conditional on the server backend.

## In progress

- Remaining concrete backend teardown audits for CANN and OpenCL.
- Optional CPU extra-buffer teardown audit.
- RPC remote synchronization/completion protocol and shared-socket concurrency.
- CUDA concurrent-stream synchronization coverage.
- SYCL all-queue completion coverage and implicit destructor semantics.
- Vulkan performance-query-pool ownership and process-exit device teardown.
- Architecture-specific graph-builder downcasts and exact state tensors.
- Runtime evidence for synchronization, event waits, page faults, memory updates, and teardown.

## Immediate next task

Audit the pinned CANN backend teardown:

```text
CANN backend wrapper free
→ stream/device synchronization
→ events and graph execution completion
→ allocator and buffer ownership
→ static device/buffer-type lifetime
→ scheduler resource independence
→ classify backend-before-scheduler ordering
```

Required deliverables:

1. exact CANN backend/context free chain;
2. completion behavior for queued work;
3. event and scheduler-buffer ownership after backend-wrapper deletion;
4. allocator/device/stream error paths;
5. safety classification for the pinned context member order;
6. truth labels and durable context updates.

## Publication and verification state

- New page: `docs/architecture/rpc-backend-teardown.md`.
- Page commit: `b61b05a8d75f8220f3cb23eece5fc9f42bb53d9a`.
- Navigation commit: `523599e2bdac99baab97a92e0d9915ce8feed235`.
- Detailed note commit: `3d616805fed9f98fe0375841cf5d29f76dc56827`.
- Research-log commit: `f038f2b4f7f491a9ef120b1acfd99b63bbeb039b`.
- Connector-side inspection confirmed the RPC client free path, socket ownership, buffer release protocol, server dispatch ordering, graph completion gap, session cleanup, and transport destruction.
- No new external secondary source was introduced; the research ledger remains unchanged.
- GitHub Actions and Pages verification results for this increment are recorded below after the final checks.

## Known blockers and caveats

- **Local validation blocker:** there is no usable repository checkout in the execution environment, so project validators, tests, strict MkDocs build, and `check_site.sh` could not run locally.
- **RPC completion caveat:** graph compute has no completion response and the no-op RPC synchronize does not invoke server-side synchronization.
- **RPC concurrency caveat:** one socket can be shared through endpoint-level weak caching and buffer-held strong references; the inspected request helpers do not establish a per-socket request mutex.
- **SYCL completion caveat:** backend free does not explicitly wait before destroying context-owned resources.
- **Vulkan query-pool caveat:** the optional performance query pool still needs a focused ownership audit.
- Mapping, allocation, residency, validity, command completion, ownership, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
