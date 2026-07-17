# Local learner progress contract

_Last updated: 2026-07-17 14:18 Africa/Cairo_

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
| Validation | JSON Schema, semantic validator, explicit migration, round-trip tests and corruption-recovery tests |
| Accessibility fallback | Downloadable readable JSON, readable validation errors, and no interaction that depends on color or pointer input |

## Verified contract

The current schema is `0.1.0` and permits only:

- course identity and semantic version;
- one immutable 40-character repository revision;
- timezone-aware export timestamp;
- the fixed storage scope `local-only`;
- lesson version, status, last step, checkpoint state, and bounded attempt counts.

The validator rejects names, email addresses, usernames, user/device/session identifiers, IP addresses, raw prompts, responses, code, and telemetry fields at any nesting depth. It also rejects duplicate IDs, impossible status transitions, mutable source refs, unbounded exports, and inconsistent checkpoint attempt counts.

## PROGRESS-02 portability MVP

`progress/progress_store.py` provides a dependency-free core that can be reused by a browser adapter:

- deterministic JSON export after semantic validation;
- bounded UTF-8 JSON import that validates before replacing local state;
- explicit migration from the bounded legacy `0.0.1` shape to `0.1.0`;
- rejection of unknown future schema versions rather than guessing;
- a localStorage-shaped adapter with a last-known-valid recovery snapshot;
- fail-closed behavior when both primary and recovery snapshots are corrupt;
- explicit clearing of only project-owned progress keys.

The migration adds only fields already defined by the current privacy contract: `storage_scope: local-only` and a missing nullable `last_step_id`. It does not infer mastery, merge conflicts, create identities, or contact a server.

## Corruption behavior

A save retains the previous serialized state as a recovery snapshot before replacing the primary value. On load:

1. a valid primary snapshot is returned normally;
2. an invalid primary snapshot may be replaced by the last valid recovery snapshot;
3. if both are invalid, the adapter returns no progress plus a readable error and does not invent state.

This is deterministic application-level recovery, not durable storage protection. Browser storage can still be cleared by the learner, browser, or operating system.

## Interpretation

This contract provides portable resume state and machine-checkable privacy minimization. It does **not** establish learner identity, authenticated synchronization, permanent persistence, assessment validity, or learner benefit.

## Non-goals

- no server, account, email, authentication or authenticated sync;
- no silent telemetry or research-data collection;
- no raw learner code, prompts, or free-text responses;
- no claim that `completed` means conceptual mastery;
- no automatic merge of conflicting exports in version `0.1.0`;
- no automatic migration from unknown versions.

## Artifacts

- Schema: `schemas/learner-progress.schema.json`
- Validator: `scripts/validate_learner_progress.py`
- Portability/recovery core: `progress/progress_store.py`
- Example: `progress/examples/local-progress-v0.json`
- Validation tests: `tests/test_validate_learner_progress.py`
- Portability tests: `tests/test_progress_store.py`
