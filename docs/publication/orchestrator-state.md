# EAAI research orchestrator state

_Last updated: 2026-07-18 00:01 Africa/Cairo_

This file is the single source of truth for EAAI experience-report preparation. It coordinates bounded repository work and does not authorize manuscript drafting.

## Executive status

**Phase:** Week 1 foundation is substantially complete; the critical path is canonical integration, measured reproducibility and independently reviewed evidence.

**Overall judgment:** the repository contains a coherent set of source-pinned, deterministic vertical-slice components and rigorous evidence contracts. The prospective experience report remains rejectable because those components are still distributed across stacked draft PRs, local/cloud Lab 0 reproducibility is unmeasured, independent technical correctness and evaluation pathways are absent, and the longitudinal agent dataset has not been broadly extracted or independently coded.

**Current coordination base:** `agent/doc-audit01-ci-attestation` at `b2a39213615e39852cbfd90f23296a493c8e63a2`. The predecessor documentation-audit protocol passed Documentation CI run `29606172245`; final-head CI for this reconciliation is required.

**Stack state:** `STACK-01` has a canonical merge map, but the human choice between overlapping progress implementations is still unresolved. `DEMO-01A`, `BLIND-01` and `DOC-AUDIT-01` now have bounded contracts; none of those contracts substitutes for an executed integrated demo, anonymous release artifact or completed systematic audit.

## Frozen educational framing

### Target audience

Primary audience: advanced undergraduate and beginning graduate learners in systems, computer architecture or ML systems who can read C/C++ and Python but cannot yet connect GGUF storage, virtual memory, GGML graph construction, backend scheduling and token generation.

Secondary audience: early-stage researchers onboarding to llama.cpp/GGML internals. Benefit to experienced maintainers remains unevidenced.

### Educational problem

The environment teaches learners to distinguish:

- file format from executable graph;
- mapped bytes from resident physical pages;
- authored explanation from source-derived or native-captured runtime evidence;
- build success from model loading and inference;
- browser-derived format inspection from native llama.cpp behavior.

The claim that existing documentation broadly fails to make these distinctions remains an **Open Question** pending execution of the predefined documentation audit.

### Initial learning experiences

1. **Lab 0 — Build and Run llama.cpp:** identify environment, configure, compile, executable-launch, model-load and inference stages; diagnose which stage owns a failure.
2. **Lab 1 — GGUF Anatomy:** predict, parse, inspect and explain a deterministic synthetic GGUF while preserving browser/native boundaries.
3. **Executable Lecture 0 — GGUF loading trace:** reconstruct a bounded source-pinned path using authored/source-derived evidence and a fair static-source/text baseline.

`DEMO-01A` freezes one learner route joining these experiences, local progress portability and evidence-kind synthesis. It is an acceptance specification, not evidence that the route has been executed end to end.

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

The project must not be framed as a tool collection. `DEMO-01` must execute the accepted route on one canonical branch.

## Evidence status

### Evidenced contracts and bounded artifacts

- legal deterministic synthetic GGUF fixture and licensing boundary;
- Lab 0 reproducibility/report contract and semantic validator;
- browser-first GGUF parser/visualizer with Predict-Discover-Explain checkpoints;
- versioned trace schema, immutable source anchors and deterministic replay;
- keyboard-operable authored/source-derived viewer with transcript fallback;
- local-only progress export/import and Lab 1 resume-state integration;
- deterministic figure and media provenance/lifecycle validators;
- frozen information-equivalent static-versus-viewer benchmark contract;
- three-record agent-workflow batch, explicit missing-data rules and frozen DATA-01B coding protocol;
- adversarial claims-evidence, rejection-risk and scorecard package;
- canonical integration map and integrated-demo acceptance specification;
- official EAAI-27 call verification;
- machine-checkable double-blind release contract with a deliberately non-ready example;
- predefined documentation-gap audit protocol with commit-scoped CI evidence.

### Unevidenced central claims

- one canonical integrated branch with end-to-end passing CI;
- measured Ubuntu 24.04 and devcontainer Lab 0 reproducibility;
- learner benefit or expert usefulness;
- independent llama.cpp/GGML correctness;
- native or faithfully captured trace provenance beyond authored/source-derived replay;
- longitudinal representativeness, inter-rater agreement and adjudicated agent-workflow evidence;
- a supported ecosystem-wide documentation gap;
- a reviewed anonymous submission artifact;
- generalization beyond llama.cpp.

## Reviewer disposition

**Current adversarial disposition:** reject in current state; promising artifact, insufficient experience-report evidence.

Fatal evidence gaps:

1. no approved and completed learner or expert-usefulness evaluation;
2. no independent technical correctness review;
3. no measured Ubuntu 24.04 or devcontainer Lab 0 execution;
4. no broader independently coded longitudinal agent dataset;
5. no canonical integrated end-to-end demo.

Submission-critical but not yet fatal-to-concept gaps: no completed fair baseline, no reviewed anonymous artifact and no completed documentation audit.

## Venue state

`VENUE-01` verified the official EAAI-27 call on 2026-07-17. Planning uses:

- likely category: Main Track, Area 2 — Experience Report and Innovative Practice;
- abstract deadline: September 1, 2026, 11:59 PM UTC-12;
- paper deadline: September 8, 2026, 11:59 PM UTC-12;
- notification: November 17, 2026;
- camera ready: December 14, 2026;
- symposium: February 21-23, 2027 in Montréal;
- double-blind review and seven pages plus two reference pages.

The experience-report requirement for context of use, collected data and substantive reflection means validators and implementation artifacts alone are insufficient. AAAI-27 main-track July deadlines do not apply to EAAI.

## Next 7 dependency-ordered actions

1. **Human + Orchestrator — `STACK-01`:** approve PR #24 as the lowest-risk canonical progress base or explicitly choose an alternative; then reconcile the mapped stack into one combined branch and run the complete Documentation CI suite.
2. **Validation Architect — `LAB0-03`:** retain one measured model-free Ubuntu 24.04 record when a suitable environment is available.
3. **Validation Architect — `LAB0-04`:** run the same bounded evidence contract in the devcontainer/Codespaces-compatible environment.
4. **Orchestrator + Documentation Builder — `DEMO-01`:** execute the frozen `DEMO-01A` route on the canonical branch, including save/export/clear/import/resume and a no-JavaScript/static route.
5. **Human technical reviewer — `REVIEW-01`:** review fixture, browser explanations, trace anchors, deterministic figure and benchmark answer key; retain corrections.
6. **Validation Architect — `DATA-01B`:** approve an immutable study window, extract every eligible durable run, obtain independent double-coding and adjudicate disagreements.
7. **Human + Validation Architect — `EVAL-01`:** approve an expert-review or learner-evaluation pathway and ethics determination before recruitment or personal-data collection.

Parallel maintenance only: materialize `BLIND-01` after canonical integration, and execute `DOC-AUDIT-01` only with an independent second coder. Neither should displace the P0 integration and reproducibility path.

## Assignments by agent

- **Documentation Builder:** support `STACK-01` reconciliation and `DEMO-01`; no broad content expansion.
- **Validation Architect:** `LAB0-03`, `LAB0-04`, then `DATA-01B`; preserve failed runs and never fabricate timings.
- **Literature and Venue Scout:** retain the official venue record, recruit an independent documentation-audit coder and monitor only material author-kit changes.
- **Adversarial Reviewer:** review the canonical integration branch and executed demo for evidence inflation, tool-collection framing and browser/native confusion.
- **Paper Integrator:** disabled.

## Human-action blockers

- approve the canonical progress implementation and stacked-PR merge order;
- provide or approve clean Ubuntu 24.04 and devcontainer execution environments;
- nominate an independent llama.cpp/GGML reviewer;
- approve an evaluation pathway and any required ethics review;
- approve the retrospective study revision/window and independent coder;
- nominate an independent documentation-audit coder;
- approve the eventual anonymized artifact after identity, licensing, accessibility and technical checks;
- decide whether optional paid media credentials may ever be used; the core demo does not require them.

## Readiness judgment

**Coordination estimate:** 55% of pre-manuscript readiness.

The one-point increase credits validated `BLIND-01` and `DOC-AUDIT-01` contracts and removal of stale venue uncertainty from the execution plan. It gives no credit for measured educational benefit, independent correctness, measured native/container reproducibility, a combined branch, completed retrospective extraction, an anonymous artifact or completed audit.

## Manuscript-writing gate

Do not activate the Paper Integrator until all conditions below have durable evidence:

- stable audience, learning progression, objectives and research questions;
- frozen workflow/autonomy/human-supervision description;
- one canonical integrated branch with passing CI and reproducible Lab 0, GGUF lab, viewer, progress and media vertical slice;
- broader audited retrospective dataset with assignments, failures, corrections, human labor, costs and accepted/rejected outputs;
- at least one completed fair baseline comparison;
- independent technical correctness review with correction records;
- approved and completed learner or expert evaluation pathway, with ethics approval when required;
- current official EAAI requirements and a reviewed double-blind release artifact;
- no unresolved fatal reviewer concern that invalidates the central contribution.
