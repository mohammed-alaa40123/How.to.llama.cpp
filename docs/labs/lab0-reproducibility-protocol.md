# Lab 0 reproducibility and timing protocol

_Last updated: 2026-07-17_

This protocol defines comparable evidence for **Lab 0: Build and Run llama.cpp** across local-native and cloud-container environments. It does not claim that a browser-only lab executes native llama.cpp.

## Learning contract

- **Intended learner:** terminal-capable advanced undergraduate, graduate, or early-stage systems learner who has not built llama.cpp from source.
- **Prerequisite:** basic shell and Git usage; no model is required for the mandatory path.
- **Learning objective:** distinguish Python environment preparation, native toolchain discovery, CMake configuration, Ninja compilation, executable launch, optional model loading, and token generation.
- **Predicted misconception:** `uv sync`, successful compilation, or `llama-cli --help` proves that a model loaded or produced a token.
- **Executable action:** run the pinned checks and emit a versioned reproducibility JSON record.
- **Observable output:** tool versions, exact bounded commands, monotonic timing fields, explicit success states, and stable diagnostic codes.
- **Formative assessment:** given a report with setup/build/launch success and `model_kind=none`, identify why inference remains `not_attempted`.
- **Source revision:** every record pins full course and llama.cpp commit SHAs plus the `uv.lock` checksum.
- **Validation method:** JSON Schema plus `scripts/validate_lab0_reproducibility.py` semantic checks and focused malformed-record tests.
- **Accessibility fallback:** all status, diagnostics, commands, and timings are plain text and never color-only.

## Supported-environment matrix

| Environment | Tier | Architecture | Week-1 status | Required evidence |
|---|---|---:|---|---|
| Ubuntu 24.04 | local native | x86_64 | validation target | locked uv sync, compiler/CMake/Ninja checks, bounded target build, model-free launch |
| macOS 15 | local native | arm64 | planned | same contract with Apple compiler version recorded |
| Windows 11 + WSL2 Ubuntu | local native | x86_64 | planned | report Linux guest identity; do not conflate host Windows paths with native Windows support |
| Ubuntu 24.04 devcontainer | cloud container | x86_64 | planned | pinned container definition, workspace persistence note, bounded build and launch |
| Browser/static | browser | portable | separate Lab 1 tier | concept parsing only; excluded from this native reproducibility schema |

An environment may be marked `validated` only when required tools, setup, bounded compilation, and model-free executable launch all pass in the recorded run. Documentation support without execution evidence is `planned`, not `validated`.

## Required toolchain checks

Record command, exact returned version string, and pass/fail for:

```text
uv --version
python3 --version
cmake --version
ninja --version
c++ --version
```

The Python tooling command is exactly:

```bash
uv sync --locked
```

The native path must use CMake with the Ninja generator and a named bounded target. The initial reproducibility command shape is:

```bash
cmake -S llama.cpp -B build/lab0 -G Ninja -DGGML_NATIVE=OFF
cmake --build build/lab0 --target llama-cli -j 2
build/lab0/bin/llama-cli --help
```

`GGML_NATIVE=OFF` improves portability of the smoke build; it is not a performance recommendation. The target and options must be reviewed against the pinned llama.cpp revision before claiming a completed native run.

## Timing definitions

Use a monotonic clock, not wall-clock timestamps.

- **Start:** immediately before `uv sync --locked`.
- **Ready:** after the bounded executable launch exits successfully.
- **Time to ready:** `ready_monotonic_ms - started_monotonic_ms`.
- **First token:** optional and recorded only for an explicitly learner-provided model after model loading succeeds.
- **Time to first token:** `first_token_monotonic_ms - started_monotonic_ms`.

Model-free CI must omit first-token fields. Timing results are descriptive environment evidence and must not be compared as hardware performance benchmarks without a separate protocol.

## Stable diagnostic taxonomy

| Code | Meaning | Educational response |
|---|---|---|
| `UV_MISSING` | uv command unavailable | explain Python tooling ownership and installation boundary |
| `UV_LOCK_DRIFT` | locked synchronization cannot satisfy `uv.lock` | distinguish environment resolution from native compilation |
| `PYTHON_UNSUPPORTED` | Python version outside the supported range | show detected version and required range |
| `CMAKE_MISSING` | CMake unavailable | identify configure-stage dependency |
| `NINJA_MISSING` | Ninja unavailable | explain generator versus compiler roles |
| `COMPILER_MISSING` | native C++ compiler unavailable | identify compilation dependency |
| `CONFIGURE_FAILED` | CMake generation failed | retain bounded stderr excerpt separately; do not capture personal paths |
| `COMPILE_FAILED` | named target failed to build | distinguish source/build failure from environment sync |
| `EXECUTABLE_MISSING` | expected bounded executable absent | reject launch success |
| `MODEL_PATH_MISSING` | optional learner path not found | do not download or redistribute a substitute model |
| `MODEL_LOAD_FAILED` | optional local model rejected | do not report inference |
| `INFERENCE_FAILED` | model loaded but bounded generation failed | preserve model-load/inference separation |
| `OFFLINE_DEPENDENCY_MISS` | required cached dependency unavailable | report degraded mode explicitly |
| `UNSUPPORTED_PLATFORM` | matrix does not claim this platform | provide static/browser fallback rather than guessing commands |

## Offline and degraded mode

A record distinguishes:

- `ready_from_cache`: all required dependencies were already present and no network was required;
- `blocked_without_cache`: setup needs a dependency fetch and the network is unavailable;
- `not_tested`: no offline conclusion is permitted.

The browser GGUF lab and static documentation remain available as degraded learning paths, but they do not substitute for native build evidence.

## Security and licensing boundary

- Ordinary CI uses the model-free launch path.
- No model weights are redistributed.
- Optional inference accepts only a learner-provided local model path.
- Reports exclude prompts, generated text, usernames, home-directory paths, tokens, credentials, telemetry identifiers, and model bytes.
- Commands must use placeholders such as `MODEL.gguf`, not personal absolute paths.
- Container execution is unprivileged by default; mounting host credentials, Docker sockets, or broad home directories is outside the supported protocol.

## Evidence status

- **Verified:** the schema, semantic validator, deterministic model-free example, and malformed-input tests define a machine-checkable comparison contract.
- **Interpretation:** stable diagnostics and timings may make setup failures more educational and comparable.
- **Historical:** the earlier Lab 0 checker already separated environment, configure, compile, launch, model load, and inference phases.
- **Open question:** real reproducibility runs on each matrix row, exact tool-version support ranges, and learner diagnostic usefulness remain unevidenced until executed and independently reviewed.
