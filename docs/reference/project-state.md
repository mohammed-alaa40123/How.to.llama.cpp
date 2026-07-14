# Project state

_Last updated: 2026-07-14 07:05 Africa/Cairo_

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
- Bounded CPU repack, AMX, KleidiAI, and SpacemiT IME extra-buffer lifetime audits.

## Latest concrete findings

- SpacemiT owns a dedicated 64-byte-aligned weight allocation through `spine_mem_pool_alloc()` and returns it through `spine_mem_pool_free()`.
- The Spine pool serializes allocation/free with a mutex, tracks live allocations, returns ranges to chunks, and can release empty chunks independently of `ggml_backend_cpu_context`.
- `tensor->extra` points to process-static IME1, IME2, or RVV traits; the extra-buffer type and buffer-type metadata are function-static.
- Upload/repacking and graph execution remain synchronous CPU work using the threadpool and explicit barriers, with no scheduler event or accelerator queue.
- Worker setup may acquire thread-local TCM state; the paired clear-affinity hook releases it through `spine_mem_pool_tcm_mem_release()`.
- Therefore audited weight-buffer destruction is independent of the ordinary CPU backend wrapper, while complete worker/process teardown remains conditional on TCM cleanup and pool-manager shutdown.

## In progress

- Regeneration of the pinned source inventory with line-aware records and pinned source links.
- Exact OpenCL backend/context teardown, queue completion, scheduler events/buffers, and program/kernel/context release order.
- Cross-implementation CPU extra-buffer comparison and destruction tests for repack, AMX, KleidiAI, and SpacemiT.
- CPU extra-buffer destruction regression tests under ASan/LSan and SpacemiT TCM/threadpool teardown tests on supported hardware.
- Shared generated metadata for the static inference atlas and interactive workflow.
- Runtime overlays for page faults, scheduler copies, event waits, KV/recurrent growth, and backend queues.
- CANN reset semantics, RPC completion, CUDA all-stream coverage, SYCL all-queue coverage, and Vulkan query-pool ownership.

## Immediate next task

Finish the OpenCL teardown audit when the complete pinned source is searchable. Otherwise synthesize the completed CPU optional-buffer series:

```text
repack / AMX / KleidiAI / SpacemiT
→ allocation and free owner
→ tensor->extra lifetime
→ synchronous/thread-local state
→ unsupported transfer callbacks
→ backend-wrapper independence
→ portable destruction test matrix
```

## Publication and verification state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`; checked head `f86b8c67c959f47d01a5574b65f0c471b3eb9353` was mergeable before the final state-only commit.
- Added `docs/architecture/cpu-spacemit-ime-extra-buffer-lifetime.md` and linked it after the KleidiAI audit.
- Added detailed note `logs/research/2026-07-14/0650-cpu-spacemit-ime-extra-buffer-lifetime.md`.
- Updated README TODOs, project state, and research log; the research ledger is unchanged because no external source changed.
- Local cloning again failed with `Could not resolve host: github.com`, so local Python tests, strict MkDocs build, and `check_site.sh` could not run.
- Documentation CI run `29304828892` completed with failure. Checkout, Python setup, and context reading succeeded; step 5, `Validate project context, interactive links, and scripts`, failed, so dependency installation and strict MkDocs build were skipped.
- The decoded job log exposed the failing step but was truncated before the validator stderr/assertion, so no evidence-backed fix could be applied in this run.
- Direct opening of the Pages root and the existing KleidiAI route was rejected by the web safe-URL gate. The new SpacemiT route is branch-only until PR #1 merges, so its deployed HTTP response cannot yet be checked.

## Known blockers and caveats

- **Pinned regeneration blocker:** local GitHub DNS resolution failed, so the source index could not be regenerated here.
- **Large upstream file blocker:** the connector exposes the pinned OpenCL blob as truncated output and exact hidden symbols remain difficult to search.
- **Local validation blocker:** Python tests, strict MkDocs build, and `check_site.sh` require a usable checkout.
- **CI failure:** run `29304828892` failed specifically at `Validate project context, interactive links, and scripts`; the available decoded log was truncated before the exact validator message, and later build steps were skipped.
- **Pages verification blocker:** direct URL access was rejected; the SpacemiT page cannot deploy until PR #1 merges.
- **SpacemiT caveat:** buffer lifetime is distinct from thread-local TCM leases and process-level pool-manager lifetime.
- **Scope caveat:** optional CPU extra-buffer audits do not prove behavior for HBM or future implementations.
- Mapping, allocation, residency, validity, command completion, ownership, reset, thread-local leases, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
