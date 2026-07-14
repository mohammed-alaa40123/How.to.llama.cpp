# Attributed C++ function indexing

- Run time: 2026-07-14 14:52 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: extend the approximate source index to recognize same-line C++ attributes before function definitions

## Startup and inspection

Read the complete repository README first, then project state, research log, research ledger, and the latest detailed note. Inspected PR #1, `scripts/index_upstream.py`, `tests/test_index_upstream.py`, and the pinned OpenCL blob before editing.

## Artifact

Extended `FUNC_RE` so function definitions remain discoverable when one or more same-line C++ attributes precede the return type:

```cpp
[[nodiscard]] static int attributed_function(int value) {
    return value;
}

[[gnu::always_inline]] int namespace_name::attributed_method() const noexcept {
    return 0;
}
```

Added a focused unit test requiring both symbols to retain their physical declaration lines.

## Verified

- The prior function pattern required the return type to be the first non-horizontal-whitespace token, so a leading `[[...]]` attribute prevented the function from being indexed.
- The updated pattern accepts one or more same-line attribute groups before the return type.
- The test covers a free function and a namespace-qualified `const noexcept` method at lines 1 and 5.
- Type extraction, duplicate retention, source ordering, and pinned link construction are unchanged.
- The pinned OpenCL source blob is retrievable, but connector output remains truncated before the backend teardown section; no teardown claim was inferred from hidden text.

## Interpretation

Leading same-line attributes are a bounded and useful expansion for a navigation index. This does not turn the regular-expression scanner into a C++ parser; multiline attributes, declaration macros, trailing-return syntax, requires clauses, and more complex declarators remain explicit limitations.

## Historical

This increment follows the type-declaration attribute support added in the previous run and applies the same bounded policy to function definitions.

## Open questions

- Determine from the pinned tree whether multiline attributes, trailing-return functions, or export/declaration macros justify targeted scanner support.
- Regenerate the pinned source inventory once a usable pinned checkout is available.
- Finish the OpenCL teardown audit when the complete pinned translation unit can be searched or locally indexed.

## Validation and CI

A bounded local regular-expression reproduction returned the expected function names and physical lines. GitHub-hosted Documentation CI must verify the isolated source-index suite, full discovery, and strict MkDocs build. Full local checkout validation remains blocked because direct GitHub DNS resolution is unavailable in this runtime.

## Next priority

Inspect the commit-scoped CI run. If green, resume complete pinned OpenCL source recovery; otherwise repair the exact failing validator. The next implementation track remains the admitted CPU repack backend-free-before-buffer-free fixture.
