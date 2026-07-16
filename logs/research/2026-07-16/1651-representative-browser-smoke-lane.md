# Representative browser smoke lane

- Run time: 2026-07-16 16:51 Africa/Cairo
- Documentation branch: `automation/accessibility-ci-result`
- Bounded artifact: browser-level smoke validation for representative generated-site routes

## Verified

- Direct production Pages retrieval remains unavailable from the browsing environment, and exact-site search returned no indexed result.
- Documentation CI previously validated generated HTML structure but did not execute the built site in a browser.
- Added `scripts/validate_browser_smoke.mjs`, which launches headless Chromium against a locally served strict MkDocs build.
- The validator covers the homepage, Architecture index, a diagram-heavy ownership page, and the interactive inference workflow.
- Each route is exercised at 1440×1000 and 390×844 with reduced motion requested.
- Checks include successful HTTP navigation, exactly one main landmark and H1, a discoverable search input, no document-level horizontal overflow, reduced-motion preference propagation, visible keyboard focus after Tab, Architecture entry-link presence, and a titled interactive iframe.
- Browser console errors and uncaught page errors fail the run.
- Failure screenshots and the local server log are uploaded for fourteen days.
- Documentation CI now installs pinned Playwright `1.54.1` and Chromium, serves `site/`, and runs the representative browser validator after strict MkDocs and static accessibility checks.

## Interpretation

This lane closes part of the gap between static HTML inspection and deployed browser behavior. It provides deterministic rendering, responsive-overflow, focus-target, and interaction-shell evidence without depending on production Pages availability.

It is still not a full accessibility audit. It does not yet compute WCAG contrast ratios, inspect full keyboard order, run axe-core, validate visible focus styling for every control, or interact deeply inside both standalone explorers.

## Historical

The 14:51 increment added static generated-site accessibility checks, and the 15:51 increment preserved their first passing CI result. The remaining highest-priority blocker was browser-level verification while production Pages remained unreachable. This increment implements the documented preview-CI fallback.

## Open questions

- Whether all eight route/viewport combinations pass in the first authoritative workflow run.
- Whether Chromium reports external Mermaid CDN console errors in the isolated CI environment.
- Whether the first Tab target is consistently visible under both Material desktop and mobile navigation shells.
- Whether axe-core and explicit dark-palette/contrast checks should be added after the smoke lane stabilizes.

## Validation

- Read the complete branch README, project state, research log, research ledger, and latest detailed note before editing.
- Inspected the current Documentation CI workflow, MkDocs navigation, Architecture routes, and interactive route definitions.
- Confirmed PR #2 head `e8f9c1ef0c4febb71cc5e1fc869704f911825104` had a passing Documentation CI run `29500081175` before this increment.
- JavaScript execution and browser behavior await the new commit-scoped Documentation CI run.

## Blockers

- Direct production Pages HTTP and rendering verification remains blocked in this environment.
- The new browser lane has not yet produced its first authoritative CI result.

## Next priority

Inspect the first browser-smoke workflow result. Fix route, focus, overflow, external-resource, or selector failures narrowly; do not weaken the representative checks globally. After it passes, add axe-core or explicit contrast/focus-style coverage for the same bounded route set.
