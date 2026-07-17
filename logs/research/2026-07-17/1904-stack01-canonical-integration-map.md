# STACK-01 canonical integration map

- **Date:** 2026-07-17 19:04 Africa/Cairo
- **Starting commit:** `982ec391ab4ec1ed5c99b0343e62deaf149d2fb2`
- **Assigned milestone:** `STACK-01` — produce a human-reviewable canonical merge map before adding more executable-learning features.
- **Learner outcome supported:** make the Lab 0 → GGUF Anatomy → source-path reconstruction progression integrable as one artifact rather than a collection of disconnected draft branches.

## Files and state inspected

- `README.md`
- `docs/reference/project-state.md`
- `docs/reference/research-log.md`
- `docs/reference/research-ledger.md`
- `docs/publication/orchestrator-state.md`
- `docs/publication/evidence-backlog.md`
- `docs/publication/two-week-execution-plan.md`
- `docs/publication/agent-handoffs.md`
- latest orchestration run log
- open draft PR metadata and recorded component CI evidence

## Increment

Added `docs/publication/canonical-integration-map.md` with:

- one proposed canonical implementation spine;
- exact handling of parallel PRs #30, #31 and #32;
- explicit overlap decisions for trace PRs #13/#14 and progress PRs #23/#24;
- supersession rules for reviewer and orchestration snapshots;
- a human integration workflow;
- one-commit final validation requirements;
- truth-labelled claims and unresolved human choices.

## Sources

Repository PR metadata, branch ancestry and durable CI identifiers are the sources for this increment. No new external technical source was added, so the research ledger is unchanged.

## Claims

### Verified

- The current executable-learning work is distributed across a long draft-PR stack with parallel descendants.
- PRs #13/#14 and #23/#24 overlap from common bases.
- PR #25 and later learner-facing branches depend on PR #24.
- PRs #30, #31 and #32 are parallel descendants of PR #29 and cannot be blindly merged as a linear authority-state sequence.

### Interpretation

- PR #24 is the lowest-risk canonical progress choice because the downstream Lab 1 integration and benchmark/media/reviewer stack were built from it.
- Historical orchestration snapshots should retain unique run logs but not overwrite the single current authority files.

### Historical

- Hourly specialist runs intentionally produced small stacked increments while measured Ubuntu/devcontainer evidence remained blocked.

### Open Question

- Human approval of the canonical progress branch.
- Whether unique migration/recovery semantics from PR #23 should become a later bounded follow-up.
- Full combined-branch CI and deployed-site verification.

## Validators

This increment is documentation/state only. Commit-scoped Documentation CI is authoritative. The eventual canonical branch must run the complete unit, compilation, shell, strict MkDocs and built-site accessibility suite on one head.

## Failures and blockers

- No clean local checkout or native execution environment was available in this connector run.
- `STACK-01` cannot be closed until the human progress choice is recorded and the canonical combined branch passes CI.
- LAB0-03, LAB0-04, REVIEW-01 and EVAL-01 remain blocked by their existing human/environment dependencies.

## Human-review needs

- approve PR #24 as the canonical progress implementation or explicitly select PR #23 and accept downstream adaptation work;
- verify that no unique invariant is lost when superseding PR #14 and PR #23;
- approve the final integration order before closing superseded draft PRs.

## Evidence produced

- proposed canonical spine and side-branch reconciliation order;
- explicit retained/superseded/deferred decisions;
- final combined-head validation gate;
- bounded handoff for canonical integration.

- **Ending content commit:** `d26fd259b6d5a8d793d8f51c93cbdfc2aa23bf9d`
- **Next dependency:** human approval and canonical-branch execution for `STACK-01`; meanwhile `DEMO-01A` is the next dependency-safe Documentation Builder assignment.