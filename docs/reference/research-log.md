# Research log

This is the concise chronological ledger. Detailed notes live under `logs/research/`.

## 2026-07-12 — Baseline, decode, scheduler, and backends

**Verified**

- Baseline pinned to `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- The minimal path loads backends/model, tokenizes, creates a context, decodes, samples, and feeds the next token back.
- Decode delegates to `llama_context::decode()`; graph reuse requires specialized compatibility checks.
- Scheduler allocation assigns backends, creates splits and copy-ring destinations, and execution uses events plus synchronized fallback copies.
- CPU, CUDA, Metal, Vulkan, and SYCL execution/buffer/copy semantics are documented.

**Interpretation**

- Reuse preserves compatible topology/allocation, not token values or outputs.
- CPU-mapped addressability does not prove physical residency.

## 2026-07-12 — Documentation architecture and core objects

**Verified**

- Added the documentation-quality roadmap and six-tab foundations explorer.
- Published canonical `llama_context` and `llama_model` pages and linked their explorer entries.
- The context stores a non-owning model reference while owning mutable runtime state, scheduler resources, outputs, and memory modules.
- `llama_model` owns architecture/vocabulary state, persistent tensors, buffers, retained mappings, and architecture-specific graph dispatch.

## 2026-07-12 — GGUF, model placement, graph construction, and MoE

**Verified**

- Published canonical GGUF anatomy and model tensor-placement chapters.
- GGUF stores tensors and metadata, not an executable graph; architecture code rebuilds GGML operations over loaded tensors.
- Population paths include mapped alias, mapped copy/upload, direct read, asynchronous staging, and synchronous fallback.

**Interpretation**

- `weights_map` joins physical GGUF layout to backend-aware tensor construction.
- Cache-aware routing should generally bias selection scores before top-k when expert weights should remain based on original probabilities.

## 2026-07-12 — Memory lifetimes and validation

**Verified**

- Published the memory-lifetime atlas and interactive ownership overlay.
- Mapping, allocation, residency, validity, command completion, and ownership are distinct states.
- Added static validation for interactive routes and Markdown anchors, fixture tests, and Documentation CI integration.

## 2026-07-13 01:52–07:50 — File-by-file Pass A and subsystem synthesis

**Verified**

- Published Pass A pages for the public API/minimal example, model/GGUF loader, runtime context/memory, backend scheduler, and concrete context-memory implementations.
- Published the cross-subsystem ownership and execution map.
- The pinned tree contains ordinary KV, iSWA, DSA, DSV4, recurrent, hybrid, and hybrid-iSWA persistent memory implementations.
- Scheduler copy allocation, current-generation validity, and previous-consumer completion are separate states.

**Interpretation**

- The loader is a transactional publisher, `llama_context` is a mutable session around a borrowed model, and the scheduler is an execution planner.
- A per-batch memory context behaves like a transaction plan.

## 2026-07-13 08:50–18:51 — Teardown audits and OpenCL foundation

**Verified**

- Published model/context, generic scheduler, CPU, CUDA, Metal, Vulkan, SYCL, RPC, and CANN teardown audits.
- Published the pinned OpenCL build, kernel deployment, platform scope, and initial `cl_mem` ownership map.

**Interpretation**

- Backend-before-scheduler safety depends on both resource-deleter independence and queued-work completion.
- OpenCL buffer-local RAII does not itself prove command completion before release.

## 2026-07-13 19:51 — Line-aware generated source index

**Verified**

- `scripts/index_upstream.py` now emits untruncated, source-ordered `symbol_locations` records for every indexed file.
- Each record includes approximate declaration `name`, `kind`, and 1-based `line`.
- The legacy compact `symbols` field remains for compatibility.
- Duplicate names remain visible in the line-aware list, and tests cover ordering, line calculation, scoped names, and conditional duplicates.

**Interpretation**

- The change removes the navigation blocker for large files such as `ggml-opencl.cpp`, but remains a regex-based aid rather than a compiler-grade call graph.

**Historical**

- The previous format exposed only a deduplicated alphabetized list capped at 500 names per file.

**Open questions**

- Generate direct pinned source-line links and decide whether to add parser-assisted extraction for methods, templates, macros, and destructors.

## 2026-07-13 20:51 — Revision-pinned source-line links

**Verified**

- Generated file and symbol records can now carry pinned GitHub URLs.
- Symbol links include line fragments and derive from the exact revision selected by `update_upstream.sh`.
- Regression tests cover base normalization, absent-base behavior, line-fragment generation, and non-mutation.

**Interpretation**

- The generated index can now take reviewers directly from approximate symbol metadata to the candidate declaration at the pinned revision.

**Historical**

- The previous line-aware format required callers to construct source URLs themselves.

**Open questions**

- Regenerate the pinned inventory when upstream access is available, validate generated links, and use them to finish the OpenCL teardown audit.
