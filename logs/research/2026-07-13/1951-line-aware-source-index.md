# Line-aware source indexing increment

- Run time: 2026-07-13 19:51 Africa/Cairo
- Scope: make very large pinned source files reviewable by adding approximate symbol kinds and 1-based declaration lines to the generated source inventory
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Updated `scripts/index_upstream.py`, added `tests/test_index_upstream.py`, and documented the new format in `docs/reference/source-index.md`.

## Verified

- Every indexed file now receives an untruncated, source-ordered `symbol_locations` list.
- Each record contains `name`, `kind` (`function` or `type`), and a 1-based `line`.
- The existing compact `symbols` field remains for compatibility and preserves its 500-name cap.
- Duplicate names remain in `symbol_locations`, allowing overloads and conditional-compilation branches to remain visible as navigation targets.
- Regression tests cover line calculation, source ordering, scoped function names, and duplicate declarations.

## Interpretation

- This removes the repository's tooling blocker for navigating very large translation units such as `ggml-opencl.cpp`, but does not turn regex extraction into a compiler-grade call graph.
- The generated locations should be used to select review ranges; human source review remains the authority for ownership, dispatch, and synchronization claims.

## Historical

- The previous generated inventory stored only a deduplicated, alphabetized symbol-name list capped at 500 entries per file, which could hide later declarations in large files.

## Open questions

- Whether to generate direct pinned GitHub line links from `symbol_locations`.
- Whether class methods, constructors, destructors, macros, lambdas, and template specializations need separate extractors.
- Whether a future tree-sitter or compiler-assisted index should replace the regex layer.

## Validation

- Connector-side review confirmed the implementation and test fixture structure.
- Local validation could not run because cloning the pinned source failed with `Could not resolve host: github.com`.
- CI and Pages verification are recorded in project state.

## Next priority

Regenerate the pinned source index, locate the exact OpenCL backend/context destruction and synchronization symbols, and finish the backend-before-scheduler classification.
