# Project state

_Last updated: 2026-07-17 12:03 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream OpenCL revision audited: `505b1ed15ca80e2a19f12ff4ac365e40fb374053`
- Current upstream CPU_REPACK suitability revision reviewed: `8ee54c8b32a1b0cf13c03fc5723142bc62c775f6`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Executable-learning Week 1 foundation transitioning into measured Week 2 vertical slices**

## Completed foundations

- Canonical GGUF, model placement, `llama_model`, `llama_context`, graph/MoE, scheduler, memory-lifetime, backend, and inference-atlas pages.
- Source indexing, strict documentation CI, Pages deployment workflow, health checks, and durable run context.
- Generic scheduler plus CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL teardown audits.
- First executable CPU_REPACK lifetime regression with exact path proof, numerical comparison, and repeated ASan/LSan evidence.
- Website UX review, task-oriented Architecture navigation, and generated-HTML accessibility validation.
- EAAI July 17-31 executable-learning plan and legal fixture decision.
- Deterministic synthetic GGUF package and bounded corruption variants.
- Lab 0 six-phase checker contract and semantic validator.
- Executable-trace, learner-progress, media-manifest and Lab 0 reproducibility schemas and validators.
- Authoritative EAAI orchestration state, evidence backlog, roadmap, and readiness scorecard.
- Strict MkDocs integration, deterministic GGUF figure, immutable trace source anchors, keyboard-operable trace viewer and browser-first GGUF Anatomy slice with passing commit-scoped CI.

## Latest concrete findings

### Verified

- `LAB1-01` final head `0c70d9d4dec118095b2049b7442cfee6818c0f07` passed Documentation CI run `29562479577`.
- `LAB0-02` head `9d05719e25a25a1da644ec17237f2f3c5259afe1` passed Documentation CI run `29565651085`.
- The Lab 0 contract requires full course/upstream revisions, a `uv.lock` checksum, exact `uv sync --locked`, CMake with Ninja, a named bounded target, monotonic readiness timing, explicit offline state, stable diagnostics, and security declarations.
- The semantic validator prevents model-free runs from recording inference or first-token timings and prevents a matrix row from being called `validated` unless setup, build, and model-free launch all pass.

### Interpretation

- `LAB0-02` is evidenced as a validation contract, not as cross-platform reproducibility.
- Splitting measured execution into local-native `LAB0-03` and devcontainer `LAB0-04` prevents illustrative values from being misreported as observed evidence.
- `DATA-01` is now the highest-priority coordination dependency because the agent-workflow contribution needs a stable retrospective extraction contract before baseline analysis.

### Historical

- Earlier work established source-pinned documentation, legal fixture policy, deterministic GGUF evidence, Lab 0 reporting, trace/progress/media contracts, deterministic figures, orchestration state, the authored trace viewer, and the browser GGUF slice.

### Open questions

- The pinned `llama-cli` target/options must be verified in a real Ubuntu run.
- Real Ubuntu local-native and devcontainer rows remain required.
- Exact supported tool-version ranges should be set from observed runs, not illustrative values.
- Independent technical review and an approved educational evaluation pathway remain required.

## Immediate next task

```text
DATA-01 retrospective extraction schema
  → define assignments, commits, failures, corrections, validators, human decisions, cost proxies and accepted/rejected outputs
  → then execute LAB0-03 Ubuntu local-native row
  → then execute LAB0-04 devcontainer row
  → never call model-free launch inference
```

## In progress

- Draft PR stack for the EAAI executable-learning foundation.
- `DATA-01` retrospective agent-workflow extraction contract.
- `LAB0-03` and `LAB0-04` measured reproducibility rows.
- `PROGRESS-02` progress export/import, migration, and corruption recovery.
- Current-tree CPU_REPACK regeneration and sanitizer validation.
- Website browser-level accessibility and deployed verification.

## Publication and validation state

- `docs/publication/orchestrator-state.md` and `docs/publication/evidence-backlog.md` remain authoritative.
- `CI-01`, `MEDIA-01`, `FIG-01`, `TRACE-02`, `VIEW-01`, `LAB1-01`, and the `LAB0-02` contract have passing commit-scoped CI evidence.
- No real Lab 0 environment row, participant data, model, telemetry, credential, paid API call, generated media output, native trace instrumentation, or manuscript prose was introduced.

## Known blockers and caveats

- **Lab 0 execution:** no real environment row has yet been executed under the new contract.
- **Lab 0 target:** the initial `llama-cli` command shape must be verified against the pinned upstream checkout before becoming a validated run.
- **Educational effectiveness:** no learner-benefit claim is permitted before an approved evaluation pathway and baseline comparison.
- **Progress integration:** Lab 1 does not save learner answers until `PROGRESS-02` establishes import/export and corruption recovery.
- **Native acceptance:** the synthetic file is a format-teaching fixture and is not claimed to be a valid inference model.
- **Live-site verification:** Pages should be rechecked only after stacked changes merge to `main` and deploy.
- **Evidence retention:** artifact `8368782428` expires on 2026-08-15.
- **Upstream permission:** direct issue/PR creation in `ggml-org/llama.cpp` is blocked for the connected GitHub App.

## Definition of done for the executable-learning foundation phase

- Complete learning contracts and dependency-ordered July 17-31 plan.
- Legal fixture policy with no ambiguous model redistribution.
- Deterministic synthetic GGUF generator, manifest, golden output, and validators.
- Machine-readable trace, media-manifest, progress, Lab 0 phase, and reproducibility schemas.
- Authored sample trace with explicit evidence kinds and a narrow viewer shell.
- Lab 0 checker interface, model-free environment/build report, diagnostics, timing contract, and measured local/container rows.
- One deterministic technical figure from structured input.
- Accessibility fallbacks, reproducibility evidence, and CI gates for every introduced artifact.