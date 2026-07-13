# Project state

_Last updated: 2026-07-13 15:49 Africa/Cairo_

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

## Latest concrete findings

- `ggml_backend_sycl_free()` deletes the per-backend context and generic wrapper without an explicit queue wait.
- `ggml_backend_sycl_synchronize()` waits on `stream(device, 0)`, but backend free does not call it.
- Async tensor set/get and graph execution can enqueue SYCL work and return without host completion.
- The SYCL context borrows device-manager default-queue pointers and owns pools, host pools, scratchpads, flash-attention buffers, and optional executable graph state through members.
- Scheduler events own independent `sycl::event` objects; their free path does not require the deleted backend context.
- Ordinary scheduler buffers retain buffer-local device, pointer, queue, tensor-extra, and allocation-mode state; their deleter does not use the backend context.
- Backend-before-scheduler destruction is structurally independent for ordinary SYCL scheduler events and buffers, but queued-work completion remains conditional.

## In progress

- Remaining concrete backend teardown audits for RPC, CANN, and OpenCL.
- Optional CPU extra-buffer teardown audit.
- CUDA concurrent-stream synchronization coverage.
- SYCL all-queue completion coverage and implicit destructor semantics.
- Vulkan performance-query-pool ownership and process-exit device teardown.
- Architecture-specific graph-builder downcasts and exact state tensors.
- Runtime evidence for synchronization, event waits, page faults, memory updates, and teardown.

## Immediate next task

Audit the pinned RPC backend teardown:

```text
RPC backend wrapper free
→ client/session/socket lifetime
→ remote allocation and buffer destruction
→ request completion and synchronization
→ scheduler event/buffer behavior
→ reconnect/error paths
→ classify backend-before-scheduler ordering
```

Required deliverables:

1. exact RPC backend/client free chain;
2. completion behavior for outstanding requests;
3. remote buffer and scheduler-resource ownership after backend-wrapper deletion;
4. transport/session lifetime and error paths;
5. safety classification for the pinned context member order;
6. truth labels and durable context updates.

## Publication and verification state

- New page: `docs/architecture/sycl-backend-teardown.md`.
- Page commit: `b8c8cf2cf1ea6bdb0ab384b52b12c91c0e29a6bb`.
- Navigation commit: `c042f9f5ea140eff2f439c30138173f3cc2ff62a`.
- Detailed note commit: `f0f78da40afa0e617bbbf0a6befb5a8436d649ce`.
- Connector-side inspection confirmed the new page and pinned source claims.
- No new external secondary source was introduced; the research ledger remains unchanged.
- Local validation remains blocked because cloning fails with `Could not resolve host: github.com`.
- Latest GitHub Actions and Pages verification results are recorded below after inspection.

## Known blockers and caveats

- **Local validation blocker:** the execution environment cannot resolve `github.com` and has no usable repository checkout, so project validators, tests, strict MkDocs build, and `check_site.sh` cannot run locally.
- **CI visibility blocker:** connector commit-status and workflow data may lag or omit push-triggered runs; absence of records is treated as unverified, not as success or failure.
- **Pages verification blocker:** if the public route cannot be opened or indexed, HTTP status and rendered content remain unverified.
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
