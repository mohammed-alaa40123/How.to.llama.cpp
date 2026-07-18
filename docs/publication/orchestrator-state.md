# EAAI research orchestrator state

_Last updated: 2026-07-18 06:02 Africa/Cairo_

This file is the single source of truth for EAAI experience-report preparation. It coordinates bounded repository work and does not authorize manuscript drafting.

## Executive status

**Phase:** Week 1 foundation with two measured Lab 0 reproducibility rows completed ahead of Week 2.

**Overall judgment:** the project has a coherent executable-learning prototype, deterministic evidence contracts, a successful Ubuntu local-native Lab 0 row and a successful Codespaces-compatible devcontainer row. The decisive weaknesses are no canonical integrated branch, incomplete local progress import/export, no independently coded longitudinal repository dataset, no baseline comparison, no independent technical correctness review and no approved educational evaluation.

**Current evidence head:** `agent/lab0-04-devcontainer-repro` at `ab1db83938176dc4fd766cf66fccf18e5b0e2116`.

**Current CI:** Documentation CI `29626470196`, Lab 0 devcontainer reproducibility `29626470197`, and Lab 0 Ubuntu reproducibility `29626470190` passed for the implementation head.

## Frozen educational framing

### Target audience

Advanced undergraduate, graduate and early-stage systems researchers who can read C/C++ and Python but cannot yet connect GGUF storage, virtual memory, GGML graph construction, backend scheduling and token generation.

### Educational problem

The environment teaches learners to distinguish file format from runtime graph, mapped bytes from resident pages, authored explanation from captured evidence, build success from model loading/inference, and browser parsing from native llama.cpp execution. The claim that existing documentation broadly fails at this remains a hypothesis until the systematic audit is completed.

### Initial experiences

1. **Lab 0 — Build and Run llama.cpp:** attribute responsibilities to `uv`, CMake/Ninja, the compiler, llama.cpp and model assets; diagnose bounded failures.
2. **Lab 1 — GGUF Anatomy:** predict, parse, inspect and explain a deterministic synthetic GGUF without implying that GGUF stores an executable graph.
3. **Executable Lecture 0 — GGUF loading trace:** step through a source-pinned authored/source-derived path while distinguishing evidence kinds.

## Research questions

- **RQ1:** Can source-pinned executable labs and evidence-labelled traces improve code-tracing and systems explanations?
- **RQ2:** Can browser-derived, source-derived, authored and native-captured evidence be made understandable and machine-checkable?
- **RQ3:** What succeeds, fails and requires human correction when scheduled specialist agents maintain an educational resource in a persistent repository?
- **RQ4:** Which combination of browser, local-native and cloud-container execution provides access without obscuring runtime differences?

These remain planning questions, not answered claims.

## Defensible contributions under construction

1. A revision-pinned executable-learning environment for source-level AI-systems education.
2. Machine-checkable contracts for lab evidence, trace provenance/replay, local learner progress and media provenance.
3. A longitudinal case study of scheduled specialist agents operating with human supervision, deterministic tests and repository memory.
4. Design lessons separating deterministic technical evidence from optional generated educational media.

## Verified evidence

- Frozen learner and lesson contracts for Lab 0, Lab 1 and Executable Lecture 0.
- Legal fixture policy: model-free Lab 0 core, learner-provided optional models and project-owned synthetic GGUF.
- Deterministic GGUF fixture, parser agreement, figure and browser-first Predict-Discover-Explain slice.
- Versioned trace schema, immutable source anchors, deterministic replay and keyboard-operable viewer with transcript fallback.
- Local-only progress schema and privacy boundary.
- Media provenance schema and deterministic authoritative figure pipeline.
- Successful Ubuntu 24.04 local-native Lab 0 row: run `29622240261`, artifact `8422651113`, 326,905 ms model-free time to ready.
- Successful Ubuntu 24.04 devcontainer Lab 0 row: run `29626470197`, artifact `8424069914`, digest `sha256:2aaf62980561e141244b5552f4cd397cb7c9a4e1215b75c35a04fdc3ad7c3121`, 280,753 ms model-free time to ready.

## Claim boundaries

- Both Lab 0 rows establish locked setup, pinned bounded build and executable launch only; neither establishes model loading, inference or learner benefit.
- The devcontainer run does not establish Codespaces service reliability, offline use or image-digest reproducibility.
- The viewer remains authored/source-derived, not native-captured.
- Browser parsing is evidence about a synthetic fixture, not native execution.
- Passing CI establishes deterministic integration at each branch head, not educational effectiveness or canonical-stack integration.
- No participant data has been collected.

## Two-week milestone status

- **Week 1 contracts and architecture:** 94% — core contracts, fixtures, schemas and narrow vertical slices exist; systematic documentation audit and canonical reconciliation remain.
- **Week 1 smallest vertical slice:** 95% — Lab 0 runners, browser GGUF slice, trace viewer and deterministic figure exist with validation.
- **Week 2 Lab 0 evidence:** 75% — local-native and devcontainer model-free rows pass; inference, offline/degraded behavior and additional platform rows remain explicitly optional or unevidenced.
- **Week 2 coherent demo:** 52% — components exist in stacked branches, but progress import/export and canonical integration remain blocking.
- **Publication evidence package:** 45% — reproducibility improved, while learner/expert evaluation, baseline, independent review and longitudinal extraction remain absent.

## Readiness by category

| Category | Readiness | Status |
|---|---:|---|
| Educational framing | 70% | frozen but not independently reviewed |
| Executable-learning architecture | 72% | three tiers specified; two Lab 0 tiers measured |
| Lab 0 reproducibility | 68% | Ubuntu native and devcontainer model-free rows pass |
| GGUF browser lab | 62% | bounded slice validated; progress integration incomplete |
| Executable lecture | 64% | deterministic authored viewer; native capture and baseline absent |
| Progress/privacy | 48% | schema exists; export/import, migration and recovery pending |
| Media/provenance | 66% | deterministic core validated; lifecycle dry run incomplete |
| Agent-workflow evidence | 38% | logs exist; systematic extraction and coding pending |
| Baseline and evaluation | 15% | protocols not completed |
| Independent correctness | 20% | source pinning exists; external review absent |
| Venue readiness | 35% | requirements must remain freshly verified |

**Overall coordination readiness: 57%.** This is a conservative project-management signal, not a statistical result. The adversarial disposition remains reject in the current state.

## Next dependency-ordered actions

1. **Human + Orchestrator — `STACK-01`:** approve PR #24 as canonical progress base or record an alternative; reconcile one combined branch and run full CI.
2. **Validation Architect — `PROGRESS-02`:** implement export/import, migration, corruption recovery and storage-adapter tests.
3. **Validation Architect — `DATA-01`:** extract assignments, failures, corrections, validators, human effort and cost proxies into a reviewable dataset.
4. **Human — `REVIEW-01`:** nominate an independent llama.cpp/GGML reviewer.
5. **Literature Scout — `VENUE-01`:** verify current official EAAI requirements and retain primary-source evidence.
6. **Validation Architect — `BASE-01`:** freeze benchmark tasks after DATA-01 and compare simpler workflows against the full orchestration workflow.
7. **Human + Validation Architect — `EVAL-01`:** approve learner or expert evaluation and ethics pathway before collection.

## Human-action blockers

- Canonical progress implementation and merge order.
- Independent technical reviewer nomination.
- Evaluation and ethics pathway approval.
- Any optional paid-media credentials; deterministic work does not require them.

## Exact manuscript-writing condition

Do not activate the Paper Integrator until one canonical integrated branch passes full CI and the following are evidenced: stable framing and research questions; documented workflow and autonomy boundaries; reproducible lab/media/progress architecture; retrospective repository dataset; at least one fair baseline; independent technical correctness review; approved and completed learner or expert evaluation pathway where required; current official venue requirements; and no fatal reviewer concern that invalidates the central contribution.
