# EAAI readiness scorecard

_Last updated: 2026-07-18 06:02 Africa/Cairo_

Scores use a 0-4 evidence scale: `0` absent, `1` planned, `2` implemented, `3` validated/exercised, and `4` publication-ready with independent evidence and limitations.

| Category | Score | Current evidence | Next requirement |
|---|---:|---|---|
| Educational framing | 2.8/4 | audience, prerequisites, misconceptions, objectives and three lesson contracts frozen | systematic documentation audit and independent objective review |
| Research questions/contribution | 2.2/4 | four bounded RQs and claim boundaries | claims-evidence table tied to data, baselines and limitations |
| Lab platform architecture | 3.0/4 | unequal browser/local/cloud tiers; Ubuntu native and devcontainer rows exercised | canonical integration, offline/degraded tests and any additional supported rows |
| Lab 0 | 3.0/4 | model-free Ubuntu and devcontainer setup/build/launch reports retained and validated | learner-facing diagnostics exercise; optional model path kept separate |
| GGUF browser lab | 2.5/4 | deterministic fixture, parser agreement, checkpoints and static fallback | progress integration and browser-level accessibility evidence |
| Executable lecture | 2.6/4 | pinned trace, replay and keyboard-operable viewer | bounded faithful/native capture, independent review and static baseline |
| Progress/privacy | 2.0/4 | local-only schema and minimization boundary | export/import, migration, corruption recovery and adapter tests |
| Media/provenance | 2.7/4 | manifest validator, deterministic figure and secret-safe policy | lifecycle dry run, stale-asset check and review log |
| Accessibility | 2.6/4 | keyboard viewer, transcript, reduced motion and static fallbacks | browser-level focus/keyboard checks across the integrated demo |
| Technical correctness | 2.1/4 | immutable sources, validators and deterministic fixtures | independent llama.cpp/GGML review |
| Reproducibility | 3.0/4 | retained Ubuntu native and devcontainer Lab 0 rows plus deterministic browser artifacts | combined-stack run, offline/degraded behavior and image/source pin audit |
| Agent-workflow evidence | 1.7/4 | durable logs, handoffs, failures and corrections | structured extraction, double-coding, human-effort and cost records |
| Baseline comparison | 0.5/4 | candidate workflow conditions named | frozen tasks and completed fair comparison |
| Learner/expert evaluation | 0.5/4 | outcomes and instruments outlined | approved protocol and collected evidence |
| Ethics/AI disclosure | 2.2/4 | no telemetry, local-first progress, generated-media boundaries | formal pathway decision and disclosure inventory |
| Venue fit/requirements | 1.5/4 | prior EAAI criteria retained and current verification assigned | current official call, author instructions and timeline |
| Reflection/negative results | 1.8/4 | lock drift, retention-order failures and source corrections retained | structured retrospective dataset and synthesis |

## Overall readiness

**Coordination estimate: 57%.**

This is a conservative project-management signal, not a statistical measure. The adversarial disposition remains **reject in the current state** because implementation and reproducibility cannot substitute for learner/expert-use evidence, independent correctness, a baseline, a canonical artifact or the longitudinal dataset.

## Two-week milestone status

- **Week 1 contracts:** 94%.
- **Week 1 smallest vertical slice:** 95%.
- **Week 2 Lab 0:** 75% — two model-free environment rows pass; no inference claim is made.
- **Week 2 integrated demo:** 52% — components exist but canonical integration and progress portability block closure.
- **Publication evidence package:** 45%.

## Fatal gate failures

- No canonical integrated learner-facing artifact.
- No independent technical correctness review.
- No complete longitudinal agent-workflow dataset with human effort and cost accounting.
- No fair baseline comparison.
- No approved and completed learner or expert evaluation pathway.
- Current official venue requirements are not yet frozen.

## Manuscript gate

Paper integration begins only after all fatal gates above are closed with durable evidence and the combined artifact passes full CI.
