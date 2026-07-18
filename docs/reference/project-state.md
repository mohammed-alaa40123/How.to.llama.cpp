# Project state

_Last updated: 2026-07-18 03:00 Africa/Cairo_

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
- Ubuntu Lab 0 workflow run `29619847701` used Ubuntu `24.04.4` and retained artifact `8421805335` before semantic validation.
- The retained report checksum is `0e5d3b3db9b706aa6f4ccfaa5608fb76514a6401af5ed8149264485a58583ffa`.
- The existing semantic validator accepted the degraded report.
- The report recorded only `UV_LOCK_DRIFT`; setup failed before clone, configuration, compilation, or executable launch.
- Documentation CI run `29619847677` passed on the same pull-request head.
- A local lock-consistency reproduction showed that the metadata-only lock omitted the dependency-free virtual project package required by `uv sync --locked`.
- The branch now contains a minimal dependency-free `pyproject.toml` and corrected `uv.lock`; no external Python dependency was added.

### Interpretation

- Retaining failed evidence before rejection converted an opaque workflow failure into a phase-specific, reviewable diagnosis.
- Stable diagnostic codes may turn setup failures into educational checkpoints, but learner usefulness is not established by implementation alone.
- Correcting the lock is narrower and more defensible than weakening the required `uv sync --locked` command.

### Historical

- Earlier work established source-pinned documentation, legal fixture policy, deterministic GGUF evidence, Lab 0 reporting, trace/progress/media contracts, deterministic figures, orchestration state, the authored trace viewer, and the browser GGUF slice.
- The first Ubuntu run lost its report because validation preceded artifact upload; the retention-order repair resolved that evidence-loss defect.

### Open questions

- Whether the corrected lock permits the pinned llama.cpp clone, CMake/Ninja configuration, bounded `llama-cli` compilation, and model-free launch on Ubuntu 24.04.
- Real devcontainer, macOS, and WSL2 runs remain required.
- Exact supported tool-version ranges and the pinned llama.cpp target/options require independent native review.
- Independent technical review and an approved educational evaluation pathway remain required.

## Immediate next task

```text
inspect the next commit-scoped Ubuntu 24.04 workflow
  → confirm uv sync --locked passes
  → download and review the retained JSON artifact
  → classify only the next failing phase, if any
  → do not claim LAB0-03 reproducibility before setup, build and launch all validate
```

## In progress

- Draft PR stack for the EAAI executable-learning foundation.
- `LAB0-03` measured Ubuntu run and phase-specific repair.
- `DATA-01` retrospective agent-workflow extraction contract.
- `PROGRESS-02` progress export/import, migration, and corruption recovery.
- Current-tree CPU_REPACK regeneration and sanitizer validation.
- Website browser-level accessibility and deployed verification.

## Publication and validation state

- `docs/publication/orchestrator-state.md` and `docs/publication/evidence-backlog.md` remain authoritative.
- `CI-01`, `MEDIA-01`, `FIG-01`, `TRACE-02`, `VIEW-01`, and `LAB1-01` have passing commit-scoped CI evidence.
- `LAB0-02` has a validated contract; `LAB0-03` has a retained, semantically valid degraded Ubuntu report and a bounded lock repair awaiting rerun.
- No participant data, model, telemetry, credential, paid API call, generated media output, native instrumentation, or manuscript prose was introduced.

## Known blockers and caveats

- **Canonical integration:** `STACK-01` still requires a human choice of progress implementation and merge order.
- **Lab 0 evidence:** the corrected lock requires a new commit-scoped Ubuntu run; native build and launch remain unverified.
- **Lab 0 target:** the `llama-cli` command shape must be supported by a retained validated record and independent review.
- **Educational effectiveness:** no learner-benefit claim is permitted before an approved evaluation pathway and baseline comparison.
- **Progress integration:** canonical progress implementation remains unresolved across overlapping branches.
- **Native acceptance:** the synthetic file is a format-teaching fixture and is not claimed to be a valid inference model.
- **Live-site verification:** Pages should be rechecked only after stacked changes merge to `main` and deploy.
- **Evidence retention:** artifact `8368782428` expires on 2026-08-15; Lab 0 artifact `8421805335` uses the workflow's 30-day retention.
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
