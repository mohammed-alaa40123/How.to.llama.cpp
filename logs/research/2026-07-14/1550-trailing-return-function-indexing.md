# Trailing-return C++ function indexing

- Run time: 2026-07-14 15:50 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: extend the approximate source index to recognize same-line trailing-return function definitions

## Startup and inspection

Read the complete repository README first, then project state, research log, research ledger, and the latest detailed note. Inspected PR #1, the current source-index implementation and tests, the final CI result for the preceding increment, and the pinned OpenCL blob before editing.

## Artifact

Extended `FUNC_RE` so definitions using C++ trailing-return syntax remain discoverable:

```cpp
auto trailing_function(int value) -> int {
    return value;
}

[[nodiscard]] auto namespace_name::trailing_method() const noexcept -> long long {
    return 0;
}
```

Added a focused unit test requiring both symbols to retain their physical definition lines.

## Verified

- Documentation CI run `29330951186` completed successfully for the preceding attributed-function increment.
- The prior function pattern stopped after optional `const` and `noexcept`, so a `-> return_type` clause prevented the opening brace from matching.
- The updated pattern accepts one bounded same-line trailing-return clause after optional qualifiers.
- The new test covers a free function and an attributed namespace-qualified `const noexcept` method at lines 1 and 5.
- All trailing-return matching excludes newlines, semicolons, and braces, preserving the physical-line invariant and avoiding declaration-only matches.
- Type extraction, duplicate retention, source ordering, and pinned URL construction are unchanged.

## Interpretation

This is a targeted navigation improvement, not a complete C++ grammar. Same-line trailing-return definitions are common and can be recognized without permitting vertical whitespace to shift source locations. Multiline return clauses, requires clauses, macros, lambdas, operators, and complex declarators remain explicit limitations.

## Historical

This increment follows the line-number repair and same-line attribute support. It removes one limitation explicitly listed by the prior run while retaining the scanner's bounded, revision-aware scope.

## Open questions

- Determine from the pinned tree whether requires clauses, export/declaration macros, operators, or multiline attributes justify additional targeted rules.
- Regenerate the complete pinned source inventory once a usable checkout is available.
- Finish the OpenCL teardown audit when the full pinned translation unit can be searched or locally indexed.

## Validation and CI

The implementation and regression test were committed to PR #1. GitHub-hosted Documentation CI is the authoritative full-suite and strict-MkDocs validation path because direct GitHub DNS resolution remains unavailable in the local runtime.

## Next priority

Inspect the commit-scoped CI run. If green, resume complete pinned OpenCL source recovery; otherwise repair the exact failing step. The next implementation track remains the admitted CPU repack backend-free-before-buffer-free fixture.
