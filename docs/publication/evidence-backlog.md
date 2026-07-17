# EAAI evidence backlog

_Last updated: 2026-07-17 17:58 Africa/Cairo_

This queue is dependency-aware. Close an item only with a durable artifact, validator, measured run or review record. Status values: `blocked`, `ready`, `in progress`, `evidenced`.

| Priority | ID | Status | Owner | Dependency | Required evidence | Claim supported or falsified |
|---|---|---|---|---|---|---|
| P0 | STACK-01 | ready | Orchestrator + Documentation Builder | current stacked PR chain | canonical merge map, superseded/overlap decisions, exact dependency order, CI state and human choices | The repository can become one reviewable artifact rather than an unmerged sequence of prototypes |
| P0 | REVIEW-02 | in progress | Adversarial Reviewer + Orchestrator | final-head CI | reviewer package plus authoritative-state integration and passing commit-scoped CI | Rejection risks drive work ordering rather than broad feature expansion |
| P0 | LAB0-03 | blocked | Validation Architect | clean Ubuntu 24.04 environment | measured model-free local-native record with exact revisions, commands, diagnostics and time-to-ready | The local-native tier completes the bounded path reproducibly |
| P0 | LAB0-04 | blocked | Validation Architect | devcontainer execution environment | measured model-free devcontainer record using the same contract | The cloud-container tier completes the bounded path reproducibly |
| P0 | REVIEW-01 | blocked | Human technical reviewer | reviewer nominated | signed/dated review and correction record for fixture, lab, trace, figure and benchmark | Technical correctness is independently supported |
| P1 | DEMO-01A | ready | Documentation Builder + Validation Architect | STACK-01; existing vertical slices | integrated-demo acceptance checklist and cross-experience learner path | The contribution is a coherent learning progression rather than a tool collection |
| P1 | DATA-01B | ready | Validation Architect | DATA-01 contract and first batch | frozen coding/missing-value rules, broader bounded sample and independent coding review | The agent process is analyzable as a longitudinal case study rather than selected anecdotes |
| P1 | EVAL-01 | blocked | Human + Validation Architect | pathway and ethics decision | approved expert or learner protocol, instruments, consent/ethics determination and recruitment boundary | Educational usefulness can be evaluated rather than inferred |
| P1 | BASE-01 | blocked | Validation Architect | EVAL-01; BASE-01A; REVIEW-01 | completed information-equivalent comparison with frozen scoring and limitations | Viewer benefit is measured rather than attributed to visual novelty |
| P1 | VENUE-01 | in progress | Literature Scout | official publication | verified EAAI-27 call, deadlines, area, format and review criteria | Submission planning matches the current venue |
| P2 | LAB0-02 | evidenced | Validation Architect | Lab 0 report contract | schema, validator, toolchain checks, diagnostic taxonomy, timing definitions and security boundaries; CI `29565651085` | Setup/build evidence has a comparable machine-readable contract |
| P2 | LAB1-01 | evidenced | Documentation Builder | deterministic fixture | browser parser/visualizer, golden agreement, checkpoints and static fallback; CI `29562479577` | Browser GGUF inspection is bounded and does not imply native inference |
| P2 | PROGRESS-02 | evidenced | Documentation Builder / Validation Architect | LAB1-01 | local export/import, version gate, corruption-preserving import and Lab 1 resume state; CI `29579032392` | Anonymous local progress is portable at the application-contract level |
| P2 | TRACE-02 | evidenced | Validation Architect | trace schema | immutable source anchors, authored trace, deterministic replay and malformed-input tests; CI `29556540213` | Trace provenance and replay are machine-checkable |
| P2 | VIEW-01 | evidenced | Documentation Builder | TRACE-02 | keyboard viewer, evidence labels, source links and transcript fallback; CI `29559239071` | A narrow authored/source-derived executable lecture can coordinate source, state and explanation |
| P2 | BASE-01A | evidenced | Validation Architect | VIEW-01 | information-equivalent fixture, tasks, answer key, scoring, timing and accessibility validator; CI `29583741909` | A fair comparison can avoid information-availability confounding |
| P2 | MEDIA-01 | evidenced | Documentation Builder | none | media schema, provenance validator and secret-safe optional-generation boundary; CI `29549208249` | Generated supplements can be review-gated without becoming technical evidence |
| P2 | FIG-01 | evidenced | Documentation Builder | MEDIA-01 | deterministic SVG, exact replay, checksums and alt text; CI `29553868078` | Authoritative technical figures need not depend on generative models |
| P2 | MEDIA-02 | evidenced | Validation Architect | MEDIA-01; FIG-01 | accepted/revised/rejected lifecycle, reasons, exact hashes and stale detection; CI `29587245436` | Media decisions are auditable without ordinary-CI regeneration |
| P2 | DATA-01 | evidenced | Validation Architect | stable log format | schema, validator and first three-archetype batch; CI `29572506104` | The retrospective contract represents success, repair and blocked reassignment |
| P3 | DEMO-01 | blocked | Orchestrator | STACK-01; LAB0-03; LAB0-04; DEMO-01A | clean integrated end-to-end execution and deployed or locally reproducible artifact | The system exists as one coherent educational experience |

## Current evidence boundaries

- Passing CI proves deterministic integration, not learning, native execution or independent correctness.
- The browser GGUF lab uses a synthetic teaching fixture and does not execute llama.cpp, `mmap`, GGML graph construction or inference.
- The viewer replays authored/source-derived evidence and is not yet a native capture.
- The Lab 0 contract is evidenced, but no measured Ubuntu or devcontainer row exists.
- The first retrospective batch demonstrates schema coverage, not representativeness or workflow superiority.
- Progress is local-only and anonymous; no server sync, identity or telemetry is approved.
- Deterministic technical figures are authoritative. Optional generated media remains supplemental, cached, review-gated and unnecessary for the core demo.

## Fatal rejection-risk mapping

1. **No usefulness evidence:** EVAL-01 and BASE-01.
2. **No independent correctness:** REVIEW-01 and retained correction records.
3. **No measured native/cloud reproducibility:** LAB0-03 and LAB0-04.
4. **Selected agent anecdotes:** DATA-01B and independent coding review.
5. **Tool collection rather than learning progression:** STACK-01, DEMO-01A and DEMO-01.

## Scope cuts retained

- no authenticated synchronization;
- no participant recruitment before approval;
- no paid media dependency for the core path;
- no full native instrumentation before bounded provenance and size review;
- no manuscript drafting before the explicit gate in `orchestrator-state.md`.
