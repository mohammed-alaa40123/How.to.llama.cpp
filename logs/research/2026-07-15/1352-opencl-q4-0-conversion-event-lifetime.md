# OpenCL Q4_0 conversion event-lifetime audit

- Run time: 2026-07-15 13:52 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Pinned source: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: the two `GGML_TYPE_Q4_0` conversion-kernel paths in pinned `ggml/src/ggml-opencl/ggml-opencl.cpp`

## Verified

The exact source-bearing Actions artifact from successful workflow run `29406303147` (artifact `8339175662`) was downloaded and its preserved `ggml-opencl.cpp` inspected.

The Q4_0 tensor initialization path first performs a blocking host-to-device write into temporary `cl_mem data_device`. It then creates persistent scale and quant sub-buffers (`extra->d` and `extra->q`) as aliases of the tensor's preallocated backing buffer.

There are two conversion-kernel branches:

1. the Adreno MoE transpose/unshuffle conversion path around pinned lines 7988–8021;
2. the ordinary/Adreno-noshuffle Q4_0 conversion path around pinned lines 8025–8055.

Both branches use the same completion pattern:

```cpp
cl_event evt;
clEnqueueNDRangeKernel(..., &evt);
clWaitForEvents(1, &evt);
clReleaseMemObject(data_device);
```

The explicit wait completes the conversion kernel before `data_device` is released and before the produced `extra->q` / `extra->d` aliases are consumed. All work is submitted to the single per-device queue. No host staging allocation is freed asynchronously, no pooled region is returned for reuse, and no cross-queue dependency exists in this group.

However, neither branch calls `clReleaseEvent(evt)`. A command that returns an event performs an implicit retain. `clWaitForEvents()` is a host synchronization operation; it does not decrement the event reference count. The official OpenCL specification requires `clReleaseEvent()` to decrement that reference.

Therefore each successful Q4_0 conversion leaks one host event reference in the pinned implementation. The temporary memory-object lifetime is safe, but the event lifetime is incomplete.

## Interpretation

This group should be classified as:

> **Explicit completion before temporary-buffer release; persistent event-reference leak.**

The leak is bounded per Q4_0 tensor conversion rather than per decode token because this path initializes or transforms tensor storage. Its practical magnitude depends on how many Q4_0 tensors take each path and whether initialization is repeated in one process. It is still a correctness and teardown-accounting defect: waiting for completion does not release the application-owned event handle.

The minimal source fix is to add:

```cpp
CL_CHECK(clReleaseEvent(evt));
```

immediately after each successful `clWaitForEvents(1, &evt)` and before releasing `data_device`. Error-path behavior should also be reviewed because the current `CL_CHECK` mechanism may abort or unwind before later releases.

## Historical

The prior `transpose_2d()` audit focused on `cl_mem` command retention and found all live callers explicitly wait. This Q4_0 group demonstrates a separate lifetime axis: command completion can be correct while the completion-event reference itself leaks.

The complete lifecycle inventory reported 51 direct waits but only 6 direct event releases. This case confirms that the mismatch is not merely due to events being wrapper-owned; at least two locally declared command events are waited but not released.

## Open questions

- How many of the remaining `clWaitForEvents()` sites omit the matching `clReleaseEvent()`?
- Does `CL_CHECK` terminate the process on wait failure, or can a failed wait leak both the event and temporary `data_device` while execution continues?
- Should the lifecycle extractor add a bounded `waited_event_without_release` diagnostic for simple lexical scopes?
- How often are Q4_0 conversions repeated during model load, reload, or backend reinitialization?

## Sources

- Pinned Q4_0 conversion implementation: `ggml/src/ggml-opencl/ggml-opencl.cpp`, approximately lines 7910–8067.
- Khronos OpenCL specification, event objects: `clWaitForEvents`, `clRetainEvent`, and `clReleaseEvent`.
- Source-bearing workflow run `29406303147`, artifact `8339175662`.

## Next priority

Audit all locally declared events passed to `clWaitForEvents()` and classify them as released, transferred, process-lifetime, or leaked. Then add a regression-oriented extractor/test for the simple wait-without-release pattern if the source frequency justifies it.
