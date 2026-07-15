# OpenCL waited-event follow-up annotation

- Run time: 2026-07-15 18:51 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Pinned source: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: convert the reviewed 22/24 blocking-read split into a bounded machine-readable report field

## Verified

Added `scripts/annotate_opencl_wait_followups.py`, a lexical post-processor for the existing pinned OpenCL lifecycle report. It preserves the ownership status emitted by `analyze_simple_waited_events()` and independently annotates whether the immediately following statement is a same-queue blocking read:

```json
{
  "event": "evt",
  "wait_line": 4123,
  "status": "unmatched_in_scope",
  "followed_by_same_queue_blocking_read": true,
  "next_read_line": 4124
}
```

The recognizer requires all of the following:

1. a simple `clWaitForEvents(1, &identifier)` record;
2. the immediately following semicolon-terminated statement;
3. a direct `clEnqueueReadBuffer(...)` call in that statement;
4. first argument exactly `queue`;
5. blocking argument exactly `CL_TRUE`.

Comments and quoted literals are masked using the existing extractor helper. Focused tests cover a positive same-queue blocking read, `CL_FALSE`, a different queue, an intervening statement, comments/literals, and report-level count aggregation.

The pinned workflow now runs the annotator after lifecycle extraction and guards the reviewed baseline:

```text
22 unmatched waits followed by an immediate same-queue blocking read
24 other unmatched waits
```

Ownership remains independently guarded as 4 released and 46 unmatched among the 50 simple `&identifier` waits.

## Interpretation

This is a synchronization-review hint, not an ownership classification and not C++ control-flow analysis. A record can remain `unmatched_in_scope` while also being marked as followed by a blocking read. That distinction is intentional: the read may make the explicit wait redundant, but it does not release the application-owned event reference.

The artifact makes the previous manual 22/24 classification reproducible and provides a stable acceptance point for two separate future changes:

- release-only leak fix: unmatched ownership reaches zero while the 22/24 synchronization hint remains unchanged;
- later synchronization cleanup: the 22 immediate blocking-read waits disappear after separate review.

## Historical

The preceding run established the 22/24 split manually and listed a future improvement to add a bounded `followed_by_same_queue_blocking_read` hint. This increment implements that improvement without broadening the ownership heuristic.

## Open questions

- Whether the remaining 24 waits should receive separate hints for temporary-buffer release, image creation, transpose, or return.
- Whether argument aliases other than literal `queue` exist in future revisions and warrant an explicitly versioned extension.
- Whether the report should include the enclosing function only for unresolved entries.

## Validation

- Added `tests/test_annotate_opencl_wait_followups.py` with five focused tests.
- Updated `.github/workflows/opencl-lifecycle-report.yml` to execute the annotator and require the pinned 22/24 counts.
- Documentation CI and the pinned OpenCL workflow were triggered for implementation head `d6dd18fb39c8109adcf84fbf28c93ccc3e03fbe5`; both were still running at the first status check.
- Local clone-based validation remains blocked by `Could not resolve host: github.com`.

## Next priority

Prepare the behavior-preserving release-only patch plan for all 46 leaked event references, then classify the remaining 24 waits against the OpenCL backend `set_tensor` completion contract and same-queue consumer chain.
