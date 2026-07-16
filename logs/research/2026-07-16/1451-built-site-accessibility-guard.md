# Built-site accessibility structure guard

- Run time: 2026-07-16 14:51 Africa/Cairo
- Documentation branch: `automation/backend-teardown-audit-method`
- Bounded artifact: `scripts/validate_built_site_accessibility.py`, focused tests, and Documentation CI integration

## Verified

- Documentation CI previously ended at `mkdocs build --strict`; it did not inspect generated HTML accessibility structure.
- The new dependency-free validator walks generated documentation HTML and checks high-confidence invariants: a non-empty `html[lang]`, exactly one `<main>`, exactly one `<h1>`, `alt` attributes on images, non-empty iframe titles, and accessible names for buttons.
- Standalone files under `assets/interactive/` are excluded because they do not use the MkDocs page shell and require a separate interaction-focused audit.
- The validator fails when the site directory is missing or contains no HTML, preventing an empty build from appearing successful.
- Four focused unit tests cover a passing page, combined structural failures, interactive-asset exclusion, and missing/empty site handling.
- Documentation CI now runs the validator after the strict MkDocs build, so it evaluates generated HTML rather than Markdown source alone.

## Interpretation

This is a narrow regression guard, not a WCAG conformance claim. Static parsing can reliably catch absent language metadata, landmarks, top-level headings, alternative-text attributes, iframe titles, and unnamed buttons. It cannot establish computed color contrast, focus visibility, keyboard order, reduced-motion behavior, responsive layout, or script-driven accessible names.

Keeping the first increment dependency-free reduces CI fragility and makes failures easy to reproduce locally. A later browser-based audit can add axe-core or equivalent checks after the live or preview site becomes accessible.

## Historical

The 13:16 website review identified accessibility verification as a P0/P1 gap. The 13:52 run improved Architecture discoverability. This run implements the first automated built-output accessibility guard while live Pages verification remains blocked.

## Open questions

- Whether the generated Material theme pages satisfy every new invariant without narrow documented exceptions.
- Whether standalone interactive explorers expose complete keyboard operation, visible focus, and equivalent text content.
- Whether a browser-based axe-core lane should run on every pull request or only on a smaller representative route set.
- Whether custom Mermaid and card colors meet contrast requirements in both palettes.

## Validation

- Read the complete README, project state, research log, research ledger, and latest detailed note before editing.
- Inspected the current Documentation CI workflow and MkDocs configuration.
- Added focused tests discoverable by the existing `unittest` guard.
- Added Python compilation coverage through the existing `scripts/*.py tests/*.py` step.
- Final generated-site behavior must be confirmed by the new Documentation CI run.

## Blockers

- The live Pages site still cannot be fetched from this environment, so production HTTP status, keyboard behavior, focus visibility, computed contrast, responsive layout, and script-driven interactions remain unverified.
- Branch content cannot appear on production Pages until PR #1 merges.

## Next priority

Inspect the first Documentation CI result for the generated HTML validator and fix any real or theme-generated exception. After it passes, add a separate audit for standalone interactive explorers or a representative browser-based accessibility lane.
