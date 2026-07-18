# LAB0-03 Ubuntu success attestation

## Run identity

- Starting commit: `712016f1522fd6f4f1184f9c37b76e3956b70c6a`
- Assigned milestone: `LAB0-03` — measured Ubuntu 24.04 local-native Lab 0 row
- Learner outcome under test: a learner can complete locked Python tooling setup, a bounded pinned llama.cpp native build, and executable launch without a model

## Highest-priority selection

`STACK-01` remains blocked by the required human decision on the canonical progress implementation and merge order. The next dependency-safe task was to inspect the completed rerun produced by the bounded `uv.lock` repair and retain a precise evidence attestation.

## Evidence inspected

- GitHub Actions workflow run `29622240261` — `Lab 0 Ubuntu reproducibility` — success
- GitHub Actions workflow run `29622240365` — `Documentation CI` — success
- Artifact `8422651113`
- Artifact name: `lab0-ubuntu-24.04-d895eddc1c5e69452d90571c4ccb5d80f410da07`
- Artifact digest: `sha256:2db76be20de63afb5ab080fbdca8354de60859d34d4f21970c5331f9f2871295`
- Artifact expiry: 2026-08-17

## Retained report findings

### Verified

- Environment: Ubuntu 24.04, x86_64, local-native tier.
- Toolchain: uv 0.8.0, Python 3.12.3, CMake 3.31.6, Ninja 1.13.2, GCC 13.3.0.
- `uv sync --locked` passed.
- `uv.lock` SHA-256: `b332308fd26688b552acd6546a91ea95a3acd9e9d6457a1d3be97c59621f9ba3`.
- llama.cpp revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- Configure command: `cmake -S llama.cpp -B build/lab0 -G Ninja -DGGML_NATIVE=OFF`.
- Compile command: `cmake --build build/lab0 --target llama-cli -j 2`.
- Launch command: `build/lab0/bin/llama-cli --help`.
- Setup, build and launch all succeeded.
- Time to ready: 326,905 ms.
- No model was used and inference was not attempted.
- No diagnostics, model redistribution, secrets, personal paths, telemetry or learner data were recorded.

### Interpretation

The successful rerun supports one bounded reproducibility claim: the model-free local-native Lab 0 setup/build/launch path completes in one clean Ubuntu 24.04 GitHub-hosted environment. It also shows that failed-artifact retention plus stable diagnostic classification enabled a narrow repair rather than weakening the locked-sync requirement.

### Historical

The preceding retained run failed with `UV_LOCK_DRIFT` before clone/configure/build/launch. The repair added the dependency-free virtual project package to the lock while preserving the exact required `uv sync --locked` command.

### Open question

Equivalent devcontainer execution, offline/degraded behavior, cached rebuild timing, macOS/WSL2 rows, model loading, time to first token, learner benefit and independent technical correctness remain unverified.

## Files changed

- `docs/reference/project-state.md`
- `docs/publication/evidence-backlog.md`
- `docs/publication/handoffs/2026-07-18-0400-lab0-ubuntu-success.md`
- this run log

No external source was added or reclassified, so `docs/reference/research-ledger.md` remains unchanged.

## Validation and claim boundary

The exact retained JSON artifact and the two commit-scoped workflow results are authoritative. This attestation does not change the Lab 0 runner, schema, fixture, commands or educational content. It does not claim inference, time to first token, cross-platform reproducibility, offline support or educational effectiveness.

## Human-review needs

- Decide the canonical progress implementation and merge order for `STACK-01`.
- Nominate an independent llama.cpp/GGML reviewer before broad technical-correctness claims.

## Evidence produced

A bounded repository-native attestation that closes only the Ubuntu local-native matrix row and makes the next dependency explicit.

## Ending commit

To be filled by the final branch head and pull request.

## Next dependency

Return to `STACK-01` when the human decision exists. Otherwise run the equivalent retained devcontainer/Codespaces-compatible model-free path as `LAB0-04`.