# Project state

_Last updated: 2026-07-16 19:50 Africa/Cairo_

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
- Three evidence-driven browser-smoke corrections that preserve the route matrix and functional assertions.

## Latest concrete findings

### Verified

- Documentation CI run `29513543532` passed all pre-browser stages and failed only at `home/desktop` with `rendered 0 of 1 Mermaid diagrams`.
- The browser step started at 15:59:04 UTC and failed at 15:59:07 UTC, so the SVG assertion sampled the DOM before bounded application-level render readiness was established.
- Artifact `8381667636` was retained with digest `sha256:08294cbc09e5699e261abafd6c4b5e3153a2fadf2b4b6586303ec413e1cdbf81`.
- `scripts/validate_browser_smoke.mjs` now waits up to 15 seconds for every Mermaid container under `main` to contain an SVG.
- After the wait, exact rendered/count equality remains mandatory. A timeout still fails with the observed counts.
- Same-origin console and request failures, page exceptions, HTTP failures, landmarks, headings, search, horizontal overflow, reduced motion, iframe titles, keyboard focus, and the complete four-route by two-viewport matrix remain hard failures.

### Interpretation

- Playwright `networkidle` is a network-quiet signal, not proof that asynchronous Mermaid DOM rendering has completed.
- Waiting for the exact visible postcondition is stronger than adding an arbitrary sleep and less flaky than immediate sampling.
- This distinguishes a readiness race from a true render failure without weakening the rendering contract.

### Historical

- The 13:16 and 13:52 runs improved website information architecture.
- The 14:51 and 15:51 runs added and validated generated-HTML accessibility checks.
- The 16:51 run added representative browser validation.
- The 17:52 and 18:52 runs corrected unsupported console-origin assumptions and added durable JSONL diagnostics.
- The 19:50 run identified the first genuine functional race and added bounded Mermaid readiness.
- Workflow run `29481384561` established pinned CPU_REPACK evidence: twenty AVX2-confirmed ASan/LSan processes with stable NMSE `3.82787e-16`.

### Open questions

- Whether all eight route/viewport combinations pass with bounded Mermaid readiness.
- Whether recurring CDN delays or failures justify vendoring Mermaid locally.
- Which cross-origin or unlocated diagnostics recur after the matrix advances beyond the first case.
- Whether the post-merge Pages deployment serves the merged Architecture pages correctly.
- Whether axe-core and explicit dark-palette contrast/focus checks should be added after the smoke lane stabilizes.
- Whether current upstream `8ee54c8` still admits the exact CPU_REPACK fixture at runtime.

## Immediate next task

```text
inspect the bounded Mermaid-readiness Chromium result
  → confirm the full eight-case matrix or inspect retained diagnostics
  → keep the rendered-SVG requirement strict
  → vendor Mermaid locally if bounded readiness still fails from CDN behavior
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
- Added detailed note `logs/research/2026-07-16/1950-browser-smoke-mermaid-readiness.md`.
- Updated the browser validator, README living TODOs, project state, and research log.
- Research ledger unchanged because no external source was added or reclassified.
- The bounded Mermaid-readiness policy awaits its commit-scoped Documentation CI result.

## Known blockers and caveats

- **Current browser result:** the readiness-aware validator has not yet produced authoritative workflow evidence.
- **Live-site verification:** direct Pages access remains unavailable, so production HTTP status and deployed rendering cannot be independently tested.
- **Local validation:** cloning the repository is blocked by DNS resolution for `github.com` in the current runtime.
- **Pages workflow visibility:** commit-scoped workflow lookup exposes pull-request-triggered runs and does not surface the post-merge `main` Pages run.
- **Accessibility scope:** the smoke lane does not prove computed contrast, complete keyboard order, visible focus quality for every control, axe-core compliance, or deep interactive-state behavior.
- **External-resource sensitivity:** Mermaid is loaded from a CDN; rendered SVGs remain required.
- **Current-tree runtime evidence:** source/API compatibility at `8ee54c8` is verified, but the fixture has not yet been compiled and executed against that exact current revision.
- **Evidence retention:** CPU_REPACK artifact `8368782428` expires on 2026-08-15; browser artifact `8381667636` is retained for 14 days.
- **Hardware scope:** the passing CPU_REPACK evidence is AVX2-specific and does not cover ARM, KleidiAI, AMX, or SpacemiT.
- **Upstream permission:** direct issue/PR creation in `ggml-org/llama.cpp` is blocked for the connected GitHub App.
- Mapping, allocation, residency, representation validity, command completion, event ownership, reset, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map and source-pinned end-to-end workflow.
- Deep GGUF/model-loading, model/context, graph, scheduler, memory, and teardown documentation.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays and executable lifetime regressions where source reasoning alone is insufficient.
