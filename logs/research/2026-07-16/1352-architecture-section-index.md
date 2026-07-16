# Architecture section index and audience-based reading paths

- Run time: 2026-07-16 13:52 Africa/Cairo
- Documentation branch: `automation/backend-teardown-audit-method`
- Bounded artifact: `docs/architecture/index.md` plus its navigation entry

## Verified

- The Architecture section contains 27 detailed pages across core architecture, ownership/teardown, CPU optional buffers, and accelerator backends.
- The previous run grouped these pages into four task-oriented navigation subsections without changing routes.
- The new `docs/architecture/index.md` provides six goal-based entry cards: repository orientation, GGUF/model loading, memory/ownership, graphs/scheduling, CPU optional buffers, and accelerator comparison.
- The index includes concise tables for every Architecture page and four ordered reading paths for beginners, mmap/copy/page-fault investigators, scheduler investigators, and ownership/teardown investigators.
- Existing routes remain unchanged. `mkdocs.yml` adds only `Architecture → Overview: architecture/index.md`.
- The page states the pinned baseline, intended audience, recommended prerequisite, truth-label meanings, and next page.

## Interpretation

The navigation grouping reduced menu scanning cost, but grouping alone still required readers to infer which sequence matched their question. A section index gives the Architecture subtree one canonical orientation point and makes the distinction between repository structure, runtime flow, ownership, CPU packed representations, and accelerator teardown explicit.

The index intentionally links to relevant pages outside Architecture—GGUF anatomy, model placement, memory lifetimes, graph construction, scheduler execution, copy fallback, and buffer compatibility—because real reader tasks cross the repository's section boundaries.

## Historical

The Architecture section began as a small flat list. Teardown audits and CPU optional-buffer research expanded it to 27 pages. The 13:16 run introduced semantic navigation groups; this run adds the reader-facing landing page that explains those groups and provides ordered paths.

## Open questions

- Whether the Material card grid and nested Architecture navigation remain comfortable on narrow mobile screens.
- Whether the page summaries use the same terminology readers encounter on the destination pages.
- Whether an equivalent Inference lifecycle index should be added after deployed verification.
- Whether duplicate Foundations explorer navigation should be removed or explicitly labelled as a shortcut.

## Validation

- Read the complete README, project state, research log, research ledger, and latest detailed note before editing.
- Inspected `mkdocs.yml` and all current Architecture navigation entries.
- Preserved every existing page route.
- Added only internal relative links to existing documented routes.
- Strict MkDocs and link validation are delegated to Documentation CI; final-head results must be checked before completion.

## Blockers

- The branch is not deployed to production Pages before PR #1 merges, so the new index cannot yet be visually verified on the public site.
- Browser-level mobile, keyboard, dark-mode, search, and card-grid behavior remain unverified until deployed or previewable.

## Next priority

After strict Documentation CI passes, verify the Architecture index and grouped navigation in a deployed desktop/mobile browser. Then add a built-site accessibility check or an Inference lifecycle index, prioritizing whichever deployed review exposes as the larger discoverability gap.
