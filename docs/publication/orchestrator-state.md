# EAAI research orchestrator state

_Last updated: 2026-07-17 03:06 Africa/Cairo_

This file is the single source of truth for the EAAI experience-report preparation. It coordinates bounded repository work; it does not authorize manuscript drafting.

## Executive status

**Phase:** Week 1 foundation — contracts, deterministic fixtures, schemas, and the smallest executable-learning vertical slice.

**Overall judgment:** the project has a coherent educational-artifact direction and a useful repository-native agent case study, but it is not manuscript-ready. The strongest completed evidence is machine-checkable provenance and boundary enforcement. The weakest areas are actual learner/expert-use evidence, independent correctness review, baseline comparison, retrospective agent-workflow data, and a working end-to-end demo.

**Current stacked branch:** `agent/progress-schema-validation` at `82f3f8c7bdfaff1e33ffb4ea733422c07fa00ad5`.

**Current CI state:** Documentation CI run `29543838455` failed only at strict MkDocs integration after all context, link, source-index, unit-test discovery, shell, Python-compilation, and asset-validation steps passed. This is a release blocker for the stacked branch and must be resolved before new viewer or media features are accepted.

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
2. Machine-checkable contracts for lab evidence, trace provenance/replay, local learner progress, and eventually media provenance.
3. A longitudinal, auditable case study of scheduled specialist agents operating with human supervision, deterministic tests, and repository memory.
4. Design lessons about separating deterministic technical evidence from optional generated educational media.

## Verified completed evidence

- Dependency-ordered July 17-31 plan and lesson contracts.
- Legal fixture decision: model-free Lab 0 core, learner-provided optional inference, and project-owned synthetic GGUF.
- Deterministic 428-byte GGUF v3 generator, manifest, golden parse, checksum, alignment/range assertions, and corruption fixtures.
- Lab 0 six-phase report contract and semantic validator.
- Versioned executable-trace schema, authored GGUF-loading trace, replay/provenance validator, and malformed-input tests.
- Versioned local-only learner-progress schema and privacy-minimizing validator on the latest stacked branch.
- Initial literature map supporting intentionally unequal browser, local-native, and cloud-container tiers.

## Current contradictions and corrections

- README/project-state still list trace and progress schemas as unfinished even though stacked PRs implement them. They must be updated only after the stack is integrated and CI passes.
- The latest progress-schema branch did not append its result to `agent-handoffs.md`; the orchestrator records it here pending a dedicated ledger update.
- The sample trace is authored/source-derived, not native-captured. No documentation or UI may imply otherwise.
- A passing model-free Lab 0 report proves environment/build/executable launch only, not model load or inference.

## Venue state

As of 2026-07-17, no official EAAI-27 call was found. The official AAAI-27 main-conference page lists Montréal, February 16-23, 2027, with main-track abstract and paper deadlines on July 21 and July 28, 2026; these dates must **not** be assumed to apply to EAAI. The latest verified EAAI call is EAAI-26, whose Experience Report and Innovative Practice area required development and use context, collected data, prior-literature motivation, novelty, and rich reflection on what worked, what did not, and why. Reverify the official EAAI-27 call before any submission decision.

Official sources:

- https://aaai.org/conference/aaai/aaai-27/
- https://aaai.org/conference/aaai/aaai-26/eaai-26-call/

## Next 7 dependency-ordered actions

1. **Documentation Builder — CI repair:** inspect strict MkDocs failure for run `29543838455`; make the narrowest integration fix and obtain a passing final-head Documentation CI result.
2. **Documentation Builder — media contract:** add the media manifest/provenance schema and validator; deterministic technical figures remain authoritative and paid API calls remain manual/review-gated.
3. **Documentation Builder — viewer shell:** after trace contract review and passing CI, add a static, keyboard-operable viewer shell for the authored GGUF trace with forward/back controls, evidence labels, and transcript fallback.
4. **Validation Architect — source-link/replay validation:** validate trace source paths against the pinned revision and define browser performance, missing-data, and step-navigation acceptance tests.
5. **Validation Architect — reproducibility matrix:** define supported local/container environments, exact toolchain checks, time-to-ready instrumentation, and stable diagnostic codes for Lab 0.
6. **Literature and Venue Scout — media/provenance slice:** verify current official OpenAI, Gemini/Nano Banana, and NotebookLM capabilities and restrictions; produce design requirements, not promotional feature lists.
7. **Literature and Venue Scout — venue watch:** locate the official EAAI-27 call when published and update venue requirements without borrowing AAAI main-track dates.

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
