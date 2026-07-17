# BASE-01A — information-equivalent static versus viewer benchmark

## Run metadata

- Starting commit: `e0afc79f36f447b352ef8639c085a9188df9b68d`
- Assigned milestone: `BASE-01A`
- Learner outcome: trace a bounded GGUF-loading path and distinguish descriptor/layout evidence from physical-residency or native-execution evidence.
- Implementation head before this run record: `ff869efb90d08bf17185fa283f256d96624fc792`
- Final PR head: recorded in the PR handoff because a commit cannot contain its own SHA.

## Assignment selection

The highest Documentation Builder dependency, Lab 1 progress integration, passed commit-scoped Documentation CI run `29579032392`. Measured Ubuntu 24.04 and devcontainer Lab 0 rows remained blocked because this execution environment does not provide those runtimes. The next ready dependency-safe orchestrator assignment was `BASE-01A`.

## Files produced

- `schemas/trace-viewer-benchmark.schema.json`
- `executable_lectures/benchmarks/gguf-load-static-vs-viewer-v0.json`
- `scripts/validate_trace_viewer_benchmark.py`
- `tests/test_validate_trace_viewer_benchmark.py`
- `docs/publication/benchmark-tasks.md`
- updates to `docs/publication/evidence-backlog.md` and `docs/reference/project-state.md`

## Sources and evidence

- Existing validated authored trace: `executable_lectures/traces/gguf-load-authored-v0.json`
- Pinned llama.cpp revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Existing deterministic figure evidence ID: `figure:synthetic-gguf-layout`
- No new external source was introduced, so the research ledger was unchanged.

## Frozen comparison

Both conditions receive identical ordered evidence IDs and identical ordered questions. The viewer may add only bounded navigation, coordinated highlighting and deterministic visualization. The static condition retains source links, ordered source/text evidence and the complete static alternative.

Four tasks are frozen:

1. next parser phase and active function;
2. descriptor parsing versus physical residency;
3. tensor-data start, alignment and payload bytes;
4. held-out transfer about unsupported residency/native-access claims.

Scoring uses a frozen answer key, bounded partial credit and zero for missing responses. Timing uses a monotonic clock with a 600-second limit; partial responses are retained and timeout is reported separately.

## Claims

### Verified

- The semantic validator checks immutable source revision and trace-revision agreement.
- It requires identical evidence and question ordering across conditions.
- It rejects interactive-only features in the static condition.
- It requires at least one transfer task, valid evidence references, frozen scoring/timing semantics and all accessibility fallbacks.
- Eight focused tests cover the committed fixture and key failure modes.

### Interpretation

An information-equivalent control is more defensible than raw upstream source because it isolates interface support from curated-content availability.

### Historical

Raw-source comparison was previously identified as a rejection risk because it would give the viewer additional information rather than only a different presentation.

### Open question

Whether the viewer improves correctness, completion time, transfer or confidence calibration remains unevidenced until an approved evaluation is conducted.

## Validators and failures

- Local execution was unavailable in the connector-only environment.
- Documentation CI is the commit-scoped validation authority for the final branch head.
- No failure was hidden or converted into a learner-benefit claim.

## Security, privacy and ethics

- No participant recruitment or personal-data collection.
- No telemetry, identity, webcam/eye tracking or server synchronization.
- No model weights, model downloads, credentials, paid APIs or generated media.

## Human-review needs

- Independent technical review of task wording and answer keys.
- Approval of the learner or expert evaluation pathway before recruitment.
- Review of timeout and partial-credit policy before data collection.

## Evidence produced

A versioned, machine-checkable pre-evaluation benchmark contract that can support or falsify the claim that the viewer is evaluated without information-availability confounds.

## Next dependency

After passing final-head CI, `MEDIA-02` is the next ready validation increment. Measured `LAB0-03` and `LAB0-04` remain higher-value but blocked until suitable execution environments are available.
