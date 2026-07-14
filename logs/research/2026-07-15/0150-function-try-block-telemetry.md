# Constructor function-try-block telemetry

- Run time: 2026-07-15 01:50 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: measure bounded qualified constructor function-try-block candidates without changing navigation extraction

## Startup and inspection

Read the complete repository README first, then project state, research log, research ledger, and the latest detailed note. Inspected `scripts/index_upstream.py`, existing unsupported-syntax tests, constructor boundary tests, PR state, and the preceding Documentation CI result before editing.

## Artifact

Added a bounded `CONSTRUCTOR_FUNCTION_TRY_BLOCK_RE` telemetry pattern and focused regression coverage. The generated per-file `unsupported_syntax` object, aggregate JSON counts, and Markdown inventory now include `constructor_function_try_blocks`.

Symbol extraction remains unchanged: function-try-block constructors are counted but are not emitted as navigation records.

## Verified

- The counter requires a qualified constructor name whose final function component equals the immediately preceding class name.
- Same-line and next-line `try` tokens are counted.
- Both `try : initializer(...) {` and `try {` forms are admitted as candidates.
- Ordinary function function-try-blocks are excluded by the constructor backreference.
- Constructor function-try-blocks remain absent from `extract_symbols()`.
- Existing braced and multiline constructor-initializer counters retain their keys and behavior.
- Root aggregate generation and Markdown reporting now include the new counter.

## Interpretation

This closes an observability gap without weakening navigation accuracy. Candidate volume from a regenerated pinned tree can now decide whether a stateful extractor is justified and where a future symbol link should point.

## Historical

The preceding run established that constructor function-try-blocks were omitted from both navigation and telemetry. This increment implements the narrower next step proposed by that audit.

## Open questions

- How many constructor function-try-block candidates exist in pinned llama.cpp revision `e3546c7948e3af463d0b401e6421d5a4c2faf565`?
- If any exist, should future navigation target the constructor signature line or the `try` line?
- Does pinned-tree evidence justify stateful extraction, or is telemetry sufficient?
- Complete OpenCL teardown remains blocked until the pinned source inventory can be regenerated or the hidden portion of `ggml-opencl.cpp` becomes searchable.

## Validation

The focused tests are committed to the branch. GitHub-hosted Documentation CI is the authoritative full validation path because this runtime still cannot resolve `github.com` for a local clone.

## Next priority

Regenerate the pinned source inventory and inspect the three unsupported-syntax totals. Use actual candidate volume to prioritize scanner work and continue the OpenCL teardown audit; otherwise proceed to the admitted CPU repack backend-free-before-buffer-free ASan/LSan fixture.
