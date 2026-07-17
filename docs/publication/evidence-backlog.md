# EAAI evidence backlog

_Last updated: 2026-07-17 23:00 Africa/Cairo_

This queue is dependency-aware. Close an item only with a durable artifact, validator, measured run or review record. Status values: `blocked`, `ready`, `in progress`, `evidenced`.

| Priority | ID | Status | Owner | Dependency | Required evidence | Claim supported or falsified |
|---|---|---|---|---|---|---|
| P0 | STACK-01 | in progress | Human + Orchestrator | canonical progress choice | approved merge order, combined integration branch and passing full CI | The repository is one reviewable artifact rather than a stack of prototypes |
| P0 | LAB0-03 | blocked | Validation Architect | clean Ubuntu 24.04 environment | measured model-free local-native record with revisions, commands, diagnostics and time-to-ready | The local-native tier completes the bounded path reproducibly |
| P0 | LAB0-04 | blocked | Validation Architect | devcontainer execution environment | measured model-free devcontainer record using the same contract | The cloud-container tier completes the bounded path reproducibly |
| P0 | REVIEW-01 | blocked | Human technical reviewer | reviewer nominated | signed/dated review and correction record for fixture, lab, trace, figure and benchmark | Technical correctness is independently supported |
| P1 | DEMO-01A | evidenced | Documentation Builder + Validation Architect | STACK-01 map; vertical slices | integrated-demo acceptance contract and cross-experience learner route; CI `29598615326` | The intended contribution is a coherent progression rather than a tool menu |
| P1 | DEMO-01 | blocked | Orchestrator + Documentation Builder | completed STACK-01; LAB0-03; LAB0-04 | executed accepted route on one clean canonical head with static fallback | The system exists as one coherent educational experience |
| P1 | DATA-01B | in progress | Validation Architect | approved immutable window; independent coder | frozen protocol/schema/validator now pass CI `29598733410`; still require broader extraction, double-coding and adjudication | The agent process is a longitudinal case study rather than selected anecdotes |
| P1 | EVAL-01 | blocked | Human + Validation Architect | pathway and ethics decision | approved expert or learner protocol, instruments, consent/ethics determination and recruitment boundary | Educational usefulness can be evaluated rather than inferred |
| P1 | BASE-01 | blocked | Validation Architect | EVAL-01; BASE-01A; REVIEW-01 | completed information-equivalent comparison with frozen scoring and limitations | Viewer benefit is measured rather than attributed to visual novelty |
| P1 | BLIND-01 | in progress | Literature Scout + Orchestrator | official EAAI-27 call | plan, schema, semantic validator and non-ready example now exist; still require anonymous bundle, identity scan, final license/accessibility checks and human approvals | Submission materials comply without destroying evidence provenance |
| P1 | DOC-AUDIT-01 | in progress | Literature Scout | independent second coder and frozen result capture | predefined protocol/schema/validator/test fixture passed Documentation CI `29606172245`; still require retained search results, double-coding and adjudication | The source-level documentation-gap hypothesis is supported, revised, rejected or left inconclusive |
| P2 | VENUE-01 | evidenced | Literature Scout | official call | official EAAI-27 dates, area, format and review constraints in PR #31 | Submission planning matches the current venue |
| P2 | REVIEW-02 | evidenced | Adversarial Reviewer + Orchestrator | reviewer package | rejection-risk package and orchestration integration; CI-backed ancestors | Rejection risks drive ordering rather than feature expansion |
| P2 | LAB0-02 | evidenced | Validation Architect | Lab 0 report contract | schema, validator, toolchain checks, diagnostic taxonomy, timing and security; CI `29565651085` | Setup/build evidence has a comparable machine-readable contract |
| P2 | LAB1-01 | evidenced | Documentation Builder | deterministic fixture | browser parser/visualizer, golden agreement, checkpoints and static fallback; CI `29562479577` | Browser GGUF inspection is bounded and not native inference |
| P2 | PROGRESS-02 | evidenced | Documentation Builder / Validation Architect | LAB1-01 | local export/import, version gate, corruption-preserving import and Lab 1 resume state; CI `29579032392` | Anonymous local progress is portable at the application-contract level |
| P2 | TRACE-02 | evidenced | Validation Architect | trace schema | immutable source anchors, authored trace, deterministic replay and malformed-input tests; CI `29556540213` | Trace provenance and replay are machine-checkable |
| P2 | VIEW-01 | evidenced | Documentation Builder | TRACE-02 | keyboard viewer, evidence labels, source links and transcript fallback; CI `29559239071` | A narrow authored/source-derived lecture can coordinate source, state and explanation |
| P2 | BASE-01A | evidenced | Validation Architect | VIEW-01 | information-equivalent fixture, tasks, answer key, scoring, timing and accessibility; CI `29583741909` | A fair comparison can avoid information-availability confounding |
| P2 | MEDIA-01 | evidenced | Documentation Builder | none | media schema, provenance validator and secret-safe optional-generation boundary; CI `29549208249` | Generated supplements can be review-gated without becoming technical evidence |
| P2 | FIG-01 | evidenced | Documentation Builder | MEDIA-01 | deterministic SVG, exact replay, checksums and alt text; CI `29553868078` | Authoritative technical figures need not depend on generative models |
| P2 | MEDIA-02 | evidenced | Validation Architect | MEDIA-01; FIG-01 | accepted/revised/rejected lifecycle, reasons, hashes and stale detection; CI `29587245436` | Media decisions are auditable without ordinary-CI regeneration |
| P2 | DATA-01 | evidenced | Validation Architect | stable log format | schema, validator, first three-archetype batch and explicit missing-data boundary; CI `29572506104` | The retrospective contract represents success, repair and blocked reassignment |

## Dependency decisions

- `STACK-01` remains implementation-critical and human-blocked; no new broad learner-facing feature should precede the canonical branch.
- `DOC-AUDIT-01` was the authorized dependency-safe task. Its protocol now has commit-scoped CI evidence, but the audit result remains open until retained search results, two independent coders and adjudication exist.
- `DEMO-01A` is closed only as a specification. `DEMO-01` remains blocked until the route is executed on the canonical branch and measured tiers exist.
- `VENUE-01` is closed because the official EAAI-27 call was verified. Venue monitoring continues only for author-kit changes.
- `DATA-01B` protocol evidence is complete, but the case-study dataset is not. A protocol must not be reported as a longitudinal result.
- `BLIND-01` has a machine-checkable non-ready contract. It remains open until a clean anonymous bundle passes identity, licensing, accessibility and human-review gates.

## Current evidence boundaries

- Passing CI proves deterministic integration, not learning, native execution or independent correctness.
- The browser GGUF lab uses a synthetic teaching fixture and does not execute llama.cpp, `mmap`, GGML graph construction or inference.
- The viewer replays authored/source-derived evidence and is not a native capture.
- The Lab 0 contract is evidenced, but no measured Ubuntu or devcontainer row exists.
- The first retrospective batch and coding protocol do not establish representativeness, inter-rater reliability or workflow superiority.
- The documentation-gap statement remains an Open Question until `DOC-AUDIT-01` completes; passing protocol CI cannot support novelty.
- Progress is local-only and anonymous; no server sync, identity or telemetry is approved.
- Deterministic technical figures are authoritative. Optional generated media remains supplemental and outside the critical path.
- The live repository is not a double-blind artifact; public review materials require a clean allowlisted export and private source crosswalk.

## Fatal rejection-risk mapping

1. **No usefulness evidence:** `EVAL-01` and `BASE-01`.
2. **No independent correctness:** `REVIEW-01` and retained corrections.
3. **No measured native/cloud reproducibility:** `LAB0-03` and `LAB0-04`.
4. **Selected agent anecdotes:** `DATA-01B` extraction, double-coding and adjudication.
5. **Tool collection rather than progression:** `STACK-01`, `DEMO-01A` and executed `DEMO-01`.
6. **Double-blind evidence leakage:** complete `BLIND-01` with a scanned, reviewed anonymous bundle.
7. **Unsupported novelty claim:** complete `DOC-AUDIT-01` or retain the documentation gap as inconclusive.

## Scope cuts retained

- no authenticated synchronization;
- no participant recruitment before approval;
- no paid media dependency for the core path;
- no full native instrumentation before bounded provenance and size review;
- no manuscript drafting before the explicit gate in `orchestrator-state.md`.
