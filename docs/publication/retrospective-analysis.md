# Retrospective agent-workflow analysis protocol

_Status: DATA-01B protocol frozen; broader extraction and independent coding remain open._

## EAAI claim under test

The longitudinal case study may support the bounded claim that human-supervised scheduled agents can produce, validate, repair and maintain repository-native educational artifacts while exposing blockers, rejected work and human decisions. It must also be able to falsify that claim by showing duplication, unresolved failures, missing evidence, high supervision burden or non-reconstructable effort.

This protocol does **not** claim workflow superiority, labor savings, autonomous correctness or educational benefit.

## Sampling frame

The primary frame is every eligible scheduled or manual EAAI run with a durable run log during the declared study window. The frame is pinned by an immutable repository revision and explicit UTC start/end timestamps.

Preferred rule: `all_eligible_runs`. If the corpus becomes too large for independent review, use `systematic_every_nth` with a predeclared interval. Exclusions must be listed by stable run ID; silent convenience sampling is forbidden.

Eligible runs must contain an assignment or dependency decision and at least one durable repository artifact, blocker record or validation result. Pure conversational planning without durable repository evidence is excluded.

## Frozen codebook

Each run receives one value for each dimension:

| Dimension | Codes | Decision rule |
|---|---|---|
| Assignment outcome | `completed`, `partial`, `blocked_reassigned`, `blocked_stopped` | Code the final bounded outcome, not intent. |
| Selection path | `highest_priority_ready`, `blocked_then_dependency_safe`, `human_override`, `historical_reconstruction` | Use the orchestrator/backlog and run log. |
| Human intervention | `none_recorded`, `approval`, `correction`, `merge_resolution`, `environment_access`, `ethics_or_privacy_decision`, `not_reconstructable` | Do not infer unrecorded labor. |
| Validation outcome | `passed_first_attempt`, `failed_then_fixed`, `failed_unresolved`, `not_run`, `not_reconstructable` | Require a durable validator or CI reference when available. |
| Evidence completeness | `complete_for_protocol`, `partial`, `not_reconstructable` | Missingness is explicit, never encoded as zero. |
| Coding status | `single_coded`, `double_coded_agree`, `double_coded_disagree`, `adjudicated` | Independent review state, not implementation quality. |

Missing fields are limited to tool calls, human minutes, API cost, failed attempts, CI run, output decisions and blocker detail. A row marked complete cannot list missing fields. A blocked row cannot omit blocker detail.

## Double-coding and adjudication

1. The primary coder codes the frozen sample without changing the codebook.
2. An independent reviewer codes the same run IDs from the same pinned revision.
3. Exact agreement is computed per categorical field; no reliability statistic is reported until the sample size and prevalence make it interpretable.
4. Disagreements are retained, not overwritten.
5. Adjudication requires a note identifying the disputed field, evidence consulted and final decision.
6. Codebook changes require a new protocol version and recoding of the affected sample.

## Machine-checkable contract

- Schema: `schemas/retrospective-coding-batch.schema.json`
- Semantic validator: `scripts/validate_retrospective_coding_batch.py`
- Example: `progress/examples/retrospective-coding-batch-v0.json`
- Tests: `tests/test_validate_retrospective_coding_batch.py`

The validator rejects mutable revisions, duplicate run IDs or evidence paths, unsafe paths, silent missingness, blocked rows without blocker evidence, unrecorded disagreement fields and adjudication without a rationale.

## Analysis plan

Descriptive results may include counts and proportions of outcomes, blocked reassignment, validation repair, human-intervention categories and evidence completeness. Cross-tabs are exploratory. No causal claim is permitted because runs are not randomized, tasks differ in difficulty and the repository evolves over time.

The analysis must report:

- denominator and excluded-run list;
- unresolved and adjudicated coding disagreements;
- non-reconstructable effort/cost fields;
- stacked-branch and CI availability biases;
- human decisions that altered scope or canonical integration;
- accepted, revised and rejected outputs when evidenced.

## Privacy and ethics boundary

The dataset stores run IDs and repository paths, not names, email addresses, prompts, raw conversations, learner data, device identifiers or credentials. Research use of human-review labor or participant data requires a separate ethics determination. No recruitment or telemetry is authorized by this protocol.

## Acceptance criteria for closing DATA-01B

DATA-01B remains open until:

1. the sampling frame is frozen at an immutable revision;
2. a broader bounded sample is extracted with no silent exclusions;
3. every row passes the validator;
4. an independent reviewer double-codes the sample;
5. disagreements are retained and adjudicated;
6. missing effort/cost evidence is disclosed;
7. the final analysis makes no workflow-superiority claim unsupported by the design.

## Limitations

Repository logs may be incomplete, post-hoc edits can improve documentation quality, CI availability varies across branches, and tool-call or human-time totals may be impossible to reconstruct. The protocol improves transparency; it does not recover evidence that was never recorded.
