# EAAI research orchestrator state

_Last updated: 2026-07-17 12:03 Africa/Cairo_

This file is the single source of truth for the EAAI experience-report preparation. It coordinates bounded repository work; it does not authorize manuscript drafting.

## Executive status

**Phase:** Week 1 foundation transitioning into Week 2 vertical-slice execution.

**Overall judgment:** the repository now has validated contracts and integrated bounded slices for the synthetic GGUF lab, authored trace viewer, deterministic figure, media provenance, local-only progress, and Lab 0 reproducibility reporting. The Lab 0 contract passed CI, but no real local-native or devcontainer matrix row has been executed, so reproducibility remains partial. The strongest evidence is deterministic provenance, source-revision pinning, evidence-kind separation, privacy boundaries, and passing integration CI. The weakest areas remain real Lab 0 execution, progress import/export, retrospective agent-workflow extraction, baseline comparison, independent correctness review, approved educational evaluation, and current EAAI-27 requirements.

**Current stacked branch:** `agent/lab0-reproducibility-validation` at `9d05719e25a25a1da644ec17237f2f3c5259afe1`.

**Current CI state:** Documentation CI run `29565651085` completed successfully. This validates the Lab 0 reproducibility schema, semantic checks, tests, and MkDocs integration. It does not validate any real operating-system/container row, the pinned native command against llama.cpp, model loading, inference, learner benefit, or cross-platform reproducibility.

## Frozen educational framing

### Target audience

Advanced undergraduate, graduate, and early-stage systems researchers who can read C/C++ and Python but cannot yet connect GGUF storage, virtual memory, GGML graph construction, backend scheduling, and token generation.

### Educational problem

Existing usage-oriented material does not reliably teach learners to distinguish:

- file format from runtime graph;
- mapped bytes from resident physical pages;
- authored explanation from captured runtime evidence;
- build success from model loading and inference;
- browser simulation from native llama.cpp execution.

The claim that this gap is widespread remains a **hypothesis** until a systematic documentation audit is completed.

### Initial learning experiences

1. **Lab 0 — Build and Run llama.cpp:** distinguish Python tooling, native configuration/compilation, executable launch, model load, and inference.
2. **Lab 1 — GGUF Anatomy:** predict, parse, inspect, and explain a deterministic synthetic GGUF without implying that GGUF stores an executable graph.
3. **Executable Lecture 0 — GGUF loading trace:** step through a source-pinned authored/source-derived trace before native instrumentation is attempted.

## Research questions

- **RQ1 — Educational artifact:** Can source-pinned executable labs and evidence-labelled traces improve learners' ability to explain and trace difficult llama.cpp/GGML concepts?
- **RQ2 — Evidence boundaries:** Can the environment make distinctions among browser-derived, source-derived, authored, and native-captured evidence understandable and machine-checkable?
- **RQ3 — Development workflow:** What succeeds, fails, and requires human correction when role-specialized scheduled agents build and maintain the resource in a persistent repository?
- **RQ4 — Reproducibility:** Which combination of browser, local-native, and cloud-container execution provides useful learning access without obscuring runtime differences?

These are planning questions, not answered claims.

## Defensible contributions under construction

1. A revision-pinned executable-learning environment for source-level AI-systems education.
2. Machine-checkable contracts for lab evidence, trace provenance/replay, local learner progress, and media provenance.
3. A longitudinal, auditable case study of scheduled specialist agents operating with human supervision, deterministic tests, and repository memory.
4. Design lessons about separating deterministic technical evidence from optional generated educational media.

## Verified completed evidence

- Dependency-ordered July 17-31 plan and lesson contracts.
- Legal fixture decision: model-free Lab 0 core, learner-provided optional inference, and project-owned synthetic GGUF.
- Deterministic 428-byte GGUF v3 generator, manifest, golden parse, checksum, alignment/range assertions, and corruption fixtures.
- Lab 0 six-phase report contract and semantic validator.
- Lab 0 reproducibility record contract with exact `uv sync --locked`, CMake/Ninja, bounded-target, timing, diagnostics, offline, and security semantics; passing CI run `29565651085`.
- Browser-first GGUF Anatomy slice with Predict-Discover-Explain checkpoints and passing CI run `29562479577`.
- Versioned executable-trace schema, immutable source anchors, corrected authored GGUF-loading trace, deterministic replay, and malformed-input tests.
- Minimal static trace viewer with Previous/Next and Arrow/Home/End navigation, evidence labels, pinned source links, live text status, reduced-motion handling, and ordered transcript fallback.
- Versioned local-only learner-progress schema and privacy-minimizing validator.
- Media manifest/provenance schema and validator.
- Deterministic GGUF-layout SVG with exact replay, checksums, alt text, and passing CI.
- Official media/API capability review that keeps generated media supplemental and manually review-gated.

## Current claim boundaries

- The viewer is authored/source-derived, not native-captured.
- The Lab 0 reproducibility example is illustrative, not a measured environment run.
- A passing model-free Lab 0 report proves environment/build/executable launch only, not model load or inference.
- Browser parsing is evidence about a synthetic fixture, not native llama.cpp execution.
- Passing CI establishes deterministic integration, not educational effectiveness or cross-platform reproducibility.
- No learner or participant data has been collected.

## Venue state

As of 2026-07-17, no official EAAI-27 call has been verified. The official AAAI-27 main-conference page lists Montréal, February 16-23, 2027, with main-track deadlines on July 21, July 28, and July 31, 2026; these dates must **not** be assumed to apply to EAAI. The latest verified EAAI call is EAAI-26, whose main track accepted research papers and experience reports and required technical soundness, clear presentation, evaluation of claims/results as applicable, and ethics/inclusivity engagement as applicable. Reverify the official EAAI-27 call before any submission decision.

Official sources:

- https://aaai.org/conference/aaai/aaai-27/
- https://aaai.org/conference/aaai/aaai-26/eaai-26-call/

## Next 7 dependency-ordered actions

1. **Validation Architect — `DATA-01`:** define the retrospective extraction schema for assignments, commits, failures, corrections, validators, human decisions, cost proxies, and accepted/rejected outputs.
2. **Validation Architect — `LAB0-03`:** execute and retain a real Ubuntu 24.04 local-native model-free row, verifying the pinned target and command shape.
3. **Validation Architect — `LAB0-04`:** execute the same bounded model-free path in the devcontainer and compare diagnostics and time-to-ready semantics.
4. **Validation Architect — `PROGRESS-02`:** implement local export/import, migration, corruption recovery, and storage-adapter tests before connecting progress to Lab 1.
5. **Adversarial Reviewer + Orchestrator — `REVIEW-02`:** integrate the reviewer package into the active stack and convert every major concern into an evidence gate.
6. **Literature and Venue Scout — source-comprehension baseline:** identify primary evidence for a fair static-source/text baseline and code-tracing outcome measures for the viewer.
7. **Literature and Venue Scout — `VENUE-01`:** continue monitoring official EAAI-27 requirements without borrowing AAAI main-track dates.

## Agent assignments

- **Documentation Builder:** avoid new broad features; prepare only dependency-safe integration support for progress persistence and the end-to-end demo.
- **Validation Architect:** own `DATA-01`, then real Lab 0 local/devcontainer rows, then `PROGRESS-02`.
- **Literature and Venue Scout:** define the viewer baseline and continue official venue monitoring; keep the documentation-gap claim hypothetical.
- **Adversarial Reviewer:** integrate major concerns into the active evidence queue and reject unsupported learner-benefit, reproducibility, or generalization claims.

## Human-action blockers

- Approve the intended evaluation pathway before participant recruitment or personal-data collection.
- Nominate an independent llama.cpp/GGML technical reviewer before correctness claims are made.
- Review the pinned Lab 0 native target/options after the first real run.
- Decide whether any optional paid media API credentials may be used; no credential is needed for the deterministic core path.
- Review and merge the stacked PR chain in dependency order after CI passes.

## Manuscript-writing gate

Do not activate the Paper Integrator until all conditions below are evidenced:

- stable audience, educational problem, learning objectives, and research questions;
- frozen workflow/autonomy/human-supervision description;
- passing integrated CI and reproducible Lab 0, GGUF lab, trace-viewer, progress, and media-manifest vertical slice;
- retrospective repository dataset with agent runs, assignments, failures, corrections, costs, and accepted/rejected outputs;
- at least one fair baseline comparison;
- independent technical correctness review;
- approved learner or expert evaluation pathway and, when applicable, ethics approval;
- current official venue requirements;
- no unresolved fatal or major reviewer concern that invalidates the central contribution.

**Exact condition for beginning manuscript writing:** every item above must be linked to durable repository evidence and marked evidenced in `evidence-backlog.md`; implementation or CI success alone is insufficient.