# EAAI agent handoffs

This file is the append-only coordination ledger for bounded assignments, evidence, blockers, and reviewer feedback. Agents should link durable repository artifacts rather than copying long reports here.

## 2026-07-16 23:00 — Documentation Builder

### Assignment status

The requested `docs/publication/orchestrator-state.md`, `docs/publication/evidence-backlog.md`, `docs/publication/two-week-execution-plan.md`, and `docs/publication/agent-handoffs.md` were not present on `main` at run start. Therefore no authoritative orchestrator-ranked implementation assignment could be read.

### Dependency-safe increment completed

Created [`two-week-execution-plan.md`](two-week-execution-plan.md), which freezes:

- the initial target learner and prerequisites;
- learning contracts for Lab 0, Lab 1, and Executable Lecture 0;
- browser, local-native, and cloud-container execution tiers;
- deterministic technical-media authority and optional AI-media review gates;
- minimum trace schema and evidence-kind distinctions;
- local-first learner-progress privacy boundary;
- Week 1 and Week 2 milestones, acceptance gates, CI lanes, evidence-retention requirements, and definition of done.

### Truth labels

- **Verified:** the publication coordination files above were absent from `main` when checked.
- **Interpretation:** architecture and acceptance gates are the safest prerequisite before implementation because broad scaffolding without fixtures, validators, source-revision policy, privacy boundaries, and accessibility fallbacks would create non-reviewable feature sprawl.
- **Open question:** choose GGUF loading, graph construction, or one-token decode as the first bounded trace after fixture and instrumentation feasibility review.

### Validation

- The document uses repository-relative links and no external source was added.
- The research ledger therefore requires no source change.
- No paid API, model download, or participant data was used.
- Full MkDocs and CI execution remains pending because this connector environment does not provide a local authenticated checkout or `gh` executable.

### Requested orchestrator action

Create or populate `orchestrator-state.md` and `evidence-backlog.md`, then record the next 3-7 dependency-ordered assignments. Recommended first assignment: select and document the legal synthetic/tiny fixture shared by Lab 0 and the GGUF Anatomy lab, because schemas, smoke tests, golden parser output, and browser demonstrations depend on it.

## 2026-07-17 00:00 — Documentation Builder

### Assignment status

`orchestrator-state.md` and `evidence-backlog.md` were still unavailable on the active branch, so the run followed the previously recorded dependency-safe recommendation: close the legal fixture decision before adding parsers, smoke tests, or trace instrumentation.

### Bounded increment completed

Created [`../labs/legal-fixture-decision.md`](../labs/legal-fixture-decision.md).

The decision separates three evidence paths:

- mandatory Lab 0 uses model-free build and executable-launch checks;
- optional real inference uses a learner-provided local GGUF path and is labelled separately;
- Lab 1 uses a deterministic project-owned synthetic GGUF with metadata, tensor descriptors, alignment, offsets, and non-model payload bytes.

Executable Lecture 0 may begin with a bounded GGUF-loading authored/source-derived trace, but every field must declare whether it is captured runtime evidence, source-derived, authored, interpretation, or an open question.

### Truth labels

- **Verified:** the project baseline and licensing policy already separate project-owned MIT content from pinned/linked upstream llama.cpp.
- **Interpretation:** separating build validation, file-format education, and real inference is safer and more educationally precise than redistributing a tiny third-party model as a universal fixture.
- **Open question:** the exact synthetic fixture fields and tensor shapes remain to be implemented and validated byte-for-byte.

### Validation and safety

- No third-party model, corpus, prompt, personal data, external API, or network download was introduced.
- The decision defines deterministic regeneration, checksum, golden parse, alignment/range checks, corruption tests, browser/Python agreement, keyboard/static fallbacks, and explicit non-inference success states.
- The research ledger remains unchanged because no new external source was added.

### Next dependency

Implement the deterministic synthetic GGUF generator, manifest schema, golden parser output, and bounded corruption variants. Do not add model downloads or call model-free launch checks “inference.”