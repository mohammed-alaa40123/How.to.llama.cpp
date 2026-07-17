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
- run record `logs/research/2026-07-17/0100-synthetic-gguf-fixture.md`.

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

## 2026-07-17 01:58 — Documentation Builder

### Assignment status

`orchestrator-state.md` and `evidence-backlog.md` remain unavailable. The repository TODO ranked the Lab 0 checker interface ahead of the remaining schema package, so this run selected that bounded dependency.

### Bounded increment completed

Added the Lab 0 learning contract, JSON Schema, dependency-free semantic validator, a valid model-free example report, five focused unit tests, and run record `logs/research/2026-07-17/0158-lab0-checker-interface.md`.

The interface separates `environment`, `configure`, `compile`, `executable_launch`, `model_load`, and `inference`. It rejects impossible success chains and prevents a model-free executable launch from being represented as model loading or inference.

### Truth labels

- **Verified:** the committed validator encodes explicit dependency and claim-consistency invariants.
- **Interpretation:** the report makes setup evidence auditable and turns the build-equals-inference misconception into a machine-checkable assessment artifact.
- **Open question:** the exact bounded build target, diagnostic taxonomy, platform matrix, and command runner remain unimplemented.

### Validation and safety

Five focused tests were added, but this connector environment could not execute them locally. CI is the remaining validation authority for the branch head. No model, prompt, generated output, telemetry, credential, paid API, or personal data was introduced.

### Next dependency

Add the trace schema and authored sample trace contract unless the orchestrator publishes a different dependency order.

## 2026-07-17 02:06 — Validation Architect

### Assignment status

`orchestrator-state.md` and `evidence-backlog.md` remain unavailable. The highest dependency-safe evidence gap in the two-week plan and latest handoff was the machine-readable trace schema and authored sample-trace contract.

### Bounded increment completed

Added:

- `schemas/executable-trace.schema.json`;
- `scripts/validate_executable_trace.py`;
- `executable_lectures/traces/gguf-load-authored-v0.json`;
- `tests/test_validate_executable_trace.py`;
- [`validation-plan.md`](validation-plan.md).

The package pins the upstream revision, labels evidence at trace, step, and nested-object levels, bounds trace and collection sizes, requires safe repository-relative source/figure paths, requires alt text and a static summary, and defines contiguous zero-based sequences as the deterministic forward/back replay contract.

### EAAI claim supported or falsified

This increment tests whether repository-native agent work can produce source-pinned educational traces with machine-checkable evidence boundaries, replay order, provenance, and accessibility fallbacks. The claim is weakened if malformed traces can use mutable revisions, overstate native capture, reorder steps, traverse paths, omit static summaries, or exceed browser-review bounds.

### Truth labels

- **Verified:** the committed schema and semantic validator encode the invariants above, and seven focused test cases were added.
- **Interpretation:** an authored GGUF-loading trace is the safest minimum contract before native instrumentation because it makes absent runtime evidence explicit.
- **Open question:** source-link resolution against the pinned commit, viewer keyboard behavior, native capture, and browser performance remain unvalidated.

### Validation and limitations

- No model download, paid API, credential, telemetry, participant data, or server-side progress sync was introduced.
- This connector environment could not execute the tests locally; CI is the validation authority for the branch.
- The sample source lines are authored contract locations and must pass a later network source-link CI lane before publication.

### Next dependency

Review and merge the trace contract, then implement either the media manifest/provenance validator or local progress export/import schema according to the next orchestrator ranking. A minimal viewer must not begin until the trace contract is accepted.

## 2026-07-17 04:02 — Documentation Builder

### Assignment status

The authoritative orchestrator ranked strict MkDocs repair as the P0 dependency before viewer or media expansion. Documentation CI run `29544077919` failed only at `mkdocs build --strict`; all context, link, unit-test, shell, compilation, and asset checks before it passed.

### Bounded increment completed

Replaced two Markdown links from `docs/publication/agent-handoffs.md` to run notes outside the MkDocs `docs/` tree with explicit repository-path code references. The run notes remain durable repository evidence, but MkDocs no longer interprets them as documentation-page targets.

### Truth labels

- **Verified:** CI reported exactly two strict-mode warnings, for the `0100-synthetic-gguf-fixture.md` and `0158-lab0-checker-interface.md` links.
- **Interpretation:** code-form repository paths are preferable here because the files intentionally live under `logs/research/`, outside the generated documentation site.
- **Historical:** the warning existed across the stacked executable-learning branch before the orchestrator state was added.
- **Open question:** the new branch must obtain a passing commit-scoped Documentation CI result before this blocker is closed.

### Validation and next dependency

No runtime, schema, fixture, learner-data, model, paid API, or publication claim changed. After CI passes, the next Documentation Builder assignment is the media manifest/provenance validator.

## 2026-07-18 02:02 — Documentation Builder

### Assignment status

`STACK-01` remains blocked by the required human choice of canonical progress implementation and merge order. The next dependency-safe P0 item was the first available measured `LAB0-03` Ubuntu run, whose dedicated workflow failed while Documentation CI passed.

### Bounded increment completed

Hardened `.github/workflows/lab0-ubuntu-reproducibility.yml` so the exact JSON report is staged, checksummed and uploaded before semantic validation. The workflow now emits `LAB0_REPORT_MISSING` when no report exists and validates the same retained path that reviewers can download.

Detailed record: `logs/research/2026-07-18/0202-lab0-evidence-retention-order.md`.

### Truth labels

- **Verified:** Ubuntu workflow run `29619592906` reached the runner step but failed validation and artifact upload; no artifact was retained. Documentation CI `29619592930` passed on the same PR head.
- **Interpretation:** failed evidence must be retained before semantic rejection so setup/build/launch contradictions remain diagnosable and educationally useful.
- **Historical:** the original lane validated before upload.
- **Open question:** the next run must show whether the emitted report is semantically invalid or whether the failure was only retention/path related.

### Validation and next dependency

No Lab 0 commands, source revision, model policy, schema or claim changed. Commit-scoped workflow results are authoritative. Next: inspect the retained report from the rerun and make at most one evidence-backed repair; do not call `LAB0-03` reproducible until the report validates.
