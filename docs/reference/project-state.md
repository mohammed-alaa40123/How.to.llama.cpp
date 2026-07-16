# Project state

_Last updated: 2026-07-16 15:51 Africa/Cairo_

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

## Latest concrete findings

### Verified

- Documentation CI run `29496291134` completed successfully for commit `bc98c6fcadeb2f5194686355f4c6d9a053669d28`.
- `mkdocs build --strict` passed before the generated-site accessibility validator ran.
- `Validate built-site accessibility structure` passed without an exception, suppression, or weakened rule.
- The same Documentation CI job passed durable-context, link, source-index, unit-test discovery, shell, Python, and required-interactive-asset checks.
- CPU_REPACK sanitizer run `29496291183`, pinned OpenCL lifecycle run `29496291154`, and current-upstream OpenCL audit run `29496291112` also passed on the same commit.
- PR #1 was merged into `main` at `f33d16945433581e484c3b1112dc36c9f807861c`.

### Interpretation

- The generated Material pages satisfy the validator's bounded structural contract: language metadata, one main landmark, one top-level heading, image alternative-text attributes, iframe titles, and button accessible names.
- No theme exception is currently justified; the validator should remain strict.
- Static generated-HTML success does not establish keyboard order, focus visibility, computed contrast, reduced-motion behavior, responsive layout, or script-driven interactions.

### Historical

- The 13:16 run identified accessibility verification as a major site-quality gap.
- The 13:52 run improved Architecture discoverability.
- The 14:51 run implemented the generated-HTML accessibility guard.
- The 15:51 run closes its first-real-site-result TODO with passing workflow evidence.
- Workflow run `29481384561` established the pinned CPU_REPACK executable evidence: twenty AVX2-confirmed ASan/LSan processes with stable NMSE `3.82787e-16`.

### Open questions

- Whether the post-merge Pages deployment succeeded and serves the merged Architecture pages.
- Whether the deployed Architecture index, grouped navigation, search, diagrams, cards, and iframes behave correctly across desktop and mobile.
- Whether standalone interactive explorers provide complete keyboard operation, visible focus, and text equivalents.
- Whether a representative browser-based accessibility lane should run on every pull request.
- Whether current upstream `8ee54c8` still admits the exact CPU_REPACK fixture at runtime.

## Immediate next task

```text
verify post-merge Pages deployment
  → audit homepage, Architecture index, one diagram-heavy page, and one interactive explorer
  → check keyboard focus, accessible names, contrast, reduced motion, and responsive layout
  → if live access remains blocked, add a representative preview/browser CI lane
```

## In progress

- Current-tree regeneration and sanitizer validation of the CPU_REPACK lifetime candidate.
- Manual/upstream submission of the reviewed 46-release OpenCL ownership correction; GitHub App write access to upstream is blocked.
- Source-index regeneration with pinned line-aware symbol inventory.
- Hardware-specific lifetime extensions for KleidiAI, AMX, SpacemiT, and ARM repack.
- Runtime overlays for mmap/page faults, scheduler copies, events, KV/recurrent growth, and backend queues.
- Website browser-level accessibility and deployed verification.

## Publication and validation state

- PR #1 has merged to `main` at `f33d16945433581e484c3b1112dc36c9f807861c`.
- Current increment is on branch `automation/accessibility-ci-result`.
- Added detailed note `logs/research/2026-07-16/1551-first-accessibility-ci-result.md`.
- Updated README living TODOs, project state, and research log.
- Research ledger unchanged because no external source was added or reclassified.
- Documentation CI and all three technical evidence workflows passed on the accessibility-guard commit.

## Known blockers and caveats

- **Live-site verification:** direct Pages access remains unavailable in this environment, so production HTTP status, rendered navigation, search, responsive layout, keyboard behavior, computed contrast, and interactive assets cannot be independently tested.
- **Pages workflow visibility:** commit-scoped workflow lookup currently exposes pull-request-triggered runs, so the post-merge `main` Pages run was not available through that endpoint.
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