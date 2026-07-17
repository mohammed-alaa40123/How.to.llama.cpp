# EAAI research orchestrator state

_Last updated: 2026-07-17 06:01 Africa/Cairo_

This file is the single source of truth for the EAAI experience-report preparation. It coordinates bounded repository work; it does not authorize manuscript drafting.

## Executive status

**Phase:** Week 1 foundation — contracts, deterministic fixtures, schemas, and the smallest executable-learning vertical slice.

**Overall judgment:** the project now has a coherent contract layer with passing commit-scoped CI through the media-manifest branch. The strongest evidence is machine-checkable separation of build, inference, authored/source-derived trace data, local progress, and deterministic versus generated media. The weakest areas remain learner/expert-use evidence, independent technical review, a fair workflow baseline, retrospective agent-workflow extraction, native/container reproducibility, and a coherent end-to-end demo.

**Current stacked branch:** `agent/media-manifest-validation` at `bcb7555ef8b4e80817b5b812c35db6b1c6f7b9a9`.

**Current CI state:** Documentation CI run `29549208249` completed successfully for the media-manifest branch. Strict MkDocs integration, unit tests, compilation and asset checks are therefore no longer the active blocker for the contract stack.

**Parallel review state:** draft PR #8 contains an adversarial EAAI review package. Its findings are coordination evidence but are not yet integrated into the active stack. The review recommends rejection in the current evidence state and identifies major gaps in educational outcomes, workflow comparison, native reproducibility, viewer learning value and independent technical correctness review.

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
- Versioned executable-trace schema, authored GGUF-loading trace, replay/provenance validator, and malformed-input tests.
- Versioned local-only learner-progress schema and privacy-minimizing validator.
- Media asset manifest schema, semantic validator, deterministic authoritative example and generated-media safety boundaries.
- Initial literature map supporting intentionally unequal browser, local-native, and cloud-container tiers.
- Passing Documentation CI for the current media-manifest stack: run `29549208249`.

## Current contradictions and corrections

- The adversarial review artifacts live on parallel PR #8, not the active media stack. They must be integrated deliberately rather than treated as already merged evidence.
- The shared handoff ledger lacks the progress, adversarial-review and media-manifest entries; this run appends a consolidated coordination record without rewriting earlier history.
- The sample trace is authored/source-derived, not native-captured. No documentation or UI may imply otherwise.
- A passing model-free Lab 0 report proves environment/build/executable launch only, not model load or inference.
- A valid media manifest proves policy compliance and provenance fields, not educational effectiveness or technical correctness of a figure.

## Venue state

As of 2026-07-17, no official EAAI-27 call has been verified. The official AAAI-27 main-conference page lists Montréal, February 16-23, 2027, with main-track abstract and paper deadlines on July 21 and July 28, 2026; these dates must **not** be assumed to apply to EAAI. The latest verified EAAI call is EAAI-26, whose Experience Report and Innovative Practice area required development and use context, collected data, prior-literature motivation, novelty, and rich reflection on what worked, what did not, and why. Reverify the official EAAI-27 call before any submission decision.

Official sources:

- https://aaai.org/conference/aaai/aaai-27/
- https://aaai.org/conference/aaai/aaai-26/eaai-26-call/

## Next 7 dependency-ordered actions

1. **Validation Architect — TRACE-02:** validate source paths and line/function anchors against the immutable llama.cpp revision; add deterministic replay, missing-data and browser-bound tests.
2. **Validation Architect — LAB0-02:** define the supported local/container matrix, exact `uv`/compiler/CMake/Ninja checks, stable diagnostic codes, and time-to-ready protocol.
3. **Documentation Builder — FIG-01:** generate one deterministic GGUF-layout SVG from structured fixture data and replace placeholder manifest hashes with recomputed input/output checksums.
4. **Documentation Builder — VIEW-01:** only after TRACE-02 passes, add the minimal keyboard-operable authored-trace viewer with forward/back controls, visible evidence labels and transcript/static fallback.
5. **Validation Architect — DATA-01:** freeze and implement the retrospective extraction schema for assignments, commits, failures, corrections, CI, human decisions, cost proxies and accepted/rejected outputs.
6. **Literature and Venue Scout — LIT-02:** verify current official OpenAI, Gemini/Nano Banana and NotebookLM capabilities and restrictions; produce media design requirements rather than promotional feature lists.
7. **Literature and Venue Scout — VENUE-01:** locate the official EAAI-27 call when published and update venue requirements without borrowing AAAI main-track dates.

## Scope cuts for July 17-31

- Optional generated image/audio/video samples remain noncritical and must not delay Lab 0, GGUF Anatomy, trace validation, deterministic figures, progress portability or retrospective evidence.
- Codespaces polish is secondary to one reproducible devcontainer definition and documented local-native evidence.
- Native trace instrumentation remains blocked until authored-trace source links, replay semantics and viewer accessibility pass.

## Human-action blockers

- Approve the intended evaluation pathway before participant recruitment or personal-data collection.
- Nominate an independent llama.cpp/GGML technical reviewer before correctness claims are made.
- Decide whether any optional paid media API credentials may be used; no credential is needed for the deterministic Week 1 path.
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
