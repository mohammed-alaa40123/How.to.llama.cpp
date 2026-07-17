# EAAI research orchestrator state

_Last updated: 2026-07-17 17:58 Africa/Cairo_

This file is the single source of truth for EAAI experience-report preparation. It coordinates bounded repository work and does not authorize manuscript drafting.

## Executive status

**Phase:** Week 1 foundation transitioning to Week 2 vertical-slice evidence.

**Overall judgment:** the repository now contains a coherent, source-pinned prototype stack: legal synthetic GGUF fixtures, a browser GGUF slice, an authored/source-derived trace viewer, local-only progress portability, deterministic technical figures, media lifecycle validation, a Lab 0 evidence contract and a frozen information-equivalent benchmark. The adversarial review still recommends rejection in the current state because implementation contracts are ahead of measured educational, reproducibility and longitudinal evidence.

**Current stacked branch:** `agent/review02-adversarial-evidence-gates` at `4c72b8908c0d41941a7f61f2d041a2668a788af5`.

**Current CI state:** dependencies through MEDIA-02 have passing commit-scoped Documentation CI. REVIEW-02 remains in progress until its final head passes CI. CI validates integration and deterministic contracts; it does not establish learner benefit, native execution, independent correctness or cross-environment reproducibility.

## Frozen educational framing

### Target audience

Primary audience: advanced undergraduate and beginning graduate learners in systems, computer architecture or ML systems who can read C/C++ and Python but cannot yet connect GGUF storage, virtual memory, GGML graph construction, backend scheduling and token generation.

Secondary audience: early-stage researchers onboarding to llama.cpp/GGML internals. Claims about benefit to experienced maintainers require separate evidence.

### Educational problem

The environment teaches learners to distinguish:

- file format from executable graph;
- mapped bytes from resident physical pages;
- authored explanation from source-derived or native-captured runtime evidence;
- build success from model loading and inference;
- browser-derived format inspection from native llama.cpp behavior.

The claim that existing documentation broadly fails to make these distinctions remains a **hypothesis** pending a systematic audit.

### Initial learning experiences

1. **Lab 0 — Build and Run llama.cpp:** identify environment, configure, compile, executable-launch, model-load and inference stages; diagnose which stage owns a failure.
2. **Lab 1 — GGUF Anatomy:** predict, parse, inspect and explain a deterministic synthetic GGUF while preserving browser/native boundaries.
3. **Executable Lecture 0 — GGUF loading trace:** reconstruct a bounded source-pinned path using an authored/source-derived trace and a fair static-source/text baseline.

## Research questions

- **RQ1 — Educational artifact:** Does the integrated progression improve bounded setup diagnosis, GGUF reasoning and source-path reconstruction relative to fair baselines?
- **RQ2 — Evidence boundaries:** Can learners and reviewers correctly distinguish browser-derived, authored, source-derived and native-captured evidence?
- **RQ3 — Development workflow:** What work succeeds, fails, duplicates or requires human correction when scheduled specialist agents maintain an evolving systems-learning repository?
- **RQ4 — Reproducibility:** Which browser, local-native and cloud-container paths are reproducible, and what educational tradeoffs arise from their unequal capabilities?

These are planning questions, not answered claims.

## Defensible contributions under construction

1. A revision-pinned executable-learning progression for difficult AI-systems internals.
2. Machine-checkable contracts for fixtures, lab evidence, trace provenance/replay, local progress and media review.
3. A repository-native longitudinal case study of human-supervised scheduled agents, including failures, corrections, rejected work, costs and maintenance burden.
4. Design lessons about deterministic technical evidence, optional generated media and explicit browser/native boundaries.

The project must not be framed as a tool collection; DEMO-01 must show that the three experiences form one learning progression.

## Evidence status

### Evidenced contracts and bounded artifacts

- legal fixture boundary and deterministic 428-byte GGUF fixture;
- Lab 0 reproducibility/report contract and semantic validator;
- browser-first GGUF parser/visualizer with Predict-Discover-Explain checkpoints;
- versioned trace schema, immutable source anchors and deterministic replay;
- keyboard-operable authored/source-derived viewer with transcript fallback;
- local-only progress export/import, validation and Lab 1 resume-state integration;
- deterministic technical figure and media provenance/lifecycle validators;
- frozen information-equivalent static-versus-viewer benchmark contract;
- first three-record agent-workflow batch;
- adversarial claims-evidence, rejection-risk and scorecard package.

### Unevidenced central claims

- measured Ubuntu 24.04 and devcontainer Lab 0 reproducibility;
- integrated end-to-end demo on a clean supported environment;
- learner benefit or expert usefulness;
- independent llama.cpp/GGML correctness;
- native or faithfully captured trace provenance beyond authored/source-derived replay;
- longitudinal representativeness of agent-workflow evidence;
- generalization beyond llama.cpp;
- current EAAI-27 venue requirements.

## Reviewer disposition

**Current adversarial disposition:** reject in current state; promising artifact, insufficient experience-report evidence.

Fatal evidence gaps:

1. no approved and completed learner or expert-usefulness evaluation;
2. no independent technical correctness review;
3. no measured Ubuntu 24.04 or devcontainer Lab 0 execution;
4. no longitudinal agent dataset beyond the selected three-record sample.

## Venue state

As of 2026-07-17, no official EAAI-27 call has been verified. AAAI-27 main-conference dates must not be transferred to EAAI. EAAI-26 remains the latest verified experience-report call. Reverify only from official AAAI/EAAI sources before submission planning.

## Next 7 dependency-ordered actions

1. **Orchestrator + Documentation Builder — `STACK-01`:** produce a human-reviewable merge map for the stacked PR chain, identify superseded/overlapping progress branches and nominate one canonical integration path.
2. **Validation Architect — `LAB0-03`:** run and retain one measured model-free Ubuntu 24.04 local-native record when a suitable environment is available.
3. **Validation Architect — `LAB0-04`:** run the same bounded evidence contract in the devcontainer/Codespaces-compatible environment.
4. **Documentation Builder + Validation Architect — `DEMO-01A`:** define the integrated demo acceptance checklist and exact cross-experience learner path without claiming deployment success.
5. **Human technical reviewer — `REVIEW-01`:** review fixture, browser explanations, trace anchors, deterministic figure and benchmark answer key; record corrections.
6. **Validation Architect — `DATA-01B`:** freeze missing-value and coding rules, then extract a broader bounded retrospective sample with independent coding review.
7. **Human + Validation Architect — `EVAL-01`:** choose an expert-review or learner-evaluation pathway, determine ethics requirements and authorize no recruitment until approved.

`VENUE-01` monitoring continues independently and does not borrow AAAI main-track dates.

## Assignments by agent

- **Documentation Builder:** STACK-01 and DEMO-01A only; no broad content expansion.
- **Validation Architect:** LAB0-03, LAB0-04 and DATA-01B in dependency order; preserve failed runs and do not fabricate timings.
- **Literature and Venue Scout:** official VENUE-01 monitoring and systematic documentation-gap audit design.
- **Adversarial Reviewer:** review STACK-01/DEMO-01A for tool-collection framing, evidence inflation and unrealistic scope.
- **Paper Integrator:** disabled.

## Human-action blockers

- provide or approve access to clean Ubuntu 24.04 and devcontainer execution environments;
- nominate an independent llama.cpp/GGML reviewer;
- choose the canonical progress implementation and stacked-PR merge order;
- approve an evaluation pathway and any required ethics review;
- decide whether optional paid media credentials may ever be used; the core demo does not require them.

## Readiness judgment

**Coordination estimate:** 50% of pre-manuscript readiness.

This rises only for validated vertical-slice contracts, progress integration, benchmark freezing, media lifecycle evidence and explicit reviewer gates. It gives no credit for learner benefit, independent correctness, measured native/container reproducibility or official EAAI-27 requirements.

## Manuscript-writing gate

Do not activate the Paper Integrator until all conditions below have durable evidence:

- stable audience, learning progression, objectives and research questions;
- frozen workflow/autonomy/human-supervision description;
- one canonical integrated branch with passing CI and reproducible Lab 0, GGUF lab, viewer, progress and media vertical slice;
- broader audited retrospective dataset with assignments, failures, corrections, human labor, costs and accepted/rejected outputs;
- at least one completed fair baseline comparison;
- independent technical correctness review with correction records;
- approved and completed learner or expert evaluation pathway, with ethics approval when required;
- current official EAAI requirements;
- no unresolved fatal reviewer concern that invalidates the central contribution.
