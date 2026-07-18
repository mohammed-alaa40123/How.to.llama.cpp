# DATA-01 explicit unknown effort migration

- Starting commit: `6630666e2ea0f5e6dfc11113b84f60dde181d1e1`
- Assigned milestone: `DATA-01` retrospective evidence contract
- Learner outcome: indirect; this increment strengthens the credibility of the agent-workflow case-study evidence rather than changing a learner-facing lab
- Files changed: workflow-run schema, semantic validator, explicit-unknown example, focused tests, data-schema documentation, handoff, evidence backlog
- Source basis: repository-retained missing-value policy and existing schema `1.0.0`; no external source added

## Evidence produced

Schema `1.1.0` represents each effort field with a status, optional measured value, reason for unavailable/inapplicable data, and evidence paths. The validator retains legacy compatibility while rejecting zero-as-unknown and unsupported fractional count values.

## Claim supported or falsified

The increment supports or can falsify the claim that the longitudinal repository dataset preserves missing labor, tool-use, and cost information without silent imputation.

## Validators

- `scripts/validate_agent_workflow_run.py`
- `tests/test_validate_agent_workflow_run.py`
- Documentation CI on the final pull-request head

## Failures and limitations

No local test execution was available in the connector runtime. Historical completeness, independent coding agreement, and the accuracy of legacy numeric zeros remain unresolved.

## Human review needs

A second coder must independently classify missingness for the next extraction batch. Human approval is also required before any participant or personal-data collection.

## Ending state

The branch is ready for review and commit-scoped CI. The next dependency is one independently coded `1.1.0` historical record and adjudication of any disagreement.
