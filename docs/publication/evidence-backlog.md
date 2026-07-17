# EAAI evidence backlog

_Last updated: 2026-07-17 06:01 Africa/Cairo_

This queue is dependency-aware. Close an item only with a durable artifact, validator or review record. Status values: `blocked`, `ready`, `in progress`, `evidenced`.

| Priority | ID | Status | Owner | Dependency | Required evidence | Claim supported or falsified |
|---|---|---|---|---|---|---|
| P0 | CI-01 | evidenced | Documentation Builder | latest stacked branch | strict MkDocs root cause, narrow fix, passing final-head Documentation CI run `29546570700` | The executable-learning artifacts integrate without degrading the existing site |
| P0 | COORD-01 | evidenced | Orchestrator | none | `orchestrator-state.md`, this backlog, roadmap, scorecard | Scheduled agents can share an explicit dependency order rather than infer work independently |
| P1 | MEDIA-01 | evidenced | Documentation Builder | CI-01 | schema, semantic validator, deterministic example, malformed-input tests, passing run `29549208249` | Generated educational media can be provenance- and review-gated without making it technical evidence |
| P1 | TRACE-02 | ready | Validation Architect | trace schema accepted; CI-01 | pinned source-link resolver, deterministic replay tests, missing-field tests, 500-step/2 MiB browser bound | Trace provenance and navigation remain valid against immutable source |
| P1 | LAB0-02 | ready | Validation Architect | Lab 0 report contract | reproducibility matrix, toolchain checks, diagnostic taxonomy, time-to-ready protocol | Setup/build evidence is comparable across supported environments |
| P1 | FIG-01 | ready | Documentation Builder | MEDIA-01 | deterministic GGUF-layout SVG generated from fixture data plus recomputed manifest/input/output checksums and alt text | Authoritative technical figures are reproducible without generative models |
| P1 | DATA-01 | ready | Validation Architect | stable log formats | retrospective extraction schema for assignments, commits, failures, corrections, tests, cost proxies and accepted/rejected outputs | The multi-agent process can be analyzed as a longitudinal case study |
| P1 | LIT-02 | ready | Literature Scout | none | official media/API capability matrix with provenance, privacy, accessibility, licensing, cost and caching implications | Optional media choices are evidence-based and reproducible enough for an experience report |
| P1 | VENUE-01 | in progress | Literature Scout | official publication | verified EAAI-27 call, deadlines, area, format, review criteria | Submission plan matches the current venue rather than prior-year assumptions |
| P2 | VIEW-01 | blocked | Documentation Builder | TRACE-02 | keyboard-operable viewer shell, step forward/back, evidence labels, transcript/static fallback | A narrow executable lecture can expose source, state and explanation without evidence inflation |
| P2 | LAB1-01 | blocked | Documentation Builder | progress contract integrated; FIG-01 | browser parser/visualizer, Python/golden agreement, Predict-Discover-Explain checkpoints, static fallback | Learners can inspect GGUF layout in-browser without confusing it with native inference |
| P2 | PROGRESS-02 | blocked | Validation Architect | progress schema integrated | import/export round trip, migration, corruption recovery, local storage adapter tests | Local-first progress is portable and privacy-minimizing |
| P2 | REVIEW-02 | in progress | Adversarial Reviewer + Orchestrator | PR #8 integration | integrate reviewer notes, claims-evidence table, rejection risks and scorecard into the active stack | Major rejection risks are visible and drive dependency ordering |
| P2 | REVIEW-01 | blocked | Human | independent reviewer nominated | expert rubric and signed/dated review of fixture, trace, lab explanations and figure | Technical correctness is independently supported |
| P2 | BASE-01 | blocked | Validation Architect | DATA-01, frozen benchmark tasks | fair comparison protocol: single authoring agent; author+reviewer; full repository-memory/validator workflow | Specialized scheduled workflow provides measurable benefit over simpler workflows |
| P3 | EVAL-01 | blocked | Human + Validation Architect | evaluation pathway approval | learner or expert study protocol, instruments, consent/ethics decision | Educational usefulness is evaluated rather than inferred from implementation |
| P3 | DEMO-01 | blocked | Orchestrator | TRACE-02 through PROGRESS-02 | reproducible end-to-end Lab 0 + GGUF lab + viewer + figure + progress demo | The proposed system exists as a coherent educational artifact |

## Closed evidence from the current stack

- Legal fixture policy and deterministic synthetic GGUF package.
- Lab 0 six-phase report schema and semantic checks.
- Executable-trace schema, authored GGUF trace and provenance/replay constraints.
- Local-only learner-progress schema and privacy constraints.
- Initial browser/local/cloud platform literature map.
- Strict MkDocs handoff-link repair with passing commit-scoped CI.
- Media manifest/provenance schema, semantic validator and passing commit-scoped CI.

## Rejection-risk mapping

- **Only documentation generation:** require DEMO-01, DATA-01 and BASE-01.
- **No educational evidence:** require EVAL-01 and formative-assessment artifacts in Lab 0/Lab 1/viewer.
- **Incorrect technical content:** require REVIEW-01 and pinned source-link validation.
- **Visual novelty without learning value:** viewer and media work must state measurable code-tracing or misconception outcomes.
- **Unreproducible AI media:** deterministic figures are authoritative; optional generated assets require MEDIA-01 and provider-specific review.
- **Unclear agent contribution:** retain assignments, failures, corrections, human decisions and costs through DATA-01.
- **Unrealistic two-week scope:** optional generated media, hosted synchronization and cloud polish are explicitly cut before the core vertical slice.
