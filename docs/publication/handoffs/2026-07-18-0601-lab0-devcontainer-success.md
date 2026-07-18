# LAB0-04 devcontainer success handoff

## Assignment and starting point

- **Starting commit:** `ab1db83938176dc4fd766cf66fccf18e5b0e2116`
- **Assigned milestone:** `LAB0-04` — retain and validate the cloud-container equivalent of the model-free Lab 0 setup/build/launch path.
- **Higher-priority blocker:** `STACK-01` remains blocked pending a human canonical-progress and merge-order decision.

## Learner outcome

A learner-facing cloud-container environment can complete the same bounded prerequisites as the Ubuntu local-native row: locked Python tooling, pinned source checkout, CMake/Ninja configuration, bounded compilation and executable launch. This does not include model loading or inference.

## Verified evidence

- Devcontainer workflow run `29626470197`: passed.
- Documentation CI run `29626470196`: passed.
- Unchanged Ubuntu regression workflow `29626470190`: passed.
- Retained artifact: `8424069914`.
- Artifact digest: `sha256:2aaf62980561e141244b5552f4cd397cb7c9a4e1215b75c35a04fdc3ad7c3121`.
- Artifact expiry: 2026-08-17.
- Report course revision: `6b5c02d78b36c6283fa40c3c4ccdbdd5c051ea55`.
- Pinned llama.cpp revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- `uv sync --locked`, configure, compile and `llama-cli --help` all passed.
- Model-free time to ready: 280,753 ms.
- `model_kind=none`; `inference_state=not_attempted`; no diagnostics.

## Claims and limitations

- **Verified:** one Ubuntu 24.04/x86_64 devcontainer row reproduces the bounded setup/build/launch path using the shared runner and semantic validator.
- **Interpretation:** sharing the runner reduces command drift between local-native and container evidence.
- **Historical:** this row was added only after the equivalent Ubuntu local-native row passed.
- **Open question:** exact image digest, real Codespaces service behavior, persistence, offline/degraded use, model loading, inference, macOS/WSL2 equivalence and learner benefit remain untested.

The 280,753 ms container value and 326,905 ms local-native value are not a controlled performance comparison.

## Files updated

- `docs/publication/evidence-backlog.md`
- `docs/reference/project-state.md`
- this handoff
- `logs/research/2026-07-18/0601-lab0-devcontainer-success-attestation.md`

No primary source or bibliographic classification changed, so `docs/reference/research-ledger.md` is unchanged.

## Human review needs

- Approve or amend the canonical progress implementation and integration order for `STACK-01`.
- Do not treat this container row as Codespaces service validation or inference evidence.
- Nominate an independent technical reviewer before correctness claims.

## Next dependency

Return to `STACK-01` when the human decision exists. Otherwise take the next orchestrator-ranked dependency-safe task, currently `DATA-01` or `PROGRESS-02`; do not add another Lab 0 environment lane without an explicit matrix requirement.
