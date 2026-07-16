# Vendor Mermaid into generated documentation builds

- Run time: 2026-07-16 20:49 Africa/Cairo
- Documentation branch: `automation/accessibility-ci-result`
- Bounded artifact: replace the runtime Mermaid CDN dependency with a pinned build-time local asset

## Verified

- Documentation CI run `29517576858` passed every stage before representative Chromium validation and failed only at `home/desktop`.
- The retained `diagnostics.jsonl` records `rendered 0 of 1 Mermaid diagrams after 15000 ms` and an uncaught promise rejection.
- The same record contains an external 404 from the repository releases API, but the local server log shows successful responses for the page, Material assets, project CSS and JavaScript, Mermaid initialization, sitemap, and search index.
- Extending the readiness timeout would not address a diagram that remains unrendered for the full bound.
- Mermaid `11.16.0` is now pinned in `scripts/prepare_mermaid_asset.sh`.
- Documentation CI and Pages both run the preparation script before `mkdocs build --strict`.
- `mkdocs.yml` now loads `assets/javascripts/vendor/mermaid.min.js` from the generated site instead of loading Mermaid directly from jsDelivr at browser runtime.
- The browser validator still requires every Mermaid container to contain an SVG within the existing 15-second bound.

## Interpretation

The failure evidence is consistent with runtime dependency or initialization failure rather than a slow-but-eventually-successful render. Moving the pinned library fetch to build time changes the failure boundary:

```text
runtime CDN failure
    → generated page silently lacks Mermaid

pinned build-time fetch failure
    → Documentation CI or Pages build fails before publication

successful build-time fetch
    → browser loads Mermaid from the same origin as the site
```

This improves reproducibility and makes local browser validation representative of the deployed asset graph. It does not eliminate all external dependencies: the build still needs to fetch the pinned package, but publication cannot succeed with a missing library.

## Historical

The preceding browser-smoke increments corrected unsupported console-origin assumptions, added durable diagnostics, and introduced a bounded SVG-readiness wait. The readiness-aware run proved that waiting alone was insufficient, triggering the previously documented fallback of vendoring Mermaid locally.

## Open questions

- Whether all eight route/viewport cases pass with the same-origin Mermaid asset.
- Whether the uncaught promise rejection disappears or exposes a separate diagram-syntax problem.
- Whether the external releases-API 404 should be handled independently by project JavaScript.
- Whether a checksum should be added after the first successful pinned-asset build preserves the exact downloaded bytes.

## Validation

- Read the complete README, project state, research log, research ledger, and latest detailed note before editing.
- Inspected workflow run `29517576858`, job `87686412691`, artifact `8383341340`, `diagnostics.jsonl`, and the local server log.
- Preserved the four-route by two-viewport matrix and all functional assertions.
- Updated Documentation CI and Pages to prepare the same pinned local Mermaid asset before strict MkDocs builds.
- Authoritative execution awaits the new commit-scoped Documentation CI result.

## Blockers

- Direct production Pages retrieval remains unavailable from this environment.
- Local repository cloning remains blocked by DNS resolution for `github.com`.

## Next priority

Inspect the first same-origin Mermaid browser result. If the matrix passes, preserve the full diagnostics and move to axe-core or computed contrast/focus-style checks. If it still fails, inspect the now-local page exception and diagram source rather than increasing the timeout.
