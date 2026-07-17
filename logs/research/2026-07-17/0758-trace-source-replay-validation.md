# Trace source and replay validation

## Run metadata

- Starting commit: `61a0ffdc10d421576826ed2325f074839c39d125`
- Assigned milestone: `TRACE-02` — validate pinned source locations, replay behavior, missing optional data, and browser bounds before viewer implementation
- Learner outcome: a learner can distinguish a plausible source label from a verified immutable anchor and can traverse the authored trace without wraparound or hidden state
- Implementation head before this run-log commit: `e22cca432db23dbfcf7baac5da534667a49e7d44`

## Files and primary sources

- `executable_lectures/source-locks/gguf-load-e3546c7.json`
- `scripts/validate_trace_source_replay.py`
- `tests/test_validate_trace_source_replay.py`
- `executable_lectures/traces/gguf-load-authored-v0.json`
- `docs/executable-lectures/source-replay-validation.md`
- Primary source: `ggml-org/llama.cpp`, commit `e3546c7948e3af463d0b401e6421d5a4c2faf565`, file `ggml/src/gguf.cpp`, Git blob `c3ffa1a13435bd531c259b6106a3a6763e4f2df9`

## Failure discovered and correction

The authored sample claimed `gguf_init_from_file_impl` at lines 1100, 1110, and 1260. Those locations do not identify that function at the pinned revision. The pinned reader implementation is `gguf_init_from_reader`, beginning at line 451. The trace now uses verified anchors at lines 451, 456, and 757, with call-stack frames locked to line 451. The figure path was also corrected to the checked-in deterministic SVG.

## Validators and tests

The new dependency-free validator:

- requires lock repository and revision to equal the trace source;
- recomputes each exact source-line SHA-256;
- requires every step location and call-stack frame to appear in the lock;
- retains the existing immutable-revision, evidence-kind, 500-step, 2 MiB, path-safety, and static-fallback checks;
- defines bounded `next`, `previous`, `first`, and `last` replay semantics;
- emits a deterministic ordered static replay for keyboard-free and reduced-motion fallbacks.

Seven focused tests cover valid resolution, shifted lines, wrong functions, altered line text, unlocked call-stack frames, bounded reversible navigation, deterministic replay, and missing optional runtime arrays.

## Truth labels

- **Verified:** the previous sample anchors were inconsistent with the pinned primary source.
- **Verified:** the new lock records the immutable commit, upstream blob SHA, exact source text, function identity, line number, and line-text digest.
- **Interpretation:** a small checked-in lock is suitable for ordinary offline CI, while a later native/container lane should additionally resolve the same anchors against a pinned checkout.
- **Historical:** the original trace contract already bounded size and ordering but explicitly left network/source resolution open.
- **Open question:** the eventual viewer still needs a fair static-source/text baseline and evidence that it improves code-tracing accuracy rather than visual novelty.

## Validation status and limitations

The connector environment could not clone the repository because direct network DNS was unavailable. Source anchors were verified through the connected GitHub primary-source fetch. Commit-scoped Documentation CI is therefore the execution authority for the new tests. No model, native instrumentation, participant data, telemetry, paid API, credential, or manuscript prose was introduced.

Independent technical review remains required. A passing source lock proves source identity and replay integrity; it does not prove native execution or learner benefit.

## Next dependency

If final-head CI passes, mark `TRACE-02` evidenced and unblock only the minimal keyboard-operable authored-trace viewer (`VIEW-01`). If CI fails, repair the validator or integration without expanding scope.
