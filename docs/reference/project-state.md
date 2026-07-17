# Project state

_Last updated: 2026-07-17 09:02 Africa/Cairo_

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
- CPU repack, AMX, KleidiAI, and SpacemiT extra-buffer ownership comparison and destruction-harness specification.
- Complete pinned/current OpenCL event-ownership audit, generated 46-release correction, synchronous tensor-set contract analysis, and upstream proposal staging.
- First executable CPU_REPACK lifetime regression with exact path proof, numerical comparison, and repeated ASan/LSan evidence.
- Upstream-suitability decision and staged two-file CPU_REPACK regression proposal.
- Website UX review with task-oriented Architecture navigation grouping.
- Architecture landing page with six goal-based entry points, concise page summaries, and ordered reading paths.
- Dependency-free generated-HTML accessibility structure validator with focused tests and Documentation CI integration.
- EAAI July 17-31 executable-learning plan and initial agent handoff ledger.
- Legal-fixture decision separating model-free Lab 0 checks, learner-provided optional inference, and a project-owned synthetic GGUF for Lab 1.
- Deterministic synthetic GGUF v0 generator, manifest, golden parse, SHA-256, alignment/range checks, and three bounded corruption variants.
- Lab 0 machine-readable checker contract, JSON Schema, dependency-free semantic validator, model-free example report, and focused invariant tests.
- Executable-trace schema, authored GGUF-loading sample, semantic validator, and focused malformed-input tests.
- Local-only learner-progress schema, semantic validator, example export, privacy constraints, and focused malformed-input tests.
- Authoritative EAAI orchestration state, evidence backlog, roadmap, and readiness scorecard.
- Strict MkDocs handoff-link repair verified by successful Documentation CI run `29546570700`.
- Media asset manifest schema and validator verified by successful Documentation CI run `29549208249`.
- Deterministic GGUF-layout figure verified by successful Documentation CI run `29553868078`.
- Immutable trace source anchors and deterministic replay verified by successful Documentation CI run `29556540213`.

## Latest concrete findings

### Verified

- TRACE-02 is closed by successful Documentation CI run `29556540213` for commit `e2361200d80028c86205359979487a94b958f306`.
- The minimal viewer payload is deterministically generated from the validated authored trace rather than maintained as an independent narrative copy.
- The viewer shell exposes Previous/Next controls, Arrow/Home/End navigation, pinned source links, evidence labels, live text status, and an ordered transcript fallback.
- The viewer explicitly labels missing runtime collections as unrecorded authored-step data rather than evidence that native state is absent.

### Interpretation

- A static browser shell is the smallest safe executable-lecture prototype because it tests source/state/explanation coordination without adding native instrumentation or a frontend framework.
- The viewer can support a later code-tracing evaluation, but its existence alone does not establish learner benefit.

### Historical

- Earlier work established source-pinned documentation, executable lifetime regressions, accessibility guards, legal fixture policy, synthetic GGUF evidence, Lab 0 reporting, trace/progress/media contracts, deterministic figures, and orchestration state.

### Open questions

- Independent technical review of the three pedagogical GGUF anchors remains required.
- A fair static-source/text baseline and learner or expert evaluation pathway remain unapproved.
- Native-captured trace evidence remains a separate Week 2 artifact.
- Browser/Python parser agreement and pinned native GGUF-reader acceptance remain unimplemented.

## Immediate next task

```text
obtain commit-scoped CI for VIEW-01
  → if passing, mark the static authored trace viewer evidenced
  → preserve the authored/source-derived boundary
  → proceed to LAB1-01 only after progress integration and figure dependencies are present on one branch
```

## In progress

- Draft PR stack for the EAAI executable-learning foundation.
- `VIEW-01` static keyboard-operable trace viewer shell awaiting final-head CI.
- Lab 0 reproducibility matrix and diagnostic taxonomy under `LAB0-02`.
- Retrospective agent-workflow extraction contract under `DATA-01`.
- Current-tree regeneration and sanitizer validation of the CPU_REPACK lifetime candidate.
- Website browser-level accessibility and deployed verification.

## Publication and validation state

- `docs/publication/orchestrator-state.md` and `docs/publication/evidence-backlog.md` remain authoritative.
- `CI-01`, `MEDIA-01`, `FIG-01`, and `TRACE-02` have passing commit-scoped CI evidence.
- `VIEW-01` is implemented on this branch and remains in progress until final-head CI passes.
- No participant data, model, telemetry, credential, paid API call, generated media output, native instrumentation, or manuscript prose was introduced in this increment.

## Known blockers and caveats

- **Viewer correctness:** final-head Documentation CI is required; independent llama.cpp/GGML review remains separate.
- **Educational effectiveness:** no learner-benefit claim is permitted before an approved evaluation pathway and baseline comparison.
- **Lab 0 runner:** the interface is defined, but no platform-specific build command runner exists yet.
- **Browser agreement:** no browser parser yet proves agreement with the Python golden output.
- **Native acceptance:** the synthetic file is a format-teaching fixture and is not claimed to be a valid inference model.
- **Live-site verification:** Pages should be rechecked only after the stacked changes merge to `main` and deploy.
- **Evidence retention:** artifact `8368782428` expires on 2026-08-15.
- **Upstream permission:** direct issue/PR creation in `ggml-org/llama.cpp` is blocked for the connected GitHub App.

## Definition of done for the executable-learning foundation phase

- Complete learning contracts and dependency-ordered July 17-31 plan.
- Legal fixture policy with no ambiguous model redistribution.
- Deterministic synthetic GGUF generator, manifest, golden output, and validators.
- Machine-readable trace, media-manifest, and progress schemas.
- Authored sample trace with explicit evidence kinds and a narrow viewer shell.
- Lab 0 checker interface and model-free environment/build report.
- One deterministic technical figure from structured input.
- Accessibility fallbacks, reproducibility evidence, and CI gates for every introduced artifact.
