# DATA-01 first retrospective evidence batch

## Run identity

- **Starting commit:** `176729838aba05e1572feb4a24246cd994b0af65`
- **Assigned milestone:** first bounded historical extraction after the DATA-01 contract passed Documentation CI run `29568983813`
- **Learner/research outcome:** test whether heterogeneous scheduled-agent history can be represented consistently without learner identity, raw prompts, or invented measurements

## Selection and scope

The highest-priority orchestrator dependency was DATA-01 historical coverage. This increment extracts exactly three existing run archetypes:

1. a successful viewer increment with no recorded validation failure;
2. a deterministic-figure CI repair that retained strict byte-for-byte validation;
3. a blocked real Lab 0 execution followed by the next dependency-safe DATA-01 assignment.

No fourth historical run, aggregate analysis, baseline comparison, or manuscript prose was added.

## Files added or changed

- `progress/examples/agent-workflow-run-viewer-success-v0.json`
- `progress/examples/agent-workflow-run-figure-ci-repair-v0.json`
- `progress/examples/agent-workflow-run-lab0-blocked-data01-v0.json`
- `scripts/validate_agent_workflow_batch.py`
- `tests/test_validate_agent_workflow_batch.py`
- `docs/publication/evidence-backlog.md`
- `docs/reference/project-state.md`
- `docs/publication/agent-handoffs.md`
- this run record

## Validation contract

The batch validator:

- validates every record using the existing DATA-01 semantic validator;
- requires exactly three records and unique run IDs;
- classifies a clean passed run as `successful_increment`;
- classifies revised output plus a fixed failure as `ci_repair`;
- classifies an explicit blocker plus a blocked failure as `blocked_reassignment`;
- rejects duplicate records or a batch missing any required archetype.

## Claims and limitations

- **Verified:** the parent DATA-01 contract passed Documentation CI run `29568983813`.
- **Verified:** the batch contains evidence-linked records for three distinct workflow outcomes already documented in repository logs and commit-scoped CI.
- **Interpretation:** the schema appears capable of representing success, repair and dependency-safe reassignment without flattening them into a single success metric.
- **Historical:** effort counts come from prior run records and remain proxies rather than independently timed labor measurements.
- **Open Question:** independent coding agreement, broader historical coverage, missing-value policy, aggregate analysis and BASE-01 remain unevidenced.

This increment does not claim workflow superiority, educational benefit, complete history, exact human labor, or real Lab 0 reproducibility.

## Human-review needs

- Check the three records against their source logs and PR histories.
- Approve coding rules for ambiguous or missing historical fields before larger extraction.
- Keep DATA-01 in progress until final-head CI and independent first-batch review pass.

## Ending state

The ending commit and commit-scoped CI run are pending. The next dependency is human review of this batch, followed by a bounded expansion or BASE-01 fixture only after coding consistency is accepted.
