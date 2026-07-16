# Function-try-block source-index boundary audit

- Run time: 2026-07-15 00:52 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: determine whether the approximate source scanner recognizes or measures out-of-class constructor function-try-block definitions

## Startup and inspection

Read the complete repository README first, followed by project state, research log, research ledger, and the latest detailed note. Inspected `scripts/index_upstream.py`, the constructor matcher, unsupported-syntax counters, and focused constructor-boundary tests before writing this note.

## Artifact

Completed a bounded behavior audit for constructor function-try-blocks such as:

```cpp
backend_state::backend_state(int device)
try : device(device) {
    initialize();
} catch (...) {
    recover();
}
```

No production regex was broadened in this increment.

## Verified

- `SPECIAL_MEMBER_RE` expects optional `noexcept`, optional `requires`, an optional same-line parenthesized initializer list, and then the function-body `{`.
- A `try` token between the constructor signature and initializer/body prevents `SPECIAL_MEMBER_RE` from matching the constructor.
- `BRACED_CONSTRUCTOR_INITIALIZER_RE` and `MULTILINE_CONSTRUCTOR_INITIALIZER_RE` are scoped to constructor initializer syntax and do not count function-try-blocks.
- Therefore constructor function-try-blocks are explicit false negatives: they produce neither a navigation record nor unsupported-syntax telemetry.
- This behavior is consistent with the README and project-state caveat that function-try-blocks remain unresolved.

## Interpretation

The current omission is safer than partially indexing a constructor at the wrong line or treating the `catch` body as the constructor body. The next useful implementation step is a bounded telemetry counter, not immediate symbol extraction. Candidate volume from the pinned tree should determine whether a stateful scanner is justified.

## Historical

Constructor support was intentionally expanded in narrow stages: qualified special members, same-line parenthesized initializers, delegating constructors, negative boundary tests, and candidate counters for braced and multiline initializers. Function-try-blocks remained outside those contracts.

## Open questions

- How many constructor function-try-block candidates occur in the pinned llama.cpp revision?
- Can a bounded counter distinguish constructor function-try-blocks from ordinary function function-try-blocks without false positives?
- If candidates are present, should navigation target the constructor signature line or the `try` line?
- Complete pinned OpenCL teardown still requires searchable access to the hidden portion of `ggml-opencl.cpp` or a regenerated local inventory.

## Validation and CI

This increment changes documentation only. Local checkout validation remains blocked because direct GitHub DNS resolution fails. GitHub-hosted Documentation CI is the authoritative validation path.

## Next priority

Add bounded function-try-block telemetry only if pinned-tree evidence or a focused fixture demonstrates value; otherwise prioritize pinned inventory regeneration/OpenCL teardown or the admitted CPU repack backend-free-before-buffer-free sanitizer fixture.
