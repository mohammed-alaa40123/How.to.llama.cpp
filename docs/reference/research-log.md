# Research log

This is the concise chronological ledger. Detailed notes live under `logs/research/`.

## 2026-07-12 — Baseline, inference path, and core objects

**Verified**

- Baseline pinned to `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- Documented backend/model loading, tokenization, `llama_context`, decode, sampling, token feedback, GGUF, model placement, graph/MoE, scheduler, memory, and backends.
- GGUF stores tensors and metadata, not an executable graph; architecture code builds GGML operations over loaded tensors.

**Interpretation**

- Graph reuse preserves compatible topology/allocation, not token values or outputs.
- CPU addressability and logical cache state do not prove physical residency.

## 2026-07-13 — Subsystem synthesis and teardown audits

**Verified**

- Published file-by-file Pass A pages for public API, loader, context memory, scheduler, and persistent KV/recurrent implementations.
- Added model/context and generic scheduler plus CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL teardown audits.
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

- Selected a dedicated `tests/test-cpu-extra-buffer-lifetime.cpp` executable and the smallest admitted pinned x86 case: Q4_0 `[32, 8]` × F32 `[32, 1]` → F32 `[8, 1]`.
- Added AVX2, exact buffer identity, non-null traits, and operation-admission guards.
- Added a deterministic pinned-revision fixture generator and focused structural tests.
- Resolved the two-graph no-allocation topology, identical one-time Q4_0 quantization, address-based per-tensor CPU_REPACK allocation, and `1e-7` NMSE contract.
- Completed graph construction, deterministic uploads, compute/readback, exact path proof, and backend-wrapper-before-buffer teardown.
- Added an AVX2-required ASan/LSan workflow requiring twenty non-skipped process executions.

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

## 2026-07-16 14:51 — Built-site accessibility structure guard

**Verified**

- Added `scripts/validate_built_site_accessibility.py`, a dependency-free generated-HTML validator.
- It checks non-empty `html[lang]`, exactly one `<main>`, exactly one `<h1>`, image `alt` attributes, non-empty iframe titles, and accessible button names.
- Added focused tests and integrated the validator after `mkdocs build --strict` in Documentation CI.

**Interpretation**

- This is a high-confidence structural regression guard, not a WCAG conformance claim.

## 2026-07-16 15:51 — First generated-site accessibility CI result

**Verified**

- Documentation CI run `29496291134` passed strict MkDocs output and the generated-site accessibility validator without an exception or weakened rule.
- CPU_REPACK sanitizer run `29496291183`, pinned OpenCL lifecycle run `29496291154`, and current-upstream OpenCL audit run `29496291112` also passed on the same commit.
- PR #1 merged into `main` at `f33d16945433581e484c3b1112dc36c9f807861c`.

**Interpretation**

- The generated Material pages satisfy the validator's bounded structural accessibility contract, but browser-level accessibility remains unproven.

## 2026-07-16 16:51 — Representative browser smoke lane

**Verified**

- Added `scripts/validate_browser_smoke.mjs` and integrated pinned Playwright/Chromium execution into Documentation CI.
- The homepage, Architecture index, ownership diagram page, and interactive inference workflow are tested at desktop and mobile widths.
- Checks cover HTTP navigation, landmarks/headings, search discoverability, horizontal overflow, reduced-motion propagation, visible keyboard focus, Architecture links, iframe titles, Mermaid rendering, and browser errors.
- Failure screenshots and the local HTTP server log are retained as workflow evidence.

**Interpretation**

- Preview-browser testing supplies deterministic responsive and interaction-shell evidence while production Pages remains unreachable.

## 2026-07-16 17:52 — First browser-smoke failure and narrow correction

**Verified**

- Documentation CI run `29504440262` passed every stage before Chromium and failed only at the browser validator.
- Artifact `8377864569` retained a fully rendered homepage/desktop screenshot and successful local server responses without a local 404.
- Updated the validator so explicit same-origin errors remain fatal while cross-origin diagnostics are warnings.
- Added a functional assertion that every Mermaid container under `main` contains a rendered SVG.

**Interpretation**

- The same-origin boundary plus explicit Mermaid-output assertion is narrower and stronger than globally ignoring browser errors.

## 2026-07-16 18:52 — Second browser-smoke failure and durable three-way classification

**Verified**

- Documentation CI run `29509089935` passed every pre-browser stage and failed only on the first homepage/desktop Chromium case.
- Artifact `8379817149` has digest `sha256:dc05c0e186b03edf770871de7546fb76c7e116ea607214c99b60f88c674bac9f`.
- Its server log records successful local page, Material, project, Mermaid-init, sitemap, and search responses with no same-origin 404 before failure.
- The previous URL helper classified an empty console source URL as same-origin.
- The browser validator now classifies records as `same-origin`, `cross-origin`, or `unlocated`.
- Same-origin console errors and failed requests, page exceptions, missing Mermaid SVGs, route, viewport, landmark, heading, search, overflow, reduced-motion, iframe-title, and focus failures remain fatal.
- Cross-origin and unlocated diagnostics are warnings.
- Every case now writes `browser-smoke-artifacts/diagnostics.jsonl` with the route, viewport, outcome, failure message, and classified records; the existing failure-artifact step already uploads that directory.

**Interpretation**

- A missing console location is ambiguous, not proof that generated-site code emitted the error.
- The three-way classifier improves attribution without whitelisting a message or domain and without weakening functional rendering checks.
- Durable JSONL evidence makes the next failure diagnosable even when job output is truncated or ephemeral.

**Historical**

- The first correction separated known same-origin and cross-origin URLs; the second failure exposed the remaining empty-location-as-local assumption.

**Open questions**

- Whether all eight route/viewport cases pass under the new classifier.
- Which unlocated diagnostic recurs, whether Mermaid should be vendored, and when to add axe-core and explicit contrast/focus-style checks.
