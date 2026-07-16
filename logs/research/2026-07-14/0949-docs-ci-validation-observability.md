# Documentation CI validation observability increment

- Run time: 2026-07-14 09:49 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: make the recurring Documentation CI validation failure actionable without changing validation semantics

## Startup and inspection

Read the complete repository README first, then project state, research log, research ledger, and the latest detailed note. Inspected PR #1, `.github/workflows/docs-ci.yml`, the validation scripts, the latest failed Documentation CI run, its job steps, and the decoded job log before editing.

## Artifact

Refactored `.github/workflows/docs-ci.yml` so the former compound validation block is split into named steps:

1. durable project-context validation;
2. interactive-link validation;
3. verbose Python unit tests;
4. shell syntax validation;
5. Python bytecode compilation;
6. required interactive-asset checks.

The commands themselves are unchanged except that unittest now uses `-v` so a failing test name is visible in the Actions UI and logs.

## Verified

- Documentation CI run `29309938483` failed in the compound step `Validate project context, interactive links, and scripts`.
- Checkout, Python setup, and startup-context reading succeeded.
- Dependency installation and strict MkDocs building were skipped after the compound step failed.
- The connector-decoded job log was truncated before the final failing command or assertion, so the previous workflow structure did not expose which validator failed.
- Splitting the commands into named steps preserves their order and failure semantics while making the failing subsystem visible in the workflow job summary.

## Interpretation

This is an observability fix rather than a claim that the underlying validation bug is already repaired. The next CI run should identify the exact failing validator or test, allowing a bounded follow-up fix instead of speculative changes.

## Historical

The workflow structure and run IDs are revision-sensitive. This note describes PR #1 and the workflow state observed on 2026-07-14.

## Open questions

- Which named validation step fails on the new workflow head?
- If the unit-test step fails, which exact test and assertion are responsible?
- If validation passes, does strict MkDocs reveal a second independent issue?
- Should future workflows upload validation logs as artifacts, or are named steps and verbose unittest output sufficient?

## Validation and CI

Local cloning was attempted again and failed with `Could not resolve host: github.com`, so checkout-based validation remains unavailable in this runtime. The workflow change itself is valid YAML by inspection and retains the original commands as separate steps. A new pull-request workflow run should start from commit `25c21b506c83eaff590bb59e2a34c83fefc5a5d4` or a later metadata-update head.

## Next priority

Inspect the new Documentation CI run, fix the exact named failing validator when possible, then return to the admitted CPU repack lifetime fixture or the complete OpenCL teardown audit.
