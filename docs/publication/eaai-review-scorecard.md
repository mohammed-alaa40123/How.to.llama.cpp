# Adversarial EAAI review scorecard

_Last reviewed: 2026-07-17 17:15 Africa/Cairo_

Scale: 1 = absent or seriously deficient; 2 = planned/contract only; 3 = credible partial evidence; 4 = strong evidence with limited gaps; 5 = submission-ready evidence.

| Category | Score | Reviewer judgment | Condition for next score |
|---|---:|---|---|
| Educational significance | 3/5 | Difficult source-level AI-systems concepts are important and the evidence-boundary framing is promising. The claimed widespread documentation gap remains unverified. | Systematic documentation audit and clearer evidence that the selected misconceptions matter to the primary audience. |
| Target audience precision | 2/5 | The audience spans advanced undergraduates through researchers and is too broad for one evaluation. | Freeze one primary population, prerequisites, screener and exclusions. |
| Learning objectives and alignment | 3/5 | Each experience has learner/action/output/assessment contracts, but cross-lab progression is not yet frozen. | Demonstrate a coherent progression and transfer assessment across all three experiences. |
| Lab 0 educational quality | 2/5 | Strong phase-separation contract; no clean execution and no evidence learners diagnose failures. | Measured local/cloud runs plus seeded diagnostic tasks and reviewed answer key. |
| Browser GGUF lab | 3/5 | Deterministic legal fixture, browser/Python agreement and explicit exclusions are strong. External validity and independent correctness remain open. | Independent review, unsupported-subset documentation and checkpoint/transfer evidence. |
| Executable lecture / trace viewer | 3/5 | Source pinning, corrected anchors, replay bounds, evidence labels and accessibility fallbacks are credible. The trace is authored/source-derived. | One faithfully/native-captured path and completed information-equivalent comparison. |
| Three-tier reproducibility | 2/5 | Browser tier is validated; local-native and devcontainer evidence are contractual only. | Clean measured rows with exact revisions, tools, commands, logs and failure classifications. |
| Assessment and learner evidence | 1/5 | No approved study, participant data or completed expert-usefulness evaluation exists. | Approved pathway and completed frozen outcomes; ethics decision documented. |
| Independent technical correctness | 1/5 | No independent reviewer has signed off on the core educational artifacts. | Dated review, corrections and final acceptance across fixture/parser/trace/figure/tasks. |
| Accessibility | 3/5 | Keyboard semantics, transcript/static fallbacks, reduced-motion and structural CI exist. Real assistive-technology review is missing. | Manual keyboard/screen-reader/contrast/focus review and defect closure. |
| Progress privacy and portability | 3/5 | Local-first, versioned export/import, recovery and privacy minimization are appropriate. Cross-browser behavior is unmeasured. | Browser matrix, quota/storage-denial tests and UI accessibility review. |
| Media provenance and safety | 4/5 | Deterministic figures are authoritative; manifests, review states, hashes, stale detection and no-cost ordinary CI are strong. | Independent review of any technical figure used in evaluation and full audit of any optional generated asset. |
| Reproducibility of artifacts | 3/5 | Component CI and deterministic fixtures are substantial, but the integrated stack is not merged/deployed. | Single integrated branch, clean acceptance run, main/Pages verification and durable artifact links. |
| Longitudinal agent case study | 2/5 | Machine-checkable schema and three archetypes show feasibility, not longitudinal findings. | Complete bounded sampling frame, coding manual, denominator, independent audit, human effort and cost accounting. |
| Ethical AI use and disclosure | 3/5 | Boundaries for media, privacy, telemetry and human review are explicit. Actual agent/tool disclosure and ethics pathway are unfinished. | Frozen disclosure policy, approved evaluation/ethics decision and quantified human/agent contributions. |
| Generalization beyond llama.cpp | 2/5 | Contracts may be reusable, but no external replication or strong limits argument exists. | Mechanism-level generalization analysis and preferably one bounded second-codebase test. |
| Reflective experience-report evidence | 2/5 | Failures and repairs are logged, but broader reflection lacks a reviewed longitudinal dataset. | Analyze success/failure patterns, maintenance burden, tradeoffs and rejected alternatives from the complete sample. |
| Venue readiness | 1/5 | No verified EAAI-27 call is available and core evidence gates remain open. | Verify official current requirements and close fatal evidence gaps. |

## Weighted readiness judgment

**Reviewer readiness: 38/100.**

This is lower than an implementation-readiness score because EAAI review weights educational evidence, independent correctness, reflection, and reproducibility more heavily than contract coverage.

- Artifact/architecture maturity: **65/100**
- Educational evidence: **15/100**
- Technical correctness assurance: **20/100**
- Reproducibility/deployability: **35/100**
- Longitudinal case-study evidence: **25/100**
- Ethics/accessibility/disclosure: **55/100**
- Venue/submission readiness: **10/100**

## Current disposition

**Reject — promising artifact, insufficient experience-report evidence.**

The project should not begin manuscript integration. The fastest path to a materially better score is not more features. It is:

1. independent technical review;
2. measured Ubuntu and devcontainer Lab 0 evidence;
3. one integrated vertical slice;
4. approved and executed usefulness evaluation;
5. a broader audited retrospective dataset with human labor and cost disclosure.

## Re-review threshold

A new adversarial review is warranted when at least two of the five priorities above have durable evidence, or when any proposed claim expands beyond the current claims-evidence table.