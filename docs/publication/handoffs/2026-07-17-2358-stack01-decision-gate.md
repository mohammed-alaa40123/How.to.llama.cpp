# STACK-01 decision-gate handoff

## Assignment status

`STACK-01` remains the highest-priority orchestrator assignment. It is blocked on explicit human approval of the canonical progress implementation and merge order.

## Bounded increment completed

Added a versioned pending decision record, schema, semantic validator and focused tests. The record freezes:

- PR #24 as the proposed canonical progress implementation;
- PR #23 as the overlapping implementation not selected for the spine;
- migration and last-known-valid recovery as preserved later follow-ups;
- the reviewed 19-PR integration order;
- #14→#13 and #23→#24 supersession;
- consistent pending, approved and validated state transitions.

## Evidence boundaries

- **Verified:** the parent head passed Documentation CI run `29609856424`; the proposed choice matches the existing canonical integration map.
- **Interpretation:** encoding the exact pending choice reduces accidental integration drift while retaining human authority.
- **Historical:** repeated runs have identified this decision as the P0 blocker.
- **Open question:** whether the human reviewer approves or amends the proposal.

## Human action

Review `progress/examples/canonical-integration-decision-pending-v0.json`. Do not create or claim a canonical integration branch until the record is approved by a named human with a timestamp.

## Next dependency

After approval, create `integration/eaai-july-vertical-slice`, apply each retained increment once, preserve conflicts and repairs, and require the complete Documentation CI suite on one combined head.
