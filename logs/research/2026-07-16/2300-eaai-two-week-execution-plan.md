# EAAI executable-learning two-week plan

- Run time: 2026-07-16 23:00 Africa/Cairo
- Starting commit: `f33d16945433581e484c3b1112dc36c9f807861c`
- Branch: `agent/eaai-two-week-execution-plan`
- Assigned milestone: establish the dependency-ordered July 17-31 executable-learning implementation plan
- Learner outcome targeted: a coherent path from first build through GGUF inspection and source-level executable tracing

## Startup inspection

Read the complete README, project state, research log, research ledger, and latest detailed note. The requested publication files `orchestrator-state.md`, `evidence-backlog.md`, `two-week-execution-plan.md`, and `agent-handoffs.md` were absent from `main`.

## Bounded increment

Created the canonical two-week execution plan and initialized the agent handoff ledger. The plan defines:

- target learners and prerequisites;
- complete lesson contracts for Lab 0, Lab 1, and Executable Lecture 0;
- browser, local-native, and cloud-container execution tiers;
- legal-fixture and model-redistribution constraints;
- deterministic technical-figure authority;
- optional AI-media provenance, review, accessibility, caching, and cost gates;
- the minimum trace contract and captured/source-derived/authored evidence distinctions;
- local-only progress persistence and privacy boundaries;
- Week 1/Week 2 milestones, acceptance gates, CI lanes, evidence retention, and July 31 definition of done.

## Verified

- The repository baseline is pinned to `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- Existing project context already requires bounded increments, truth labels, source pinning, validation, and durable logs.
- The publication coordination files were absent at the start of this run.
- No new external source was introduced, so the research ledger was not changed.

## Interpretation

Architecture, fixture, validation, accessibility, privacy, and licensing gates should precede implementation. Creating broad directories or UI shells before those decisions would make later educational and EAAI claims difficult to audit.

## Open questions

- Which legal tiny/synthetic fixture should be shared by Lab 0 and the GGUF Anatomy lab?
- Which first trace is least invasive and most educational: GGUF loading, graph construction, or one-token decode?
- Which supported environments belong in the first reproducibility matrix?

## Validation and limitations

- Reviewed the document for complete lesson-contract fields and dependency ordering.
- Used repository-relative links only.
- No paid API, model download, participant data, or server-side persistence was used.
- Full local test and MkDocs execution were unavailable because this environment has no local authenticated checkout and no `gh` executable.
- CI status must be checked after the draft pull request is created.

## Human review needs

- Approve the target learner scope.
- Approve the legal fixture choice before implementation.
- Confirm whether the first trace should prioritize GGUF loading or graph construction.

## Evidence produced

- `docs/publication/two-week-execution-plan.md`
- `docs/publication/agent-handoffs.md`
- this run note

## Next dependency

The orchestrator should create/populate `orchestrator-state.md` and `evidence-backlog.md` and assign fixture selection as the next bounded task.