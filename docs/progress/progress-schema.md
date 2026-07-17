# Local learner progress contract

_Last updated: 2026-07-17 03:03 Africa/Cairo_

## Learning and privacy boundary

| Field | Requirement |
|---|---|
| Intended learner | A learner completing browser-first labs or executable lectures without an account |
| Prerequisite | Basic browser use and ability to export/import a JSON file |
| Learning objective | Resume checkpoints while understanding that progress state is local evidence, not proof of mastery |
| Predicted misconception | Local progress storage is equivalent to authenticated cloud sync or research telemetry |
| Executable action | Export, validate, clear, and re-import a versioned progress JSON file |
| Observable output | Restored lesson status, last step, checkpoint states, and attempt counts |
| Formative assessment | Identify which fields are intentionally excluded and explain why completion is not a learning-outcome claim |
| Source revision | Every export pins the course repository revision used when it was created |
| Validation | JSON Schema plus dependency-free semantic validator and malformed-input tests |
| Accessibility fallback | Downloadable JSON, readable validation errors, and no interaction that depends on color or pointer input |

## Verified contract

The first schema is `0.1.0` and permits only:

- course identity and semantic version;
- one immutable 40-character repository revision;
- timezone-aware export timestamp;
- the fixed storage scope `local-only`;
- lesson version, status, last step, checkpoint state, and bounded attempt counts.

The validator rejects names, email addresses, usernames, user/device/session identifiers, IP addresses, raw prompts, responses, code, and telemetry fields at any nesting depth. It also rejects duplicate IDs, impossible status transitions, mutable source refs, unbounded exports, and inconsistent checkpoint attempt counts.

## Interpretation

This contract provides portable resume state and machine-checkable privacy minimization. It does **not** establish learner identity, authenticated synchronization, cross-device persistence, assessment validity, or learner benefit.

## Import and corruption behavior

The browser implementation must validate before replacing current state. Invalid, unsupported, oversized, or corrupt files must leave existing local state unchanged and return a readable error. Migration across schema versions is not implicit: a future version must provide an explicit tested migration function.

## Non-goals

- no server, account, email, or authentication;
- no silent telemetry or research-data collection;
- no raw learner code, prompts, or free-text responses;
- no claim that `completed` means conceptual mastery;
- no automatic merge of conflicting exports in version `0.1.0`.

## Artifacts

- Schema: `schemas/learner-progress.schema.json`
- Validator: `scripts/validate_learner_progress.py`
- Example: `progress/examples/local-progress-v0.json`
- Tests: `tests/test_validate_learner_progress.py`
