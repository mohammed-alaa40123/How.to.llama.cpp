# LAB0-02 reproducibility validation increment

## Run identity

- **Starting commit:** `0c70d9d4dec118095b2049b7442cfee6818c0f07`
- **Assigned milestone:** `LAB0-02` — supported-environment matrix, exact tool checks, stable diagnostics, and readiness/first-token timing semantics
- **Learner outcome:** distinguish environment preparation, native configuration/build, executable launch, optional model loading, and inference while diagnosing which tool owns a failure

## Dependency decision

`LAB1-01` final-head Documentation CI run `29562479577` succeeded. The highest-priority unblocked orchestrator item was therefore `LAB0-02`.

## Files added or changed

- `schemas/lab0-reproducibility-run.schema.json`
- `scripts/validate_lab0_reproducibility.py`
- `labs/lab0/examples/reproducibility-local-linux-v0.json`
- `tests/test_validate_lab0_reproducibility.py`
- `docs/labs/lab0-reproducibility-protocol.md`
- `docs/publication/evidence-backlog.md`
- `docs/reference/project-state.md`
- `mkdocs.yml`

## Evidence and validators

The package records full source revisions, the `uv.lock` checksum, exact `uv sync --locked`, CMake/Ninja command shape, bounded target compilation, monotonic time-to-ready, optional learner-model time-to-first-token, offline/degraded state, stable failure codes, and explicit security/licensing declarations.

The semantic validator rejects:

- unlocked Python synchronization;
- mutable/short revisions;
- readiness timing that is not derived from monotonic endpoints;
- `validated` environments without successful setup/build/launch;
- model-free inference or first-token claims;
- passed inference without a learner-provided model and timing evidence;
- contradictory offline/network claims;
- model redistribution, secrets, or personal paths.

Eight focused tests cover valid and malformed records.

## EAAI claim supported or falsified

**Candidate claim:** setup/build evidence can be made comparable across local-native and cloud-container environments without conflating model-free launch with inference.

**Falsification condition:** the contract permits contradictory states, mutable revisions, unlocked environments, unbounded build commands, false first-token claims, or privacy/licensing violations; or real environment runs cannot satisfy the same record format.

## Truth labels

- **Verified:** schema, semantic validator, example record, diagnostics, timing definitions, and focused tests are committed.
- **Interpretation:** stable diagnostics may improve conceptual ownership and troubleshooting learning.
- **Historical:** the earlier Lab 0 checker already separated six execution phases but left the environment matrix and timing semantics open.
- **Open question:** real Ubuntu/macOS/WSL2/devcontainer runs, supported version ranges, learner usefulness, and independent review remain unevidenced.

## Limitations and human review

- The checked-in versions and timing values are explicitly illustrative, not measured environment evidence.
- The `llama-cli` target/options require verification in a real pinned checkout.
- Cross-platform reproducibility cannot be claimed until matrix rows are executed.
- No participant recruitment or personal data collection occurred.
- An independent llama.cpp/GGML reviewer and approved evaluation pathway remain required.

## Ending state

Final-head Documentation CI is required before accepting the validator as integrated. Even after CI passes, `LAB0-02` remains in progress until at least Ubuntu local-native and devcontainer rows are executed and retained.

## Next dependency

Run the model-free protocol on Ubuntu 24.04 local-native and the pinned devcontainer, recording actual tool versions, `uv.lock` checksum, commands, diagnostics, and monotonic timings. Do not add optional model inference until the mandatory path is reproducible.
