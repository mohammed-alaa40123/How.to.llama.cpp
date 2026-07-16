# Project state

_Last updated: 2026-07-16 14:51 Africa/Cairo_

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

## Latest concrete findings

### Verified

- Documentation CI previously stopped after `mkdocs build --strict`; it did not inspect generated HTML accessibility structure.
- `scripts/validate_built_site_accessibility.py` now checks generated documentation pages for a non-empty `html[lang]`, exactly one `<main>`, exactly one `<h1>`, image `alt` attributes, non-empty iframe titles, and button accessible names.
- Standalone `assets/interactive/` HTML is excluded because it does not use the MkDocs page shell and needs a separate interaction-focused audit.
- The validator fails on a missing or empty site directory.
- Four focused tests cover passing output, combined structural failures, interactive-asset exclusion, and missing/empty site handling.
- Documentation CI runs the validator after the strict MkDocs build.

### Interpretation

- This is a high-confidence regression guard, not a WCAG conformance claim.
- Static generated-HTML checks complement Markdown/link validation and can catch structural accessibility regressions before deployment.
- Computed contrast, focus visibility, keyboard order, responsive layout, reduced motion, and script-driven interactions still require browser-level testing.

### Historical

- The 13:16 run identified accessibility verification as a major site-quality gap.
- The 13:52 run improved Architecture discoverability; the 14:51 run implements the first automated built-output accessibility guard.
- Current upstream commit `8ee54c8b32a1b0cf13c03fc5723142bc62c775f6` still defines `llama_build_and_test()` and retains the internal CPU_REPACK buffer-type entry point.
- Workflow run `29481384561` established the pinned CPU_REPACK executable evidence: twenty AVX2-confirmed ASan/LSan processes with stable NMSE `3.82787e-16`.

### Open questions

- Whether all generated Material pages satisfy the new invariants without narrow documented exceptions.
- Whether standalone interactive explorers provide complete keyboard operation, visible focus, and text equivalents.
- Whether a browser-based axe-core lane should run on every pull request or a representative route subset.
- Whether Mermaid and custom card colors meet contrast requirements in both palettes.
- Whether current upstream `8ee54c8` still admits the exact CPU_REPACK fixture at runtime.

## Immediate next task

```text
wait for the first Documentation CI accessibility result
  → inspect and fix genuine generated-HTML failures
  → document narrow theme exceptions rather than weakening checks globally
  → add standalone-interactive or browser-based accessibility coverage
```

## In progress

- Current-tree regeneration and sanitizer validation of the CPU_REPACK lifetime candidate.
- Manual/upstream submission of the reviewed 46-release OpenCL ownership correction; GitHub App write access to upstream is blocked.
- Source-index regeneration with pinned line-aware symbol inventory.
- Hardware-specific lifetime extensions for KleidiAI, AMX, SpacemiT, and ARM repack.
- Runtime overlays for mmap/page faults, scheduler copies, events, KV/recurrent growth, and backend queues.
- Website browser-level accessibility and deployed verification.

## Publication and validation state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`.
- Added `scripts/validate_built_site_accessibility.py`, `tests/test_validate_built_site_accessibility.py`, and detailed note `logs/research/2026-07-16/1451-built-site-accessibility-guard.md`.
- Updated Documentation CI, README living TODOs, project state, and research log.
- Research ledger unchanged because no external source was added or reclassified.
- Final-head workflow results must be checked after context updates complete.

## Known blockers and caveats

- **Final-head CI:** the first generated-HTML validator run must complete before its real-site behavior is established.
- **Live-site verification:** direct Pages access remains unavailable in this environment, so HTTP status, rendered navigation, search, responsive layout, keyboard behavior, computed contrast, and interactive assets cannot be independently tested.
- **Deployment scope:** branch-added changes cannot appear on production Pages until PR #1 merges.
- **Accessibility scope:** static parsing does not prove keyboard order, focus visibility, computed contrast, reduced-motion behavior, responsive layout, or script-driven accessible names.
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
