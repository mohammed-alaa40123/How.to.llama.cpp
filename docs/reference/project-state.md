# Project state

_Last updated: 2026-07-17 01:00 Africa/Cairo_

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

## Latest concrete findings

### Verified

- `scripts/generate_synthetic_gguf.py` deterministically emits a 428-byte little-endian GGUF v3 fixture.
- The fixture contains five metadata records, including string, `uint32`, and string-array values, plus two F32 tensor descriptors with different shapes.
- Tensor data begins at absolute offset 384; the second tensor begins at relative offset 32 under 32-byte alignment.
- Whole-file SHA-256 is `688d0ef28c83d6972e291cc0342e695540eae8496b3ec8e92bdbb91e3982a564`.
- Golden parsing, checksum, alignment/range assertions, and rejection of bad magic, misaligned offset, and truncated payload pass in focused tests.
- The generator and tests use only project-authored numeric payloads and perform no model download, paid API call, telemetry, or learner-data collection.

### Interpretation

- Generator plus manifest and golden output are stronger review artifacts than an opaque committed binary; binaries and corruption variants can be regenerated deterministically for labs and tests.
- The fixture validates format understanding, not llama.cpp model loading or inference.
- The bounded fixture is now suitable as the shared source for the first browser parser and authored GGUF-loading trace.

### Historical

- Earlier work established source-pinned documentation, executable lifetime regressions, accessibility guards, and browser-level CI work.
- The 2026-07-16 23:00 run froze the two-week executable-learning plan; the 2026-07-17 00:00 run closed its fixture policy; the 01:00 run implemented the first fixture package.

### Open questions

- Browser/Python parser agreement is not yet implemented.
- Native acceptance through pinned llama.cpp `gguf_init_from_file` is not yet tested in ordinary CI.
- Which bounded llama.cpp parser entry path yields the clearest first trace with stable source links.
- Which operating systems and container targets belong in the first reproducibility matrix.

## Immediate next task

```text
add machine-readable executable-learning schemas
  → trace schema and authored sample trace contract
  → media manifest/provenance schema
  → local progress schema
  → focused malformed-input validators
```

If the orchestrator ranks it higher, define the Lab 0 checker interface before environment automation.

## In progress

- Draft PR #3 for the EAAI executable-learning foundation.
- Current-tree regeneration and sanitizer validation of the CPU_REPACK lifetime candidate.
- Manual/upstream submission of the reviewed 46-release OpenCL ownership correction; GitHub App write access to upstream is blocked.
- Source-index regeneration with pinned line-aware symbol inventory.
- Runtime overlays for mmap/page faults, scheduler copies, events, KV/recurrent growth, and backend queues.
- Website browser-level accessibility and deployed verification.

## Publication and validation state

- Draft PR #3 is based on `agent/eaai-two-week-execution-plan`.
- The branch now contains the two-week plan, handoff ledger, legal-fixture decision, deterministic GGUF fixture package, focused tests, and durable run notes.
- Focused local validation passed for the exact generator/test contents before repository write.
- No external source was newly introduced; the official GGUF specification was already recorded in the research ledger.
- Final-head workflow results must be checked after context updates complete.

## Known blockers and caveats

- **Orchestrator files:** `docs/publication/orchestrator-state.md` and `docs/publication/evidence-backlog.md` are not yet available on the active branch, so dependency-safe recommendations are being followed.
- **Browser agreement:** no browser parser yet proves agreement with the Python golden output.
- **Native acceptance:** the synthetic file is a format-teaching fixture and is not claimed to be a valid inference model; pinned native GGUF-reader acceptance is a separate future check.
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
