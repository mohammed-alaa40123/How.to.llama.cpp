# Project state

_Last updated: 2026-07-16 13:16 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream OpenCL revision audited: `505b1ed15ca80e2a19f12ff4ac365e40fb374053`
- Current upstream CPU_REPACK suitability revision reviewed: `8ee54c8b32a1b0cf13c03fc5723142bc62c775f6`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Foundations deepening — executable lifetime regressions for optional CPU buffers**

## Completed foundations

- Canonical GGUF, model placement, `llama_model`, `llama_context`, graph/MoE, scheduler, memory-lifetime, backend, and inference-atlas pages.
- Source indexing, strict documentation CI, Pages deployment workflow, health checks, and durable run context.
- Generic scheduler plus CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL teardown audits.
- CPU repack, AMX, KleidiAI, and SpacemiT extra-buffer ownership comparison and destruction-harness specification.
- Complete pinned/current OpenCL event-ownership audit, generated 46-release correction, synchronous tensor-set contract analysis, and upstream proposal staging.
- First executable CPU_REPACK lifetime regression with exact path proof, numerical comparison, and repeated ASan/LSan evidence.
- Upstream-suitability decision and staged two-file CPU_REPACK regression proposal.
- Website UX review with task-oriented Architecture navigation grouping.

## Latest concrete findings

### Verified

- The homepage already provides four reading modes and links to interactive, overview, source-deep-dive, and systems-foundation entry points.
- MkDocs Material enables instant navigation, sections, search suggestion/highlighting, palette switching, heading permalinks, code copy, tabs, and Mermaid.
- The interactive foundations iframe has a descriptive title and is accompanied by prose and truth-labelled content.
- The Architecture navigation previously exposed 27 pages in one flat list.
- Architecture pages are now grouped under Core architecture, Ownership and teardown, CPU optional buffers, and Accelerator backends without changing any route.

### Interpretation

- Technical depth is strong, but navigation growth had begun to mirror repository history rather than reader tasks.
- Grouping reduces scanning cost while preserving links and bookmarks.
- The next major UX gain is a section index with audience-based reading paths and concise page descriptions.
- The Foundations/Architecture/Inference lifecycle/Interactive distinction should be made more explicit, especially because the foundations explorer appears in two navigation locations.

### Historical

- The flat Architecture list was reasonable when the site contained fewer pages; teardown and optional-buffer research made it substantially denser.
- Current upstream commit `8ee54c8b32a1b0cf13c03fc5723142bc62c775f6` still defines `llama_build_and_test()` and retains the internal CPU_REPACK buffer-type entry point.
- Workflow run `29481384561` established the pinned CPU_REPACK executable evidence: twenty AVX2-confirmed ASan/LSan processes with stable NMSE `3.82787e-16`.

### Open questions

- Whether the grouped nested navigation remains comfortable on mobile.
- Whether interactive HTML assets provide complete keyboard navigation and visible focus states internally.
- Whether Mermaid and custom diagram colors satisfy contrast requirements in both palettes.
- Whether current upstream `8ee54c8` still admits the exact CPU_REPACK fixture at runtime.

## Immediate next task

```text
wait for strict Documentation CI on grouped navigation
  → inspect and fix any MkDocs/nav failure
  → add an Architecture section index with audience-based reading paths
  → verify deployed desktop/mobile navigation, search, diagrams, iframe interaction, and keyboard access
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
- Previous head `1c16b8f` passed Documentation CI, pinned/current OpenCL workflows, and CPU_REPACK sanitizer workflow.
- Added detailed UX note `logs/research/2026-07-16/1316-website-ux-review.md`.
- Updated `mkdocs.yml` to group Architecture navigation while preserving routes.
- Research ledger unchanged because no external source was added or reclassified.
- Final-head workflow results must be checked after all context commits.

## Known blockers and caveats

- **Live-site verification:** direct GitHub Pages retrieval was blocked in the browsing environment, so HTTP status, rendered navigation, search, responsive layout, keyboard behavior, and interactive assets could not be independently tested.
- **Deployment scope:** branch-added navigation cannot appear on production Pages until PR #1 merges.
- **Accessibility scope:** source inspection confirms iframe titles and prose fallbacks, but does not prove internal keyboard behavior, focus visibility, or contrast.
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
