# Project state

_Last updated: 2026-07-17 06:58 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream OpenCL revision audited: `505b1ed15ca80e2a19f12ff4ac365e40fb374053`
- Current upstream CPU_REPACK suitability revision reviewed: `8ee54c8b32a1b0cf13c03fc5723142bc62c775f6`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Executable-learning Week 1 foundation — contracts, legal fixtures, schemas, deterministic media, and smallest vertical slice**

## Completed foundations

- Canonical GGUF, model placement, `llama_model`, `llama_context`, graph/MoE, scheduler, memory-lifetime, backend, and inference-atlas pages.
- Source indexing, strict documentation CI, Pages deployment workflow, health checks, and durable run context.
- Generic scheduler plus CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL teardown audits.
- CPU repack, AMX, KleidiAI, and SpacemiT extra-buffer ownership comparison and destruction-harness specification.
- Complete pinned/current OpenCL event-ownership audit and executable CPU_REPACK lifetime regression evidence.
- Website UX review, Architecture navigation/index, and generated-HTML accessibility structure validation.
- EAAI July 17-31 plan, legal fixture boundary, deterministic synthetic GGUF, Lab 0 report contract, trace contract, progress contract, orchestration state, and evidence backlog.
- Strict MkDocs handoff-link repair verified by Documentation CI run `29546570700`.
- Media asset manifest/provenance contract verified by Documentation CI run `29549208249`.
- Deterministic GGUF-layout SVG generator, checked-in output, checksum/byte-count contract, accessibility metadata, and evidence-boundary tests.

## Latest concrete findings

### Verified

- `MEDIA-01` passed Documentation CI run `29549208249` for commit `bcb7555ef8b4e80817b5b812c35db6b1c6f7b9a9`.
- Documentation CI run `29551621279` reached unit-test discovery and failed only the two deterministic-figure replay assertions; all earlier context, link, and source-index checks passed.
- The failure was a checked-in-output drift: the generator produced header width `775.18`, while the committed SVG contained `775.25`; the manifest consequently recorded a stale output hash and byte count.
- The SVG has been regenerated from `labs/fixtures/gguf/synthetic-v0.golden.json` using the committed generator.
- Input SHA-256 remains `ae0fd013da8f7f463e79447978b5a2837e0a52b13029ad6bb23d2fcf3e150968`.
- Repaired output SHA-256 is `d93ab0a5eafe0fe7a4ee2db737ce077d2babb275a5c656c07b81105ae851cd25`; repaired output size is 2525 bytes.
- No generative model, model weight, external corpus, paid API, secret, telemetry or learner data is involved.

### Interpretation

- Exact generator replay is stronger evidence than manually reviewed visual similarity; a one-character geometric drift correctly invalidated the manifest and prevented `FIG-01` from being marked evidenced.
- The figure teaches storage layout only; using it to imply native GGUF loading, graph construction or inference would be evidence inflation.

### Historical

- Earlier work established source-pinned documentation, executable lifetime regressions, accessibility guards, legal fixtures, schemas, privacy constraints and orchestration state.

### Open questions

- The repaired branch still requires passing commit-scoped Documentation CI before `FIG-01` is evidenced.
- Independent GGUF/llama.cpp technical review remains required before correctness claims rely on the figure.
- Browser/Python parser agreement and pinned native GGUF-reader acceptance remain unimplemented.
- The exact bounded Lab 0 target, supported environment matrix and diagnostic taxonomy remain unresolved.

## Immediate next task

```text
obtain commit-scoped Documentation CI for the repaired FIG-01 output
  → if passing, mark FIG-01 evidenced
  → do not implement VIEW-01 until TRACE-02 passes
  → proceed only to the next orchestrator-unblocked vertical-slice dependency
```

## In progress

- Draft stacked PRs for the EAAI executable-learning foundation.
- Validation Architect assignments `TRACE-02`, `LAB0-02`, and `DATA-01`.
- Literature Scout assignments `LIT-02` and `VENUE-01`.
- Current-tree regeneration and sanitizer validation of the CPU_REPACK lifetime candidate.
- Website browser-level accessibility and deployed verification.

## Publication and validation state

- `docs/publication/orchestrator-state.md` and `docs/publication/evidence-backlog.md` are authoritative.
- `CI-01` and `MEDIA-01` are evidenced; `FIG-01` implementation exists but remains open pending passing repaired-head CI.
- No participant data, model, telemetry, credential, paid API call, generative-media output or manuscript prose was introduced.

## Known blockers and caveats

- **Figure CI closure:** the first figure branch CI exposed output/manifest drift; repaired final-head CI is now required.
- **Viewer dependency:** `VIEW-01` remains blocked until `TRACE-02` validates pinned source links and replay behavior.
- **Lab 0 runner:** the report interface exists, but no platform-specific runner or reproducibility matrix exists.
- **Browser agreement:** no browser parser yet proves agreement with the Python golden output.
- **Native acceptance:** the synthetic file is a format-teaching fixture and is not claimed to be an inference model.
- **Live-site verification:** Pages should be rechecked after the stacked changes merge to `main` and deploy.
- **Independent review:** `REVIEW-01` remains blocked on a nominated human technical reviewer.

## Definition of done for the executable-learning foundation phase

- Complete learning contracts and dependency-ordered July 17-31 plan.
- Legal fixture policy with no ambiguous model redistribution.
- Deterministic synthetic GGUF generator, manifest, golden output, and validators.
- Machine-readable trace, media-manifest, and progress schemas.
- Authored sample trace with explicit evidence kinds and a narrow viewer shell.
- Lab 0 checker interface and model-free environment/build report.
- One deterministic technical figure from structured input.
- Accessibility fallbacks, reproducibility evidence, and CI gates for every introduced artifact.
