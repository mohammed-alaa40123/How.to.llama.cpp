# DATA-01 retrospective missing-data policy

- **Starting commit:** `4c72b8908c0d41941a7f61f2d041a2668a788af5`
- **Assigned milestone:** `REVIEW-02` closure first; blocked because no commit-scoped workflow run was visible for the reviewer head
- **Dependency-safe task:** bounded `DATA-01` extension
- **Learner outcome:** not a learner-facing increment; strengthens the evidence package by preventing unknown effort from being treated as measured zero
- **Date:** 2026-07-17 18:00 Africa/Cairo

## Inspected

README, project state, research log, research ledger, orchestrator state, evidence backlog, two-week execution plan, handoff ledger, current open PR stack, reviewer run log and current workflow state.

## Verified

- The first DATA-01 batch contains three selected workflow records.
- The records retain assignments, revisions, outputs, CI state, failures, supervision decisions and cost fields.
- Durable historical logs do not independently reconstruct complete tool-call totals or contemporaneous human minutes.
- REVIEW-02 head `4c72b8908c0d41941a7f61f2d041a2668a788af5` had no visible commit-scoped workflow run at selection time.

## Increment

Added a versioned retrospective-coverage schema, semantic validator, first-batch coverage declaration, seven focused tests and a missing-data policy. The validator requires evidence paths for observed fields, forbids evidence paths for non-observed fields, requires all core dimensions and exposes at least one reconstruction limit.

## Interpretation

Explicit missingness is more defensible than treating unavailable effort measurements as zero. This strengthens transparency but does not make the selected batch longitudinal or independently coded.

## Historical

The adversarial reviewer identified the three-record sample and hidden human labor as major rejection risks. This increment addresses only the missing-value-policy dependency.

## Open questions

- Should future scheduled runs capture tool calls and human minutes prospectively?
- Who will independently code the first batch and approve the taxonomy?
- How many additional runs and roles are required before longitudinal analysis is defensible?

## Validators

- `python3 scripts/validate_retrospective_coverage.py progress/examples/agent-workflow-coverage-first-batch-v0.json`
- `python3 -m unittest tests.test_validate_retrospective_coverage`
- full Documentation CI

## Human review needs

Approve the three-state missingness taxonomy, review the classification of tool calls and human minutes, and prohibit efficiency comparisons until those fields are measured or defensibly reconstructed.

## Evidence produced

- `schemas/retrospective-coverage.schema.json`
- `scripts/validate_retrospective_coverage.py`
- `progress/examples/agent-workflow-coverage-first-batch-v0.json`
- `tests/test_validate_retrospective_coverage.py`
- `docs/publication/retrospective-missing-data-policy.md`

## Next dependency

Obtain commit-scoped CI, then independently review the first three records and missingness classifications before expanding the retrospective sample.
