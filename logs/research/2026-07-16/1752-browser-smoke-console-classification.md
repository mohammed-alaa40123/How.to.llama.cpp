# First browser-smoke failure and console classification

- Run time: 2026-07-16 17:52 Africa/Cairo
- Documentation branch: `automation/accessibility-ci-result`
- Bounded artifact: narrow the representative Chromium failure policy while preserving functional rendering checks

## Verified

- Documentation CI run `29504440262` completed every pre-browser stage successfully, including strict MkDocs output and the generated-site accessibility structure validator.
- The run failed only at `Validate representative routes in Chromium` and retained artifact `8377864569` with digest `sha256:58f44be36ea6100d68b8e323313d0a5ce76e95d95ca17c8da95e70a5179e4f4e`.
- The retained `home-desktop.png` shows the homepage fully rendered, the first keyboard Tab target (`Skip to content`) visibly focused, the search control present, no apparent document-level horizontal overflow, and the homepage Mermaid diagram rendered.
- The retained server log contains successful HTTP 200 responses for the page, Material CSS/JavaScript, custom CSS/JavaScript, sitemap, and search assets; it contains no local 404 response before failure.
- The original validator treated every browser console error as a site failure without considering the console message source URL.
- Updated `scripts/validate_browser_smoke.mjs` to classify same-origin console errors and failed requests as failures while retaining cross-origin diagnostics as warnings.
- Added a functional Mermaid assertion: every `main .mermaid` container must contain a rendered SVG. This prevents the narrower console policy from hiding a broken CDN-loaded diagram.
- Uncaught page exceptions remain hard failures, and all existing route, viewport, landmark, heading, search, overflow, reduced-motion, iframe-title, and focus checks remain intact.

## Interpretation

The retained evidence is consistent with a false-positive caused by a third-party console diagnostic rather than a broken generated page. The screenshot and server log do not prove the exact external message because the original script did not print diagnostics before throwing and the retained artifact did not include stderr. The correction therefore does not whitelist a guessed message or domain. It changes the policy at the trust boundary: local-site errors remain fatal; cross-origin diagnostics are visible warnings; externally supplied Mermaid behavior is verified by rendered output.

This is stronger than globally ignoring console errors. A local script exception, local asset failure, same-origin console error, missing Mermaid SVG, hidden focus target, overflow, missing iframe title, or route failure still fails CI.

## Historical

The 16:51 increment introduced the first representative browser lane. Its first authoritative run established that the static build and accessibility structure checks pass but exposed an over-broad console-error rule on the first homepage/desktop case.

## Open questions

- Whether the revised policy passes all eight route/viewport combinations.
- Which cross-origin diagnostic caused the first run to fail; the revised run will print it as a warning if it recurs.
- Whether a future increment should vendor Mermaid locally to remove the remaining CDN dependency.
- Whether axe-core, computed contrast, and explicit focus-style checks should be added after this smoke lane passes.

## Validation

- Read the complete branch README, project state, research log, research ledger, and latest detailed note before editing.
- Inspected workflow run `29504440262`, job `87641470832`, the failed step matrix, artifact metadata, the retained screenshot, the local HTTP server log, the browser validator, Mermaid initialization, and MkDocs external-script configuration.
- Preserved the four-route by two-viewport matrix and all existing functional checks.
- Authoritative execution of the revised JavaScript awaits the commit-scoped Documentation CI run.

## Blockers

- Direct production Pages retrieval remains blocked in this environment.
- The exact first-run console message was not retained separately by the original script; only the screenshot and local server log were available in the workflow artifact.

## Next priority

Inspect the revised Documentation CI result. If it passes, preserve the warning output and move to axe-core or explicit contrast/focus-style coverage. If it fails, use the newly classified diagnostic to fix the specific local route, asset, or rendering problem without weakening the route matrix.
