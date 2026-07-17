# STACK-01 canonical decision gate

- **Started from:** `b2a39213615e39852cbfd90f23296a493c8e63a2`
- **Assigned milestone:** `STACK-01` canonical integration
- **Learner outcome:** no learner-facing behavior changed; this increment reduces the integration blocker that prevents the three experiences from becoming one reviewable route.

## Dependency assessment

### Verified

- The reviewed canonical map selects PR #24 over overlapping PR #23 because PR #25 and later learner-facing work depend on #24.
- `STACK-01` cannot be closed without explicit human approval and a combined integration branch that passes the full Documentation CI suite.
- Parent Documentation CI run `29609856424` passed on the starting commit.

### Interpretation

A machine-readable pending decision record is the narrowest useful increment: it makes the exact human choice, retained follow-ups, superseded branches and status transition reviewable without claiming that approval has happened.

### Historical

Earlier runs produced the canonical integration map and repeatedly recorded the unresolved progress-store choice as the highest-priority blocker.

### Open question

Whether the human reviewer approves PR #24 as the canonical progress implementation and the listed spine without amendment.

## Files produced

- `schemas/canonical-integration-decision.schema.json`
- `scripts/validate_canonical_integration_decision.py`
- `progress/examples/canonical-integration-decision-pending-v0.json`
- `tests/test_validate_canonical_integration_decision.py`

## Validation contract

The validator requires the reviewed 19-PR spine, PR #24 as the selected progress implementation, PR #23 as the overlapping rejected implementation, preservation of migration and last-known-valid recovery as later follow-ups, explicit #14→#13 and #23→#24 supersession, immutable source revision and consistent human-approval/status transitions.

It rejects invented reviewer identities or timestamps, merge-order drift, loss of follow-up ideas and any `validated` state that does not cite combined CI.

## Safety and evidence boundaries

- No branch was merged or closed.
- No human approval was invented.
- No learner data, telemetry, model weights, paid API call, server sync or manuscript prose was introduced.
- Passing validator tests would prove decision-record consistency only, not canonical integration or educational benefit.

## Human review needed

Approve, reject or amend the pending decision record. Only an approved record may authorize creation of `integration/eaai-july-vertical-slice`.

## Next dependency

After approval, create the canonical integration branch, apply each retained increment once, run the complete Documentation CI suite and retain conflicts and repairs. Until then, `STACK-01` remains in progress.
