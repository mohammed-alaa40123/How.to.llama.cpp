# LAB0-04 successful devcontainer evidence attestation

## Run scope

Exactly one bounded, nonduplicate increment: inspect the first commit-scoped `LAB0-04` workflow, retain its exact evidence identity, close the single devcontainer matrix row only, and update durable project/publication state.

## Starting state

- Starting commit: `ab1db83938176dc4fd766cf66fccf18e5b0e2116`
- Source branch: `agent/lab0-04-devcontainer-repro`
- Highest-priority assignment: `STACK-01`, blocked by human canonical-progress and merge-order approval.
- Dependency-safe assignment selected: inspect and attest `LAB0-04` after the implementation workflow completed.

## Learner contract

- Intended learner: advanced undergraduate, graduate or early-stage systems learner who can use a shell and read C/C++ but needs a reproducible native-toolchain entry point.
- Prerequisite: Git/devcontainer-compatible host or cloud service; no model is required.
- Learning objective: distinguish locked Python-tool setup, pinned native source configuration/build and executable launch from model loading and inference.
- Predicted misconception: a successful `llama-cli --help` launch means a model was loaded or a token was generated.
- Executable action: run the shared Lab 0 measurement path inside the repository devcontainer.
- Observable output: semantically validated JSON report with exact environment, revisions, toolchain, commands, timing, success chain and security fields.
- Formative assessment: identify which phases passed and explain why `inference_state=not_attempted` is required.
- Source revision: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- Validation method: shared semantic validator plus commit-scoped workflow and exact retained artifact.
- Accessibility fallback: report is plain structured text and does not require visual interaction.

## Verified results

- `Lab 0 devcontainer reproducibility` run `29626470197`: success.
- `Documentation CI` run `29626470196`: success.
- `Lab 0 Ubuntu reproducibility` regression run `29626470190`: success.
- Artifact ID: `8424069914`.
- Artifact name: `lab0-devcontainer-ubuntu-24.04-6b5c02d78b36c6283fa40c3c4ccdbdd5c051ea55`.
- Artifact digest: `sha256:2aaf62980561e141244b5552f4cd397cb7c9a4e1215b75c35a04fdc3ad7c3121`.
- Artifact expiry: 2026-08-17.
- Environment: `github-actions-devcontainer-ubuntu-24.04-x86_64`, tier `cloud_container`, architecture `x86_64`.
- Toolchain: Python 3.12.3, uv 0.8.0, CMake 3.28.3, Ninja 1.11.1, GCC 13.3.0.
- Lock checksum: `b332308fd26688b552acd6546a91ea95a3acd9e9d6457a1d3be97c59621f9ba3`.
- Setup, build and executable launch all passed.
- Model kind: none. Inference: not attempted. Diagnostics: none.
- Monotonic time to ready: 280,753 ms.
- Security record: no redistributed model, recorded secrets or personal paths.

## Claims

### Verified

One clean Ubuntu 24.04/x86_64 devcontainer execution completes the bounded locked setup, pinned CMake/Ninja build and model-free executable-launch path using the same runner and validator as the successful Ubuntu local-native row.

### Interpretation

The shared implementation reduces command and evidence-schema drift between tiers. It does not make the tiers identical.

### Historical

The container measurement followed a failed-then-repaired Ubuntu lock path and a successful Ubuntu row, preserving a reviewable development sequence for the longitudinal case study.

### Open questions

- Exact built container-image digest was not retained.
- Real Codespaces service opening, persistence, quotas and failures were not exercised.
- Offline and cached rebuild modes remain untested.
- Model loading, inference and time to first token remain untested.
- macOS and WSL2 remain unmeasured.
- No learner benefit or independent technical-correctness claim is supported.

## Validation and failures

No phase failed in the final run. The report was downloaded and inspected directly from retained artifact `8424069914`. The container time-to-ready and prior local-native time-to-ready are not a controlled performance comparison because cache state, runner allocation and timing boundaries were not normalized.

## Files and sources

Updated:

- `docs/publication/evidence-backlog.md`
- `docs/reference/project-state.md`
- `docs/publication/handoffs/2026-07-18-0601-lab0-devcontainer-success.md`
- this run log

No new external source was introduced; the research ledger remains unchanged.

## Ending state and next dependency

`LAB0-04` is evidenced for one devcontainer row. `STACK-01` remains blocked. Next, return to canonical integration after human approval; otherwise take `DATA-01` or `PROGRESS-02` according to the orchestrator. Do not claim Codespaces service reliability, image reproducibility, inference, cross-platform equivalence or educational effectiveness.
