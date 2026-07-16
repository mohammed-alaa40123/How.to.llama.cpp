# Project state

_Last updated: 2026-07-16 16:51 Africa/Cairo_

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
- Complete pinned/current OpenCL event-ownership audit, generated 46-release correction, synchronous tensor-set contract analysis, and upstream proposal staging.
- First executable CPU_REPACK lifetime regression with exact path proof, numerical comparison, and repeated ASan/LSan evidence.
- Upstream-suitability decision and staged two-file CPU_REPACK regression proposal.
- Website UX review with task-oriented Architecture navigation grouping.
- Architecture landing page with six goal-based entry points, concise page summaries, and ordered reading paths.
- Dependency-free generated-HTML accessibility structure validator with focused tests and Documentation CI integration.
- First authoritative generated-site accessibility run passed without Material-theme exceptions.
- Representative Chromium smoke lane covering four routes at desktop and mobile widths.

## Latest concrete findings

### Verified

- Direct production Pages retrieval remains unavailable from this environment, and exact-site search returned no indexed result.
- PR #2 head `e8f9c1ef0c4febb71cc5e1fc869704f911825104` passed Documentation CI run `29500081175` before this increment.
- Added `scripts/validate_browser_smoke.mjs` using pinned Playwright `1.54.1` and headless Chromium.
- The browser lane covers the homepage, Architecture index, system ownership diagram page, and interactive inference workflow at 1440×1000 and 390×844.
- It checks HTTP success, one main landmark and H1, search discoverability, horizontal overflow, reduced-motion preference propagation, a visible first keyboard focus target, Architecture entry links, titled iframes, and browser console/page errors.
- Documentation CI now serves the strict `site/` build locally, executes the browser validator, and uploads failure screenshots plus the server log for fourteen days.

### Interpretation

- Local preview-browser execution is a deterministic substitute for part of the deployed-site audit while production Pages remains unreachable.
- The lane tests rendered behavior that static HTML parsing cannot establish, especially viewport overflow, browser focus, media preferences, and runtime console failures.
- It is not full WCAG conformance: contrast, complete keyboard order, axe-core rules, focus-style quality, and deep standalone-explorer interactions remain open.

### Historical

- The 13:16 run identified accessibility verification as a major site-quality gap.
- The 13:52 run improved Architecture discoverability.
- The 14:51 run implemented the generated-HTML accessibility guard.
- The 15:51 run preserved its first passing authoritative result.
- The 16:51 run implements the documented browser-preview fallback because live Pages access remains blocked.
- Workflow run `29481384561` established the pinned CPU_REPACK executable evidence: twenty AVX2-confirmed ASan/LSan processes with stable NMSE `3.82787e-16`.

### Open questions

- Whether all eight browser route/viewport combinations pass in the first authoritative workflow run.
- Whether external Mermaid loading emits console errors in the isolated CI environment.
- Whether Material's first Tab target is visible and stable on desktop and mobile shells.
- Whether the post-merge Pages deployment succeeded and serves the merged Architecture pages.
- Whether axe-core and explicit dark-palette contrast/focus checks should be added after the smoke lane stabilizes.
- Whether current upstream `8ee54c8` still admits the exact CPU_REPACK fixture at runtime.

## Immediate next task

```text
inspect the first representative Chromium workflow result
  → fix route, selector, focus, overflow, iframe, or external-resource failures narrowly
  → preserve the bounded route and viewport matrix
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
- Added `scripts/validate_browser_smoke.mjs` and detailed note `logs/research/2026-07-16/1651-representative-browser-smoke-lane.md`.
- Updated Documentation CI, README living TODOs, project state, and research log.
- Research ledger unchanged because no external source was added or reclassified.
- The previous PR #2 head passed Documentation CI; the new browser-lane head awaits commit-scoped workflow results.

## Known blockers and caveats

- **First browser result:** the new Chromium lane has not yet produced authoritative workflow evidence.
- **Live-site verification:** direct Pages access remains unavailable, so production HTTP status and deployed rendering cannot be independently tested.
- **Pages workflow visibility:** commit-scoped workflow lookup exposes pull-request-triggered runs and does not surface the post-merge `main` Pages run.
- **Accessibility scope:** the smoke lane does not prove computed contrast, complete keyboard order, visible focus quality for every control, axe-core compliance, or deep interactive-state behavior.
- **External-resource sensitivity:** Mermaid is loaded from a CDN and could produce CI browser errors even when local generated pages are structurally correct.
- **Current-tree runtime evidence:** source/API compatibility at `8ee54c8` is verified, but the fixture has not yet been compiled and executed against that exact current revision.
- **Evidence retention:** artifact `8368782428` expires on 2026-08-15.
- **Hardware scope:** the passing CPU_REPACK evidence is AVX2-specific and does not cover ARM, KleidiAI, AMX, or SpacemiT.
- **Upstream permission:** direct issue/PR creation in `ggml-org/llama.cpp` is blocked for the connected GitHub App.
- Mapping, allocation, residency, representation validity, command completion, event ownership, reset, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map and source-pinned end-to-end workflow.
- Deep GGUF/model-loading, model/context, graph, scheduler, memory, and teardown documentation.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays and executable lifetime regressions where source reasoning alone is insufficient.
