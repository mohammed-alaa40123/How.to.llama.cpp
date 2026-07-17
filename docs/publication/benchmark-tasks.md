# Static source/text versus trace-viewer benchmark

_Status: frozen pre-evaluation fixture; no participant recruitment or learner data collection is authorized._

## Bounded purpose

This benchmark tests whether synchronized navigation, coordinated source highlighting and deterministic visualization can help with bounded source-tracing tasks **without changing the evidence or questions available to the comparison condition**.

The machine-readable contract is `executable_lectures/benchmarks/gguf-load-static-vs-viewer-v0.json`. It is validated by `scripts/validate_trace_viewer_benchmark.py` against the source-pinned authored trace.

## Learning contract

| Field | Declaration |
|---|---|
| Intended learner | Advanced undergraduate, graduate or early-stage systems researcher who can read C/C++ but is still connecting GGUF layout, parser control flow and memory-evidence boundaries |
| Prerequisite | Basic C/C++ function tracing, arrays and file offsets; no prior llama.cpp contribution experience required |
| Learning objective | Trace the bounded GGUF-loading sequence and distinguish descriptor/layout evidence from physical-residency or native-execution evidence |
| Predicted misconception | Seeing tensor descriptors or a source line proves that tensor pages are resident or that native inference occurred |
| Executable action | Answer the same four frozen code-tracing, evidence-boundary and transfer tasks in either presentation condition |
| Observable output | Item responses, frozen-key correctness, monotonic completion time, timeout status and accessibility mode |
| Formative assessment | Four versioned questions with evidence-linked answer keys and partial-credit points |
| Source revision | llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565` |
| Validation method | Semantic validator enforces identical evidence/question ordering, immutable source revision, bounded scoring/timing and accessibility fallbacks |
| Accessibility fallback | Complete static source/text condition, keyboard operation, screen-reader text and reduced-motion support |

## Conditions

### Static source/text

The static condition exposes the same pinned source excerpts, ordered trace/call-stack information, runtime-object text, tensor shapes, memory events, evidence labels, prompts, explanations and figure alternative as the viewer. It adds no synchronized step controls or coordinated highlighting.

### Interactive viewer

The viewer may add only:

- bounded previous/next and Home/End navigation;
- coordinated source highlighting;
- deterministic layout visualization;
- status announcements and existing static fallback.

It may not receive extra explanations, source evidence, hints, answer feedback or questions.

## Frozen outcomes

Primary outcomes are item-level correctness and bounded completion time. Timeout is reported separately while retaining completed responses. Secondary reporting may include confidence-correctness calibration, perceived difficulty, navigation errors and accessibility mode only after an approved evaluation pathway exists.

The fixture does not authorize identity collection, telemetry, webcam/eye tracking, free-form learner transcripts or server synchronization.

## Claim labels

### Verified

- The two conditions reference identical ordered evidence IDs and question IDs.
- The fixture pins the existing authored/source-derived trace and immutable llama.cpp revision.
- The semantic validator rejects information inequivalence, mutable revisions, interactive-only controls in the static condition, missing transfer tasks, unknown evidence and absent accessibility fallbacks.

### Interpretation

An information-equivalent baseline is a fairer test of interface value than comparing the viewer with raw upstream source, because raw source would confound navigation support with missing curated evidence.

### Historical

Earlier planning identified raw-source comparison as a major rejection risk because it would advantage the viewer through content availability rather than interface behavior.

### Open question

Whether the viewer improves correctness, time, transfer or confidence calibration remains unevidenced until an approved evaluation is conducted. Passing validation establishes the benchmark contract, not learner benefit.

## Validation

```bash
python3 scripts/validate_trace_viewer_benchmark.py
python3 -m unittest tests.test_validate_trace_viewer_benchmark
```
