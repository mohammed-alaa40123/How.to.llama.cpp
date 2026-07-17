# Project state

_Last updated: 2026-07-17 11:04 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream OpenCL revision audited: `505b1ed15ca80e2a19f12ff4ac365e40fb374053`
- Current upstream CPU_REPACK suitability revision reviewed: `8ee54c8b32a1b0cf13c03fc5723142bc62c775f6`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Executable-learning Week 1 foundation — contracts, legal fixtures, schemas, and smallest vertical slice**

## Completed foundations

- Canonical GGUF, model placement, `llama_model`, `llama_context`, graph/MoE, scheduler, memory-lifetime, backend, and inference-atlas pages.
- Source indexing, strict documentation CI, Pages deployment workflow, health checks, and durable run context.
- Generic scheduler plus CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL teardown audits.
- First executable CPU_REPACK lifetime regression with exact path proof, numerical comparison, and repeated ASan/LSan evidence.
- Website UX review, task-oriented Architecture navigation, and generated-HTML accessibility validation.
- EAAI July 17-31 executable-learning plan and legal fixture decision.
- Deterministic synthetic GGUF package and bounded corruption variants.
- Lab 0 six-phase checker contract and semantic validator.
- Executable-trace, learner-progress, and media-manifest schemas and validators.
- Authoritative EAAI orchestration state, evidence backlog, roadmap, and readiness scorecard.
- Strict MkDocs integration, deterministic GGUF figure, immutable trace source anchors, and keyboard-operable trace viewer with passing commit-scoped CI.
- Browser-first GGUF Anatomy vertical slice with deterministic Python/browser agreement and passing Documentation CI run `29562479577`.

## Latest concrete findings

### Verified

- `LAB1-01` final head `0c70d9d4dec118095b2049b7442cfee6818c0f07` passed Documentation CI run `29562479577`.
- The new Lab 0 reproducibility contract requires full course/upstream revisions, a `uv.lock` checksum, exact `uv sync --locked`, CMake with Ninja, a named bounded target, monotonic readiness timing, explicit offline state, stable diagnostics, and security declarations.
- The semantic validator prevents model-free runs from recording inference or first-token timings and prevents a matrix row from being called `validated` unless setup, build, and model-free launch all pass.
- Focused tests cover locked sync, impossible validated states, timing derivation, offline/network contradictions, missing tools, model-free first-token inflation, and a valid learner-provided-model timing path.

### Interpretation

- A separate reproducibility record is useful because the earlier six-phase Lab 0 report identifies phase outcomes but does not define cross-environment comparability, stable failure codes, offline behavior, or timing semantics.
- Stable diagnostic codes may turn setup failures into educational checkpoints, but learner usefulness is not established by implementation alone.

### Historical

- Earlier work established source-pinned documentation, legal fixture policy, deterministic GGUF evidence, Lab 0 reporting, trace/progress/media contracts, deterministic figures, orchestration state, the authored trace viewer, and the browser GGUF slice.

### Open questions

- Final-head CI must validate the new schema, semantic validator, tests, and MkDocs integration.
- Real Ubuntu, macOS, WSL2, and devcontainer runs remain required; the checked-in report is a contract example, not cross-platform evidence.
- Exact supported tool-version ranges and the pinned llama.cpp target/options require native execution review.
- Independent technical review and an approved educational evaluation pathway remain required.

## Immediate next task

```text
obtain commit-scoped CI for LAB0-02 contract
  → if passing, retain status as partial/in-progress until real matrix runs exist
  → execute Ubuntu local-native and devcontainer rows first
  → do not claim inference or cross-platform reproducibility from the example report
```

## In progress

- Draft PR stack for the EAAI executable-learning foundation.
- `LAB0-02` reproducibility schema, validator, diagnostics, and timing protocol awaiting final-head CI and real environment runs.
- `DATA-01` retrospective agent-workflow extraction contract.
- `PROGRESS-02` progress export/import, migration, and corruption recovery.
- Current-tree CPU_REPACK regeneration and sanitizer validation.
- Website browser-level accessibility and deployed verification.

## Publication and validation state

- `docs/publication/orchestrator-state.md` and `docs/publication/evidence-backlog.md` remain authoritative.
- `CI-01`, `MEDIA-01`, `FIG-01`, `TRACE-02`, `VIEW-01`, and `LAB1-01` have passing commit-scoped CI evidence.
- `LAB0-02` now has a concrete validation contract but remains in progress until CI and real reproducibility rows are recorded.
- No participant data, model, telemetry, credential, paid API call, generated media output, native instrumentation, or manuscript prose was introduced.

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
- Lab 0 checker interface, model-free environment/build report, diagnostics, and timing contract.
- One deterministic technical figure from structured input.
- Accessibility fallbacks, reproducibility evidence, and CI gates for every introduced artifact.
