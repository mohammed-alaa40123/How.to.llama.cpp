# Pinned OpenCL lifecycle report workflow

- Run time: 2026-07-15 05:51 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: remove the local-checkout blocker for generating the exact pinned OpenCL lifecycle inventory

## Startup and inspection

Read the complete README first, then project state, research log, research ledger, and the latest detailed note. Inspected the current lifecycle extractor, focused tests, current PR state, and the pinned upstream OpenCL blob before editing.

## Artifact

Added `.github/workflows/opencl-lifecycle-report.yml`.

The workflow checks out this documentation repository, fetches exactly llama.cpp revision `e3546c7948e3af463d0b401e6421d5a4c2faf565` into an isolated build directory, verifies that `ggml/src/ggml-opencl/ggml-opencl.cpp` exists and is non-empty, runs `scripts/extract_opencl_lifecycle_calls.py --context-lines 3`, checks that the generated report contains at least one lifecycle call, prints the per-call counts, and uploads the JSON report as a 30-day Actions artifact.

## Verified

- The upstream source revision is hard-pinned rather than following `master`.
- The source path matches the pinned OpenCL backend translation unit.
- Report generation uses the already-tested lexical masking and exact-line extraction path.
- Artifact upload fails if the report file is missing.
- The workflow is available manually and also runs when the extractor, its tests, or this workflow changes.
- Documentation CI run `29382836507` passed for the preceding branch head.

## Interpretation

This converts a runtime-specific local DNS/checkout blocker into a reproducible GitHub-hosted source-recovery path. The generated artifact is still an inventory, not proof of ownership, command completion, or safe release order. Human classification of each context window remains required.

## Historical

Previous runs could fetch only the beginning of the large pinned blob through connector rendering. The lifecycle extractor and bounded context existed, but there was no repository-owned mechanism to obtain the complete pinned file and preserve the generated report.

## Open questions

- Whether three context lines are sufficient for every lifecycle site.
- Whether enclosing-function metadata is still needed after reviewing the artifact.
- Whether creation/retention pairing is necessary for ambiguous release sites.
- Whether the artifact should later be committed as generated evidence or remain CI-only.

## Validation

The workflow syntax and source/report assertions are now exercised by GitHub Actions. The first workflow result and artifact contents must be inspected after the commit-scoped run appears.

## Next priority

Download the generated pinned lifecycle artifact, classify every completion and release call in context, and update the OpenCL teardown comparison matrix.
