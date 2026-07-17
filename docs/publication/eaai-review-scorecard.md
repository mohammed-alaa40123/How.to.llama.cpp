# EAAI adversarial review scorecard

_Last reviewed: 2026-07-17. Scores are evidence-readiness judgments, not predicted acceptance probabilities._

| Category | Score / 5 | Judgment |
|---|---:|---|
| Educational significance | 3 | Important topic, but need is still partly a documentation-gap hypothesis |
| Target learners and objectives | 4 | Audience and misconceptions are unusually explicit |
| Coherent instructional design | 2 | Components are specified but not yet demonstrated as one learning sequence |
| Technical correctness | 2 | Strong provenance rules; independent expert review and source-link verification absent |
| Educational evaluation | 1 | Instruments are planned; no approved evaluation or outcome evidence |
| Reproducibility | 2 | Deterministic fixture and schemas exist; native/container runs are missing |
| Executable lecture value | 2 | Sound trace contract; viewer and comparative learning evidence absent |
| Accessibility | 2 | Requirements are explicit; vertical-slice operation is unverified |
| Ethical AI/media use | 3 | Correct deterministic-authority policy; manifest implementation and cost logs missing |
| Privacy/progress handling | 3 | Strong local-only schema boundary; persistence and recovery implementation missing |
| Multi-agent case-study evidence | 1 | Handoffs exist, but no dataset, baseline or human-effort analysis |
| Reflection and failure analysis | 2 | CI failures and corrections are logged; longitudinal synthesis is absent |
| Generalizability | 1 | Plausible hypotheses only; no transfer evidence |
| Venue readiness | 1 | Current EAAI-27 requirements are not yet verified and core evidence gates remain open |

**Total: 29/70. Recommendation: reject in current form.**

## Threshold for reconsideration

Reconsider after an integrated vertical slice passes CI and reproducibility checks, an independent technical review is complete, an approved educational evaluation yields analyzable evidence, and the multi-agent workflow has a retrospective dataset plus at least one baseline comparison.