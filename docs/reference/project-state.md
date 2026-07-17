# Project state

_Last updated: 2026-07-17 14:04 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Executable-learning Week 1 foundation — validated vertical slices plus auditable retrospective evidence**

## Completed foundations

- Source-pinned MkDocs documentation, strict CI, deployment checks and durable run context.
- Frozen July 17-31 learning contracts for Lab 0, Lab 1 and Executable Lecture 0.
- Legal model-free and learner-provided-model policy plus deterministic synthetic GGUF fixture.
- Lab 0 phase and reproducibility contracts; real environment rows remain open.
- Versioned trace, progress, media and retrospective-workflow schemas and validators.
- Corrected source-pinned authored trace, deterministic replay and keyboard-operable static viewer.
- Deterministic GGUF-layout figure with provenance and exact replay.
- Browser-first GGUF Anatomy slice with Predict-Discover-Explain checkpoints.
- DATA-01 contract and first three-archetype retrospective batch with passing parent CI.

## Latest bounded increment

### Verified

- The first DATA-01 batch passed commit-scoped Documentation CI run `29572506104`.
- Real Lab 0 execution was retried first but remained blocked because this runtime could not resolve `github.com`; no environment row was fabricated.
- `progress/progress-store.mjs` now implements deterministic export, bounded import, explicit version handling and a framework-free `localStorage`-compatible adapter.
- Import validates before mutation, so corrupt, oversized, privacy-unsafe or unsupported input cannot replace existing local state.
- Focused Node-backed tests cover deterministic round trip, storage preservation after corrupt import, unsupported versions, privacy-sensitive fields, clear behavior and empty export.

### Interpretation

- Local progress can be portable and privacy-minimizing without introducing accounts, telemetry or server dependencies.
- This is implementation evidence for resume-state handling, not evidence that completion implies learning or that browser storage provides authenticated sync.

### Historical

- The storage behavior was added only after the `0.1.0` schema and privacy contract were frozen.
- The design intentionally rejects implicit migration and requires a future explicit migration function for every new schema version.

### Open questions

- Final-head CI must pass for the progress implementation.
- Lab 1 is not connected to the adapter in this bounded increment.
- Browser-level keyboard, screen-reader and corruption-recovery verification remains part of the integrated demo.
- Real Ubuntu and devcontainer Lab 0 measurements remain absent.
- Independent technical review and an approved educational evaluation pathway remain required.

## Immediate next task

```text
obtain commit-scoped CI for PROGRESS-02
  → connect the validated adapter to Lab 1 without adding telemetry
  → execute real Ubuntu and devcontainer Lab 0 rows when network access exists
  → freeze the information-equivalent BASE-01 benchmark fixture
  → do not claim learner benefit or workflow superiority before evaluation
```

## Publication and validation state

- `docs/publication/orchestrator-state.md` and `docs/publication/evidence-backlog.md` remain authoritative.
- Passing CI establishes deterministic integration, not learner benefit or workflow superiority.
- No participant data, learner identity, model weights, telemetry, credentials, paid API generation, native instrumentation or manuscript prose were introduced.

## Known blockers and caveats

- **Lab 0 execution:** this runtime still cannot resolve `github.com`; no real environment row was fabricated.
- **Retrospective accuracy:** historical tool-call and human-minute values may be incomplete and must never be guessed.
- **Independent review:** the three-run batch requires a human coding check before publication analysis.
- **Workflow comparison:** DATA-01 enables analysis but does not replace BASE-01.
- **Educational effectiveness:** no learner-benefit claim is permitted before an approved evaluation and fair baseline.
- **Progress integration:** this increment provides the adapter, but Lab 1 does not yet save learner answers.
- **Live site:** verify Pages only after the stacked chain merges to `main` and deploys.

## Definition of done for this phase

- Complete learning contracts, legal fixture policy and three-tier platform boundaries.
- Deterministic fixture, trace, figure, browser lab and model-free Lab 0 validation contracts.
- Accessibility and privacy fallbacks for every introduced artifact.
- Real Lab 0 environment evidence, progress import/export integrated into one lab, first retrospective dataset review and passing integrated CI.
