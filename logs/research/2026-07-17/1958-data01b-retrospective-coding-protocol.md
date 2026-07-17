# DATA-01B retrospective coding protocol

- **Date:** 2026-07-17 19:58 Africa/Cairo
- **Starting commit:** `083a2bf606714a616e0dc5e5dd46f4081bedcaa1`
- **Assigned milestone:** DATA-01B, after LAB0-03 and LAB0-04 remained blocked by unavailable execution environments.
- **Learner outcome supported:** indirect; strengthens the validity of the longitudinal maintenance case study that supports the executable-learning artifact.

## Increment

Frozen a bounded retrospective sampling/codebook contract, semantic validator, example batch and focused tests. This run does not perform the broader extraction or independent coding.

## Claims

### Verified

- The validator rejects mutable revisions, duplicate records, unsafe evidence paths, silent missingness, blocked rows without blocker detail, unrecorded disagreements and adjudication without rationale.
- Nine focused tests and the valid example passed in an isolated local workspace.

### Interpretation

- A frozen codebook before broader extraction reduces post-hoc outcome coding and cherry-picking risk.

### Historical

- The first DATA-01 batch established representational coverage for success, CI repair and blocked reassignment, but not longitudinal representativeness.

### Open Question

- Which immutable revision and date window will define the broader extraction corpus.
- Who will serve as the independent coder.

## Validation

- `python3 -m unittest discover -s tests -p 'test_validate_retrospective_coding_batch.py'`
- `python3 scripts/validate_retrospective_coding_batch.py progress/examples/retrospective-coding-batch-v0.json`
- `python3 -m py_compile scripts/validate_retrospective_coding_batch.py tests/test_validate_retrospective_coding_batch.py`

Local isolated result: nine tests passed; example batch valid; Python compilation passed. Commit-scoped Documentation CI remains authoritative after publication.

## Safety and limitations

No participant data, telemetry, raw conversations, model weights, paid generation or external API calls were added. The example contains one already-durable repository run solely to exercise the contract. DATA-01B remains in progress until broader extraction and independent double-coding are complete.

## Human review needed

Nominate an independent coder and approve the frozen study window before extraction.

## Next dependency

Extract the broader all-eligible-run sample at one immutable revision, then double-code and adjudicate it. LAB0-03/LAB0-04 remain higher priority when suitable environments become available.
