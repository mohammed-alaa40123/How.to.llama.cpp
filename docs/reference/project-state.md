# Project state

_Last updated: 2026-07-17 01:58 Africa/Cairo_

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
- EAAI July 17-31 executable-learning plan and initial agent handoff ledger on draft PR #3.
- Legal-fixture decision separating model-free Lab 0 checks, learner-provided optional inference, and a project-owned synthetic GGUF for Lab 1.
- Deterministic synthetic GGUF v0 generator, manifest, golden parse, SHA-256, alignment/range checks, and three bounded corruption variants.
- Lab 0 machine-readable checker contract, JSON Schema, dependency-free semantic validator, model-free example report, and focused invariant tests.

## Latest concrete findings

### Verified

- The Lab 0 report has six distinct phases: environment, configure, compile, executable launch, model load, and inference.
- The validator enforces configure→compile→launch→model-load→inference dependencies.
- Model-free reports must leave model loading and inference not attempted or not applicable.
- Claim booleans must exactly match passed phase states; a passing `--help` launch cannot claim model loading or inference.
- Learner-provided model metadata accepts only a redacted basename and optional checksum, not a full path.

### Interpretation

- The checker contract makes setup evidence auditable and turns the build-equals-inference misconception into a machine-checkable formative assessment.
- The contract is deliberately narrower than a full Lab 0 runner: it freezes evidence semantics before platform-specific commands and diagnostics are implemented.

### Historical

- Earlier work established source-pinned documentation, executable lifetime regressions, accessibility guards, and browser-level CI work.
- The 23:00 run froze the two-week plan; the 00:00 run closed fixture policy; the 01:00 run implemented the synthetic GGUF; the 01:58 run defined the Lab 0 checker contract.

### Open questions

- Which bounded llama.cpp target and command matrix should the first runner execute.
- Which operating systems and container targets belong in the first reproducibility matrix.
- Which diagnostic codes are stable and educationally useful.
- Browser/Python parser agreement and pinned native GGUF-reader acceptance remain unimplemented.

## Immediate next task

```text
add machine-readable executable-learning schemas
  → trace schema and authored sample trace contract
  → media manifest/provenance schema
  → local progress schema
  → focused malformed-input validators
```

## In progress

- Draft PR #3 for the EAAI executable-learning foundation.
- Current-tree regeneration and sanitizer validation of the CPU_REPACK lifetime candidate.
- Manual/upstream submission of the reviewed 46-release OpenCL ownership correction; GitHub App write access to upstream is blocked.
- Source-index regeneration with pinned line-aware symbol inventory.
- Runtime overlays for mmap/page faults, scheduler copies, events, KV/recurrent growth, and backend queues.
- Website browser-level accessibility and deployed verification.

## Publication and validation state

- Draft PR #3 is based on `agent/eaai-two-week-execution-plan`.
- The branch now contains the two-week plan, handoff ledger, legal-fixture decision, deterministic GGUF fixture package, Lab 0 checker contract, focused tests, and durable run notes.
- No external source was newly introduced in this increment.
- Final-head workflow results must be checked after context updates complete.

## Known blockers and caveats

- **Orchestrator files:** `docs/publication/orchestrator-state.md` and `docs/publication/evidence-backlog.md` are not yet available on the active branch, so dependency-safe recommendations are being followed.
- **Execution validation:** this connector environment could not execute the new Python tests; Documentation CI is the remaining authority.
- **Lab 0 runner:** the interface is defined, but no platform-specific build command runner exists yet.
- **Browser agreement:** no browser parser yet proves agreement with the Python golden output.
- **Native acceptance:** the synthetic file is a format-teaching fixture and is not claimed to be a valid inference model.
- **Live-site verification:** direct Pages access remains unavailable in this environment.
- **Current-tree runtime evidence:** source/API compatibility at `8ee54c8` is verified, but the CPU_REPACK fixture has not yet been compiled and executed against that exact current revision.
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