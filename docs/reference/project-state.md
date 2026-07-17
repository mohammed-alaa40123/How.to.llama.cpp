# Project state

_Last updated: 2026-07-17 07:58 Africa/Cairo_

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

- Canonical source-pinned llama.cpp/GGML documentation, indexing, strict Documentation CI, Pages workflow, and durable run context.
- EAAI July 17-31 plan, frozen initial learner/lesson contracts, legal fixture boundary, deterministic synthetic GGUF, and three-tier platform decision.
- Lab 0 six-phase report contract, executable-trace contract, local-progress contract, and media-manifest contract.
- Strict MkDocs repair verified by Documentation CI run `29546570700`.
- Media manifest/provenance validation verified by Documentation CI run `29549208249`.
- Deterministic GGUF-layout SVG and exact replay/checksum validation verified by Documentation CI run `29553868078`.

## Latest concrete findings

### Verified

- The original authored trace locations at lines 1100, 1110, and 1260 did not identify the claimed `gguf_init_from_file_impl` function at pinned revision `e3546c7`.
- The pinned GGUF reader implementation is `gguf_init_from_reader`, beginning at `ggml/src/gguf.cpp:451`.
- Relevant verified anchors are line 451 (function entry), 456 (file magic), 623 (tensor info), and 757 (aligned data-section handling).
- The upstream Git blob for the pinned file is `c3ffa1a13435bd531c259b6106a3a6763e4f2df9`.
- `TRACE-02` now has a checked-in source lock, exact line-text hashes, call-stack anchor checks, deterministic replay operations, a static transcript fallback, and seven focused tests.
- The sample trace now points to the actual deterministic figure path and remains explicitly authored/source-derived rather than native-captured.

### Interpretation

- A small source lock makes source drift an explicit maintenance failure in ordinary offline CI; it is stronger than checking that an immutable GitHub URL merely exists.
- The source lock validates identity and provenance, not native execution or educational effectiveness.

### Historical

- Earlier work established evidence labels, contiguous zero-based steps, immutable commit SHAs, safe paths, static summaries, and 500-step/2 MiB browser bounds.

### Open questions

- Commit-scoped Documentation CI must pass before `TRACE-02` is evidenced and `VIEW-01` is unblocked.
- A future native/container lane should resolve the same anchors against a pinned llama.cpp checkout.
- Independent llama.cpp/GGML review and a fair viewer-versus-static baseline remain required.

## Immediate next task

```text
obtain commit-scoped Documentation CI for TRACE-02
  → if passing, mark TRACE-02 evidenced
  → unblock only the minimal keyboard-operable authored-trace viewer
  → do not add native instrumentation until viewer/source/replay/accessibility gates pass
```

## In progress

- Draft stacked PRs for the EAAI executable-learning foundation.
- `TRACE-02` final-head CI.
- Validation Architect assignments `LAB0-02` and `DATA-01`.
- Literature Scout assignment `VENUE-01`.

## Known blockers and caveats

- **Viewer dependency:** `VIEW-01` remains blocked until `TRACE-02` obtains passing final-head CI.
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
- Authored sample trace with verified immutable source anchors and a narrow viewer shell.
- Lab 0 checker interface and model-free environment/build report.
- One deterministic technical figure from structured input.
- Accessibility fallbacks, reproducibility evidence, and CI gates for every introduced artifact.
