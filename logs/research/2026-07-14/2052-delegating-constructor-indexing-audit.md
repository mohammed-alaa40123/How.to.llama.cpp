# Delegating constructor indexing audit

- Run time: 2026-07-14 20:52 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: determine whether the bounded qualified-constructor scanner already recognizes same-line delegating constructors, and document the exact boundary

## Startup and inspection

Read the complete repository README first, followed by project state, research log, research ledger, and the latest detailed note. Inspected PR #1, the current source-index implementation and tests, and the commit-scoped Documentation CI result for the preceding initializer-list increment.

## Artifact

This run records a bounded source-index behavior audit rather than broadening the parser. The existing `SPECIAL_MEMBER_RE` initializer-list clause already recognizes same-line delegating constructors such as:

```cpp
backend_state::backend_state(int device)
    : backend_state(device, nullptr) {
}
```

For the scanner's actual same-line contract, the definition is represented as:

```cpp
backend_state::backend_state(int device) : backend_state(device, nullptr) {
}
```

A focused local reproduction using the branch's exact regular expression returned:

```text
backend_state::backend_state   line 1
nested::resource::resource     line 4
```

## Verified

- Documentation CI run `29352222406` completed successfully for initializer-list head `f427ab95f3a9147acfc58a7248ebc2bd312f1a24`.
- The optional initializer-list clause does not distinguish member initialization from constructor delegation; both are syntactically accepted when the complete list and opening body brace occur on one physical line.
- The class-name backreference still constrains the extracted callable to a qualified constructor or destructor definition.
- Newlines, semicolons, and braces remain excluded from the initializer-list body, so multiline delegation and braced arguments are not covered.
- No scanner implementation change was required for this bounded behavior.

## Interpretation

Delegating constructors are already part of the current same-line initializer-list capability. Recording that fact avoids carrying a false TODO and clarifies that the real unresolved boundary is multiline or brace-containing initialization, not delegation itself.

## Historical

The behavior was introduced by the initializer-list clause added in the preceding run, but that run described only member initializers and conservatively listed delegating constructors as unsupported.

## Open questions

- Add an explicit regression fixture before relying on delegating-constructor coverage as a permanent compatibility promise.
- Multiline delegating constructors, braced arguments, function-try-blocks, and in-class definitions remain unsupported.
- Complete pinned OpenCL teardown still requires searchable access to the end of the large translation unit or a regenerated local source inventory.

## Validation and CI

The preceding implementation is fully validated by GitHub-hosted Documentation CI. Direct local checkout remains blocked by `Could not resolve host: github.com`; the bounded regex behavior was reproduced independently with the exact current expression.

## Next priority

Add a focused delegating-constructor regression test, then resume pinned source regeneration and the OpenCL teardown audit. The independent CPU repack backend-free-before-buffer-free fixture remains the second highest-priority track.
