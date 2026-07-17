# Executable trace source-link and replay validation

## Validation target

**Intended learner:** advanced undergraduate, graduate, or early-stage systems researcher who can read C/C++ but needs help connecting GGUF bytes to parser control flow.

**Prerequisite:** the learner can distinguish a file format from an executable graph and understands that the sample trace is authored/source-derived rather than native-captured.

**Learning objective:** follow a bounded GGUF-loading path while identifying the exact immutable source revision, function, line anchor, evidence label, and replay position for each step.

**Predicted misconception:** a plausible function name or line number is sufficient provenance, or an authored trace proves that native execution followed the displayed path.

**Executable action:** validate the authored trace against the checked-in immutable source-anchor manifest and replay forward/back transitions.

**Observable output:** a successful validator result, or a stable error identifying revision drift, unknown file/function anchors, out-of-range lines, or invalid navigation.

**Formative assessment:** ask the learner to explain why `authored-example` remains the correct capture label even after source anchors pass validation.

**Source revision:** `ggml-org/llama.cpp@e3546c7948e3af463d0b401e6421d5a4c2faf565`.

**Validation method:** dependency-free Python unit tests plus ordinary Documentation CI.

**Accessibility fallback:** the trace retains ordered static summaries; navigation semantics are pure index transitions that can be exposed through buttons, keyboard controls, or a linear text transcript.

## Evidence classification

### Verified

- The pinned llama.cpp revision contains `ggml/src/gguf.cpp` with blob SHA-1 `c3ffa1a13435bd531c259b6106a3a6763e4f2df9`.
- The bounded parser implementation is `gguf_init_from_reader`, not the previously recorded `gguf_init_from_file_impl`.
- The corrected authored trace uses pinned anchors at lines 451, 480, and 757 within the verified function range.
- The validator rejects repository/revision mismatch, unregistered file/function pairs, and lines outside the pinned range.
- Replay uses deterministic, clamped `previous` and `next` transitions and remains valid when optional runtime collections are absent.

### Interpretation

Passing this contract makes the trace auditable enough to unblock a narrow viewer shell. It does not establish that the viewer improves learning or that the authored steps are a complete runtime execution path.

### Historical correction

The earlier sample trace named `gguf_init_from_file_impl` at lines 1100, 1110, and 1260. Verification against the immutable source showed that those anchors pointed elsewhere in the file. This increment corrects the trace rather than preserving plausible but false source links.

### Open questions

- Native capture still requires separate instrumentation and provenance.
- Independent llama.cpp/GGML technical review remains required.
- A future source-refresh tool should regenerate manifests when a new pinned revision is intentionally adopted; ordinary CI must not silently follow upstream changes.

## Rejected alternative

The project does not resolve source links against the moving upstream default branch during ordinary CI. That would make the same trace change meaning over time and would introduce a network dependency into deterministic validation.

## EAAI claim supported or falsified

This increment supports—and can falsify—the claim that source-linked executable learning artifacts can make revision, location, evidence type, and replay semantics machine-checkable. The discovered incorrect anchors are direct evidence that source-link validation catches errors that schema-only validation misses.
