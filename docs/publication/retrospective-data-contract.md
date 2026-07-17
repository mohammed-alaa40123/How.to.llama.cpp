# Retrospective agent-workflow data contract

## Purpose

`DATA-01` defines the minimum repository-native record needed to analyze the scheduled-agent process as a longitudinal EAAI case study. It records assignments, dependency choices, commits, accepted/revised/rejected outputs, validator failures, human-review boundaries, effort proxies and truth-labelled claims.

## Evidence boundary

- **Verified:** the schema and semantic validator require immutable commits, bounded collections, explicit output decisions, CI state, human-review state, cost proxies and evidence paths for verified claims.
- **Interpretation:** these records may support comparison of specialized scheduled agents with simpler author/reviewer workflows.
- **Historical:** earlier run logs contain much of this information in prose, but not in a consistent machine-readable form.
- **Open Question:** extraction coverage, inter-rater reliability, human effort accuracy and any workflow advantage remain unevidenced.

## Privacy and ethics

The record contains no learner identity, email, account, device/session identifiers, IP addresses, raw prompts, responses, secrets or API keys. It is operational repository evidence, not participant research data. Any later collection of learner or reviewer personal data requires a separate approved protocol.

## Required fields

- stable run ID and specialist role;
- orchestrator assignment, priority, dependency state and selection reason;
- immutable starting and ending commits plus branch identities;
- bounded repository-relative outputs marked accepted, revised or rejected;
- validators, failures, resolutions and commit-scoped CI state;
- human-supervision requirement, decisions and review status;
- agent turns, tool calls, paid-generation count, external API cost and optional human minutes;
- Verified, Interpretation, Historical and Open Question claims.

## Validation

```bash
python3 scripts/validate_agent_workflow_run.py progress/examples/agent-workflow-run-v0.json
python3 -m unittest tests.test_validate_agent_workflow_run
```

The validator rejects mutable revisions, blocked assignments without blockers, duplicate or unsafe output paths, unexplained rejected/revised outputs, passed CI without a run ID, paid generation without recorded cost, verified claims without evidence, and privacy-sensitive fields.

## Use in later analysis

The contract enables counts and timelines for assigned versus completed work, failure categories, correction rates, validator coverage, accepted/revised/rejected outputs, human-review backlog and cost proxies. It does not by itself establish that the multi-agent workflow is better than a baseline; `BASE-01` remains required.
