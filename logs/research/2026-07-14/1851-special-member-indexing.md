# Qualified constructor and destructor indexing

- Run time: 2026-07-14 18:51 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: recognize common out-of-class constructor and destructor definitions without weakening physical-line accuracy

## Startup and inspection

Read the complete repository README first, then project state, research log, research ledger, and the latest detailed note. Inspected PR #1, the current source-index implementation and tests, the latest commit-scoped Documentation CI result, and the outstanding scanner and OpenCL TODOs before editing.

## Artifact

Added a dedicated bounded `SPECIAL_MEMBER_RE` pattern to `scripts/index_upstream.py`. It recognizes same-line qualified definitions such as:

```cpp
backend_state::backend_state(int device) noexcept {
}

backend_state::~backend_state() noexcept {
}

[[deprecated("use factory")]] nested::resource::resource() requires Enabled<nested::resource> {
}
```

Added focused regression coverage requiring exact physical lines for a constructor, destructor, and attributed constrained nested constructor.

## Verified

- Documentation CI run `29343666640` passed the complete suite and strict MkDocs for the preceding operator-indexing head `c815b11fa0caddb846d60e4489a08f06592aa06f`.
- Constructors and destructors have no return type, so the ordinary function pattern cannot reliably index them.
- Requiring at least one `::` qualifier limits the new rule to out-of-class definitions and avoids treating arbitrary free functions as special members.
- The pattern uses horizontal-only leading whitespace and same-line parameter, `noexcept`, and bounded `requires` clauses, so it cannot consume a preceding template or blank line.
- Existing ordinary functions, operators, and type declarations keep their dedicated patterns and source-order behavior.

## Interpretation

Qualified constructors and destructors are high-value navigation targets because backend ownership, resource acquisition, synchronization, and release often live in RAII special members. A dedicated rule is safer than making the ordinary return-type pattern optional, which would create broad false positives.

## Historical

This increment follows the source-index sequence for exact type lines, attributes, trailing returns, constraints, and operators. It closes the common out-of-class constructor/destructor gap while preserving the project's explicit approximate-scanner boundary.

## Open questions

- In-class constructor and destructor definitions remain unsupported by design because they lack a qualification anchor.
- Constructor initializer lists, multiline signatures, defaulted/deleted declarations, literal operators, and macro-generated definitions remain unsupported.
- Complete pinned OpenCL teardown still requires searchable access to the end of the large translation unit or a regenerated local source index.

## Validation and CI

Direct local checkout remains blocked by `Could not resolve host: github.com`. GitHub-hosted Documentation CI is therefore the authoritative complete validation path. The new head requires a commit-scoped run covering isolated source-index tests, full discovery, and strict MkDocs.

## Next priority

Inspect the commit-scoped CI result. If green, resume pinned OpenCL source recovery; otherwise repair the exact failing source-index assertion. The next independent implementation track remains the admitted CPU repack backend-free-before-buffer-free fixture under ASan/LSan.
