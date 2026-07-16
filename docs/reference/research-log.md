# Research log

This is the concise chronological ledger. Detailed notes live under `logs/research/`.

## 2026-07-12 — Baseline, inference path, and core objects

**Verified**

- Baseline pinned to `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- Documented backend/model loading, tokenization, `llama_context`, decode, sampling, and token feedback.
- Published canonical GGUF, model placement, `llama_model`, `llama_context`, graph/MoE, scheduler, memory, and backend pages.
- GGUF stores tensors and metadata, not an executable graph; architecture code builds GGML operations over loaded tensors.

**Interpretation**

- Graph reuse preserves compatible topology/allocation, not token values or outputs.
- CPU addressability and logical cache state do not prove physical residency.

## 2026-07-13 — Subsystem synthesis and teardown audits

**Verified**

- Published file-by-file Pass A pages for public API, loader, context memory, scheduler, and persistent KV/recurrent implementations.
- Added model/context, generic scheduler, CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL teardown audits.
- Added line-aware source indexing with pinned file and symbol links.

**Interpretation**

- Backend-before-scheduler safety depends on queued-work completion and resource-deleter independence.

## 2026-07-14 — Inference atlas, CPU optional buffers, and CI observability

**Verified**

- Added a clickable inference atlas and reusable teardown worksheet.
- Audited CPU repack, AMX, KleidiAI, and SpacemiT optional-buffer lifetimes.
- Added the CPU optional-buffer destruction-harness specification.
- Split Documentation CI into named validators and expanded bounded C++ source-index tests.

## 2026-07-15 — OpenCL lifecycle evidence and ownership

**Verified**

- Added an exact-line OpenCL lifecycle extractor with masking, bounded context, focused tests, and a pinned-source artifact workflow.
- Verified process-lifetime queue/context state, unsupported scheduler events, buffer-local deleters, and Adreno binary-library lifetime.
- Audited 51 direct waits: five waited events are released and 46 local command-event references are not.
- Classified 22 waits before same-queue blocking reads and 24 synchronous set-tensor waits.
- Established a pinned de facto synchronous tensor-set completion contract across generic, CUDA, SYCL, and OpenCL behavior.

**Interpretation**

- Event ownership repair and synchronization cleanup are separate changes; the first behavior-preserving fix retains every wait and releases all 46 event references.

## 2026-07-16 00:52–03:49 — Current-upstream OpenCL re-audit and proposal

**Verified**

- Audited exact revision `505b1ed15ca80e2a19f12ff4ac365e40fb374053` with a current-upstream workflow.
- Current upstream retained 51 direct waits, 46 unmatched simple event references, and the 22/24 split.
- The generated current-source patch inserted 46 releases and reached zero unmatched records without removing synchronization.
- Reviewed all insertions and staged an upstream-ready issue/PR proposal.

**Open question**

- Direct upstream submission is blocked by connected GitHub App permission.

## 2026-07-16 04:52–10:50 — CPU_REPACK fixture design and implementation

**Verified**

- Selected a dedicated `tests/test-cpu-extra-buffer-lifetime.cpp` executable and reused backend-op quantization, upload, graph, readback, and comparison patterns.
- Selected the smallest admitted pinned x86 case: Q4_0 `[32, 8]` × F32 `[32, 1]` → F32 `[8, 1]`, with AVX2, exact buffer identity, non-null traits, and operation-admission guards.
- Added a deterministic pinned-revision fixture generator and focused structural tests.
- Resolved the two-graph no-allocation topology, identical one-time Q4_0 quantization, address-based per-tensor CPU_REPACK allocation, and `1e-7` NMSE contract.
- Completed graph construction, deterministic uploads, compute/readback, exact path proof, and backend-wrapper-before-buffer teardown.
- Added an AVX2-required ASan/LSan workflow that compiles the exact pinned target and requires twenty non-skipped process executions.

**Interpretation**

- Correct output alone does not prove CPU_REPACK ran; pointer identity, selected traits, and admission checks are required.
- Separate process executions strengthen process-lifetime evidence but do not cover concurrency or every packed layout.

## 2026-07-16 11:58 — First passing CPU_REPACK sanitizer evidence

**Verified**

- Workflow run `29481384561` passed checkout, AVX2 verification, exact pinned source, generation, sanitizer configuration, compilation, twenty executions, and artifact upload.
- All twenty processes executed `q4_0_8x8` and reported stable NMSE `3.82787e-16`, with no skip or ASan/LSan diagnostic.
- Artifact `8368782428` is retained as `cpu-repack-lifetime-sanitizer-e3546c7` with digest `sha256:ef4f0a36e27f7811b106e0a870c278724f1e620aed991807b7f2c3e443d1efaf`.
- Updated the canonical CPU optional-buffer destruction-harness page with the bounded executable result.

**Interpretation**

- For this admitted pinned synchronous `MUL_MAT`, the CPU_REPACK buffer remains safely destructible after the tested CPU backend wrapper is freed.

**Open questions**

- Upstreaming the fixture and extending the method to ARM repack, KleidiAI, AMX, and SpacemiT.

## 2026-07-16 12:50 — CPU_REPACK upstream-suitability decision

**Verified**

- Reviewed current upstream commit `8ee54c8b32a1b0cf13c03fc5723142bc62c775f6`.
- Current tests still support a dedicated `llama_build_and_test()` target, and the internal CPU_REPACK buffer-type entry point remains available.
- Staged `docs/reference/upstream-cpu-repack-lifetime-fixture-proposal.md` with the proposed two-file patch and validation requirements.

**Interpretation**

- The first upstream contribution should contain only the C++ test and CMake registration; project-specific generation and artifact retention should remain here.

**Open questions**

- Current-tree runtime admission at `8ee54c8` and the authoritative upstream AVX2 sanitizer lane.

## 2026-07-16 13:16 — Website UX review and navigation grouping

**Verified**

- Reviewed the homepage, MkDocs configuration, interactive foundations page, custom stylesheet, living context, and prior CI state.
- The homepage already offered four reading modes and strong Material search/navigation features.
- Grouped 27 Architecture entries into Core architecture, Ownership and teardown, CPU optional buffers, and Accelerator backends while preserving routes.
- Recorded a prioritized backlog for deployment verification, indexes, accessibility, diagram equivalents, interaction fallbacks, and consistency.

**Interpretation**

- The strongest immediate UX issue was navigation reflecting page-addition history rather than reader tasks.

## 2026-07-16 13:52 — Architecture section index

**Verified**

- Added `docs/architecture/index.md` as the canonical orientation page for the 27-page section.
- Added six goal-based entry cards, concise summaries for every page, and ordered paths for beginners, mmap/copy/page-fault investigators, scheduler investigators, and teardown investigators.
- Added `Architecture → Overview` without changing existing routes.

**Interpretation**

- Navigation grouping lowers scanning cost; the index explains how sections and pages map to reader goals.

**Open questions**

- Mobile layout, nested navigation, keyboard behavior, dark-mode contrast, deployed rendering, an Inference lifecycle index, and duplicate Foundations explorer cleanup.

## 2026-07-16 14:51 — Built-site accessibility structure guard

**Verified**

- Added `scripts/validate_built_site_accessibility.py`, a dependency-free generated-HTML validator.
- It checks non-empty `html[lang]`, exactly one `<main>`, exactly one `<h1>`, image `alt` attributes, non-empty iframe titles, and accessible button names.
- It fails for missing or empty site output and excludes standalone `assets/interactive/` HTML for a separate interaction audit.
- Added four focused tests and integrated the validator after `mkdocs build --strict` in Documentation CI.

**Interpretation**

- This is a high-confidence structural regression guard, not a WCAG conformance claim.
- Browser-level testing is still required for computed contrast, focus visibility/order, responsive layout, reduced motion, and script-driven interactions.

**Historical**

- This implements the first automated accessibility item from the 13:16 UX review after the 13:52 discoverability improvement.

**Open questions**

- Whether generated Material pages need narrow documented exceptions, and whether the next increment should audit standalone explorers or add a representative axe-core browser lane.

## 2026-07-16 23:00 — Executable-learning two-week plan

**Verified**

- Added the July 17-31 dependency-ordered plan for Lab 0, GGUF Anatomy, and Executable Lecture 0.
- Defined browser, local-native, and cloud-container tiers; deterministic technical-media authority; trace evidence kinds; local-first progress; validation; accessibility; privacy; and milestone gates.

**Interpretation**

- Architecture, fixture, validation, and evidence boundaries should precede broad implementation.

## 2026-07-17 00:00 — Initial legal fixture decision

**Verified**

- Mandatory Lab 0 now requires no redistributed model and separates build/executable-launch evidence from real inference.
- Optional inference uses a learner-provided local GGUF path and remains a distinct outcome.
- Lab 1 will use deterministically generated project-owned GGUF bytes with educational metadata, tensor descriptors, alignment, offsets, and non-model payloads.
- No external source, model weights, corpus, personal data, paid API, or ordinary-CI network download was introduced.

**Interpretation**

- Separate build, format, and inference evidence paths are safer and more educationally precise than one third-party tiny model fixture.

**Open questions**

- Exact synthetic fixture fields and whether its binary is committed or generated from a committed script and manifest.
- The smallest stable pinned GGUF-loading path for Executable Lecture 0.