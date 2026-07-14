# Project state

_Last updated: 2026-07-14 05:03 Africa/Cairo_

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
- Bounded CPU repack extra-buffer audit.
- Bounded CPU AMX extra-buffer audit covering feature admission, aligned allocation ownership, static traits, synchronous execution, and backend-wrapper-independent buffer destruction.

## Latest concrete findings

- AMX is compile-time gated by `__AMX_INT8__` and `__AVX512VNNI__`, and buffer-type publication also depends on runtime tile-permission initialization.
- Unlike CPU repack, AMX allocates a dedicated aligned host buffer and stores the allocation pointer in `buffer->context`.
- The AMX buffer interface independently owns base lookup, tensor initialization, weight conversion/set, clear, and allocation release.
- `tensor->extra` points to one function-static AMX `tensor_traits` instance; the buffer type and `extra_buffer_type` context are function-static/process-lifetime state.
- AMX adds no queue, event, or asynchronous completion path; it inherits ordinary synchronous CPU graph completion.
- Therefore audited AMX buffer destruction is independent of `ggml_backend_cpu_context`.
- The `ggml_aligned_malloc()` plus `free()` pairing remains an explicit platform-validation question, especially on Windows.

## In progress

- Regeneration of the pinned source inventory with line-aware records and pinned source links.
- Exact OpenCL backend/context teardown, queue completion, scheduler events/buffers, and program/kernel/context release order.
- Remaining optional CPU extra-buffer audits: KleidiAI and SpacemiT IME.
- CPU repack and AMX destruction regression tests under ASan/LSan.
- Shared generated metadata for the static inference atlas and interactive workflow.
- Runtime overlays for page faults, scheduler copies, event waits, KV/recurrent growth, and backend queues.
- CANN reset semantics, RPC completion, CUDA all-stream coverage, SYCL all-queue coverage, and Vulkan query-pool ownership.

## Immediate next task

Finish the OpenCL teardown audit when the complete pinned source is searchable. If that source-access blocker persists, continue the optional CPU series with KleidiAI:

```text
KleidiAI buffer type and registration
→ allocation/free callbacks
→ tensor->extra ownership
→ execution and thread synchronization
→ backend-wrapper deleter independence
→ bounded classification
```

## Publication and verification state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`.
- Added `docs/architecture/cpu-amx-extra-buffer-lifetime.md` and linked it after the CPU repack audit.
- Added detailed note `logs/research/2026-07-14/0450-cpu-amx-extra-buffer-lifetime.md`.
- Updated README TODOs, project state, and research log; the research ledger was unchanged because no external source changed.
- Local cloning failed with `Could not resolve host: github.com`, so local Python tests, strict MkDocs build, and `check_site.sh` could not run.
- Documentation CI run `29299858341` for commit `135ae6134f638342853d1ef89480119443a3b728` completed with failure. Job `86981164561` failed specifically in `Validate project context, interactive links, and scripts`; dependency installation and strict MkDocs build were skipped.
- The connector's decoded job-log response was truncated before the failing command's stderr, so the exact validator/test assertion could not be identified or safely fixed in this run.
- Public search returned no indexed result for the Pages root. Direct opening was rejected by the safe-URL gate, and the AMX route is branch-only until PR #1 merges; HTTP status and rendered content remain unverified.

## Known blockers and caveats

- **Pinned regeneration blocker:** local GitHub DNS resolution failed, so the source index could not be regenerated here.
- **Large upstream file blocker:** the connector exposes the pinned OpenCL blob as truncated output and exact hidden symbols remain difficult to search.
- **Local validation blocker:** Python tests, strict MkDocs build, and `check_site.sh` require a usable checkout.
- **CI blocker:** run `29299858341` fails in the combined validation/test shell step, but the available decoded log truncates before the command output that names the exact failing validator or assertion.
- **Pages verification blocker:** public search has no indexed site result, direct safe-URL access is rejected, and the new AMX route cannot deploy until PR #1 merges.
- **AMX allocator caveat:** verify that the aligned allocation/release pair is correct on every supported platform.
- **Scope caveat:** AMX and repack do not stand in for KleidiAI, SpacemiT IME, HBM, or future CPU extra-buffer implementations.
- Mapping, allocation, residency, validity, command completion, ownership, reset, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
