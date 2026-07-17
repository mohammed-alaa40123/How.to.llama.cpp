# Project state

_Last updated: 2026-07-17 05:18 Africa/Cairo_

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
- Strict MkDocs handoff-link repair verified by successful Documentation CI run `29546570700`.
- Media asset manifest schema, dependency-free semantic validator, deterministic authoritative example, accessibility/licensing/review gates, stale-source detection, and focused malformed-input tests.

## Latest concrete findings

### Verified

- Documentation CI run `29546570700` completed successfully for commit `5bbc595b9e2d076ddbc8393514e2a9f26fab9fa8`, closing the P0 strict-MkDocs integration blocker.
- The media contract rejects generative assets as authoritative technical evidence.
- Generative API manifests must be supplemental, cached, manually triggered, excluded from ordinary CI, prompt/storyboard hashed, and human-review gated.
- Accepted or published assets require human approval and redistribution permission.
- Audio/video assets require transcript fallbacks; video additionally requires captions and a static fallback.
- The validator rejects unsafe repository paths, stale source revisions, oversized manifests, and credential-like fields.

### Interpretation

- Deterministic figures derived from hashed structured inputs are the appropriate authoritative media layer because their transformation can be replayed and checksum-verified.
- Human approval can permit publication of generated media but cannot convert it into technical evidence.

### Historical

- Earlier work established source-pinned documentation, executable lifetime regressions, accessibility guards, browser-level CI, legal fixture policy, synthetic GGUF evidence, Lab 0 reporting, trace validation, progress validation, and orchestration state.

### Open questions

- Provider-specific API, licensing, privacy, cost, and reproducibility constraints remain unverified pending the Literature Scout assignment.
- The example media manifest points to the future deterministic GGUF layout SVG; actual generation and checksum verification remain under `FIG-01`.
- Which bounded llama.cpp target and command matrix the first Lab 0 runner should execute.
- Which operating systems and container targets belong in the first reproducibility matrix.
- Browser/Python parser agreement and pinned native GGUF-reader acceptance remain unimplemented.

## Immediate next task

```text
obtain commit-scoped CI for the media manifest contract
  → if passing, mark MEDIA-01 evidenced
  → implement FIG-01 deterministic GGUF layout generation
  → then proceed to the minimal keyboard-operable trace viewer after TRACE-02 acceptance
```

## In progress

- Draft PR stack #3–#7 for the EAAI executable-learning foundation and orchestration state.
- Media manifest/provenance validation branch based on PR #7.
- Current-tree regeneration and sanitizer validation of the CPU_REPACK lifetime candidate.
- Manual/upstream submission of the reviewed 46-release OpenCL ownership correction; GitHub App write access to upstream is blocked.
- Source-index regeneration with pinned line-aware symbol inventory.
- Runtime overlays for mmap/page faults, scheduler copies, events, KV/recurrent growth, and backend queues.
- Website browser-level accessibility and deployed verification.

## Publication and validation state

- `docs/publication/orchestrator-state.md` and `docs/publication/evidence-backlog.md` are authoritative on the stacked branch.
- `CI-01` is evidenced by successful run `29546570700`.
- `MEDIA-01` is implemented and awaiting commit-scoped CI on its final branch head.
- No participant data, model, telemetry, credential, paid API call, generated media output, or manuscript prose was introduced in this increment.

## Known blockers and caveats

- **Media CI closure:** the contract is committed, but a passing workflow result for the final branch head is still required.
- **Provider selection:** no generated-media provider may be selected until the Literature Scout verifies current official constraints.
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
