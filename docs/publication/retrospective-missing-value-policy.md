# Retrospective evidence missing-value and coding policy

_Last updated: 2026-07-18 07:00 Africa/Cairo_

## Purpose

This policy governs `DATA-01` extraction from scheduled-agent run logs, commits, pull requests, CI records and retained artifacts. It prevents absent historical measurements from being converted into plausible-looking numbers and defines the minimum consistency checks required before expanding the longitudinal dataset.

## EAAI claim supported or falsified

The policy can support the claim that the agent-workflow case study is auditable and does not silently impute human labor, tool usage, cost or validation outcomes. The claim is falsified when a dataset record contains an uncited value, treats absence as zero, collapses blocked and failed runs, or labels an output accepted without durable evidence.

## Source hierarchy

Use the first available source in this order:

1. retained machine-readable artifact or workflow result;
2. immutable commit or pull-request metadata;
3. durable `logs/research/` run record;
4. `docs/publication/agent-handoffs.md` or a bounded handoff;
5. reconstructed interpretation, explicitly labelled and never used as a measured value.

A later source may clarify an earlier source but must not overwrite contradictory evidence silently. Record the contradiction and require adjudication.

## Missing-value rules

| Field class | Allowed representation | Prohibited representation |
|---|---|---|
| Exact revisions, run IDs and artifact IDs | Exact retained value or record exclusion | Mutable branch name presented as an immutable revision |
| Tool calls, agent turns and human minutes | Exact retained count; otherwise `unknown` in the extraction worksheet | `0` used to mean unavailable |
| External API cost | Exact billing/usage record; otherwise `unknown` | Estimated cost presented as paid cost |
| Paid generation calls | Exact retained invocation count; otherwise `unknown` | Inferring calls from the presence of an asset |
| CI state | Exact commit-scoped workflow state | Treating queued or absent CI as passed |
| Output decision | `accepted`, `revised` or `rejected` only with a cited review, commit or validator result | Inferring acceptance because a file exists |
| Failure outcome | `fixed`, `deferred`, `blocked` or `not_reproducible` with cited evidence | Collapsing blocked dependencies into technical failure |

The current `agent-workflow-run` schema requires numeric effort fields. Until a reviewed schema revision represents unknown values explicitly, records with unknown required effort values must remain in a staging worksheet and must not be added to the canonical JSON dataset.

## Coding rules

1. One record represents one bounded assignment selection and its resulting reviewable increment.
2. A repair run is separate from the run that first exposed the failure unless the durable record explicitly treats them as one bounded iteration.
3. `blocked` means a required dependency or permission prevented execution; `failed` means the attempted path produced a negative technical or validation result.
4. Reassignment after a blocker must retain both the blocker and the dependency-safe task selected.
5. Claims must use only `Verified`, `Interpretation`, `Historical` or `Open Question` and cite repository evidence paths.
6. Human approval, technical review and ethics approval may never be inferred from a mergeable PR, passing CI or an agent-authored note.
7. A successful model-free launch may not be coded as model loading, inference or time to first token.
8. Browser-derived, authored/source-derived and native-captured evidence remain separate categories.

## Double-coding and adjudication

Before publication analysis, two coders independently classify a predefined sample. They must compare assignment ID, dependency state, output decisions, failure category/resolution, evidence labels and missing-value status. Disagreements are retained, adjudicated by a named human reviewer and linked to the final record. No inter-rater statistic is reported until the sample frame and coding decisions are retained.

## Acceptance checklist for the next extraction batch

- Every record validates against the accepted schema.
- Every nonzero effort or cost value has a direct source.
- No unavailable value is encoded as zero.
- Commit, CI and artifact identifiers resolve to the stated evidence.
- Blocked, failed, repaired and clean-success outcomes remain distinguishable.
- Output decisions cite acceptance, revision or rejection evidence.
- At least one independent coder reviews the batch before it is used for claims.
- The batch report lists excluded candidate records and exclusion reasons.

## Claim boundaries

**Verified:** the existing first DATA-01 batch demonstrates that three workflow archetypes can be represented and validated.

**Interpretation:** explicit exclusion is more defensible than numeric imputation for incomplete historical effort records.

**Historical:** early run logs were not designed as complete time-and-motion records, so some effort fields may be unavailable.

**Open Question:** the rate and pattern of missing fields across the full repository history are not yet measured, and workflow superiority remains unevaluated pending `BASE-01`.
