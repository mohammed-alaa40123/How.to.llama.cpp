# Third browser-smoke failure: Mermaid readiness race

- Run time: 2026-07-16 19:50 Africa/Cairo
- Documentation branch: `automation/accessibility-ci-result`
- Bounded artifact: wait for observable Mermaid SVG readiness without weakening the rendering requirement

## Verified

- Documentation CI run `29513543532` passed every stage through strict MkDocs output, generated-site accessibility validation, and Playwright/Chromium installation.
- It failed only at the first `home/desktop` browser case with `rendered 0 of 1 Mermaid diagrams`.
- The failure occurred about 2.6 seconds after the local browser step started, so the validator sampled the DOM immediately after `networkidle` rather than waiting for Mermaid's asynchronous render completion.
- Failure artifact `8381667636` was uploaded with digest `sha256:08294cbc09e5699e261abafd6c4b5e3153a2fadf2b4b6586303ec413e1cdbf81`.
- The browser validator now waits up to 15 seconds for every `main .mermaid` container to contain an SVG, then retains the exact rendered/count assertion.
- The timeout is configurable through `MERMAID_RENDER_TIMEOUT_MS`; a timeout still fails with the observed rendered and total counts.
- Same-origin console/request failures, page exceptions, route status, landmarks, headings, search, overflow, reduced motion, iframe titles, keyboard focus, and the full route/viewport matrix remain strict.

## Interpretation

`networkidle` is not a reliable readiness signal for application-level asynchronous rendering. It only indicates a quiet network period; Mermaid initialization and DOM replacement can still be pending. Waiting for the exact user-visible postcondition—an SVG inside each Mermaid container—is a stronger and less timing-sensitive contract.

This change does not convert a rendering failure into a warning. It separates `not rendered yet` from `failed to render within a bounded interval`.

## Historical

The first two browser failures exposed unsupported console-origin assumptions. The three-way diagnostic classifier removed those assumptions and allowed the real functional failure to surface: the Mermaid assertion itself was racing asynchronous rendering.

## Open questions

- Whether all eight route/viewport cases pass with bounded Mermaid readiness.
- Whether the CDN dependency is reliable enough for production and CI, or Mermaid should be vendored locally.
- Which cross-origin or unlocated warnings recur once the matrix advances beyond the first case.

## Validation

- Read the complete README, project state, research log, research ledger, and latest detailed note before editing.
- Inspected run `29513543532`, job `87672765335`, the failing step, exact error, artifact identity, and current validator.
- Preserved every functional assertion and route/viewport case.
- Updated the validator to await the actual rendered-SVG postcondition.
- Authoritative execution awaits the new commit-scoped Documentation CI run.

## Blockers

- Direct production Pages retrieval remains unavailable from this environment.
- Local repository cloning remains blocked by DNS resolution for `github.com`.

## Next priority

Inspect the new Documentation CI result. If the matrix passes, preserve the diagnostics and move to axe-core or computed contrast/focus-style coverage. If Mermaid still times out, inspect retained warnings and vendor Mermaid locally rather than extending the timeout without evidence.
