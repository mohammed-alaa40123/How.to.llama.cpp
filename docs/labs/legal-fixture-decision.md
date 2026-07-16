# Legal fixture decision for the initial executable-learning labs

_Last updated: 2026-07-17 00:00 Africa/Cairo_

This decision closes the first fixture dependency in the July 17-31 executable-learning plan. It deliberately separates **format education**, **native build validation**, and **real inference** instead of forcing one redistributed model file to serve incompatible purposes.

## Decision summary

| Experience | Fixture or input | Redistribution policy | What it validates |
|---|---|---|---|
| Lab 0 build smoke test | No model file | No model redistribution | Tool ownership, locked Python tooling, CMake/Ninja configuration, compilation, binary discovery, and deterministic non-inference smoke checks |
| Lab 0 optional inference extension | Learner-provided GGUF path | The repository stores no weights | End-to-end model loading and inference on a model the learner obtained under its own terms |
| Lab 1 GGUF Anatomy | Repository-generated synthetic GGUF fixture | Generated from project-owned code and metadata only | Header, metadata, tensor descriptors, alignment, offsets, byte ranges, parsing, and mapping concepts |
| Executable Lecture 0 | Synthetic GGUF plus authored/source-derived trace initially | No model weights and no claim of native capture | Source-linking, evidence-kind labels, deterministic replay, call-flow explanation, and viewer behavior |

## Why one shared model fixture is rejected

**Interpretation:** a single tiny GGUF model would create unnecessary licensing and maintenance risk while weakening the educational separation among setup, file-format reasoning, and inference.

A model-free native smoke test answers whether the toolchain and selected llama.cpp target build correctly. A synthetic GGUF answers whether the learner can reason about file structure. A learner-provided model answers whether real inference works. Treating these as separate evidence paths prevents a passing parser or version command from being misrepresented as successful inference.

## Lab 0 fixture contract

### Intended learner

A learner who can use a terminal but has not built llama.cpp from source.

### Prerequisite

Basic shell and Git usage; no local model is required for the mandatory smoke path.

### Learning objective

Explain which work belongs to `uv`, CMake/Ninja, the native compiler, llama.cpp, and an optional model input.

### Predicted misconception

A successful Python environment or compiled executable proves that a model has loaded and generated tokens.

### Executable action

1. Run `uv sync --locked` for project tooling.
2. Configure and compile a bounded llama.cpp target with CMake and Ninja where available.
3. Run deterministic model-free checks such as binary discovery, `--help`/version execution, and project checker assertions.
4. Optionally provide a local GGUF path for the separately labelled inference extension.

### Observable output

A machine-readable environment/build/smoke report whose fields distinguish:

- Python environment ready;
- native configure complete;
- native compile complete;
- executable launch complete;
- model path absent, supplied, rejected, or loaded;
- inference not attempted, passed, or failed.

### Formative assessment

Given a sample report where compilation passed but model loading was not attempted, identify which claims are justified and which are not.

### Source revision

The checker must record both the How.to.llama.cpp commit and the pinned llama.cpp revision used for the build.

### Validation method

- locked-environment verification;
- compiler, CMake, and Ninja detection;
- bounded target build;
- exact exit-code assertions;
- explicit separation of model-free launch and model-backed inference states;
- no network download during ordinary validation.

### Accessibility fallback

Copyable commands, plain-text status records, non-color state labels, and a static troubleshooting decision tree.

## Lab 1 synthetic GGUF contract

The first repository-owned fixture will be generated deterministically from source code. The committed source of truth is the generator plus a manifest; the binary may be generated in CI or committed only if size and review policy justify it.

### Required contents

The smallest useful fixture should contain:

- the GGUF magic and supported version;
- a bounded metadata set covering at least one string, integer, and array value;
- at least two tensor descriptors with different shapes;
- explicit alignment metadata;
- deterministic padding;
- deterministic tensor byte payloads that are not trained weights;
- no executable graph, tokenizer corpus, user data, copyrighted text, or downloaded model bytes.

### Intended learner

A learner who understands tensors but not GGUF physical layout.

### Prerequisite

Basic tensor-shape and byte-offset reasoning.

### Learning objective

Parse and explain the header, metadata, tensor descriptors, alignment, offsets, and mapped tensor byte ranges.

### Predicted misconceptions

- GGUF stores an executable GGML graph.
- Parsing metadata makes all tensor pages physically resident.
- Tensor descriptor offsets are identical to arbitrary unaligned byte positions.

### Executable action

Predict an offset or field value, parse the fixture, inspect the corresponding bytes and descriptors, then explain the observed alignment and layout.

### Observable output

A header summary, metadata table, descriptor table, alignment calculation, tensor byte-range view, fixture checksum, and checkpoint-answer record.

### Formative assessment

Predict-Discover-Explain checkpoints for:

1. whether a graph is stored in the file;
2. where the first tensor payload begins after alignment;
3. whether parsing or mapping proves physical residency.

### Source revision

The manifest records the fixture-generator revision, fixture-format version, GGUF specification reference used by the lesson, and pinned llama.cpp parser revision.

### Validation method

- byte-for-byte deterministic regeneration;
- SHA-256 checksum;
- golden parsed metadata and descriptor output;
- alignment and range-bound assertions;
- parser rejection tests for truncated or corrupted variants;
- browser and Python parser agreement on the bounded fields used by the lesson.

### Accessibility fallback

Equivalent ordered text and tables, keyboard-only checkpoint flow, descriptive byte-range labels, and a downloadable fixture/manifest pair.

## Executable Lecture 0 evidence boundary

The first trace may use the synthetic GGUF to illustrate a bounded loading path, but every field must declare one of:

- `captured-runtime`;
- `source-derived`;
- `authored-example`;
- `interpretation`;
- `open-question`.

An authored trace must not be presented as native runtime capture. A later native capture can replace or supplement authored steps only after instrumentation and replay validation exist.

## Licensing and privacy rules

### Verified project policy

- Original project code and prose are MIT licensed.
- Upstream llama.cpp remains under its own license and is linked or pinned rather than silently copied.

### Required fixture policy

- Synthetic payload bytes are generated by this repository and have no training or inference value.
- No third-party model weights, tokenizer corpus, prompts, learner code, personal data, or telemetry are embedded.
- Learner-provided model paths remain local and are never uploaded by default.
- CI must not download model weights during ordinary pull-request validation.
- Any future bundled model fixture requires a separate license, provenance, redistribution, size, security, and educational-necessity review.

## Rejected alternatives

| Alternative | Reason rejected for the initial slice |
|---|---|
| Commit a public tiny model from a model hub | Licensing, provenance, mutable remote artifact, download cost, and unnecessary coupling of format education to model inference |
| Download a model automatically in CI | Network fragility, cost, supply-chain exposure, and ordinary-PR dependence on a third-party service |
| Use random bytes named `.gguf` | Cannot support correct parser, alignment, corruption, or source-link validation |
| Treat `llama-cli --help` as inference success | Validates executable launch only, not model loading or token generation |
| Build the first trace from one-token decode | Too broad before trace-size, instrumentation, model-input, and evidence-provenance risks are bounded |

## Acceptance gate

This decision is complete when reviewers agree that:

- mandatory Lab 0 requires no redistributed model;
- optional inference is visibly separate and uses a learner-provided path;
- Lab 1 uses deterministic project-owned synthetic bytes;
- the synthetic fixture cannot be confused with a trained model;
- every success state states exactly what was and was not validated;
- ordinary CI performs no paid API call or model download.

## Next dependency

Implement the deterministic synthetic GGUF generator, manifest schema, golden parser output, and corruption fixtures. In parallel only after the checker interface is specified, implement the model-free Lab 0 environment/build report. The first executable lecture should prefer the bounded GGUF-loading path unless source-link feasibility review reveals a smaller graph-construction path.