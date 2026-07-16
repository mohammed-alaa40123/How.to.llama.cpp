# Second browser-smoke failure and unlocated diagnostics

- Run time: 2026-07-16 18:52 Africa/Cairo
- Documentation branch: `automation/accessibility-ci-result`
- Bounded artifact: classify source-less console diagnostics without weakening same-origin or functional checks

## Verified

- Documentation CI run `29509089935` completed every step through strict MkDocs output, generated-site accessibility validation, and Playwright installation successfully.
- The run failed only at `Validate representative routes in Chromium` on the first homepage/desktop case.
- Failure artifact `8379817149` has digest `sha256:dc05c0e186b03edf770871de7546fb76c7e116ea607214c99b60f88c674bac9f` and expires on 2026-07-30.
- The retained local server log contains HTTP 200 responses for the homepage, Material CSS and JavaScript, project CSS and Mermaid initialization, sitemap, search index, and search worker. It contains no same-origin 404 or failed local request before the assertion.
- The prior URL classifier treated an empty console-message source URL as same-origin. Browser console diagnostics can lack a source URL, so that rule attributed ambiguous diagnostics to the generated site without evidence.
- `scripts/validate_browser_smoke.mjs` now uses three explicit classes: `same-origin`, `cross-origin`, and `unlocated`.
- Explicit same-origin console errors, same-origin request failures, uncaught page exceptions, route failures, missing Mermaid SVGs, landmarks, headings, search, overflow, reduced-motion, iframe-title, and focus failures remain fatal.
- Unlocated and cross-origin diagnostics are warnings and are preserved in `browser-smoke-artifacts/diagnostics.jsonl` together with the route, viewport, outcome, failure message, and all classified records.

## Interpretation

An empty console location is not positive evidence that the error originated in local generated-site code. Treating it as fatal was stricter in appearance but weaker in attribution. The corrected policy fails only diagnostics tied to the local origin or to a directly observed functional regression. This preserves the intended trust boundary while making future failures inspectable from retained artifacts rather than only ephemeral job output.

The change does not whitelist any message or external domain. A missing Mermaid SVG still fails even when the underlying CDN diagnostic is cross-origin or unlocated.

## Historical

The first browser run failed because all console errors were fatal. The first correction separated same-origin and cross-origin URLs, but retained the assumption that an empty URL was local. The second run demonstrated that this remaining assumption still failed the fully rendered first route despite successful local resource responses.

## Open questions

- Whether the three-way classifier passes all eight route/viewport cases.
- Which exact unlocated diagnostic recurs; the new JSONL evidence will preserve it.
- Whether recurring Mermaid diagnostics justify vendoring Mermaid locally.
- Whether axe-core and computed contrast/focus-style checks should be added after the smoke matrix passes.

## Validation

- Read the complete branch README, project state, research log, research ledger, and latest detailed note before editing.
- Inspected workflow run `29509089935`, job `87657584327`, all step conclusions, artifact metadata, the retained screenshot, local server log, browser validator, and Documentation CI artifact path.
- Preserved the four-route by two-viewport matrix and every existing functional assertion.
- Added durable per-case JSONL diagnostics to the already-uploaded browser artifact directory.
- Authoritative execution awaits the new commit-scoped Documentation CI run.

## Blockers

- Direct production Pages retrieval remains blocked in this environment.
- The previous failure artifact did not preserve the exact console record; the new JSONL file closes that evidence gap for subsequent runs.

## Next priority

Inspect the three-way-classifier workflow result. If it passes, preserve the warning records and move to axe-core or explicit contrast/focus-style coverage. If it fails, use `diagnostics.jsonl` to correct the exact same-origin or functional issue without reducing the route or viewport matrix.
