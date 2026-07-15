# OpenCL lifecycle lexical masking

- Run time: 2026-07-15 03:51 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: prevent comment and literal text from becoming false OpenCL lifecycle call records

## Startup and inspection

Read the complete README first, then project state, research log, research ledger, and the latest detailed note. Inspected the extractor, focused tests, Documentation CI workflow, PR state, and failed workflow run `29377620068` before editing.

## Artifact

Updated `scripts/extract_opencl_lifecycle_calls.py` with a small C/C++ lexical masker that replaces line comments, block comments, string literals, and character literals with spaces while preserving every newline and source offset. Added regression coverage for commented-out calls, quoted call-shaped text, escaped character literals, multiline comments, and exact lines after masked regions.

During validation, isolated the pre-existing full-discovery failure to `tests.test_index_upstream_function_try_blocks`. The ordinary function matcher incorrectly treated a constructor function-try initializer line such as `try : device(device) {` as an ordinary function named `device`. Added a bounded `(?!try[\t ]*:)` guard to `FUNC_RE`, preserving telemetry while preventing the partial symbol.

## Verified

- The original lifecycle regular expression could treat call-shaped text inside comments or strings as a lifecycle call.
- The masker preserves source length and newline positions, so exact 1-based call lines remain stable.
- Direct code calls remain visible to the existing bounded API regex.
- A local focused reproduction passed for multiline comments, string literals, escaped character literals, and a real `clFlush` on line 6.
- Dedicated CI confirmed the OpenCL lifecycle extractor suite passes independently.
- Dedicated CI isolated the remaining discovery failure to the constructor function-try-block suite.
- The failure was reproduced: `FUNC_RE` matched `try : device(device) {` and emitted a false `device` symbol.
- Documentation CI run `29380673982` passed all isolated suites, full unittest discovery, shell and Python checks, asset validation, dependency installation, and strict MkDocs after the guard was added.

## Interpretation

Lexical masking makes the lifecycle inventory safer for a large generated or comment-heavy translation unit without pretending to parse C++. The function-try guard closes a separate navigation-accuracy defect revealed by improved CI observability.

## Historical

The first extractor intentionally used a direct regex and documented that surrounding source review was required. Earlier constructor function-try telemetry correctly counted unsupported constructors, but the ordinary matcher still partially indexed the initializer line. This run closes both concrete gaps.

## Open questions

- Raw string literals, preprocessor-disabled regions, macro expansions, and wrapper functions remain outside the bounded masker.
- The complete pinned `ggml-opencl.cpp` is still needed to generate and review the real lifecycle inventory.
- Production Pages content still cannot include branch-only work before PR #1 merges.

## Validation

- Local focused lexical-mask reproduction: passed.
- GitHub Documentation CI `29380673982`: passed completely for implementation head `540add358890507fb04f48f4a8e239e1a060971a`.
- Local full checkout remains blocked by `Could not resolve host: github.com`.
- Public Pages search returned no indexed result and direct safe-URL access remained unavailable.

## Next priority

Obtain the complete pinned OpenCL translation unit, run the masked extractor, inspect every completion/release site in context, and finish the OpenCL teardown classification. If source recovery remains blocked, implement the admitted CPU repack backend-free-before-buffer-free ASan/LSan fixture.
