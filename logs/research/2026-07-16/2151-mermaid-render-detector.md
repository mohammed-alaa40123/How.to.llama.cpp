# Correct the Mermaid browser-render detector

- Run time: 2026-07-16 21:51 Africa/Cairo
- Documentation branch: `automation/accessibility-ci-result`
- Bounded artifact: make the browser smoke test recognize the generated Mermaid SVG without weakening exact diagram-count validation

## Verified

- Documentation CI run `29521791301` passed every stage before representative Chromium validation and failed only at `home/desktop`.
- The pinned Mermaid asset preparation, strict MkDocs build, generated-site accessibility validator, and Playwright installation all passed.
- Artifact `8385027631` has digest `sha256:7e65774799d6fa713cb85d9c82db28c02d165a1817d8349292ff51dac7850954` and expires on 2026-07-30.
- Its `diagnostics.jsonl` reported `rendered 0 of 1 Mermaid diagrams after 15000 ms`, one `pageerror: Object`, and the separate external GitHub releases-API 404.
- The retained full-page screenshot visibly contains the rendered homepage flowchart, including nodes, edges, and labels.
- Therefore the page output and the assertion disagreed: the detector only accepted an SVG nested under the original `main .mermaid` element.

## Interpretation

The screenshot is direct user-visible evidence that Mermaid produced a diagram. The browser test was measuring one DOM-placement assumption rather than the actual postcondition.

The corrected detector now:

1. counts the original Mermaid source containers;
2. recognizes both SVGs nested under `.mermaid` and generated SVGs whose IDs begin with `mermaid-`;
3. deduplicates SVG nodes;
4. waits for the expected source-diagram count using Playwright's correct `waitForFunction(function, arg, options)` signature;
5. still requires exact rendered/count equality within the existing 15-second bound;
6. reports source-container and `data-processed` counts on failure.

This changes the measurement, not the requirement. Missing diagrams, partial rendering, same-origin failures, page exceptions, route failures, overflow, focus, iframe titles, landmarks, headings, search, and reduced-motion failures remain fatal.

## Historical

The preceding increment moved Mermaid to a pinned same-origin build asset because a complete readiness interval produced no recognized SVG. The first same-origin run showed that the diagram was visually present even though the detector still reported zero. This run corrects that final observability mismatch.

## Open questions

- Whether all eight route/viewport combinations pass with the corrected generated-SVG detector.
- Whether `pageerror: Object` is a harmless Mermaid rejection after visible output or a separate defect that remains fatal after rendering is recognized.
- Whether the external GitHub releases-API 404 should be removed or explicitly tolerated by the project JavaScript.
- Whether the prepared Mermaid asset should receive a pinned checksum after the first fully passing browser run.

## Validation

- Read the complete README, project state, research log, research ledger, and latest detailed note before editing.
- Inspected workflow run `29521791301`, job `87700455518`, artifact `8385027631`, `diagnostics.jsonl`, the local server log, and the retained homepage screenshot.
- Confirmed the screenshot contains a fully rendered flowchart despite the zero-SVG assertion.
- Updated `scripts/validate_browser_smoke.mjs` while preserving the complete four-route by two-viewport matrix and every existing functional check.
- Authoritative execution awaits the new commit-scoped Documentation CI result.

## Blockers

- Direct production Pages retrieval remains unavailable from this environment.
- Local repository cloning remains blocked by DNS resolution for `github.com`.

## Next priority

Inspect the corrected detector's Documentation CI run. If rendering is recognized but `pageerror: Object` remains, instrument Mermaid initialization to preserve the exact rejection object before deciding whether it is a real site failure. If the full matrix passes, pin the Mermaid asset checksum and proceed to axe-core or computed contrast/focus-style coverage.
