# Local progress persistence MVP

_Last updated: 2026-07-17 14:02 Africa/Cairo_

## Learning contract

| Field | Declaration |
|---|---|
| Intended learner | A learner using Lab 1 or an executable lecture without an account |
| Prerequisite | Basic browser use and ability to save and select a JSON file |
| Learning objective | Resume bounded lesson state while distinguishing progress persistence from proof of mastery |
| Predicted misconception | Browser storage is authenticated synchronization, telemetry, or a validated learning outcome |
| Executable action | Save local progress, export JSON, clear storage, import the export, and resume the same checkpoint state |
| Observable output | The same lesson status, last step, checkpoint states, and bounded attempt counts are restored |
| Formative assessment | Identify which identity, free-text, code, prompt, response, and telemetry fields are forbidden |
| Source revision | Every accepted state contains a full immutable 40-character repository revision |
| Validation method | Shared schema semantics, deterministic round-trip tests, unsupported-version rejection, and atomic corruption recovery |
| Accessibility fallback | Human-readable JSON and validation errors; no pointer-only, color-only, animation-only, or server-dependent action |

## Verified implementation boundary

`progress/progress-store.mjs` provides a framework-free browser contract for:

- validating the existing `0.1.0` local-only progress shape;
- deterministic JSON export;
- bounded JSON import;
- explicit schema-version handling with no implicit future migration;
- a `localStorage`-compatible adapter with `load`, `save`, `clear`, `import`, and `export` operations;
- atomic import behavior: invalid or corrupt input is rejected before stored state is replaced.

The adapter stores only the fields admitted by `schemas/learner-progress.schema.json`. It rejects privacy-sensitive keys at any nesting depth and does not contact a server.

## Interpretation

This implementation makes anonymous resume state portable and recoverable. It does not establish learner identity, cross-device synchronization, assessment validity, course completion, or educational benefit.

## Historical

The project first froze the progress schema and privacy boundary before adding storage behavior. This increment intentionally reuses that contract rather than adding account, server, or telemetry fields.

## Open questions

- Lab 1 is not connected to the adapter in this increment.
- Browser-level keyboard and screen-reader verification remains a separate integrated-demo check.
- Any later schema migration must be an explicit, version-to-version function with fixtures and tests.
- Authenticated synchronization remains prohibited until hosting, privacy, consent, and ethics choices are approved.

## Security and privacy boundaries

- No cookies, account identifiers, analytics, network requests, credentials, or server-side sync.
- Import is capped at 512 KiB and validated before mutation.
- Corrupt or unsupported input leaves existing storage unchanged.
- Exported status is resume metadata, not research data and not evidence of mastery.
