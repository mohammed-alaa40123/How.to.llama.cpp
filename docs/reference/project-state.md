# Project state

_Last updated: 2026-07-14 03:51 Africa/Cairo_

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
- Generic scheduler plus ordinary CPU, CUDA, Metal, Vulkan, SYCL, RPC, and CANN teardown audits.
- Cross-backend teardown comparison matrix and reusable teardown audit method.
- Pinned OpenCL build composition and initial `cl_mem` ownership map.
- Line-aware generated source indexing with pinned file and symbol links.
- Guided end-to-end inference atlas with clickable reading paths.
- Bounded `GGML_USE_CPU_REPACK` extra-buffer audit covering static registration/traits, ordinary CPU allocation delegation, synchronous execution, and backend-wrapper-independent buffer destruction.

## Latest concrete findings

- CPU extra-buffer types are exposed through function-static registries.
- The pinned repack buffer type retains a process-lifetime `extra_buffer_type` context, and its selected tensor traits are function-static objects stored through `tensor->extra`.
- Repack allocation delegates to `ggml_backend_cpu_buffer_type()`, then overrides selected tensor callbacks without replacing the ordinary CPU buffer free callback.
- `ggml_backend_cpu_free()` does not own the repack buffer type, trait objects, or existing buffers.
- CPU graph execution is synchronous and exposes no async tensor, synchronization, or event callbacks; the repack path adds no separate queue.
- Therefore audited repack buffers are independent of the ordinary CPU backend wrapper after command completion.
- This result does not yet classify AMX, KleidiAI, or SpacemiT IME.

## In progress

- Regeneration of the pinned source inventory with line-aware records and pinned source links.
- Exact OpenCL backend/context teardown, queue completion, scheduler events/buffers, and program/kernel/context release order.
- Remaining optional CPU extra-buffer audits: AMX, KleidiAI, and SpacemiT IME.
- CPU repack destruction regression test under ASan/LSan.
- Shared generated metadata for the static inference atlas and interactive workflow.
- Runtime overlays for page faults, scheduler copies, event waits, KV/recurrent growth, and backend queues.
- CANN reset semantics, RPC completion, CUDA all-stream coverage, SYCL all-queue coverage, and Vulkan query-pool ownership.

## Immediate next task

Finish the OpenCL teardown audit when the complete pinned source is searchable. If that source-access blocker persists, continue the optional CPU series with AMX:

```text
AMX buffer type and registration
→ allocation/free callbacks
→ tensor->extra ownership
→ execution and thread synchronization
→ backend-wrapper deleter independence
→ bounded classification
```

## Publication and verification state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`.
- Added `docs/architecture/cpu-repack-extra-buffer-lifetime.md` and linked it after the ordinary CPU teardown page.
- Added detailed note `logs/research/2026-07-14/0351-cpu-repack-extra-buffer-lifetime.md`.
- Updated README TODOs and the research log; the research ledger was unchanged because no external source changed.
- Local cloning still failed with `Could not resolve host: github.com`, so local Python tests, strict MkDocs build, and `check_site.sh` could not run.
- GitHub Actions and Pages status are recorded below after final checks.

## Known blockers and caveats

- **Pinned regeneration blocker:** local GitHub DNS resolution failed, so the source index could not be regenerated here.
- **Large upstream file blocker:** the connector still exposes the pinned OpenCL blob as truncated output and exact hidden symbols remain difficult to search.
- **Local validation blocker:** Python tests, strict MkDocs build, and `check_site.sh` require a usable checkout.
- **Pages verification caveat:** the new route is branch-only until PR #1 is merged and main Pages redeploys.
- **Scope caveat:** repack does not stand in for AMX, KleidiAI, SpacemiT IME, HBM, or future CPU extra-buffer implementations.
- Mapping, allocation, residency, validity, command completion, ownership, reset, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
