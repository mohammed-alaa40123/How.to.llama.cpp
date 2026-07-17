# Retrospective missing-data policy

## Purpose

The EAAI case study must distinguish evidence that can be reconstructed from repository artifacts from quantities that were never measured contemporaneously. A numeric placeholder is not evidence.

## Coverage states

Each required retrospective dimension uses exactly one state:

- **observed** — a retained repository artifact supports the value or decision;
- **not reconstructable** — the historical record is insufficient for a defensible value;
- **not applicable** — the dimension did not apply to that bounded run.

Observed dimensions require one or more repository evidence paths. Non-observed dimensions require an explicit reason and must not cite evidence as though the value were known.

## Required dimensions

The first coverage contract requires assignment selection, immutable starting and ending commits, CI state, failures, human-supervision decisions, accepted/revised/rejected outputs, agent turns, tool calls, human minutes and external API cost.

The first three-record batch exposes two important limits:

- tool-call totals are not independently reconstructable from the durable run logs;
- human minutes were not recorded contemporaneously, so zero-valued workflow fields must not be interpreted as measured absence of human labor.

## EAAI claim supported or falsified

This contract supports the narrower claim that the repository can disclose retrospective missingness explicitly. It falsifies any analysis that silently treats unknown effort as zero, extrapolates three selected records into a longitudinal dataset, or compares agent efficiency using unreconstructable counts.

## Validation

Run:

```bash
python3 scripts/validate_retrospective_coverage.py \
  progress/examples/agent-workflow-coverage-first-batch-v0.json
python3 -m unittest tests.test_validate_retrospective_coverage
```

The validator requires immutable source revision, unique stable run IDs, complete required-dimension coverage, evidence for every observed field, no evidence inflation for missing fields, and at least one explicit reconstruction limitation.

## Limitations and human review

This package does not independently recode the underlying records, estimate missing labor, establish inter-rater reliability, or demonstrate workflow superiority. Before broader extraction, a human reviewer must approve the missing-value taxonomy and decide whether future runs should capture tool calls and human time prospectively.
