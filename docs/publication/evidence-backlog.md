# EAAI evidence backlog

_Last updated: 2026-07-17 15:00 Africa/Cairo_

This queue is dependency-aware. Close an item only with a durable artifact, validator or review record. Status values: `blocked`, `ready`, `in progress`, `evidenced`.

| Priority | ID | Status | Owner | Dependency | Required evidence | Claim supported or falsified |
|---|---|---|---|---|---|---|
| P0 | CI-01 | evidenced | Documentation Builder | latest stacked branch | strict MkDocs root cause, narrow fix, passing final-head Documentation CI run `29546570700` | The executable-learning artifacts integrate without degrading the existing site |
| P0 | COORD-01 | evidenced | Orchestrator | none | `orchestrator-state.md`, this backlog, roadmap, scorecard | Scheduled agents can share an explicit dependency order rather than infer work independently |
| P1 | LAB0-02 | in progress | Validation Architect | Lab 0 report contract | reproducibility schema, semantic validator, supported-environment matrix, exact toolchain checks, diagnostic taxonomy, timing definitions, offline/security boundaries; contract CI passed in run `29565651085`; real matrix runs pending | Setup/build evidence is comparable across supported environments |
| P1 | DATA-01 | in progress | Validation Architect | stable log formats | versioned retrospective schema, semantic validator, first three-run batch covering success, CI repair and blocked reassignment, focused tests and passing run `29572506104`; independent coding review and broader historical coverage pending | The multi-agent process can be analyzed as a longitudinal case study |
| P1 | MEDIA-01 | evidenced | Documentation Builder | CI-01 | schema, semantic validator, deterministic example, malformed-input tests, passing run `29549208249` | Generated educational media can be provenance- and review-gated without making it technical evidence |
| P1 | TRACE-02 | evidenced | Validation Architect | trace schema accepted; CI-01 | pinned source-anchor manifest and validator, corrected authored trace, deterministic replay and missing-data tests; passing run `29556540213` | Trace provenance and navigation remain valid against immutable source |
| P1 | FIG-01 | evidenced | Documentation Builder | MEDIA-01 | deterministic GGUF-layout SVG generated from fixture data plus recomputed manifest/input/output checksums and alt text; passing run `29553868078` | Authoritative technical figures are reproducible without generative models |
| P1 | VIEW-01 | evidenced | Documentation Builder | TRACE-02 | keyboard-operable static viewer, deterministic payload, evidence labels, transcript fallback, focused tests; passing run `29559239071` | A narrow executable lecture can expose source, state and explanation without evidence inflation |
| P1 | LIT-02 | evidenced | Literature Scout | none | official media/API capability matrix with provenance, privacy, accessibility, licensing, cost and caching implications | Optional media choices are evidence-based and reproducible enough for an experience report |
| P1 | VENUE-01 | in progress | Literature Scout | official publication | verified EAAI-27 call, deadlines, area, format, review criteria | Submission plan matches the current venue rather than prior-year assumptions |
| P2 | LAB1-01 | evidenced | Documentation Builder | progress contract; FIG-01; VIEW-01 | browser parser/visualizer, Python/golden agreement, Predict-Discover-Explain checkpoints, static fallback; passing run `29562479577` | Learners can inspect GGUF layout in-browser without confusing it with native inference |
| P2 | PROGRESS-02 | in progress | Validation Architect | progress schema; LAB1-01 | local adapter/export/import passed run `29575542793`; Lab 1 now stores anonymous resume state and exposes validated export/import; final-head integration CI and real-browser accessibility/storage checks pending | Local-first progress is portable and privacy-minimizing without treating step completion as mastery |
| P2 | REVIEW-02 | in progress | Adversarial Reviewer + Orchestrator | PR #8 integration | integrate reviewer notes, claims-evidence table, rejection risks and scorecard into the active stack | Major rejection risks are visible and drive dependency ordering |
| P2 | REVIEW-01 | blocked | Human | independent reviewer nominated | expert rubric and signed/dated review of fixture, trace, lab explanations and figure | Technical correctness is independently supported |
| P2 | BASE-01 | blocked | Validation Architect | DATA-01, frozen benchmark tasks | fair comparison protocol: single authoring agent; author+reviewer; full repository-memory/validator workflow | Specialized scheduled workflow provides measurable benefit over simpler workflows |
| P3 | EVAL-01 | blocked | Human + Validation Architect | evaluation pathway approval | learner or expert study protocol, instruments, consent/ethics decision | Educational usefulness is evaluated rather than inferred from implementation |
| P3 | DEMO-01 | blocked | Orchestrator | LAB0-02, LAB1-01, PROGRESS-02 | reproducible end-to-end Lab 0 + GGUF lab + viewer + figure + progress demo | The proposed system exists as a coherent educational artifact |

## Current PROGRESS-02 evidence boundary

The canonical local adapter has passing commit-scoped CI and is now connected to Lab 1. A successful parse stores only anonymous resume state: the lesson is `in-progress`, the last reached step is recorded, and all formative checkpoints remain `unanswered`. Export/import is local, versioned and validation-gated. This does not establish cross-browser persistence, checkpoint correctness, mastery, learner benefit, account sync or server-side storage. Final-head integration CI and real-browser accessibility/storage-denial checks remain required.

## Rejection-risk mapping

- **Only documentation generation:** require DEMO-01, DATA-01 and BASE-01.
- **No educational evidence:** require EVAL-01 and formative-assessment artifacts in Lab 0/Lab 1/viewer.
- **Incorrect technical content:** require REVIEW-01 and pinned source-link validation.
- **Visual novelty without learning value:** require a fair static-source/text baseline and code-tracing outcome measures.
- **Unreproducible AI media:** deterministic figures are authoritative; optional generated assets require MEDIA-01 and provider-specific review.
- **Unclear agent contribution:** retain assignments, failures, corrections, human decisions and costs through DATA-01.
- **Unrealistic two-week scope:** optional generated media, hosted synchronization and cloud polish remain cut before the core vertical slice.
