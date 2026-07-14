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

## 2026-07-13 21:49 — Cross-backend teardown comparison

**Verified**

- Added a pinned comparison matrix covering ordinary CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and the current OpenCL gap.
- The matrix separates execution completion from scheduler-resource independence and links every classification to its detailed audit.
- Ordinary CPU, Metal, and Vulkan have the strongest audited source-level completion and lifetime classifications; CUDA, SYCL, RPC, and CANN retain specific conditional boundaries.

**Interpretation**

- Backend-before-scheduler safety requires two independent proofs: command completion and valid later deleter state.
- A single cross-backend table improves discoverability without replacing the backend-specific evidence pages.

**Historical**

- The comparison is revision-pinned and must be re-audited when queue models, registries, or destructor order change.

**Open questions**

- Finish OpenCL teardown, validate accelerator destruction with runtime tests, and audit optional CPU extra-buffer implementations.

## 2026-07-14 01:52 — Guided end-to-end inference atlas

**Verified**

- Added a clickable pipeline linking GGUF, model loading, `llama_model`, `llama_context`, graph construction, scheduler execution, backends, sampling, and decode reuse.
- Added a stage/lifetime table and reading paths for first-pass learning, memory/page faults, graphs/scheduler, backends/synchronization, and ownership/teardown.
- Linked the atlas first under the Inference lifecycle navigation section.

**Interpretation**

- The atlas is a routing layer over canonical evidence pages, not a claim that the runtime is a single linear thread.
- Persistent state, asynchronous queues, mappings/uploads, graph splits, and copy generations cross the simplified pipeline boundaries.

**Historical**

- The atlas reflects the current documentation structure and the pinned baseline; both remain revision-sensitive.

**Open questions**

- Generate shared versioned metadata for the atlas and interactive workflow, add runtime overlays, and validate Mermaid click targets in the built site.

## 2026-07-14 02:49 — Backend teardown audit method

**Verified**

- Added a reusable ten-step audit worksheet that separates host-visible command completion from scheduler-resource deleter independence.
- Standardized the bounded classification vocabulary already used by the CPU, CUDA, Metal, Vulkan, SYCL, RPC, and CANN audits.
- Added a minimum asynchronous-destruction runtime matrix and linked the method before the cross-backend comparison.

**Interpretation**

- A shared method improves consistency and reviewability without replacing backend-specific source evidence.

**Historical**

- The method is pinned to the current baseline and must evolve with backend interfaces, queue models, registries, and destruction order.

**Open questions**

- Generate worksheet evidence from source-index metadata, implement portable destruction tests, and finish the OpenCL application.

## 2026-07-14 03:51 — CPU repack extra-buffer lifetime

**Verified**

- The pinned CPU repack buffer type and tensor traits are function-static process-lifetime state.
- Repack allocation delegates to the ordinary CPU buffer type and overrides selected tensor callbacks without replacing the ordinary buffer free callback.
- `tensor->extra` points to static trait objects, while `ggml_backend_cpu_free()` owns only backend work data, the CPU context, and wrapper.
- Repack execution follows the synchronous CPU graph path with no extra queue or event lifetime.

**Interpretation**

- Audited repack buffers remain destructible after the ordinary CPU backend wrapper is deleted; the path is an alternate layout/kernel layer rather than a separate asynchronous backend.

**Historical**

- This classification is revision-pinned and does not automatically apply to newer repack code or other CPU extra-buffer implementations.

**Open questions**

- Audit AMX, KleidiAI, and SpacemiT IME, and add ASan/LSan tests for backend-free-before-buffer-free ordering.
