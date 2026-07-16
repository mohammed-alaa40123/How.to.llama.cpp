# Project state

_Last updated: 2026-07-16 21:51 Africa/Cairo_

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
- Evidence-driven browser-smoke corrections preserving the route matrix and functional assertions.
- Pinned build-time Mermaid asset preparation for both Documentation CI and Pages.
- Generated-SVG-aware Mermaid browser detector preserving exact source-diagram counts.

## Latest concrete findings

### Verified

- Documentation CI run `29521791301` passed every stage before representative Chromium validation and failed only at `home/desktop`.
- Pinned Mermaid preparation, strict MkDocs output, generated-site accessibility validation, and Playwright installation all passed.
- Artifact `8385027631` has digest `sha256:7e65774799d6fa713cb85d9c82db28c02d165a1817d8349292ff51dac7850954` and expires on 2026-07-30.
- Its `diagnostics.jsonl` reports `rendered 0 of 1 Mermaid diagrams after 15000 ms`, `pageerror: Object`, and the separate external GitHub releases-API 404.
- The retained full-page screenshot visibly contains a complete rendered flowchart with nodes, labels, and edges.
- The old detector only accepted an SVG nested inside the original `main .mermaid` container.
- `scripts/validate_browser_smoke.mjs` now recognizes nested Mermaid SVGs and generated SVGs whose IDs begin with `mermaid-`, deduplicates them, and compares the result against the exact source-diagram count.
- The corrected `waitForFunction` call now passes the expected count as the argument and the 15-second timeout as the options object.

### Interpretation

- The screenshot establishes that the page rendered a diagram even though the detector reported zero; this was an observability mismatch rather than evidence of a blank diagram.
- Browser validation should assert the user-visible generated SVG, not one implementation-specific DOM nesting arrangement.
- Exact source-count equality remains necessary so that recognizing generated SVGs cannot allow partial rendering to pass.
- The remaining `pageerror: Object` may still identify a separate initialization or post-render rejection and remains fatal until explained.

### Historical

- The 13:16 and 13:52 runs improved website information architecture.
- The 14:51 and 15:51 runs added and validated generated-HTML accessibility checks.
- The 16:51 run added representative browser validation.
- The 17:52 and 18:52 runs corrected unsupported console-origin assumptions and added durable JSONL diagnostics.
- The 19:50 run added bounded Mermaid readiness.
- The 20:49 run moved Mermaid from browser-runtime CDN loading to a pinned build-time local asset.
- The 21:51 run corrected the generated-SVG detector after the retained screenshot contradicted the zero-render assertion.
- Workflow run `29481384561` established pinned CPU_REPACK evidence: twenty AVX2-confirmed ASan/LSan processes with stable NMSE `3.82787e-16`.

### Open questions

- Whether all eight route/viewport combinations pass with the corrected generated-SVG detector.
- Whether `pageerror: Object` persists after visible rendering is recognized.
- Whether the external GitHub releases-API 404 should be fixed independently.
- Whether a content checksum should be pinned after the first successful browser run preserves the exact Mermaid bytes.
- Whether the post-merge Pages deployment serves the merged Architecture pages correctly.
- Whether axe-core and explicit dark-palette contrast/focus checks should be added after the smoke lane stabilizes.
- Whether current upstream `8ee54c8` still admits the exact CPU_REPACK fixture at runtime.

## Immediate next task

```text
inspect the corrected generated-SVG detector result
  → confirm the full eight-case matrix or isolate the remaining page exception
  → keep exact source-count equality and the 15-second bound strict
  → if pageerror remains, preserve the exact Mermaid rejection object
  → after passing, pin the asset checksum and add axe-core or contrast/focus coverage
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
- Added detailed note `logs/research/2026-07-16/2151-mermaid-render-detector.md`.
- Updated `scripts/validate_browser_smoke.mjs`, README living TODOs, project state, and research log.
- Research ledger unchanged because no external source was added or reclassified.
- The corrected generated-SVG detector awaits its commit-scoped Documentation CI result.

## Known blockers and caveats

- **Current browser result:** the corrected Mermaid detector has not yet produced authoritative workflow evidence.
- **Live-site verification:** direct Pages access remains unavailable, so production HTTP status and deployed rendering cannot be independently tested.
- **Local validation:** cloning the repository is blocked by DNS resolution for `github.com` in the current runtime.
- **Pages workflow visibility:** commit-scoped workflow lookup exposes pull-request-triggered runs and does not surface the post-merge `main` Pages run.
- **Accessibility scope:** the smoke lane does not prove computed contrast, complete keyboard order, visible focus quality for every control, axe-core compliance, or deep interactive-state behavior.
- **Build-time dependency:** Mermaid is still fetched externally during CI and Pages builds, but publication fails visibly if the pinned asset cannot be prepared.
- **Current-tree runtime evidence:** source/API compatibility at `8ee54c8` is verified, but the fixture has not yet been compiled and executed against that exact current revision.
- **Evidence retention:** CPU_REPACK artifact `8368782428` expires on 2026-08-15; browser artifacts `8383341340` and `8385027631` expire on 2026-07-30.
- **Hardware scope:** the passing CPU_REPACK evidence is AVX2-specific and does not cover ARM, KleidiAI, AMX, or SpacemiT.
- **Upstream permission:** direct issue/PR creation in `ggml-org/llama.cpp` is blocked for the connected GitHub App.
- Mapping, allocation, residency, representation validity, command completion, event ownership, reset, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map and source-pinned end-to-end workflow.
- Deep GGUF/model-loading, model/context, graph, scheduler, memory, and teardown documentation.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays and executable lifetime regressions where source reasoning alone is insufficient.
