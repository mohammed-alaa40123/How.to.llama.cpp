# OpenCL lifecycle lexical masking

- Run time: 2026-07-15 03:51 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: prevent comment and literal text from becoming false OpenCL lifecycle call records

## Startup and inspection

Read the complete README first, then project state, research log, research ledger, and the latest detailed note. Inspected the extractor, focused tests, Documentation CI workflow, PR state, and failed workflow run `29377620068` before editing.

## Artifact

Updated `scripts/extract_opencl_lifecycle_calls.py` with a small C/C++ lexical masker that replaces line comments, block comments, string literals, and character literals with spaces while preserving every newline and source offset. Added regression coverage for commented-out calls, quoted call-shaped text, escaped character literals, multiline comments, and exact lines after masked regions.

## Verified

- The original regular expression could treat call-shaped text inside comments or strings as a lifecycle call.
- The masker preserves source length and newline positions, so exact 1-based call lines remain stable.
- Direct code calls remain visible to the existing bounded API regex.
- A local focused reproduction passed for multiline comments, string literals, escaped character literals, and a real `clFlush` on line 6.
- PR #1 remained open and mergeable before the edit.
- Documentation CI run `29377620068` completed with failure isolated to full unittest discovery; dedicated source-index and interactive-link suites passed. The exact failing assertion was unavailable in connector-rendered logs.

## Interpretation

Lexical masking makes the lifecycle inventory safer for a large generated or comment-heavy translation unit without pretending to parse C++. It reduces false ownership evidence while retaining exact navigation lines.

## Historical

The first extractor intentionally used a direct regex and documented that surrounding source review was required. This increment closes one concrete false-positive class before running it against the complete pinned OpenCL file.

## Open questions

- Raw string literals, preprocessor-disabled regions, macro expansions, and wrapper functions remain outside the bounded masker.
- The complete pinned `ggml-opencl.cpp` is still needed to generate and review the real lifecycle inventory.
- The new branch head requires commit-scoped Documentation CI and Pages remains unverifiable before merge.

## Validation

Focused masking logic was reproduced locally. Full repository validation remains GitHub-hosted because direct cloning still fails with `Could not resolve host: github.com`.

## Next priority

Verify the new Documentation CI run. Then obtain the complete pinned OpenCL translation unit, run the extractor, and inspect every completion/release site in context.
