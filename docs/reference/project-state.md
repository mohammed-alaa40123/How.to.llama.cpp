# Project state

_Last updated: 2026-07-17 00:00 Africa/Cairo_

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

## Latest concrete findings

### Verified

- The initial executable-learning plan now declares complete learning contracts for Lab 0, Lab 1, and Executable Lecture 0.
- `docs/labs/legal-fixture-decision.md` requires no redistributed model for mandatory Lab 0 validation.
- Optional inference must use a learner-provided local GGUF path and remain a distinct outcome from build or executable launch.
- Lab 1 will use deterministically generated project-owned GGUF bytes containing educational metadata, tensor descriptors, alignment, offsets, and non-model payloads.
- Ordinary CI must not download model weights or call paid generation APIs.

### Interpretation

- Build/toolchain validation, GGUF format education, and real model inference are different evidence paths and should not be collapsed into a single “smoke test.”
- A synthetic GGUF is safer and more precise for browser parsing than a mutable third-party tiny model.
- The first executable lecture should prefer a bounded GGUF-loading path unless source-link feasibility identifies a smaller graph-construction trace.

### Historical

- Earlier work established source-pinned documentation, executable lifetime regressions, accessibility guards, and browser-level CI work.
- The 2026-07-16 23:00 run froze the two-week executable-learning plan; the 2026-07-17 00:00 run closed its first fixture-policy dependency.

### Open questions

- Exact metadata fields, tensor types/shapes, alignment, and payload pattern for synthetic GGUF v0.
- Whether the binary fixture should be committed or generated during tests from a committed generator and manifest.
- Which bounded llama.cpp parser entry path yields the clearest first trace with stable source links.
- Which operating systems and container targets belong in the first reproducibility matrix.

## Immediate next task

```text
implement deterministic synthetic GGUF generator
  → define manifest and fixture-format version
  → produce golden parser output and SHA-256
  → add alignment/range and corruption tests
  → validate browser/Python agreement
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
- Added `docs/publication/two-week-execution-plan.md`, `docs/publication/agent-handoffs.md`, and `docs/labs/legal-fixture-decision.md` plus durable run notes.
- No external source, paid API, model weight, participant data, or server-side learner state was introduced by the fixture decision.
- Research ledger unchanged because no external source was added or reclassified.
- Final-head workflow results must be checked after context updates complete.

## Known blockers and caveats

- **Orchestrator files:** `docs/publication/orchestrator-state.md` and `docs/publication/evidence-backlog.md` are not yet available on the active branch, so dependency-safe recommendations are being followed.
- **Fixture implementation:** the decision is complete, but no binary/generator, manifest, golden parser output, or corruption variants exist yet.
- **Inference scope:** mandatory Lab 0 does not prove model loading or token generation; those require the separately labelled learner-provided-model extension.
- **Live-site verification:** direct Pages access remains unavailable in this environment, so production rendering cannot be independently tested here.
- **Current-tree runtime evidence:** source/API compatibility at `8ee54c8` is verified, but the CPU_REPACK fixture has not yet been compiled and executed against that exact current revision.
- **Evidence retention:** artifact `8368782428` expires on 2026-08-15.
- **Upstream permission:** direct issue/PR creation in `ggml-org/llama.cpp` is blocked for the connected GitHub App.
- Mapping, allocation, residency, representation validity, command completion, event ownership, reset, and release remain distinct states.

## Definition of done for the executable-learning foundation phase

- Complete learning contracts and dependency-ordered July 17-31 plan.
- Legal fixture policy with no ambiguous model redistribution.
- Deterministic synthetic GGUF generator, manifest, golden output, and validators.
- Machine-readable trace, media-manifest, and progress schemas.
- Authored sample trace with explicit evidence kinds and a narrow viewer shell.
- Lab 0 checker interface and model-free environment/build report.
- One deterministic technical figure from structured input.
- Accessibility fallbacks, reproducibility evidence, and CI gates for every introduced artifact.