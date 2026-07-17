# EAAI readiness scorecard

_Last updated: 2026-07-17 09:22 Africa/Cairo_

Scores use a 0-4 evidence scale:

- `0` absent;
- `1` planned;
- `2` implemented in a bounded draft artifact;
- `3` validated and independently reviewed or exercised;
- `4` publication-ready evidence with limitations documented.

| Category | Score | Current evidence | Next requirement |
|---|---:|---|---|
| Educational framing | 2.5/4 | target audience, prerequisites, misconceptions and three lesson contracts frozen | systematic documentation-gap audit and expert review of objectives |
| Research questions and contribution | 2/4 | four planning RQs and bounded contribution statements | claims-evidence table tied to collected data and baselines |
| Lab platform architecture | 2/4 | unequal browser/local/cloud tiers and legal fixture policy | reproducibility matrix and clean-environment executions |
| Lab 0 | 1.5/4 | six-phase schema, validator and model-free report | command runner, diagnostics, timing and local/devcontainer evidence |
| GGUF browser lab | 1.25/4 | deterministic fixture, golden parse, figure and lesson contract | browser parser, checkpoints, progress adapter and accessibility validation |
| Executable lecture | 2.5/4 | pinned trace, corrected source anchors, deterministic replay and keyboard-operable viewer with transcript fallback | bounded native/faithful capture, independent review and static baseline comparison |
| Progress/privacy | 2/4 | local-only schema and privacy constraints | export/import, migration, corruption recovery and storage adapter tests |
| Media/provenance | 2.5/4 | manifest validator, official API review and deterministic figure with exact checksums | acceptance/revision/rejection dry run and stale-asset test |
| Accessibility | 2.5/4 | generated-site checks, viewer keyboard controls, live text status, reduced motion and transcript fallback | browser-level keyboard/focus testing for all vertical slices |
| Technical correctness | 2/4 | pinned sources, source-anchor validation, deterministic fixtures and semantic validators | independent llama.cpp/GGML review |
| Reproducibility | 2/4 | deterministic fixture/figure/viewer payload and passing integrated CI | supported-environment matrix and clean Lab 0 executions |
| Agent-workflow evidence | 1.5/4 | durable logs, handoffs, corrections and stacked commits | retrospective extraction, human-correction and cost records |
| Baseline comparison | 0.5/4 | three workflow conditions named | frozen benchmark tasks and completed fair comparison |
| Learner/expert evaluation | 0.5/4 | outcomes and instruments outlined | approved protocol and collected evidence |
| Ethics and AI disclosure | 2/4 | no-data/no-telemetry boundaries, local-first progress and generated-media review requirements | formal pathway decision and final disclosure inventory |
| Venue fit and requirements | 1/4 | EAAI-26 experience-report criteria verified; AAAI-27 dates recorded separately | official EAAI-27 call and author instructions |
| Reflection/negative results | 1.5/4 | CI failures, false source anchors, deterministic-output drift and limitations retained | structured retrospective dataset and synthesis |

## Overall readiness

**Weighted planning estimate: 39%**

This percentage is a coordination signal, not a statistical measure. It is intentionally conservative because implementation artifacts cannot substitute for independent review, baseline comparison, native/environment reproducibility, or educational-use evidence.

## Week 1 milestone status

- **W1.1 Freeze contracts: 90%** — audience, lessons, tiers, legal fixture, trace, progress and media contracts exist; active-stack reviewer integration remains.
- **W1.2 Smallest vertical slice: 90%** — fixture, authored trace, deterministic figure and minimal viewer exist with passing CI; Lab 0 remains a checker contract rather than an executable bootstrap.
- **W1.3 Validation before expansion: 75%** — semantic/source/replay/media/accessibility validators and passing integration CI exist; reproducibility matrix, retrospective data schema and independent review remain.

## Fatal gate failures

The manuscript gate remains closed because the project lacks:

- a reproducible end-to-end Lab 0 and GGUF browser lab;
- progress export/import connected to the lab;
- retrospective workflow dataset;
- baseline comparison;
- independent technical review;
- approved learner or expert evaluation pathway;
- verified current EAAI requirements.
