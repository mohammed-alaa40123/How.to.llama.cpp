# EAAI research orchestrator state

_Last updated: 2026-07-17 15:00 Africa/Cairo_

This file is the single source of truth for the EAAI experience-report preparation. It coordinates bounded repository work; it does not authorize manuscript drafting.

## Executive status

**Phase:** Week 1 foundation transitioning into Week 2 vertical-slice integration.

**Overall judgment:** the repository now contains all three initial educational artifacts in bounded form: a model-free Lab 0 validation contract, a browser-first GGUF Anatomy slice, and an authored/source-derived executable-lecture viewer. It also contains deterministic media, a first retrospective agent-workflow batch, and a local progress import/export implementation. The strongest evidence remains deterministic provenance, source-revision pinning, replay validation, privacy boundaries, and passing parent CI. The weakest areas are measured Lab 0 reproducibility, Lab 1 progress integration, a frozen information-equivalent baseline, independent technical review, approved educational evaluation, and a verified EAAI-27 call.

**Current stacked branch:** `agent/progress02-local-import-export` at `43f694b6bc603623b924ffcb3e81286636654fa9`.

**Current CI state:** parent DATA-01 batch CI passed in run `29572506104`. Commit-scoped CI for the current PROGRESS-02 head was not available through the connected status surface during this run, so PROGRESS-02 remains in progress. No passing result is inferred.

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
2. Machine-checkable contracts for lab evidence, trace provenance/replay, local learner progress, media provenance, and retrospective workflow records.
3. A longitudinal, auditable case study of scheduled specialist agents operating with human supervision, deterministic tests, and repository memory.
4. Design lessons about separating deterministic technical evidence from optional generated educational media.

## Evidence status

### Verified

- Dependency-ordered July 17-31 plan and complete lesson contracts.
- Legal fixture decision: model-free Lab 0 core, learner-provided optional inference, and project-owned synthetic GGUF.
- Deterministic 428-byte GGUF v3 generator, manifest, golden parse, checksum, alignment/range assertions, and corruption fixtures.
- Lab 0 six-phase report and reproducibility contracts with semantic validators; contract CI passed, but real environment rows are absent.
- Versioned executable-trace schema, immutable source anchors, corrected authored GGUF-loading trace, deterministic replay, and malformed-input tests.
- Minimal static trace viewer with bounded keyboard navigation, evidence labels, pinned source links, reduced-motion handling, and ordered transcript fallback.
- Browser-first GGUF Anatomy slice with Predict-Discover-Explain checkpoints and Python/browser fixture agreement.
- Versioned local-only learner-progress schema and a framework-free import/export adapter; final-head CI and Lab 1 integration remain open.
- Media manifest/provenance schema, official capability review, and deterministic GGUF-layout SVG with exact replay.
- DATA-01 schema plus a first three-archetype retrospective batch covering a successful increment, CI repair, and blocked reassignment.

### Interpretation

- The vertical slices are coherent enough to justify integration work, but not educational-effectiveness claims.
- The retrospective records show that corrections and blocked reassignment can be represented, but not that the agent workflow is superior to simpler workflows.

### Historical

- A false-but-plausible trace anchor and a deterministic-figure byte drift were retained as negative evidence rather than hidden.
- Real Lab 0 execution has repeatedly remained blocked in connector-only runtimes; no environment timing row has been fabricated.

### Open questions

- Can Ubuntu 24.04 local-native and devcontainer environments complete the exact model-free Lab 0 path?
- Can Lab 1 persist, export, clear, import, and resume progress without telemetry or accessibility regressions?
- Does the trace viewer outperform an information-equivalent static source/text condition on bounded code-tracing tasks?
- Will independent llama.cpp/GGML review accept the fixture, trace, explanations, and deterministic figure?

## Venue state

As of 2026-07-17, no official EAAI-27 call was found on the official AAAI EAAI or AAAI-27 pages. The AAAI-27 main conference is scheduled for Montréal, February 16-23, 2027, with main-track deadlines in July 2026; those dates must not be transferred to EAAI. EAAI-26 remains the latest verified detailed call and is historical guidance only.

Official sources:

- https://aaai.org/conference/eaai/
- https://aaai.org/conference/aaai/aaai-27/
- https://aaai.org/conference/aaai/aaai-26/eaai-26-call/

## Next 7 dependency-ordered actions

1. **Documentation Builder — `PROGRESS-03`:** after PROGRESS-02 final-head CI passes, connect the local progress adapter to Lab 1 for one checkpoint round trip, export, clear, import, and resume; add no telemetry or server sync.
2. **Validation Architect — `LAB0-03`:** execute and retain a real Ubuntu 24.04 model-free Lab 0 row with exact tool versions, commands, diagnostics, and time-to-ready when a network-capable environment is available.
3. **Validation Architect — `LAB0-04`:** execute the same bounded path in the devcontainer and compare only contract-defined fields.
4. **Validation Architect — `BASE-01A`:** freeze an information-equivalent static-source/text versus viewer benchmark fixture, tasks, answer key, scoring, timeout, source revision, and accessibility fallbacks; do not recruit participants.
5. **Orchestrator + Adversarial Reviewer — `REVIEW-02`:** consolidate active-stack rejection risks and map every fatal/major concern to an evidence gate.
6. **Human + Technical Reviewer — `REVIEW-01`:** nominate and complete independent review of the synthetic fixture, trace anchors/explanations, browser parser, and deterministic figure.
7. **Literature and Venue Scout — `VENUE-01`:** continue official EAAI-27 monitoring; do not borrow AAAI main-track dates.

## Agent assignments

- **Documentation Builder:** PROGRESS-03 only after the current progress branch passes; otherwise perform only the narrow CI repair.
- **Validation Architect:** prioritize measured LAB0-03/LAB0-04 execution when the environment permits, then BASE-01A.
- **Literature and Venue Scout:** continue venue monitoring and support the systematic documentation audit; no paper prose.
- **Adversarial Reviewer:** integrate major concerns into REVIEW-02 without expanding product scope.
- **Paper Integrator:** disabled.

## Human-action blockers

- Approve the intended evaluation pathway before participant recruitment or personal-data collection.
- Nominate an independent llama.cpp/GGML technical reviewer.
- Review the first retrospective batch coding and missing-value rules.
- Decide how to resolve the duplicate PROGRESS-02 draft PRs before merging the stack.
- Review and merge the stacked PR chain in dependency order after CI passes.

## Manuscript-writing gate

Do not activate the Paper Integrator until all conditions below are evidenced:

- stable audience, educational problem, learning objectives, research questions, and claims-evidence table;
- frozen workflow/autonomy/human-supervision description and reviewed retrospective dataset;
- passing integrated CI and reproducible Lab 0, GGUF lab, trace-viewer, progress, and media-manifest vertical slice;
- at least one fair baseline comparison;
- independent technical correctness review;
- approved learner or expert evaluation pathway and, when applicable, ethics approval;
- current official EAAI requirements;
- no unresolved fatal or major reviewer concern that invalidates the central contribution.
