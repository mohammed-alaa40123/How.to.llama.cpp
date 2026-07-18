# Handoff — LAB0-04 devcontainer reproducibility lane

## Assignment

`STACK-01` remains blocked by the required human canonical-progress and merge-order decision. The next dependency-safe task is `LAB0-04`: execute the same model-free Lab 0 setup/build/launch contract in a devcontainer/Codespaces-compatible environment.

## Learner outcome under test

A learner opening the repository through a Development Container can use the pinned Python and native toolchain to run `uv sync --locked`, build the bounded `llama-cli` target with CMake/Ninja, and launch `llama-cli --help` without downloading or redistributing a model.

## Increment

- Added a minimal Ubuntu 24.04 devcontainer with Python, Git, CMake, Ninja, GCC and uv 0.8.0.
- Added a dedicated `devcontainers/ci` lane that builds the repository devcontainer and runs the existing Lab 0 evidence runner inside it.
- Parameterized the existing runner rather than creating a second implementation.
- Preserved the exact JSON report before semantic validation and retained failed reports when available.

## Claim supported or falsified

The lane can support or falsify only whether the cloud-container tier reproduces the bounded model-free setup/build/executable-launch path. It cannot establish Codespaces service availability, model loading, inference, time to first token, offline use, learner benefit, macOS/WSL2 equivalence or independent technical correctness.

## Truth labels

- **Verified:** the repository already has one successful Ubuntu 24.04 local-native row and a schema that permits `cloud_container` plus `devcontainer-ubuntu-24.04`.
- **Interpretation:** reusing the same runner and validator reduces measurement drift between native and container rows.
- **Historical:** the Ubuntu lane exposed and then corrected `UV_LOCK_DRIFT`; failed-report retention is therefore preserved here from the first run.
- **Open question:** whether the devcontainer builds and completes the path in commit-scoped CI.

## Security and privacy

No model, prompt, learner data, telemetry, secret, paid API or server-side progress synchronization is introduced. The workflow uses network access only for container/tool installation and the pinned llama.cpp checkout; offline/cached behavior remains `not_tested`.

## Human action

Approve the canonical progress implementation and merge order for `STACK-01`. Nominate an independent llama.cpp/GGML reviewer before correctness closure.

## Next dependency

Inspect the retained `LAB0-04` report and commit-scoped CI. Record success only if the exact artifact passes semantic validation; otherwise make one evidence-backed phase-specific repair.
