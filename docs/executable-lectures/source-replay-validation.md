# Executable trace source and replay validation

## Lesson contract

| Field | Declaration |
|---|---|
| Intended learner | A C/C++-capable learner who can read individual functions but struggles to connect source locations, state, and explanatory evidence |
| Prerequisite | Basic GGUF structure, repository-relative paths, and the difference between authored and captured evidence |
| Learning objective | Follow a bounded GGUF-reader path while verifying that each displayed source location belongs to an immutable revision |
| Predicted misconception | A plausible file, line, and function label is equivalent to a verified source anchor, or every displayed state was captured natively |
| Executable action | Validate the trace and source lock, then navigate forward and backward through the ordered static replay |
| Observable output | A passing source-lock report, an ordered transcript, and bounded current-step indices |
| Formative assessment | Identify an intentionally shifted line/function anchor and explain why the validator rejects it |
| Source revision | `ggml-org/llama.cpp@e3546c7948e3af463d0b401e6421d5a4c2faf565` |
| Validation method | Structural trace checks, immutable source-lock matching, line-text SHA-256 recomputation, call-stack anchor checks, replay boundary tests, and the existing 500-step/2 MiB limits |
| Accessibility fallback | Ordered static summaries containing source, function, evidence label, and explanation; no animation is required |

## Contract

`executable_lectures/source-locks/gguf-load-e3546c7.json` records the immutable repository revision, upstream Git blob SHA, and the smallest source-line set needed by the authored sample. Each line is stored with its function identity and a SHA-256 digest of the exact UTF-8 line text.

The lock is deliberately small. It is not a substitute for a llama.cpp checkout and does not prove runtime execution. It allows ordinary, network-free CI to detect accidental line shifts, incorrect function names, mutable revisions, altered source excerpts, and unlocked call-stack frames. A future native or cloud reproducibility lane may additionally resolve the same anchors against a checkout of the pinned revision.

Run:

```bash
python3 scripts/validate_trace_source_replay.py \
  executable_lectures/traces/gguf-load-authored-v0.json \
  executable_lectures/source-locks/gguf-load-e3546c7.json
```

## Evidence boundaries

- **Verified:** the original sample locations at lines 1100, 1110, and 1260 did not identify `gguf_init_from_file_impl` at the pinned revision. The pinned implementation uses `gguf_init_from_reader`, beginning at line 451; relevant locked anchors are lines 451, 456, 623, and 757.
- **Verified:** the source lock records upstream blob `c3ffa1a13435bd531c259b6106a3a6763e4f2df9` for `ggml/src/gguf.cpp` at the pinned commit.
- **Interpretation:** exact line locks are appropriate for a narrow authored lecture because source drift must become an explicit maintenance event rather than a silently redirected link.
- **Historical:** the first trace schema already required immutable commit SHAs, contiguous sequences, evidence labels, static summaries, and browser-size bounds.
- **Open question:** learner benefit from the eventual viewer versus a static source-and-transcript baseline remains unevaluated.

## Rejected alternatives

- Resolving `main` or another mutable branch at display time.
- Treating a GitHub URL that returns successfully as proof that the claimed function owns the line.
- Starting invasive native instrumentation before authored-source anchors and replay behavior pass.
- Allowing wraparound navigation, which can obscure the beginning and end of a bounded code path.
