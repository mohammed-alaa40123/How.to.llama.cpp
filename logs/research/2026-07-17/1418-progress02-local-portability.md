# PROGRESS-02 local portability and corruption recovery

## Run identity

- **Starting commit:** `dc7a8c0bb032b3f371244fc314df93292b2ed81e`
- **Assigned milestone:** `PROGRESS-02` local export/import, migration, corruption recovery and storage-adapter tests
- **Learner outcome:** a learner can preserve and restore bounded checkpoint state without an account while recognizing that local completion state is not evidence of mastery

## Assignment selection

`LAB0-02` remains the higher-priority evidence gap, but real Ubuntu/devcontainer execution remains blocked in this connector-only environment because it cannot perform the native checkout/build run. The parent DATA-01 first batch passed Documentation CI run `29572506104`; independent coding review remains human-blocked. The next dependency-safe ready task was therefore `PROGRESS-02`.

## Bounded increment

Added:

- `progress/progress_store.py`;
- `tests/test_progress_store.py`;
- updated `docs/progress/progress-schema.md`;
- publication backlog and handoff updates.

The implementation provides validated JSON export/import, explicit `0.0.1` to `0.1.0` migration, unknown-version rejection, a localStorage-shaped adapter, last-known-valid recovery, fail-closed double-corruption behavior and project-key-only clearing.

## Claims

- **Verified:** the existing `0.1.0` schema and semantic validator already prohibit identity, telemetry, raw prompt/response/code and server-sync fields.
- **Verified:** the new code reuses that validator before import, export, save or recovery acceptance.
- **Interpretation:** a last-known-valid local snapshot is a proportionate MVP recovery mechanism for anonymous progress because it avoids inventing or remotely transmitting learner state.
- **Historical:** the two-week plan required explicit schema migration and corruption recovery before connecting progress to Lab 1.
- **Open Question:** browser integration, IndexedDB/localStorage behavior in real browsers, quota failures, concurrent-tab updates and accessibility review of the eventual UI remain unvalidated.

## EAAI claim supported or falsified

This increment supports the claim that learner progress can be portable, versioned and privacy-minimizing without authenticated infrastructure. The claim is falsified if invalid or future-version data can silently overwrite valid state, if recovery invents state, or if identity/network fields enter the export.

## Validators and limitations

Eight focused tests cover round trip, migration, future-version rejection, privacy-field rejection, primary corruption recovery, double-corruption failure, absence of sync state and scoped clearing. Local execution is unavailable in the connector runtime; commit-scoped Documentation CI is the validation authority.

No participant data, learner identity, telemetry, network call, model, credential, paid API, generated media or manuscript prose was introduced.

## Human-review needs

- Review whether retaining one prior local snapshot is the preferred recovery policy.
- Approve the exact browser storage adapter before Lab 1 integration.
- Do not authorize server-side or authenticated sync through this increment.

## Ending state

The ending commit and final-head CI run are pending. After CI passes, the next dependency is a narrow browser adapter and Lab 1 integration, unless measured Lab 0 execution becomes available first.
