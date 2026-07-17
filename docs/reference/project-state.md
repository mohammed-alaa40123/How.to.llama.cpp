# Project state

_Last updated: 2026-07-17 04:02 Africa/Cairo_

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
- Executable-trace schema, authored GGUF-loading sample, semantic validator, and focused malformed-input tests.
- Local-only learner-progress schema, semantic validator, example export, privacy constraints, and focused malformed-input tests.
- Authoritative EAAI orchestration state, evidence backlog, roadmap, and readiness scorecard.

## Latest concrete findings

### Verified

- Documentation CI run `29544077919` passed project-context, interactive-link, source-index, unit-test discovery, shell-syntax, Python-compilation, and required-asset checks.
- The same run failed only at `mkdocs build --strict` because two links in `docs/publication/agent-handoffs.md` targeted run records under repository-root `logs/research/`, outside MkDocs' `docs/` tree.
- The exact affected paths were `logs/research/2026-07-17/0100-synthetic-gguf-fixture.md` and `logs/research/2026-07-17/0158-lab0-checker-interface.md`.
- The repair preserves both run records and renders their paths as code rather than generated-site links.

### Interpretation

- Repository run logs should remain outside the public documentation tree unless intentionally promoted into a reviewed documentation page.
- Strict MkDocs is correctly acting as an integration gate by rejecting links that cannot resolve within the built site.

### Historical

- Earlier work established source-pinned documentation, executable lifetime regressions, accessibility guards, browser-level CI, legal fixture policy, synthetic GGUF evidence, Lab 0 reporting, trace validation, progress validation, and orchestration state.

### Open questions

- Whether the repaired branch obtains a passing commit-scoped Documentation CI result.
- Which bounded llama.cpp target and command matrix the first Lab 0 runner should execute.
- Which operating systems and container targets belong in the first reproducibility matrix.
- Browser/Python parser agreement and pinned native GGUF-reader acceptance remain unimplemented.

## Immediate next task

```text
verify strict MkDocs repair in commit-scoped CI
  → if passing, close the P0 integration blocker
  → implement media manifest/provenance schema and validator
  → then proceed to the minimal keyboard-operable trace viewer after trace acceptance
```

## In progress

- Draft PR stack #3–#6 for the EAAI executable-learning foundation and orchestration state.
- Strict MkDocs repair branch based on PR #6.
- Current-tree regeneration and sanitizer validation of the CPU_REPACK lifetime candidate.
- Manual/upstream submission of the reviewed 46-release OpenCL ownership correction; GitHub App write access to upstream is blocked.
- Source-index regeneration with pinned line-aware symbol inventory.
- Runtime overlays for mmap/page faults, scheduler copies, events, KV/recurrent growth, and backend queues.
- Website browser-level accessibility and deployed verification.

## Publication and validation state

- `docs/publication/orchestrator-state.md` and `docs/publication/evidence-backlog.md` are now authoritative on the stacked branch.
- The current P0 assignment is strict MkDocs repair; viewer and media feature expansion remain blocked until commit-scoped CI passes.
- No external source, participant data, model, telemetry, credential, paid API call, or manuscript prose was introduced in this increment.

## Known blockers and caveats

- **CI closure:** the link repair is committed, but a passing workflow result for the final branch head is still required.
- **Lab 0 runner:** the interface is defined, but no platform-specific build command runner exists yet.
- **Browser agreement:** no browser parser yet proves agreement with the Python golden output.
- **Native acceptance:** the synthetic file is a format-teaching fixture and is not claimed to be a valid inference model.
- **Live-site verification:** Pages should be rechecked only after the stacked changes merge to `main` and deploy.
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