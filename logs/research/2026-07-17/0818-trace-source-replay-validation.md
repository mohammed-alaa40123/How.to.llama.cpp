# Validation Architect run — TRACE-02 source and replay validation

- **Starting commit:** `bcb7555ef8b4e80817b5b812c35db6b1c6f7b9a9`
- **Assigned milestone:** TRACE-02, the highest-priority ready Validation Architect item.
- **Learner outcome:** a learner can inspect a bounded authored GGUF-loading trace whose source revision, file, function, line range, evidence label and navigation order are independently machine-checkable.

## Files and primary source

- `executable_lectures/source-anchors/llama-cpp-e3546c7.json`
- `scripts/validate_trace_source_links.py`
- `tests/test_validate_trace_source_links.py`
- corrected `executable_lectures/traces/gguf-load-authored-v0.json`
- `docs/executable-lectures/source-link-validation.md`
- `docs/publication/evidence-backlog.md`
- primary source: `ggml-org/llama.cpp`, immutable revision `e3546c7948e3af463d0b401e6421d5a4c2faf565`, `ggml/src/gguf.cpp`, blob `c3ffa1a13435bd531c259b6106a3a6763e4f2df9`

## Claims and correction

### Verified

The pinned source implements the bounded parser path in `gguf_init_from_reader`. The earlier authored sample pointed to `gguf_init_from_file_impl` at lines 1100, 1110 and 1260, which do not identify that function in the pinned file. The sample is corrected to pinned anchors at lines 451, 480 and 757.

### Interpretation

The correction demonstrates why schema-only validation is insufficient: syntactically valid, plausible source links can still be technically false. The new resolver supports the EAAI claim that repository-native validation can expose and correct this class of educational-content error.

### Historical

The incorrect anchors entered with the initial authored trace contract before immutable-source resolution was implemented.

### Open question

The source-anchor manifest still requires independent technical review, and native-captured execution remains a separate future artifact.

## Validators and expected results

Seven focused tests cover the valid committed trace, revision drift, wrong function names, out-of-range lines, clamped boundaries, forward/back round trips and graceful omission of optional runtime collections. Existing trace validation continues to enforce the 500-step and 2 MiB browser bounds.

## Failures and limitations

The connector environment cannot execute the repository test suite locally. Commit-scoped GitHub Actions remains the execution authority. The validator intentionally uses a checked-in immutable-source manifest rather than networking to upstream during ordinary CI; it verifies against the reviewed manifest and blob identity, not against a moving default branch.

## Human review needs

- independent llama.cpp/GGML reviewer confirmation of the selected pedagogical anchors;
- review that the three authored steps are educationally coherent without being represented as a complete native call trace.

## Evidence produced

A primary-source-backed correction, immutable source-anchor manifest, dependency-free validator, replay transition function, malformed-input tests and explicit claim boundary.

- **Ending commit:** to be recorded by the final branch/PR head.
- **Next dependency:** after final-head CI passes, close TRACE-02 and unblock the minimal keyboard-operable viewer shell; otherwise repair only the failing validator/integration evidence.
