# Project state

_Last updated: 2026-07-14 05:57 Africa/Cairo_

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
- Bounded CPU repack, AMX, and KleidiAI extra-buffer lifetime audits.

## Latest concrete findings

- KleidiAI initialization is guarded by the GGML critical section and process-static state containing feature selection, Q4/Q8 kernel chains, SME limits, and tuning hints.
- Its buffer allocator delegates to the ordinary CPU buffer type, then changes the buffer type and only the tensor initialization/upload callbacks; the ordinary CPU free callback remains the allocation owner.
- `tensor->extra` points to a function-static KleidiAI trait object, and the extra-buffer type plus buffer-type metadata are function-static.
- Q4_0/Q8_0 uploads synchronously build versioned packed slots and fall back to the original representation when no compatible packed slot exists.
- KleidiAI supports bounded `MUL_MAT` and `GET_ROWS` cases and introduces no independent queue or scheduler event.
- Therefore audited KleidiAI buffer destruction is independent of `ggml_backend_cpu_context`.
- Null `get_tensor`/`cpy_tensor`, concurrent initialization, packed-layout portability, and packed-slot memory expansion remain validation questions.

## In progress

- Regeneration of the pinned source inventory with line-aware records and pinned source links.
- Exact OpenCL backend/context teardown, queue completion, scheduler events/buffers, and program/kernel/context release order.
- Remaining optional CPU extra-buffer audit: SpacemiT IME.
- CPU repack, AMX, and KleidiAI destruction regression tests under ASan/LSan.
- Shared generated metadata for the static inference atlas and interactive workflow.
- Runtime overlays for page faults, scheduler copies, event waits, KV/recurrent growth, and backend queues.
- CANN reset semantics, RPC completion, CUDA all-stream coverage, SYCL all-queue coverage, and Vulkan query-pool ownership.

## Immediate next task

Finish the OpenCL teardown audit when the complete pinned source is searchable. If that source-access blocker persists, finish the optional CPU series with SpacemiT IME:

```text
SpacemiT IME buffer type and registration
→ allocation/free callbacks
→ tensor->extra ownership
→ execution and thread synchronization
→ backend-wrapper deleter independence
→ bounded classification
```

## Publication and verification state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`.
- Added `docs/architecture/cpu-kleidiai-extra-buffer-lifetime.md` and linked it after the CPU AMX audit.
- Added detailed note `logs/research/2026-07-14/0550-cpu-kleidiai-extra-buffer-lifetime.md`.
- Updated README TODOs, project state, and research log; the research ledger is unchanged because no external source changed.
- Local cloning failed with `Could not resolve host: github.com`, so local Python tests, strict MkDocs build, and `check_site.sh` could not run.
- Documentation CI run `29302275409` for final checked head `503b780dafcf1c4ce34936ee67c8f930afdbfeda` was still `in_progress`; no failure was available to inspect or fix.
- Direct opening of both the Pages root and the KleidiAI route was rejected by the available safe-URL gate. The new route is also branch-only until PR #1 merges, so deployed HTTP status and rendered content remain unverified.

## Known blockers and caveats

- **Pinned regeneration blocker:** local GitHub DNS resolution failed, so the source index could not be regenerated here.
- **Large upstream file blocker:** the connector exposes the pinned OpenCL blob as truncated output and exact hidden symbols remain difficult to search.
- **Local validation blocker:** Python tests, strict MkDocs build, and `check_site.sh` require a usable checkout.
- **CI status:** run `29302275409` was still in progress at the final check, so current-head success or failure is not yet known.
- **Pages verification blocker:** direct URL access was rejected and the KleidiAI route cannot deploy until PR #1 merges.
- **KleidiAI caveats:** validate null readback/copy callbacks, concurrent global initialization, packed-layout portability, and one-versus-two-slot memory expansion.
- **Scope caveat:** repack, AMX, and KleidiAI do not stand in for SpacemiT IME, HBM, or future CPU extra-buffer implementations.
- Mapping, allocation, residency, validity, command completion, ownership, reset, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
