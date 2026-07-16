# Lab 0 machine-readable checker interface

_Last updated: 2026-07-17_

This contract defines the evidence emitted by **Lab 0: Build and Run llama.cpp**. It deliberately separates environment readiness, native configuration, compilation, executable launch, model loading, and inference so a model-free smoke test can never be reported as successful inference.

## Learning contract

- **Intended learner:** a learner comfortable with a terminal who has not built llama.cpp from source.
- **Prerequisite:** basic shell and Git usage; no model is required for the mandatory path.
- **Learning objective:** distinguish the responsibilities of `uv`, CMake/Ninja, the compiler, the built executable, an optional GGUF input, and token generation.
- **Predicted misconception:** a successful Python environment or `--help` launch proves that a model loaded and generated tokens.
- **Executable action:** run the checker around `uv sync --locked`, CMake configuration, bounded compilation, executable launch, and an optional learner-provided model path.
- **Observable output:** a versioned JSON report validated by `schemas/lab0-check-report.schema.json`.
- **Formative assessment:** given a report where compile and launch pass but model loading is `not_attempted`, identify which claims are justified.
- **Source revision:** every report records the How.to.llama.cpp revision and pinned llama.cpp revision.
- **Validation method:** schema validation plus semantic invariants enforced by `scripts/validate_lab0_report.py`.
- **Accessibility fallback:** the same states are available as plain text, never encoded by color alone.

## State model

Each phase has one explicit state:

- `not_attempted`
- `passed`
- `failed`
- `blocked`
- `not_applicable`

The six required phases are:

1. `environment`: locked Python tooling and required command discovery.
2. `configure`: CMake configuration.
3. `compile`: bounded native target compilation.
4. `executable_launch`: deterministic model-free executable launch such as `--help` or version output.
5. `model_load`: optional learner-provided GGUF loading.
6. `inference`: optional token generation after a successful model load.

## Semantic invariants

The validator rejects reports that violate any of these rules:

- `compile=passed` requires `configure=passed`.
- `executable_launch=passed` requires `compile=passed`.
- `model_load=passed` requires `executable_launch=passed` and `model_input.kind=learner_provided`.
- `inference=passed` requires `model_load=passed`.
- `model_input.kind=none` requires both `model_load` and `inference` to be `not_attempted` or `not_applicable`.
- `claims.inference_succeeded=true` is valid only when `inference=passed`.
- `claims.model_loaded=true` is valid only when `model_load=passed`.
- A passed model-free launch may set `claims.executable_launched=true`, but never the model or inference claims.

## Evidence boundary

- **Verified:** a report passed schema and semantic validation for the commands and revisions recorded in that report.
- **Interpretation:** successful environment/build/launch evidence reduces setup ambiguity but does not demonstrate conceptual learning by itself.
- **Open question:** the exact bounded llama.cpp target and cross-platform command matrix remain to be selected and executed in the next Lab 0 implementation increment.

## Privacy and safety

Reports must not contain model bytes, prompts, generated text, usernames, home-directory paths, access tokens, telemetry identifiers, or paid-API results. A learner-provided model is represented only by a redacted basename, optional local checksum, and local validation state. Ordinary CI must use the model-free path.