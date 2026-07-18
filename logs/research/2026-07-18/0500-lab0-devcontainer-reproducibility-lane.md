# LAB0-04 devcontainer reproducibility lane

## Run identity

- Starting commit: `a34f460003fa5a5c945b9ffb0edaf72a29de562d`
- Assigned milestone: `LAB0-04` — retained devcontainer/Codespaces-compatible model-free Lab 0 row
- Learner outcome: complete locked Python setup, bounded pinned native build and executable launch inside the repository devcontainer without a model

## Assignment selection

`STACK-01` is still blocked by the human canonical-progress and merge-order decision. `LAB0-04` is the highest-priority dependency-safe item in the evidence backlog after the successful Ubuntu `LAB0-03` row.

## Files and sources inspected

- `README.md`
- `docs/reference/project-state.md`
- `docs/reference/research-log.md`
- `docs/reference/research-ledger.md`
- `docs/publication/orchestrator-state.md`
- `docs/publication/evidence-backlog.md`
- `docs/publication/two-week-execution-plan.md`
- `docs/publication/agent-handoffs.md`
- `logs/research/2026-07-18/0400-lab0-ubuntu-success-attestation.md`
- Existing Lab 0 runner, schema, semantic validator and Ubuntu workflow
- Official Development Containers specification/project and `devcontainers/ci` action documentation

## Bounded implementation

1. Added `.devcontainer/Dockerfile` based on Ubuntu 24.04 with Git, Python, CMake, Ninja, GCC and uv 0.8.0.
2. Added `.devcontainer/devcontainer.json` compatible with Development Container tooling and Codespaces.
3. Parameterized the existing Ubuntu runner through environment variables for environment ID, execution tier, OS identifier, course revision and output path.
4. Added `.github/workflows/lab0-devcontainer-reproducibility.yml` using `devcontainers/ci@v0.3`.
5. Preserved the exact report before semantic validation and kept a final success gate identical in intent to the Ubuntu lane.

## Learning contract

- Intended learner: a terminal-capable learner who has not built llama.cpp in a container.
- Prerequisite: Git/shell basics and basic C/C++ toolchain concepts.
- Learning objective: distinguish container provisioning, `uv` synchronization, CMake configuration, Ninja compilation and executable launch.
- Predicted misconception: opening Codespaces or completing a container build proves model loading or inference.
- Executable action: build/open the devcontainer and run the bounded model-free Lab 0 runner.
- Observable output: a versioned JSON report with toolchain, revisions, timing, phase outcomes and diagnostics.
- Formative assessment: identify the owner of each phase and interpret a retained failure code without calling it inference.
- Source revision: course commit supplied by CI and llama.cpp pinned to `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- Validation method: exact artifact retention, dependency-free semantic validation and commit-scoped workflow result.
- Accessibility fallback: copyable commands and machine-readable/text report; no animation or color-only status is required.

## Claims

### Verified

- The existing Lab 0 schema explicitly accepts `cloud_container` and `devcontainer-ubuntu-24.04`.
- The successful Ubuntu row established the command contract reused here.
- The new lane uses the repository devcontainer itself rather than an unrelated CI image.

### Interpretation

- A shared runner and validator make the local-native and cloud-container matrix rows more comparable than separate scripts.

### Historical

- Failed-report retention was introduced after the first Ubuntu run lost its diagnostic artifact; this lane retains that ordering from its first execution.

### Open question

- Whether the final branch head builds the container, completes `uv sync --locked`, checks out the pinned llama.cpp revision, builds `llama-cli`, launches `--help`, retains the report and passes semantic validation.

## Validators and failure behavior

- Python syntax and repository tests remain delegated to Documentation CI.
- The dedicated workflow retains the exact JSON report before semantic validation.
- Missing output emits `LAB0_REPORT_MISSING`.
- Existing stable setup/configure/compile/launch diagnostics remain unchanged.

## Security and limitations

- No model is downloaded or redistributed.
- Inference and time to first token are not attempted or recorded.
- No learner data, prompt, telemetry, credential, personal path or paid API is introduced.
- Network access is still required for initial image/tool and llama.cpp acquisition; offline/cached behavior is not tested.
- A GitHub-hosted container run is evidence for one CI environment, not a universal Codespaces reliability or performance claim.

## Human-review needs

- Canonical progress and merge-order approval for `STACK-01`.
- Independent technical review of the Lab 0 target and claims.
- Review of the eventual retained container artifact before marking `LAB0-04` evidenced.

## Evidence produced

A bounded devcontainer definition, shared parameterized runner, dedicated retained-evidence workflow, and explicit handoff.

## Ending commit

To be filled by the final branch head and pull request.

## Next dependency

Inspect commit-scoped Documentation CI and the dedicated devcontainer workflow. If the report validates and all phases pass, attest exactly one container matrix row. If it fails, retain the report and make only one phase-specific repair.
