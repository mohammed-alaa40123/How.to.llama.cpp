# OpenCL waited-event pairing audit

- Run time: 2026-07-15 14:52 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Pinned source: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Evidence artifact: workflow run `29410050891`, artifact `8340693497`
- Scope: all 51 direct `clWaitForEvents()` calls in pinned `ggml/src/ggml-opencl/ggml-opencl.cpp`

## Verified

The complete source-bearing artifact was downloaded and every direct wait was paired with its event producer and any matching `clReleaseEvent()` in the local ownership path.

| Classification | Wait sites | Notes |
|---|---:|---|
| Completed and released | 5 | profiling event, blocking transpose copy, backend barrier, BF16 upload conversion, BF16 readback conversion |
| Waited without matching release | 46 | locally returned command events across quantized upload/conversion/readback branches |
| Ownership transferred | 0 | no waited local event is moved into another owner after the wait |
| Process-lifetime event | 0 | no waited event is intentionally stored in process-lifetime state |

The five released waits are at pinned lines 889, 5982, 6625, 9358, and 10449. The separate sixth `clReleaseEvent()` at line 6654 releases peer marker events used by `sync_with_other_backends()`; those events are consumed by a barrier wait list rather than passed to `clWaitForEvents()` directly.

The 46 unmatched waited events are distributed across tensor-type branches as follows:

| Tensor type | Unmatched waits |
|---|---:|
| `Q5_0` | 6 |
| `Q5_1` | 5 |
| `Q5_K` | 5 |
| `Q6_K` | 5 |
| `Q4_0` | 4 |
| `Q4_1` | 4 |
| `MXFP4` | 4 |
| `Q8_0` | 4 |
| `Q4_K` | 4 |
| `Q1_0` | 3 |
| `IQ4_NL` | 2 |
| **Total** | **46** |

All 46 use a local `cl_event evt`, request it from an enqueue call, wait for it, and then leave the branch without releasing or transferring the event reference. Many subsequently release a temporary `cl_mem`, perform a blocking readback, set tensor metadata, or return. Those operations do not decrement the event reference count.

## Interpretation

The pinned problem is broader than the two Q4_0 branches: **46 of 51 directly waited event references leak**. The event-release defect spans tensor upload/conversion and readback helpers, not decode-token scheduling. It is therefore primarily proportional to converted/read-back tensor operations and repeated model/backend initialization, rather than tokens generated.

A safe mechanical correction is likely to add `CL_CHECK(clReleaseEvent(evt));` immediately after each successful wait, but the patch should be grouped carefully because `CL_CHECK` failure behavior can bypass later cleanup. A small RAII event wrapper or a scope guard would provide stronger error-path cleanup than 46 manual calls.

The aggregate lifecycle count of six releases is not contradictory: five releases pair with direct waits, while one releases cross-queue marker events that are never host-waited directly.

## Historical

The previous Q4_0 case study proved two leaks. This complete pairing audit shows that those were representative, not isolated. It also separates the unrelated cross-device marker release from direct host-wait pairing.

## Open questions

- Does `CL_CHECK` abort the process, throw, or return in every supported build configuration?
- Should an upstream fix use explicit release calls, a local RAII `cl_event` wrapper, or enqueue operations without returned events when a following blocking command already provides completion?
- Which waits are redundant because the immediately following command is blocking and ordered on the same queue?
- Can a focused source regression test assert that every simple local wait is followed by release without pretending to solve general C++ ownership?

## Next priority

Prepare a bounded upstream-ready patch strategy: first fix the 46 successful-wait paths with error-safe event ownership, then identify waits that can be removed entirely because a same-queue blocking operation already provides the required completion guarantee.