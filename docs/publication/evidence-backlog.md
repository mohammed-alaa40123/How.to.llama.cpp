# EAAI evidence backlog

_Last updated: 2026-07-18 06:02 Africa/Cairo_

This queue is dependency-aware. Close an item only with a durable artifact, validator or review record. Status values: `blocked`, `ready`, `in progress`, `evidenced`.

| Priority | ID | Status | Owner | Dependency | Required evidence | Claim supported or falsified |
|---|---|---|---|---|---|---|
| P0 | STACK-01 | blocked | Orchestrator + Human | canonical progress choice | approved canonical-progress record, reconciled integration branch and full combined-head CI | The evidence package exists as one reviewable artifact rather than parallel drafts |
| P0 | COORD-01 | evidenced | Orchestrator | none | authoritative orchestrator state, backlog, roadmap, scorecard and handoff ledger | Scheduled agents share an explicit dependency order |
| P1 | LAB0-02 | in progress | Validation Architect | Lab 0 report contract | reproducibility schema, semantic validator, supported-environment matrix, diagnostics, timing definitions, offline/security boundaries; additional operating-system rows pending | Setup/build evidence is comparable across environments |
| P1 | LAB0-03 | evidenced | Validation Architect | LAB0-02 | Ubuntu 24.04 model-free report; run `29622240261`; artifact `8422651113`; Documentation CI `29622240365` | One clean local-native environment completes locked setup, pinned build and executable launch |
| P1 | LAB0-04 | evidenced | Validation Architect | LAB0-03; devcontainer definition | devcontainer run `29626470197`; artifact `8424069914`; report digest `sha256:2aaf62980561e141244b5552f4cd397cb7c9a4e1215b75c35a04fdc3ad7c3121`; Documentation CI `29626470196` | One Codespaces-compatible cloud-container environment reproduces the bounded model-free setup/build/launch path |
| P1 | DATA-01 | ready | Validation Architect | stable log formats | retrospective extraction schema for assignments, commits, failures, corrections, tests, cost proxies and accepted/rejected outputs | The multi-agent process can be analyzed longitudinally |
| P1 | MEDIA-01 | evidenced | Documentation Builder | CI-01 | schema, validator, deterministic example, malformed-input tests | Generated educational media can be provenance- and review-gated without becoming technical evidence |
| P1 | TRACE-02 | evidenced | Validation Architect | trace schema accepted | pinned source anchors, validator, corrected authored trace, deterministic replay and missing-data tests | Trace provenance and navigation remain valid against immutable source |
| P1 | FIG-01 | evidenced | Documentation Builder | MEDIA-01 | deterministic GGUF-layout SVG, checksums and alt text | Authoritative technical figures are reproducible without generative models |
| P1 | VIEW-01 | evidenced | Documentation Builder | TRACE-02 | keyboard-operable static viewer, evidence labels and transcript fallback | A narrow executable lecture can expose source, state and explanation without evidence inflation |
| P1 | VENUE-01 | in progress | Literature Scout | official publication | verified current EAAI call, deadlines, area, format and review criteria | Submission planning matches the current venue |
| P2 | LAB1-01 | evidenced | Documentation Builder | progress contract; FIG-01; VIEW-01 | browser parser/visualizer, Python/golden agreement, Predict-Discover-Explain checkpoints and static fallback | Learners can inspect GGUF layout in-browser without confusing it with native inference |
| P2 | PROGRESS-02 | ready | Validation Architect | progress schema | import/export round trip, migration, corruption recovery and local storage tests | Local-first progress is portable and privacy-minimizing |
| P2 | REVIEW-02 | in progress | Adversarial Reviewer + Orchestrator | canonical integration | integrate reviewer package into the canonical stack | Major rejection risks drive dependency ordering |
| P2 | REVIEW-01 | blocked | Human | independent reviewer nominated | signed/dated review of fixture, trace, labs and deterministic figures | Technical correctness is independently supported |
| P2 | BASE-01 | blocked | Validation Architect | DATA-01; frozen benchmark tasks | fair comparison of simpler and full repository-memory/validator workflows | The scheduled multi-agent workflow provides measurable benefit |
| P3 | EVAL-01 | blocked | Human + Validation Architect | evaluation pathway approval | approved learner or expert protocol, instruments and ethics decision | Educational usefulness is measured rather than inferred |
| P3 | DEMO-01 | blocked | Orchestrator | STACK-01; PROGRESS-02 | canonical end-to-end Lab 0 + GGUF lab + viewer + figure + progress demo | The system exists as one coherent educational artifact |

## Newly verified LAB0-04 evidence

Workflow run `29626470197` completed successfully on the repository Development Container. The retained report records Ubuntu 24.04/x86_64, `uv 0.8.0`, Python 3.12.3, CMake 3.28.3, Ninja 1.11.1 and GCC 13.3.0. It executed `uv sync --locked`, checked out llama.cpp revision `e3546c7948e3af463d0b401e6421d5a4c2faf565`, configured with Ninja and `GGML_NATIVE=OFF`, built only `llama-cli`, and launched `llama-cli --help`. Setup, build and launch succeeded with no diagnostics; model use and inference were not attempted. Model-free time to ready was 280,753 ms.

This evidence supports one devcontainer/Codespaces-compatible matrix row only. It does not establish Codespaces service availability, image-digest reproducibility, offline behavior, model loading, time to first token, learner benefit, macOS/WSL2 equivalence or independent technical correctness.

## Immediate dependency order

1. Human: approve PR #24 as the canonical progress base or record an alternative for `STACK-01`.
2. Orchestrator: reconcile the accepted stack and run full combined-head CI.
3. Validation Architect: complete `PROGRESS-02` and retain migration/corruption evidence.
4. Validation Architect: define and begin `DATA-01` retrospective extraction.
5. Human: nominate an independent llama.cpp/GGML reviewer.
6. Literature Scout: verify current official EAAI requirements.
7. Validation Architect + Human: approve an evaluation pathway before any recruitment or personal-data collection.
