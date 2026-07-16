# Project state

_Last updated: 2026-07-16 18:52 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream OpenCL revision audited: `505b1ed15ca80e2a19f12ff4ac365e40fb374053`
- Current upstream CPU_REPACK suitability revision reviewed: `8ee54c8b32a1b0cf13c03fc5723142bc62c775f6`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Foundations deepening — executable lifetime regressions and reader-oriented architecture documentation**

## Completed foundations

- Canonical GGUF, model placement, `llama_model`, `llama_context`, graph/MoE, scheduler, memory-lifetime, backend, and inference-atlas pages.
- Source indexing, strict documentation CI, Pages deployment workflow, health checks, and durable run context.
- Generic scheduler plus CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL teardown audits.
- CPU repack, AMX, KleidiAI, and SpacemiT extra-buffer ownership comparison and destruction-harness specification.
- Complete pinned/current OpenCL event-ownership audit and generated 46-release correction.
- First executable CPU_REPACK lifetime regression with exact path proof, numerical comparison, and repeated ASan/LSan evidence.
- Architecture navigation grouping and audience-based Architecture landing page.
- Generated-HTML accessibility structure validator and first passing authoritative run.
- Representative Chromium smoke lane covering four routes at desktop and mobile widths.
- Two evidence-driven browser-diagnostic corrections without removing routes, viewports, or functional assertions.

## Latest concrete findings

### Verified

- Documentation CI run `29509089935` passed every stage through strict MkDocs build, generated-site accessibility validation, and Playwright installation, then failed only at the first Chromium case.
- Failure artifact `8379817149` has digest `sha256:dc05c0e186b03edf770871de7546fb76c7e116ea607214c99b60f88c674bac9f` and expires on 2026-07-30.
- Its server log contains HTTP 200 responses for the homepage, Material assets, project CSS and JavaScript, sitemap, search index, and search worker, with no same-origin 404 before failure.
- The previous classifier treated an empty console source URL as same-origin.
- `scripts/validate_browser_smoke.mjs` now distinguishes `same-origin`, `cross-origin`, and `unlocated` records.
- Explicit same-origin console errors, same-origin failed requests, page exceptions, route failures, missing Mermaid SVGs, landmarks, headings, search, overflow, reduced motion, iframe titles, and focus failures remain hard failures.
- Cross-origin and unlocated records are warnings and are durably written to `browser-smoke-artifacts/diagnostics.jsonl` with route, viewport, outcome, failure message, and classified records.

### Interpretation

- An empty console location is ambiguous and should not be treated as proof of a local-site failure.
- The three-way classifier strengthens attribution while preserving user-visible functional contracts.
- Durable JSONL evidence closes the earlier gap where the exact triggering console record existed only in ephemeral job output.

### Historical

- The 13:16 run identified accessibility verification as a major site-quality gap.
- The 13:52 run improved Architecture discoverability.
- The 14:51 run added the generated-HTML accessibility guard.
- The 15:51 run preserved its first passing result.
- The 16:51 run added the representative browser-preview fallback.
- The 17:52 run separated same-origin and cross-origin diagnostics.
- The 18:52 run removed the remaining empty-location-as-local assumption and added durable per-case diagnostics.
- Workflow run `29481384561` established the pinned CPU_REPACK executable evidence: twenty AVX2-confirmed ASan/LSan processes with stable NMSE `3.82787e-16`.

### Open questions

- Whether all eight route/viewport combinations pass under the three-way classifier.
- Which exact unlocated diagnostic recurs; the next artifact will preserve it.
- Whether recurring Mermaid diagnostics justify vendoring Mermaid locally.
- Whether the post-merge Pages deployment succeeded and serves the merged Architecture pages.
- Whether axe-core and explicit dark-palette contrast/focus checks should be added after the smoke lane stabilizes.
- Whether current upstream `8ee54c8` still admits the exact CPU_REPACK fixture at runtime.

## Immediate next task

```text
inspect the three-way-classifier Chromium workflow result
  → inspect diagnostics.jsonl for recurring unlocated/cross-origin records
  → preserve explicit same-origin and functional failures as hard failures
  → after passing, add axe-core or computed contrast/focus-style coverage
```

## In progress

- Current-tree regeneration and sanitizer validation of the CPU_REPACK lifetime candidate.
- Manual/upstream submission of the reviewed 46-release OpenCL ownership correction; GitHub App write access to upstream is blocked.
- Source-index regeneration with pinned line-aware symbol inventory.
- Hardware-specific lifetime extensions for KleidiAI, AMX, SpacemiT, and ARM repack.
- Runtime overlays for mmap/page faults, scheduler copies, events, KV/recurrent growth, and backend queues.
- Website deployed verification and browser-level accessibility validation.

## Publication and validation state

- PR #1 merged to `main` at `f33d16945433581e484c3b1112dc36c9f807861c`.
- Current increment is on PR #2 branch `automation/accessibility-ci-result`.
- Added detailed note `logs/research/2026-07-16/1852-browser-smoke-unlocated-diagnostics.md`.
- Updated the browser validator, README living TODOs, project state, and research log.
- Research ledger unchanged because no external source was added or reclassified.
- The three-way browser policy awaits its commit-scoped Documentation CI result.

## Known blockers and caveats

- **Three-way browser result:** the latest classifier has not yet produced authoritative workflow evidence.
- **Previous diagnostic evidence:** run `29509089935` did not retain the exact console record; the new JSONL artifact closes this gap for future runs.
- **Live-site verification:** direct Pages access remains unavailable, so production HTTP status and deployed rendering cannot be independently tested.
- **Pages workflow visibility:** commit-scoped workflow lookup exposes pull-request-triggered runs and does not surface the post-merge `main` Pages run.
- **Accessibility scope:** the smoke lane does not prove computed contrast, complete keyboard order, visible focus quality for every control, axe-core compliance, or deep interactive-state behavior.
- **External-resource sensitivity:** Mermaid is loaded from a CDN; rendered SVGs remain required.
- **Current-tree runtime evidence:** source/API compatibility at `8ee54c8` is verified, but the fixture has not yet been compiled and executed against that exact current revision.
- **Evidence retention:** CPU_REPACK artifact `8368782428` expires on 2026-08-15; browser artifact `8379817149` expires on 2026-07-30.
- **Hardware scope:** the passing CPU_REPACK evidence is AVX2-specific and does not cover ARM, KleidiAI, AMX, or SpacemiT.
- **Upstream permission:** direct issue/PR creation in `ggml-org/llama.cpp` is blocked for the connected GitHub App.
- Mapping, allocation, residency, representation validity, command completion, event ownership, reset, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map and source-pinned end-to-end workflow.
- Deep GGUF/model-loading, model/context, graph, scheduler, memory, and teardown documentation.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays and executable lifetime regressions where source reasoning alone is insufficient.
