# Retrospective evidence data schema

_Last updated: 2026-07-18 08:00 Africa/Cairo_

## Purpose

This document defines the machine-readable record used to study the human-supervised scheduled-agent workflow. It is an evidence contract, not a results section and not a claim that the historical dataset is complete.

## Version 1.1 effort measurements

Schema version `1.1.0` replaces ambiguous numeric effort fields with explicit measurement objects:

```json
{
  "status": "measured | not_available | not_applicable",
  "value": 12,
  "reason": "required only when a value is unavailable or inapplicable",
  "evidence_paths": ["repository/path/to/evidence"]
}
```

Rules:

- `measured` requires a value and at least one retained evidence path.
- `not_available` and `not_applicable` must omit `value`; they require a reason.
- Zero is a valid measured value only when evidence establishes zero. It must never stand in for unavailable data.
- `agent_turns`, `tool_calls`, `paid_generation_calls`, and `human_minutes` require integer values when measured.
- `external_api_cost_usd` permits a non-negative numeric value when measured.
- A positive measured paid-generation call count requires a positive measured external API cost when both fields are available.

Legacy `1.0.0` records remain validator-compatible so existing evidence is not silently rewritten. New historical extractions with incomplete effort data must use `1.1.0`.

## Evidence and privacy boundary

Evidence paths may point to retained run logs, handoffs, CI artifacts, commits, or billing records. The record must not contain learner identity, raw prompts, raw responses, credentials, tokens, IP addresses, device identifiers, or silent telemetry.

## Claim supported or falsified

This migration supports the claim that the longitudinal case-study dataset can preserve missingness without fabricating labor, tool-use, or cost measurements. It is falsified if the validator accepts unknown measurements with numeric zero, measured values without evidence, or fractional count fields.

## Limitations

- The migration does not establish historical completeness or measurement accuracy.
- Independent double-coding and adjudication remain required.
- Legacy records may contain zeros whose provenance must be reviewed before analysis.
- No learner or participant data is authorized by this schema.
