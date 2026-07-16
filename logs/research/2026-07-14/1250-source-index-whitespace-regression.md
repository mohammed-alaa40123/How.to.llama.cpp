# Source-index whitespace regression coverage

- Run time: 2026-07-14 12:50 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: verify the preceding type-line fix in CI and add bounded regression coverage for multiple blank lines and namespace indentation

## Startup and inspection

Read the complete repository README first, then project state, research log, research ledger, and the latest detailed note. Inspected PR #1, branch-head Documentation CI run `29319949484`, `scripts/index_upstream.py`, and `tests/test_index_upstream.py` before editing.

## Artifact

Extended `tests/test_index_upstream.py` with a focused regression that places two type declarations inside a namespace after multiple blank lines and with different indentation depths.

The test requires `extract_symbols()` to report the declaration lines themselves:

```text
indented_type      → line 4
more_indented_type → line 9
```

## Verified

- Documentation CI run `29319949484` completed successfully for commit `0e486859740650a998ee07531389dccc19e88e00`.
- The prior horizontal-whitespace repair passed both isolated unit-test suites, full discovery, and the later Documentation CI stages.
- `CLASS_RE` anchors at the beginning of each physical line and accepts horizontal indentation without consuming newline characters.
- The new fixture covers multiple blank lines before declarations and declarations indented inside a namespace.

## Interpretation

The successful CI run closes the original line-number defect. The additional regression protects the intended invariant rather than changing extraction behavior: a symbol location must point to the declaration line regardless of preceding vertical whitespace or namespace indentation.

## Historical

The original defect was introduced by using `\s*` in the line-aware type regex. It was fixed on the current branch by restricting leading whitespace to `[\t ]*`; this run adds coverage for the remaining whitespace cases listed in the README.

## Open questions

- Add coverage for nested class scopes, attributes, and templated type declarations if the regex index is expanded.
- Regenerate the pinned source inventory once a usable pinned llama.cpp checkout is available.
- Validate generated blob URLs and line fragments against the pinned revision in CI.

## Validation and CI

The previous branch-head Documentation CI run is green. The new test commit should be verified by the next commit-scoped workflow run. Full local checkout validation remains unavailable because direct GitHub DNS resolution is blocked in this runtime.

## Next priority

Inspect the new CI run. If green, resume either pinned OpenCL teardown source recovery or the first admitted CPU repack backend-free-before-buffer-free fixture.
