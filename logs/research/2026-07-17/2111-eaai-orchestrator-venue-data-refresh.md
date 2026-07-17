# EAAI orchestration refresh — venue, integration and retrospective state

- **Starting commit:** `9bd3e9cac12ea55909709ba0c1951e82f05e9eb0`
- **Assigned milestone:** reconcile authoritative orchestration after STACK-01, DEMO-01A, VENUE-01 and the bounded DATA-01B protocol.
- **Learner outcome:** no learner-facing feature changed; the run prevents stale priorities from directing broad or duplicate work before canonical integration.

## Evidence inspected

- authoritative orchestrator state, evidence backlog, two-week plan, roadmap, readiness scorecard and handoffs;
- recent draft PR chain through PR #35;
- Documentation CI run `29598733410`, which passed for the DATA-01B protocol head;
- official EAAI-27 requirements already retained in VENUE-01 / PR #31;
- canonical integration map in PR #33 and integrated-demo acceptance contract in PR #34.

## Changes

- updated `docs/publication/orchestrator-state.md`;
- reprioritized `docs/publication/evidence-backlog.md`;
- refreshed `docs/publication/readiness-scorecard.md`;
- corrected the stale venue state and separated evidenced specifications from executed outcomes;
- added `BLIND-01` and `DOC-AUDIT-01` as bounded Literature Scout assignments;
- preserved the Paper Integrator gate.

## Claims

- **Verified:** DATA-01B protocol head passed Documentation CI run `29598733410`.
- **Verified:** VENUE-01 records the official EAAI-27 call and replaces the stale “unverified venue” state.
- **Verified:** STACK-01 and DEMO-01A produced reviewable specifications, not an integrated execution.
- **Interpretation:** canonical integration is now the highest-value non-environment task because additional parallel features would increase merge and evidence-loss risk.
- **Open Question:** which progress implementation and merge order the human owner will approve.

## Validators and failures

- No validator was weakened.
- No timing, learner outcome, native execution or inter-rater result was fabricated.
- The central blocker remains the absence of an approved canonical merge choice and suitable Ubuntu/devcontainer environments.

## Human review needed

1. Approve PR #24 as the canonical progress base or record another choice.
2. Approve the stacked merge order and combined integration branch.
3. Nominate an independent llama.cpp/GGML reviewer.
4. Approve the retrospective study window and independent coder.
5. Approve an evaluation/ethics pathway.

## Evidence produced

A synchronized coordination state that recognizes verified venue requirements, closes DEMO-01A only as a specification, recognizes the DATA-01B protocol while keeping extraction open, and orders the next work around integration and measured evidence.

## Ending state and next dependency

The branch ending commit is recorded by the PR head. The next dependency is human approval of the canonical progress implementation, followed by one combined branch and full Documentation CI. If that remains blocked, the next dependency-safe task is `BLIND-01` or the predefined documentation-gap audit design; no broad implementation expansion is authorized.
