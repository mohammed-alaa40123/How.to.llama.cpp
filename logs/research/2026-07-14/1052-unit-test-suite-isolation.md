# Documentation CI unit-test suite isolation

- Run time: 2026-07-14 10:52 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: isolate the exact Python unit-test suite failing after the prior named-step CI observability change

## Startup and inspection

Read the complete repository README first, then project state, research log, research ledger, and the latest detailed note. Inspected PR #1, the current Documentation CI workflow, run `29312885959`, its job steps, the available decoded log, and both Python unit-test modules before editing.

## Artifact

Refined `.github/workflows/docs-ci.yml` so Python tests run in three explicit stages:

1. `tests.test_index_upstream`;
2. `tests.test_validate_interactive_links`;
3. full discovery as a guard against future unlisted test modules.

The first failing named suite will now be visible directly in the Actions job summary. Full discovery remains after both known suites so CI still verifies that no test module is accidentally omitted.

## Verified

- Documentation CI run `29312885959` completed with failure.
- Durable project-context validation and interactive-link validation both passed.
- The failure was isolated to the former aggregate `Run Python unit tests` step.
- Shell syntax, Python compilation, asset checks, dependency installation, and strict MkDocs build were skipped after the test failure.
- The repository currently contains two unit-test modules: `test_index_upstream.py` and `test_validate_interactive_links.py`.
- The available decoded job log was still truncated before the failing unittest name and traceback.

## Interpretation

The remaining ambiguity is now one level narrower: a Python unit test fails, but the previous aggregate step and truncated log did not identify which module. Running the two suites separately is a bounded observability change that preserves the full discovery guard and avoids speculative changes to tested code.

## Historical

Run IDs, step names, and the two-module inventory describe PR #1 as observed on 2026-07-14. Future test modules will still be covered by the discovery guard.

## Open questions

- Does `tests.test_index_upstream` fail first, or does `tests.test_validate_interactive_links` fail?
- What exact assertion or import error is reported by the isolated suite?
- After the unit tests pass, do shell, compilation, asset, dependency, or strict MkDocs steps expose independent failures?

## Validation and CI

A local clone was attempted and again failed with `Could not resolve host: github.com`, so checkout-based reproduction remains blocked in this runtime. The workflow edit retains Python 3.12, verbose unittest output, and complete discovery coverage.

## Next priority

Inspect the new CI run, patch the exact failing test or implementation, and continue through strict MkDocs. Once Documentation CI is green, resume the admitted CPU repack lifetime fixture or complete OpenCL teardown audit.
