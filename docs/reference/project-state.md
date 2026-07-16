# Project state

_Last updated: 2026-07-16 13:58 Africa/Cairo_

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

## Latest concrete findings

### Verified

- The Architecture section contains 27 detailed pages across core architecture, ownership/teardown, CPU optional buffers, and accelerator backends.
- The new `docs/architecture/index.md` gives readers six task-based entry points instead of requiring them to infer a sequence from page titles.
- It summarizes every Architecture page and provides ordered paths for beginners, mmap/copy/page-fault investigators, scheduler investigators, and ownership/teardown investigators.
- `mkdocs.yml` adds one Overview entry while preserving every existing route.
- The page states the pinned baseline, audience, recommended first read, truth-label meanings, and next page.

### Interpretation

- Semantic navigation groups reduce scanning, but a section index is needed to explain how those groups relate to actual reader questions.
- Cross-section links are appropriate because GGUF, memory, graph construction, scheduling, copying, and teardown span Foundations, Architecture, and Inference lifecycle.
- The next UX priority is deployed verification, followed by built-site accessibility or an Inference lifecycle index depending on observed problems.

### Historical

- The Architecture section grew from a small flat list to 27 pages as teardown and optional-buffer research expanded.
- The 13:16 run grouped the menu; the 13:52 run added the reader-facing orientation layer.
- Current upstream commit `8ee54c8b32a1b0cf13c03fc5723142bc62c775f6` still defines `llama_build_and_test()` and retains the internal CPU_REPACK buffer-type entry point.
- Workflow run `29481384561` established the pinned CPU_REPACK executable evidence: twenty AVX2-confirmed ASan/LSan processes with stable NMSE `3.82787e-16`.

### Open questions

- Whether the card grid and nested Architecture navigation remain comfortable on mobile.
- Whether interactive HTML assets provide complete keyboard navigation and visible focus states internally.
- Whether Mermaid and custom diagram colors satisfy contrast requirements in both palettes.
- Whether an Inference lifecycle index is needed after the Architecture index is deployed.
- Whether current upstream `8ee54c8` still admits the exact CPU_REPACK fixture at runtime.

## Immediate next task

```text
wait for strict Documentation CI on the Architecture index
  → inspect and fix any MkDocs or internal-link failure
  → verify deployed desktop/mobile navigation, cards, search, diagrams, iframe interaction, and keyboard access
  → add a built-site accessibility check or Inference lifecycle index based on deployed findings
```

## In progress

- Current-tree regeneration and sanitizer validation of the CPU_REPACK lifetime candidate.
- Manual/upstream submission of the reviewed 46-release OpenCL ownership correction; GitHub App write access to upstream is blocked.
- Source-index regeneration with pinned line-aware symbol inventory.
- Hardware-specific lifetime extensions for KleidiAI, AMX, SpacemiT, and ARM repack.
- Runtime overlays for mmap/page faults, scheduler copies, events, KV/recurrent growth, and backend queues.
- Website accessibility and deployed-browser verification.

## Publication and validation state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`.
- Final content head before this state-only blocker update was `831ff65ed5854a1fd654a50ddf856fd2590d30e9`.
- Added `docs/architecture/index.md` and detailed note `logs/research/2026-07-16/1352-architecture-section-index.md`.
- Updated `mkdocs.yml`, README living TODOs, project state, and research log.
- Research ledger unchanged because no external source was added or reclassified.
- GitHub returned no commit-scoped workflow runs and no combined status entries for `831ff65e` at the final check; CI is pending/unverified, not known to be failing.
- PR #1 remained open and mergeable at `831ff65e`, with 343 commits and 100 changed files.

## Known blockers and caveats

- **Final-head CI:** GitHub Actions had not exposed any commit-scoped runs or statuses for `831ff65e` at the final check, so strict MkDocs and link validation could not yet be confirmed or debugged.
- **Live-site verification:** exact-site search returned no result and direct Pages opening was rejected by the browsing environment, so HTTP status, rendered navigation, search, responsive layout, keyboard behavior, and interactive assets could not be independently tested.
- **Deployment scope:** branch-added navigation and the Architecture index cannot appear on production Pages until PR #1 merges.
- **Accessibility scope:** source inspection does not prove internal keyboard behavior, focus visibility, contrast, or mobile card layout.
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
