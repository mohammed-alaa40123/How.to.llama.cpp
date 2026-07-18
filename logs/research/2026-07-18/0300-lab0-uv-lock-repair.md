# LAB0-03 Ubuntu uv lock repair

- **Starting commit:** `d96eaf2a0da13fae993931acef839541d6f6a506`
- **Assigned milestone:** inspect the retained Ubuntu 24.04 evidence and make at most one evidence-backed repair
- **Learner outcome:** the Lab 0 Python-tooling bootstrap should pass the required locked synchronization gate before native configuration and compilation begin

## Evidence inspected

### Verified

- GitHub Actions run `29619847701` used Ubuntu 24.04.4.
- The runner emitted and retained `lab0-ubuntu-24.04-run.json` with checksum `0e5d3b3db9b706aa6f4ccfaa5608fb76514a6401af5ed8149264485a58583ffa`.
- Artifact `8421805335` was uploaded before semantic validation.
- The existing semantic validator accepted the retained report.
- The report recorded `setup_success=false`, no build or launch attempt, and diagnostic `UV_LOCK_DRIFT`.
- The workflow failed only at the final enforcement step, as designed for a degraded run.

### Interpretation

The retained evidence localizes the failure to the repository's Python lock contract. The existing `uv.lock` contained only lock metadata and omitted the dependency-free virtual project package represented by `pyproject.toml`; therefore `uv sync --locked` required a lock update and correctly refused to proceed.

### Historical

The earlier retention-order repair succeeded: failed evidence is now independently downloadable and semantically valid instead of disappearing after a failed workflow.

### Open question

Whether the corrected lock permits the pinned llama.cpp clone, CMake/Ninja configuration, bounded `llama-cli` compilation and model-free launch to complete on Ubuntu 24.04 remains to be established by the next commit-scoped run.

## Bounded change

Added a minimal dependency-free `pyproject.toml` and a complete `uv.lock` containing the virtual project package. No external Python dependency was added.

## Local validator

A temporary directory containing the same project metadata and lock completed `uv sync --locked` with uv 0.10.0. This is a narrow lock-consistency check, not Ubuntu workflow or native-build evidence.

## Claims and limitations

- **Claim supported or falsified:** the next run can test whether locked Python bootstrap is reproducible on Ubuntu 24.04.
- This increment does not establish native build success, executable launch, inference, time-to-first-token, cross-platform reproducibility or learner benefit.
- No model, learner data, telemetry, credential, paid API call or generated media was introduced.

## Files

- `pyproject.toml`
- `uv.lock`
- `docs/reference/project-state.md`
- `docs/publication/handoffs/2026-07-18-0300-lab0-uv-lock-repair.md`
- this run record

## Validation required

- commit-scoped Lab 0 Ubuntu reproducibility workflow;
- commit-scoped Documentation CI;
- retained exact JSON artifact and checksum review.

## Next dependency

Inspect the new retained report. If locked sync passes, classify the next single failing phase without broadening scope. `STACK-01` remains human-blocked.
