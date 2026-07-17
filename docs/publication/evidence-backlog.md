# EAAI evidence backlog

_Last updated: 2026-07-17 15:00 Africa/Cairo_

This queue is dependency-aware. Close an item only with a durable artifact, validator or review record. Status values: `blocked`, `ready`, `in progress`, `evidenced`.

| Priority | ID | Status | Owner | Dependency | Required evidence | Claim supported or falsified |
|---|---|---|---|---|---|---|
| P0 | CI-01 | evidenced | Documentation Builder | latest evidenced stack | strict MkDocs root cause, narrow fixes and passing commit-scoped CI for integrated artifacts | The executable-learning artifacts integrate without degrading the existing site |
| P0 | COORD-01 | evidenced | Orchestrator | none | authoritative state, dependency-aware queue, roadmap, scorecard and run handoffs | Scheduled agents can share an explicit dependency order rather than infer work independently |
| P1 | LAB0-02 | evidenced | Validation Architect | Lab 0 report contract | reproducibility schema, semantic validator, exact toolchain checks, diagnostic taxonomy, timing definitions and security boundaries; contract CI passed in run `29565651085` | Setup/build evidence has a comparable machine-readable contract |
| P1 | LAB0-03 | blocked | Validation Architect | network-capable Ubuntu 24.04 environment | measured model-free local-native record with exact revisions, tools, commands, diagnostics and time-to-ready | The local-native tier can complete the bounded path reproducibly |
| P1 | LAB0-04 | blocked | Validation Architect | devcontainer execution environment | measured model-free devcontainer record using the same contract fields | The cloud-container tier can complete the bounded path reproducibly |
| P1 | DATA-01 | in progress | Validation Architect | stable log formats | schema, semantic validator and first three-run batch with passing run `29572506104`; independent coding review and broader bounded extraction pending | The multi-agent process can be analyzed as a longitudinal case study |
| P1 | MEDIA-01 | evidenced | Documentation Builder | CI-01 | schema, semantic validator, deterministic example, malformed-input tests and passing run `29549208249` | Generated educational media can be provenance- and review-gated without making it technical evidence |
| P1 | TRACE-02 | evidenced | Validation Architect | trace schema accepted; CI-01 | pinned source-anchor manifest, corrected authored trace, deterministic replay and missing-data tests; passing run `29556540213` | Trace provenance and navigation remain valid against immutable source |
| P1 | FIG-01 | evidenced | Documentation Builder | MEDIA-01 | deterministic GGUF-layout SVG, manifest checksums, alt text and passing run `29553868078` | Authoritative technical figures are reproducible without generative models |
| P1 | VIEW-01 | evidenced | Documentation Builder | TRACE-02 | keyboard-operable static viewer, deterministic payload, evidence labels, transcript fallback and passing run `29559239071` | A narrow executable lecture can expose source, state and explanation without evidence inflation |
| P1 | LIT-02 | evidenced | Literature Scout | none | official media/API capability matrix with provenance, privacy, accessibility, licensing, cost and caching implications | Optional media choices are evidence-based and reviewable |
| P1 | VENUE-01 | in progress | Literature Scout | official publication | verified EAAI-27 call, deadlines, area, format and review criteria | Submission planning matches the current venue rather than prior-year assumptions |
| P2 | LAB1-01 | evidenced | Documentation Builder | FIG-01; VIEW-01 | browser parser/visualizer, Python/golden agreement, Predict-Discover-Explain checkpoints, static fallback and passing run `29562479577` | Learners can inspect GGUF layout in-browser without confusing it with native inference |
| P2 | PROGRESS-02 | in progress | Documentation Builder / Validation Architect | progress schema; DATA-01 parent stack | local storage adapter, deterministic export/import, version gate, corruption-preserving import, privacy checks and focused tests; final-head CI pending | Local-first progress is portable and privacy-minimizing at the application-contract level |
| P2 | PROGRESS-03 | blocked | Documentation Builder | PROGRESS-02 passing final-head CI | one Lab 1 checkpoint save/export/clear/import/resume round trip plus keyboard/static fallback tests | Progress portability works in the actual browser-learning vertical slice |
| P2 | BASE-01A | ready | Validation Architect | information-equivalent baseline design; stable VIEW-01 fixture | versioned static-versus-viewer benchmark fixture, exact tasks, answer key, scoring, timeout, source revision and accessibility fallbacks | The viewer can be evaluated without confounding information availability |
| P2 | REVIEW-02 | in progress | Adversarial Reviewer + Orchestrator | active stack | consolidated claims-evidence table, rejection risks and evidence gates | Major rejection risks are visible and drive dependency ordering |
| P2 | REVIEW-01 | blocked | Human | independent reviewer nominated | signed/dated expert review of fixture, trace, lab explanations, browser parser and figure | Technical correctness is independently supported |
| P2 | MEDIA-02 | ready | Validation Architect | MEDIA-01; FIG-01 | deterministic accepted/revised/rejected dry run and stale-asset test; no paid API call required | The media lifecycle is auditable without ordinary CI regeneration |
| P3 | BASE-01 | blocked | Validation Architect | DATA-01 review; BASE-01A frozen | completed comparison using the frozen information-equivalent benchmark and approved pathway | Viewer or workflow benefits are measured rather than inferred |
| P3 | EVAL-01 | blocked | Human + Validation Architect | evaluation pathway approval | learner or expert study protocol, instruments, consent/ethics decision and approved recruitment path | Educational usefulness is evaluated rather than inferred from implementation |
| P3 | DEMO-01 | blocked | Orchestrator | LAB0-03, LAB0-04, PROGRESS-03, MEDIA-02 | reproducible end-to-end Lab 0 + GGUF lab + viewer + figure + progress demo | The proposed system exists as a coherent educational artifact |

## Current evidence boundaries

### PROGRESS-02

The current stack provides a framework-free local storage contract for deterministic JSON export, bounded import, explicit schema-version handling, local save/load/clear and validation-before-mutation recovery. It does not yet connect Lab 1, prove cross-browser behavior, provide account/cloud synchronization, collect telemetry or establish that saved completion represents mastery.

### DATA-01

The first bounded retrospective batch contains one clean success, one CI repair retaining strict validation, and one blocked higher-priority task followed by dependency-safe reassignment. This shows representational coverage only. Independent coding review, missing-value rules and broader extraction remain required.

### LAB0

The comparison contract is evidenced, but no measured Ubuntu or devcontainer record exists. Model-free launch must never be labelled model loading or inference. macOS and WSL2 remain future matrix rows rather than Week 2 blockers.

### Viewer and baseline

The viewer is authored/source-derived and consumes a deterministic validated payload. It does not establish native capture, independent technical correctness or educational benefit. BASE-01A must expose identical evidence and questions in both conditions; only navigation, coordinated highlighting and deterministic visualization may differ.

## Rejection-risk mapping

- **Only documentation generation:** require DEMO-01, reviewed DATA-01 and BASE-01.
- **No educational evidence:** require EVAL-01 and frozen formative-assessment artifacts.
- **Incorrect technical content:** require REVIEW-01 and pinned source-link validation.
- **Visual novelty without learning value:** require BASE-01A and a completed fair comparison.
- **Unreproducible AI media:** deterministic figures remain authoritative; optional generated assets require manifest review and MEDIA-02 lifecycle evidence.
- **Unclear agent contribution:** retain assignments, failures, corrections, human decisions and cost proxies through DATA-01.
- **Unrealistic scope:** paid media, authenticated synchronization, full native instrumentation and cloud polish remain cut before the core demo.
