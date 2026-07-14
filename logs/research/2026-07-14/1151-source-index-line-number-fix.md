# Source-index type line-number fix

- Run time: 2026-07-14 11:51 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: diagnose and repair the isolated source-index unit-test failure in Documentation CI

## Startup and inspection

Read the complete repository README first, then project state, research log, research ledger, and the latest detailed note. Inspected PR #1, Documentation CI run `29316377253`, job `87031262029`, the isolated test steps, `tests/test_index_upstream.py`, and `scripts/index_upstream.py` before editing.

## Artifact

Changed `CLASS_RE` in `scripts/index_upstream.py` from leading `\s*` to horizontal `[\t ]*` and changed the separator before the type name to `[\t ]+`.

The old pattern could begin a match on the blank line before a class, struct, or enum because Python `\s` includes newline. `line_number(text, match.start())` would then report the preceding blank line instead of the declaration line. The existing regression expected `enum class second_type` on line 8, while the old match began on line 7.

## Verified

- Documentation CI run `29316377253` completed with failure in the isolated `Test source indexing` step.
- Durable project-context and interactive-link validation passed before that failure.
- The source-index test fixture contains a blank line immediately before `enum class second_type` and expects line 8.
- Reproducing the regex behavior showed the old `^\s*` pattern starts at line 7 because it consumes the preceding newline.
- The corrected `^[\t ]*` pattern starts at the actual declaration and reports line 8.
- Function extraction behavior is unchanged.

## Interpretation

This was an implementation defect rather than a brittle test: source locations should identify the declaration line, and a multiline-leading-whitespace pattern made generated pinned links point one line early whenever a type declaration followed blank space.

## Historical

The defect was introduced with line-aware source indexing on the current documentation branch. The finding and workflow IDs describe PR #1 as observed on 2026-07-14.

## Open questions

- Does the next Documentation CI run pass both isolated suites and full discovery?
- Do shell syntax, Python compilation, required assets, dependency installation, or strict MkDocs reveal a later independent failure?
- Should additional tests cover declarations preceded by multiple blank lines and indented declarations inside namespaces?

## Validation and CI

A bounded local regex reproduction confirmed the old line result of 7 and the corrected result of 8. Full checkout-based validation remains unavailable because `gh` is not installed and direct cloning has previously failed DNS resolution in this runtime. The next branch-head Actions run is the authoritative full-suite check.

## Next priority

Inspect the new Documentation CI run. If green through strict MkDocs, resume the admitted CPU repack lifetime fixture; otherwise repair the next exact failing step.