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

## 2026-07-17 00:02 — Literature and Venue Scout

### Assignment status

`orchestrator-state.md` and `evidence-backlog.md` remain absent from both `main` and the active executable-learning branch. The highest unresolved literature dependency in the two-week plan was therefore selected: evidence for the browser/local/cloud platform boundary.

### Bounded increment completed

Created [`literature-map.md`](literature-map.md) with a focused evidence map covering Stanford CS336 executable lectures, JupyterLite kernels and storage, `uv` locking/offline behavior, GitHub devcontainers and Codespaces prebuilds, Binder reproducibility guidance, and MLSysBook’s Predict–Discover–Explain labs. Updated the external-source ledger.

### Verified findings

- JupyterLite executes constrained browser kernels and is suitable for parsing, calculations, simulations, checkpoints, and trace replay; it is not evidence of native llama.cpp C++ execution.
- `uv sync --locked` supports a reproducible Python-tooling contract but does not replace compiler, CMake/Ninja, or llama.cpp source pinning.
- Devcontainers can standardize a native build environment; Codespaces prebuilds are optional, may incur storage cost, and should not be a Week 1 dependency.
- CS336 demonstrates a trace-producing lecture program separated from a React/Vite trace viewer.
- MLSysBook provides a concrete browser-first Predict–Discover–Explain pattern with persistent decision records.

### Design recommendation

Use intentionally unequal tiers: browser-first for concepts, local native as the authoritative runtime path, and a devcontainer as the reproducibility fallback. Reject presenting the three tiers as interchangeable runtimes. Require every result to identify whether it is browser-derived, native-captured, source-derived, or an authored example.

### EAAI implication

The useful contribution is the visible evidence boundary between simulation, authored explanation, source-derived structure, and native execution. Evaluation should test whether learners can distinguish these categories and trace code/runtime behavior, rather than treating one-click setup as the main educational outcome.

### Validation and limitations

- Sources are official documentation or primary project repositories and were checked on 2026-07-17.
- No implementation, paid API, model download, or participant data was used.
- Current service behavior, limits, and billing must be reverified before deployment.
- Full MkDocs/CI and live-site checks remain pending because this connector run has no local checkout or Actions-log interface.

### Next dependency

The next distinct literature slice should verify the media pipeline from current official API documentation: OpenAI image/speech/realtime/video, Gemini image generation, NotebookLM automation limits, provenance, accessibility, licensing, caching, privacy, and human-review requirements.

## 2026-07-17 01:00 — Documentation Builder

### Assignment status

`orchestrator-state.md` and `evidence-backlog.md` remain unavailable. The run followed the highest repository-ranked dependency in `project-state.md` and the previous Documentation Builder handoff: implement the deterministic synthetic GGUF fixture package.

### Bounded increment completed

Added:

- `scripts/generate_synthetic_gguf.py`;
- `labs/fixtures/gguf/synthetic-v0.manifest.json`;
- `labs/fixtures/gguf/synthetic-v0.golden.json`;
- `tests/test_generate_synthetic_gguf.py`;
- [`../../logs/research/2026-07-17/0100-synthetic-gguf-fixture.md`](../../logs/research/2026-07-17/0100-synthetic-gguf-fixture.md).

The generator creates a 428-byte, little-endian GGUF v3 teaching file with five typed metadata records, two F32 tensor descriptors, 32-byte alignment, deterministic project-authored payloads, and three bounded corruption variants.

### Verified findings

- Whole-file SHA-256: `688d0ef28c83d6972e291cc0342e695540eae8496b3ec8e92bdbb91e3982a564`.
- Tensor data starts at absolute byte 384.
- `demo.matrix` occupies bytes 384–399 at relative offset 0.
- `demo.vector` occupies bytes 416–427 at relative offset 32.
- Focused tests verify deterministic regeneration, manifest/golden agreement, aligned and bounded ranges, and rejection of bad magic, a misaligned descriptor offset, and a truncated payload.
- No model weights, corpus, learner data, network download, telemetry, or paid API were introduced.

### Truth labels

- **Verified:** the exact committed generator and tests passed three focused unit tests and `--check` in an isolated local workspace before repository write.
- **Interpretation:** generator plus manifest and golden output provide stronger provenance and reviewability than committing an opaque fixture binary as the primary artifact.
- **Open question:** browser/Python agreement and pinned native `gguf_init_from_file` acceptance remain unimplemented.

### EAAI evidence

This increment turns the fixture-policy decision into an auditable educational artifact with explicit provenance, failure cases, deterministic expected output, and a clear boundary between format learning and inference. It can support or falsify claims about reproducibility, source-linked content generation, validator coverage, and human review burden.

### Next dependency

Add machine-readable trace, media-manifest, and learner-progress schemas with focused validators, unless the orchestrator ranks the Lab 0 checker interface first.
