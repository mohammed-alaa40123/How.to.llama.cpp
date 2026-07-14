# Constrained C++ function indexing and line accuracy

- Run time: 2026-07-14 16:51 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: preserve physical function lines while recognizing bounded same-line C++20 `requires` clauses

## Startup and inspection

Read the complete repository README first, then project state, research log, research ledger, and the latest detailed note. Inspected PR #1, the current source-index implementation and tests, and the latest commit-scoped Documentation CI state before editing.

## Artifact

Updated `FUNC_RE` in `scripts/index_upstream.py` so return-type whitespace is horizontal-only and same-line constrained definitions remain discoverable:

```cpp
template <typename T>
int constrained_function(T value) requires Integral<T> {
    return value;
}

template <typename T>
[[nodiscard]] auto namespace_name::constrained_method(T value) const noexcept -> T requires Serializable<T> {
    return value;
}
```

Added a focused unit test requiring the functions to resolve to their physical definition lines, 2 and 7, rather than the preceding template lines.

## Verified

- The previous return-type character class included Python regex `\s`, which includes newline.
- For a function immediately following `template <...>`, the old match could begin on the template line and report the wrong source location.
- Return-type whitespace now uses only tabs and spaces.
- One bounded same-line `requires` clause is accepted after optional qualifiers and trailing-return syntax.
- The constraint matcher excludes newlines, semicolons, and braces.
- Existing attributes, ordinary definitions, qualified methods, and trailing-return behavior remain covered by regression tests.

## Interpretation

The source index is a navigation aid, so exact physical lines are more important than accepting every legal C++ grammar form. Supporting common same-line constraints is useful, but multiline constraints and complex requires-expressions should remain explicit limitations unless pinned-tree evidence justifies a stateful scanner.

## Historical

This increment extends the same horizontal-whitespace invariant previously applied to type declarations. It also closes the `requires` limitation listed after the attributed and trailing-return indexing runs.

## Open questions

- Search the regenerated pinned tree for multiline requires-expressions, operator definitions, and declaration/export macros before expanding the scanner again.
- Regenerate the complete pinned source inventory once a usable checkout is available.
- Finish the OpenCL teardown audit when the full pinned translation unit can be searched or locally indexed.

## Validation and CI

The implementation and regression test were committed to PR #1. GitHub-hosted Documentation CI remains the authoritative full-suite and strict-MkDocs validation path because direct cloning still fails with `Could not resolve host: github.com` in this runtime.

## Next priority

Inspect the commit-scoped CI run. If green, return to pinned OpenCL source recovery; otherwise repair the exact failing step. The next independent implementation track remains the admitted CPU repack backend-free-before-buffer-free fixture under ASan/LSan.
