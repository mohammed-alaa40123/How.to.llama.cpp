# Project state

_Last updated: 2026-07-17 10:03 Africa/Cairo_

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
- Minimal keyboard-operable trace viewer verified by successful Documentation CI run `29559239071`.

## Latest concrete findings

### Verified

- The Lab 1 payload is derived from the same project-owned Python fixture builder and golden parser used by the deterministic GGUF package.
- The bounded browser parser reads GGUF v3 header fields, supported metadata, F32 tensor descriptors, alignment, and tensor ranges using `DataView`.
- The page declares the complete learning contract, three Predict–Discover–Explain checkpoints, explicit browser/native evidence boundaries, and a static text fallback.
- Focused tests compare the checked-in payload semantically with the Python builder and inspect parser bounds and learning-contract declarations.

### Interpretation

- A 428-byte browser-parsed fixture is the narrowest useful Lab 1 slice because it isolates file-layout reasoning before native build, `mmap`, page-fault, graph, or inference complexity.
- The checkpoints may support later misconception assessment, but implementation and CI do not establish learner benefit.

### Historical

- Earlier work established source-pinned documentation, executable lifetime regressions, accessibility guards, legal fixture policy, synthetic GGUF evidence, Lab 0 reporting, trace/progress/media contracts, deterministic figures, orchestration state, and the authored trace viewer.

### Open questions

- Final-head CI must establish browser/Python payload agreement and MkDocs integration.
- Independent technical review of the fixture, parser explanation, trace anchors, and deterministic figure remains required.
- Pinned native GGUF-reader acceptance remains a separate, unclaimed validation path.
- A fair baseline and learner or expert evaluation pathway remain unapproved.

## Immediate next task

```text
obtain commit-scoped CI for LAB1-01
  → if passing, mark the bounded browser slice evidenced
  → preserve browser-derived versus native-runtime boundaries
  → connect local progress only after PROGRESS-02 is evidenced
```

## In progress

- Draft PR stack for the EAAI executable-learning foundation.
- `LAB1-01` bounded browser GGUF parser and Predict–Discover–Explain slice awaiting final-head CI.
- Lab 0 reproducibility matrix and diagnostic taxonomy under `LAB0-02`.
- Retrospective agent-workflow extraction contract under `DATA-01`.
- Progress export/import, migration, and corruption recovery under `PROGRESS-02`.
- Current-tree regeneration and sanitizer validation of the CPU_REPACK lifetime candidate.
- Website browser-level accessibility and deployed verification.

## Publication and validation state

- `docs/publication/orchestrator-state.md` and `docs/publication/evidence-backlog.md` remain authoritative.
- `CI-01`, `MEDIA-01`, `FIG-01`, `TRACE-02`, and `VIEW-01` have passing commit-scoped CI evidence.
- `LAB1-01` is implemented as a bounded first browser slice and remains in progress until final-head CI passes.
- No participant data, model, telemetry, credential, paid API call, generated media output, native instrumentation, or manuscript prose was introduced.

## Known blockers and caveats

- **Lab 1 correctness:** final-head Documentation CI and independent GGUF/llama.cpp review remain required.
- **Educational effectiveness:** no learner-benefit claim is permitted before an approved evaluation pathway and baseline comparison.
- **Lab 0 runner:** the interface is defined, but no platform-specific build command runner exists yet.
- **Progress integration:** the lab does not save learner answers until `PROGRESS-02` establishes import/export and corruption recovery.
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
