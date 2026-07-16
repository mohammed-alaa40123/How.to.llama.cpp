# Bounded C++ operator-function indexing

- Run time: 2026-07-14 17:49 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: recognize common same-line operator definitions without weakening physical-line accuracy

## Startup and inspection

Read the complete repository README first, then project state, research log, research ledger, and the latest detailed note. Inspected PR #1, the source-index implementation and tests, the pinned OpenCL CMake composition, the pinned OpenCL blob identity, and the latest commit-scoped Documentation CI result before editing.

## Artifact

Added a dedicated bounded operator-definition pattern to `scripts/index_upstream.py`. It recognizes qualified same-line definitions for:

- symbolic operators such as `operator==`;
- call and subscript operators, `operator()` and `operator[]`;
- `new`, `delete`, `new[]`, and `delete[]` spellings;
- single-token conversion targets such as `operator bool`.

Added focused regression coverage requiring exact source lines for `tensor_view::operator==`, `tensor_view::operator()`, `tensor_view::operator[]`, and `resource::operator bool`.

## Verified

- The preceding constrained-function increment passed complete Documentation CI run `29339261751`.
- The ordinary function regex cannot index operators because its captured name is restricted to identifier components.
- Conversion operators require a separate pattern because they have no return type before the operator name.
- Initial Documentation CI run `29343286214` failed specifically in `Test source indexing`.
- Local reproduction showed that the first operator pattern matched `resource::operator bool` but not symbolic/call/subscript definitions because it omitted the return-type prefix used by those forms.
- The corrected pattern makes the return-type prefix optional and horizontal-only: symbolic operators consume it, while conversion operators omit it.
- The focused fixture now reproduces all four expected names and exact lines locally.
- Existing ordinary-function and type patterns are unchanged.
- The pinned OpenCL implementation blob is `f283f65690af7790e163092207647d16dac9fb3e`, and its CMake target compiles `ggml-opencl.cpp`; connector output still truncates the large blob before teardown symbols.

## Interpretation

Operator definitions are especially useful navigation targets in RAII-heavy backend code, where ownership and release behavior may live in overloaded call, subscript, comparison, or conversion functions. A dedicated bounded regex is safer than broadening the ordinary function-name pattern until it accepts arbitrary punctuation.

The failed first run was an implementation defect rather than a brittle test: the fixture correctly distinguished operators that require a return type from conversion operators that do not.

## Historical

This increment extends the line-aware scanner after support for same-line attributes, trailing returns, and bounded constraints. It closes the operator-definition gap recorded in the living TODO list while preserving the project policy that the index is approximate rather than compiler-grade.

## Open questions

- Multiline operator signatures and complex conversion targets remain unsupported.
- Constructors, destructors, literals, and arbitrary macro-generated definitions still require pinned-tree evaluation.
- The full pinned OpenCL teardown audit still requires searchable access to the end of the large translation unit or a regenerated local source index.

## Validation and CI

The first commit-scoped run failed in the isolated source-index suite and was repaired with the optional return-type prefix. Documentation CI run `29343454516` started for fix commit `49f89f460e076d00e2bd95043c0885304f1fcc25`; full-suite and strict-MkDocs completion were pending at the final detailed-note update.

## Next priority

Inspect the corrected commit-scoped CI run. If green, return to pinned OpenCL source recovery; otherwise repair the exact failing step. The next independent implementation track remains the admitted CPU repack backend-free-before-buffer-free fixture under ASan/LSan.
