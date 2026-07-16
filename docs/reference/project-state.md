# Project state

_Last updated: 2026-07-16 17:52 Africa/Cairo_

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
- First browser-smoke failure inspected; same-origin failures and functional Mermaid rendering remain strict while cross-origin console diagnostics are now warnings.

## Latest concrete findings

### Verified

- Documentation CI run `29504440262` passed every stage before the browser lane and failed only at `Validate representative routes in Chromium`.
- Failure artifact `8377864569` has digest `sha256:58f44be36ea6100d68b8e323313d0a5ce76e95d95ca17c8da95e70a5179e4f4e`.
- The retained homepage/desktop screenshot shows the page fully rendered, the `Skip to content` target visibly focused after Tab, the search control present, no apparent horizontal overflow, and the homepage Mermaid diagram rendered.
- The retained local server log shows HTTP 200 responses for the page and local Material/search/custom assets with no local 404 before failure.
- The original validator failed on every console error regardless of source URL and did not preserve the exact console text outside the job log.
- `scripts/validate_browser_smoke.mjs` now treats same-origin console errors, same-origin request failures, and uncaught page exceptions as fatal; cross-origin diagnostics are printed as warnings.
- Every Mermaid container under `main` must now contain a rendered SVG, preserving functional detection of a broken external Mermaid dependency.
- All four routes, two viewports, landmarks, headings, search, overflow, reduced motion, iframe title, and visible first-focus checks remain unchanged.

### Interpretation

- The retained evidence is consistent with an over-broad third-party console-error policy rather than a broken generated homepage, but the exact first-run external message is not recoverable from the retained artifact.
- Classifying at the same-origin trust boundary is narrower than globally ignoring console errors and avoids whitelisting a guessed message or CDN domain.
- Functional Mermaid output is a stronger user-facing contract than requiring a completely silent third-party console.

### Historical

- The 13:16 run identified accessibility verification as a major site-quality gap.
- The 13:52 run improved Architecture discoverability.
- The 14:51 run implemented the generated-HTML accessibility guard.
- The 15:51 run preserved its first passing authoritative result.
- The 16:51 run added the representative browser-preview fallback.
- The 17:52 run inspected its first failure and narrowed only the console/request trust boundary while retaining functional rendering checks.
- Workflow run `29481384561` established the pinned CPU_REPACK executable evidence: twenty AVX2-confirmed ASan/LSan processes with stable NMSE `3.82787e-16`.

### Open questions

- Whether all eight route/viewport combinations pass under the revised error classification.
- Which cross-origin diagnostic caused the first run; the revised script will print it if it recurs.
- Whether Mermaid should be vendored locally to remove the production CDN dependency.
- Whether the post-merge Pages deployment succeeded and serves the merged Architecture pages.
- Whether axe-core and explicit dark-palette contrast/focus checks should be added after the smoke lane stabilizes.
- Whether current upstream `8ee54c8` still admits the exact CPU_REPACK fixture at runtime.

## Immediate next task

```text
inspect the revised representative Chromium workflow result
  → preserve same-origin errors and functional Mermaid rendering as hard failures
  → use printed cross-origin diagnostics to decide whether Mermaid should be vendored
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
- Added detailed note `logs/research/2026-07-16/1752-browser-smoke-console-classification.md`.
- Updated the browser validator, README living TODOs, project state, and research log.
- Research ledger unchanged because no external source was added or reclassified.
- The revised browser policy awaits its commit-scoped Documentation CI result.

## Known blockers and caveats

- **Revised browser result:** the narrowed Chromium policy has not yet produced authoritative workflow evidence.
- **Exact first diagnostic:** the original failure artifact preserved only a screenshot and local server log, not the console text that triggered the assertion.
- **Live-site verification:** direct Pages access remains unavailable, so production HTTP status and deployed rendering cannot be independently tested.
- **Pages workflow visibility:** commit-scoped workflow lookup exposes pull-request-triggered runs and does not surface the post-merge `main` Pages run.
- **Accessibility scope:** the smoke lane does not prove computed contrast, complete keyboard order, visible focus quality for every control, axe-core compliance, or deep interactive-state behavior.
- **External-resource sensitivity:** Mermaid is loaded from a CDN; rendered SVGs are now required, but cross-origin diagnostics are warnings unless they cause a page exception or missing diagram.
- **Current-tree runtime evidence:** source/API compatibility at `8ee54c8` is verified, but the fixture has not yet been compiled and executed against that exact current revision.
- **Evidence retention:** artifact `8368782428` expires on 2026-08-15; browser failure artifact `8377864569` expires on 2026-07-30.
- **Hardware scope:** the passing CPU_REPACK evidence is AVX2-specific and does not cover ARM, KleidiAI, AMX, or SpacemiT.
- **Upstream permission:** direct issue/PR creation in `ggml-org/llama.cpp` is blocked for the connected GitHub App.
- Mapping, allocation, residency, representation validity, command completion, event ownership, reset, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map and source-pinned end-to-end workflow.
- Deep GGUF/model-loading, model/context, graph, scheduler, memory, and teardown documentation.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays and executable lifetime regressions where source reasoning alone is insufficient.
