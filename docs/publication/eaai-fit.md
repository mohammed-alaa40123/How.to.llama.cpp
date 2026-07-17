# EAAI fit and evidence requirements

_Last updated: 2026-07-17_

This is a venue-planning artifact, not manuscript prose.

## Educational significance

The bounded educational problem is that advanced learners can read C/C++ but struggle to reconstruct how source locations, call flow, runtime state, and evidence provenance connect in llama.cpp/GGML.

## Evidence-backed evaluation requirement

The executable lecture should be evaluated against an information-equivalent static source/text condition. Primary outcomes are code-tracing correctness and bounded completion time. Confidence calibration, perceived difficulty/cognitive load, navigation errors, and accessibility completion mode are secondary.

A comparison against raw source alone is rejected because it confounds information availability with synchronized interaction.

## Reflective experience-report value

The case study becomes relevant to EAAI only when it records:

- why trace/source contracts were selected;
- false-but-plausible source anchors caught by validation;
- implementation and CI failures and their corrections;
- human decisions about technical correctness, scope, privacy, licensing, and ethics;
- whether the viewer helps, does not help, or harms bounded code tracing;
- maintenance burden as the upstream codebase evolves.

## Generalization boundary

A defensible generalization target is revision-pinned executable learning for evolving systems codebases, not all programming education and not all LLM tooling.

## Current gaps

- no approved participant or expert-evaluation pathway;
- no frozen benchmark or static baseline artifact;
- no independent technical review;
- no real or faithfully captured native trace;
- no retrospective workflow dataset or simpler-workflow comparison;
- no verified EAAI-27 call.

The project is not ready for manuscript drafting.