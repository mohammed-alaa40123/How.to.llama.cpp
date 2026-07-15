# OpenCL blocking-read wait classification

- Run time: 2026-07-15 17:52 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Pinned source: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: classify unmatched local command-event waits immediately followed by a same-queue blocking read

## Verified

The complete pinned `ggml-opencl.cpp` was inspected from the source-bearing workflow artifact. Of the 46 simple local waits currently reported as `unmatched_in_scope`:

- **22** are followed immediately by `clEnqueueReadBuffer(..., CL_TRUE, ...)` on the same `queue`;
- **24** are not in that pattern and remain separately unresolved.

The 22 readback sites cover:

| Tensor type | Sites |
|---|---:|
| `Q1_0` | 2 |
| `Q4_0` | 2 |
| `Q4_1` | 2 |
| `Q5_0` | 2 |
| `Q5_1` | 2 |
| `MXFP4` | 2 |
| `Q8_0` | 2 |
| `IQ4_NL` | 1 |
| `Q4_K` | 2 |
| `Q5_K` | 2 |
| `Q6_K` | 3 |
| **Total** | **22** |

Pinned queue creation does not set `CL_QUEUE_OUT_OF_ORDER_EXEC_MODE_ENABLE`, so commands on this queue execute in order. The official Khronos `clEnqueueReadBuffer` reference states that a `CL_TRUE` read does not return until the buffer data has been read and copied to host memory.

For these 22 paths, the sequence is:

```text
enqueue restore/unpack kernel and request evt
    ↓
clWaitForEvents(1, &evt)
    ↓
enqueue same-queue clEnqueueReadBuffer(..., CL_TRUE, ...)
    ↓
blocking read returns only after prior kernel and read complete
```

The explicit event wait is therefore redundant for host-visible completion. The blocking read already supplies the required completion point after the preceding in-order kernel.

The event object is still leaked in the pinned source because neither waiting nor the blocking read decrements the application-owned event reference.

The complete translation unit has 51 direct waits, but the bounded `simple_waited_events` diagnostic intentionally matches only `&identifier`. It therefore contains **50** records: **4** released and **46** unmatched. The remaining released profiling wait uses `&info.evt` and is outside the simple-identifier heuristic.

## Interpretation

These 22 sites admit two behavior-preserving correction options:

1. **Release-only first:** retain the wait and add `clReleaseEvent(evt)`. This is the lowest-risk ownership fix and does not alter synchronization.
2. **Remove event creation and wait:** enqueue the kernel with a null event, then rely on the following same-queue blocking read. This removes redundant synchronization and event ownership entirely, but is a separate optimization and should not be mixed into the first leak-fix patch.

The remaining 24 unmatched waits are mostly upload/conversion paths followed by temporary-buffer release, image creation, transpose helpers, or return. They cannot be called redundant from the blocking-read rule. Some may be removable under command retention and same-queue ordering, but the public `set_tensor` completion contract and later consumer ordering must be reviewed first.

## Historical

The previous run converted the manual direct-wait audit into a CI-enforced lexical regression, but its workflow incorrectly expected the identifier-only diagnostic to include the member-expression wait `&info.evt`. This caused the pinned report workflow to fail. The workflow contract was corrected to the actual bounded scope: 50 simple waits, 4 released, and 46 unmatched.

This increment supplies the first synchronization classification over the unmatched inventory: 22 waits are provably redundant before a same-queue blocking read, while 24 remain unclassified.

## Open questions

- Does the backend `set_tensor` contract require converted device output to be complete before return, or only host-source safety?
- Which of the remaining 24 waits precede only same-queue consumers and can be removed without changing API-visible completion?
- Should the extractor add a separate bounded `followed_by_same_queue_blocking_read` hint while keeping ownership status independent?
- Should the upstream patch be split into a release-only leak fix followed by a synchronization-cleanup patch?

## Sources

- Pinned `ggml/src/ggml-opencl/ggml-opencl.cpp` preserved by the repository workflow artifact.
- Khronos `clEnqueueReadBuffer` reference: blocking reads do not return until data reaches host memory.
- Khronos `clCreateCommandQueue` reference: queues execute in order unless `CL_QUEUE_OUT_OF_ORDER_EXEC_MODE_ENABLE` is set.

## Validation

- Recomputed the bounded heuristic locally against the exact pinned source: 50 simple `&identifier` waits, 4 released, 46 unmatched.
- Inspected the failed workflow and fixed its incorrect 51/5 expectation.
- Final-head Documentation CI and pinned lifecycle workflow were re-triggered; their final status must be checked before closing the run.

## Next priority

Prepare the release-only patch strategy for all 46 leaks, then classify the remaining 24 upload/conversion waits against the backend `set_tensor` completion contract and same-queue consumer chain.