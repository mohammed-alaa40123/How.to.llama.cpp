# Constructor initializer-list indexing

- Run time: 2026-07-14 19:53 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: recognize common same-line out-of-class constructor definitions with initializer lists while preserving exact source lines

## Startup and inspection

Read the complete repository README first, then project state, research log, research ledger, and the latest detailed note. Inspected PR #1, the current source-index implementation and tests, and the latest successful Documentation CI run before editing.

## Artifact

Extended `SPECIAL_MEMBER_RE` in `scripts/index_upstream.py` with one bounded optional constructor initializer-list clause. It recognizes common definitions such as:

```cpp
backend_state::backend_state(int device) noexcept : device(device), handle(nullptr) {
    initialize();
}

nested::resource::resource(int value) : value_(value) {
}
```

Added focused regression coverage requiring the constructor names to resolve to their exact physical definition lines.

## Verified

- Documentation CI run `29348084640` completed successfully for the preceding special-member increment.
- The previous special-member pattern required `{` immediately after optional `noexcept` and `requires`, so constructor definitions with `: member(value)` were absent from the index.
- The added initializer clause excludes newlines, semicolons, and braces. It therefore cannot consume a preceding line or silently claim support for multiline or braced initializer forms.
- Destructor behavior and the existing ordinary-function, operator, and type patterns were not broadened.

## Interpretation

Constructor initializer lists frequently expose ownership and lifetime setup directly: device handles, queues, buffers, pool references, and synchronization objects are commonly initialized there. Indexing these definitions improves navigation to backend acquisition paths without turning the source index into an attempted C++ parser.

## Historical

This increment extends the bounded out-of-class constructor/destructor support added in the previous run. It deliberately preserves the project policy that exact physical lines are more important than broad but unreliable grammar coverage.

## Open questions

- Braced member initializers such as `member{value}` remain unsupported because braces would make a regex boundary ambiguous with the function body.
- Multiline initializer lists, delegating constructors, function-try-blocks, in-class special members, and macro-generated definitions still require pinned-tree evaluation or a stateful scanner.
- Complete pinned OpenCL teardown still requires searchable access to the end of the large translation unit or a regenerated local source inventory.

## Validation and CI

Direct local checkout remains blocked by `Could not resolve host: github.com`. The new implementation and focused test were committed to the PR branch; GitHub-hosted Documentation CI is the authoritative complete validation path.

## Next priority

Inspect the commit-scoped Documentation CI result. If green, resume pinned source regeneration and the OpenCL teardown audit. The next independent implementation track remains the admitted CPU repack backend-free-before-buffer-free fixture under ASan/LSan.
