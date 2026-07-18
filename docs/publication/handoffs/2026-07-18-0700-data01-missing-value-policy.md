# Handoff — DATA-01 missing-value and coding policy

## Assignment status

`STACK-01` remains blocked by the human canonical-progress and merge-order decision. `PROGRESS-02` was not duplicated because PRs #23 and #24 already implement overlapping portability and corruption-recovery approaches. The next dependency-safe orchestrator item was therefore `DATA-01`.

## Bounded increment

Added `docs/publication/retrospective-missing-value-policy.md`, defining:

- a durable-source hierarchy;
- explicit handling for unknown effort, cost and validation values;
- a prohibition on using zero to mean unavailable;
- blocked-versus-failed and repair-run coding rules;
- output acceptance/revision/rejection evidence requirements;
- double-coding and named human adjudication;
- acceptance gates for the next extraction batch.

## Claim supported or falsified

This supports an auditable longitudinal case-study design only if later extraction follows the policy. It is falsified by uncited values, silent imputation, inferred human approval or collapsed outcome categories.

## Limitations

No broader extraction, inter-rater study, baseline comparison, learner data, model, paid API or manuscript prose was produced. The current schema still cannot encode unknown required effort fields; incomplete candidates must remain staged or excluded until a reviewed migration exists.

## Next dependency

Validation Architect: apply this policy to the next bounded DATA-01 sample and report exclusions. Human reviewer: approve an explicit unknown-value schema representation and independently double-code the predefined sample. Orchestrator: resolve `STACK-01` before canonical integration.
