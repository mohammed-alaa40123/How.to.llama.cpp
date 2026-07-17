# EAAI-27 fit assessment

_Last reviewed: 2026-07-17_

This is a venue-fit decision aid, not paper prose and not a claim of acceptance readiness.

## Prospective fit

**Best-fit track:** EAAI-27 Main Track, Area 2 — Experience Report and Innovative Practice.

**Current fit judgment:** promising but not submission-ready.

The project addresses education about AI systems by helping advanced learners connect model representation, inference-engine source, runtime state, memory behavior, and evidence provenance. This is within the official EAAI-27 scope when the learning objectives remain explicitly about AI concepts and AI-practitioner training.

## Contribution-to-requirement matrix

| Prospective contribution | EAAI relevance | Current evidence | Missing venue-critical evidence |
|---|---|---|---|
| Source-linked executable environment for GGUF and GGML internals | Tool/resource for enhancing learning about AI | Validated browser GGUF slice, authored trace viewer, Lab 0 contracts | Integrated deployment, measured local/cloud reproducibility, actual-use evidence |
| Evidence labels separating browser, authored, source-derived, and native-captured state | Pedagogical design for avoiding misconceptions in AI-systems learning | Schemas, validators, source pinning, transcript/static fallbacks | Checkpoint or code-tracing results showing learners understand the distinctions |
| Information-equivalent static-versus-viewer benchmark | Evaluation design aligned with code comprehension | Frozen tasks, answer keys, scoring and accessibility fallbacks | Approved and completed comparison plus independent answer-key review |
| Human-supervised agent maintenance process | Reflective experience evidence about maintaining an evolving AI educational resource | Structured run contract, selected success/repair/blocker examples | Bounded longitudinal sample, independent coding audit, human labor, failures, costs and maintenance over time |
| Deterministic technical media plus optional governed generative supplements | Ethical and technically sound AI use | Deterministic figures, manifests, stale detection, accepted/revised/rejected lifecycle | Review of any media actually used, licensing/privacy/accessibility audit and educational-outcome evidence if benefit is claimed |
| Local-first progress portability | Privacy-minimizing learner support | Versioned local export/import, recovery and no server sync | Cross-browser and accessibility validation; separate ethics path for research data |

## Scope guard

The official call excludes work whose focus is using AI to teach non-AI topics. Therefore:

- **In scope:** teaching model formats, inference graphs, runtime evidence, memory behavior in AI inference, responsible source-level AI-systems reasoning, and the maintenance of AI-learning resources.
- **Weak or out of scope:** generic C++ compilation, generic software documentation, or autonomous agents as productivity tools without a direct AI-education outcome.

Lab 0 must consequently assess conceptual ownership of the AI inference toolchain and failure diagnosis, not only command completion.

## Experience-report alignment

Area 2 asks for design/development/use, context, data, and reflection. The repository currently has strong **design and development evidence**, partial **reflection evidence**, and insufficient **use and data evidence**.

### Defensible now

- The repository contains deterministic, source-pinned executable-learning components.
- Contracts make several evidence boundaries machine-checkable.
- Scheduled agents have produced auditable examples of successes, repairs, blockers, and human-review gates.

### Not defensible yet

- Learners benefit from the environment.
- The viewer improves code tracing.
- Lab 0 is reproducible across local and cloud tiers.
- The multi-agent workflow is more efficient or effective than a baseline.
- The source-level documentation gap is widespread.
- The experience generalizes beyond llama.cpp without qualification.

## Generalization boundary

A defensible broader contribution should be stated at the mechanism level:

- immutable source revision and link contracts;
- evidence-kind labels;
- bounded deterministic replay;
- reproducibility records across unequal execution tiers;
- local-first progress boundaries;
- provenance and human review for optional generated media;
- repository-native records of autonomous work and human correction.

Generalization to other evolving systems codebases remains a hypothesis until demonstrated or supported by a principled limitations analysis.

## Venue-specific blockers

1. No completed use/evaluation pathway.
2. No independent technical correctness review.
3. No measured Ubuntu or devcontainer Lab 0 run.
4. No complete longitudinal agent-run sampling frame.
5. No anonymized artifact plan for double-blind review.
6. No confirmed presenter/travel/visa plan for required in-person presentation.
7. No systematic audit supporting the claimed documentation gap.

## Go/no-go rule

Proceed toward an EAAI-27 Area 2 submission only when the evidence package supports a coherent educational experience and reflective lessons within seven pages. If actual use data, independent correctness, and measured reproducibility remain absent at the internal go/no-go review, do not inflate the submission with more features; defer or choose a venue/pathway whose evidence expectations match the completed work.