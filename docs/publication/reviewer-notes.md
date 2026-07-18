# Adversarial EAAI reviewer notes

_Last reviewed: 2026-07-18 05:00 Africa/Cairo_

## Overall recommendation

**Reject if submitted now.** The retained Ubuntu 24.04 Lab 0 run is meaningful reproducibility evidence, but it does not change the central judgment: this is still a strong engineering and validation package without sufficient experience-report evidence.

## Newly verified evidence

- Ubuntu 24.04/x86_64 completed `uv sync --locked`, pinned llama.cpp checkout, CMake/Ninja configuration, bounded `llama-cli` compilation, and model-free executable launch.
- The retained run reports model-free time-to-ready of 326,905 ms.
- No model was redistributed and no inference was attempted.

This supports one local-native matrix row only. It does not support cloud-container reproducibility, offline operation, model loading, time-to-first-token, learner benefit, or cross-platform equivalence.

## Fatal flaws

1. **No approved and completed learner or expert-usefulness evaluation.** CI, schemas, and successful setup runs cannot establish learning.
2. **No independent technical correctness review.** Fixture, parser, explanations, trace, figure, and benchmark key remain internally produced and reviewed.
3. **No canonical integrated executable-learning artifact.** The project is distributed across stacked draft PRs with overlapping progress implementations and no single reviewed/deployed learner route.
4. **The longitudinal agent case study remains too thin.** Protocols and selected examples do not provide a complete denominator, independent coding, human-labor accounting, cost accounting, or maintenance analysis.

## Major concerns

### Lab 0

The Ubuntu run proves setup/build/launch feasibility, not educational quality. The lab still risks becoming a command transcript. Required evidence: seeded failures, phase-localization tasks, reviewed answer keys, and scoring of explanations rather than command completion.

### Three-tier platform

Browser and local-native tiers now have different forms of evidence, which is appropriate. The devcontainer/Codespaces-compatible tier is still contractual. Do not call the platform reproducible across three tiers until a retained devcontainer run exists.

### Browser GGUF lab

The synthetic fixture is a defensible legal teaching artifact, but learners may infer native parser, `mmap`, residency, graph construction, or inference behavior. Persistent evidence-kind labels and misconception checks remain mandatory.

### Executable lecture

The viewer replays authored/source-derived state. It is not native execution. Either preserve that narrow name and claim or add one faithfully captured bounded path with capture provenance, omissions, size limits, deterministic replay, and explicit separation of captured values from explanatory inference.

### Progress and media

Local-first progress and deterministic technical figures are appropriate. Progress must not be treated as mastery or research telemetry. Generative media must remain supplemental, cached, manually triggered, provenance-recorded, accessible, licensed, and human-approved; it cannot serve as technical evidence.

## Ranked required evidence

1. Approve the canonical progress implementation and create one integrated branch with complete CI and deployed/local acceptance evidence.
2. Obtain independent llama.cpp/GGML technical review of the fixture, browser parser, trace, source anchors, figure, and benchmark key.
3. Execute the equivalent retained devcontainer Lab 0 run and document persistence, cost, network, and degraded-mode limits.
4. Approve and execute an information-equivalent learner or expert-usefulness evaluation with correctness and transfer outcomes.
5. Complete the retrospective sampling frame, independent coding, adjudication, human-effort accounting, and cost/failure disclosure.
6. Add educational failure-diagnosis tasks to Lab 0 and one faithfully captured trace or narrower terminology.

## EAAI framing judgment

The strongest future contribution is the combination of evidence-labelled source-level learning and an auditable human-supervised agent-maintenance case study. It is not yet credible as an experience report because the repository demonstrates construction and validation more strongly than educational use, correctness assurance, longitudinal reflection, or integrated deployability.
