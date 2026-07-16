# Upstream proposal: release waited OpenCL command events

## Status

**Staged, not submitted.** The GitHub App attempted to create an issue in `ggml-org/llama.cpp` and received HTTP 403: `Resource not accessible by integration`.

## Target

- Repository: `ggml-org/llama.cpp`
- Audited revision: `505b1ed15ca80e2a19f12ff4ac365e40fb374053`
- Source file: `ggml/src/ggml-opencl/ggml-opencl.cpp`
- Generated evidence artifact: How.to.llama.cpp workflow artifact `8358479508`

## Verified

The current OpenCL source has:

- 51 direct `clWaitForEvents()` calls;
- 50 simple count-one waits of the form `clWaitForEvents(1, &event)`;
- 4 simple waited events released in the same lexical scope;
- 46 simple waited events with no matching `clReleaseEvent()` or ownership transfer;
- 24 affected sites in `ggml_backend_opencl_buffer_set_tensor()`;
- 22 affected sites in `ggml_backend_opencl_buffer_get_tensor()`.

The generated release-only correction adds exactly 46 local statements:

```cpp
CL_CHECK(clReleaseEvent(evt));
```

Each addition immediately follows its matching successful wait. The post-patch lifecycle report reaches zero unmatched simple waited events while preserving all 51 waits and all existing enqueue, conversion, readback, and memory-object ordering.

## Interpretation

This is an event-ownership fix, not a synchronization redesign. The 24 set-tensor waits preserve the backend's de facto synchronous conversion/expansion completion behavior. The 22 get-tensor waits precede same-queue blocking reads; even where the explicit wait is redundant for completion, waiting does not release the application-owned event reference.

For the first upstream change, explicit local releases are preferable to introducing an event-owner abstraction because they keep the patch mechanical, narrow, and easy to verify. A wrapper refactor and removal of redundant readback waits should be separate changes.

## Historical

The pinned baseline `e3546c7948e3af463d0b401e6421d5a4c2faf565` and current audited revision `505b1ed15ca80e2a19f12ff4ac365e40fb374053` have the same bounded 46-site ownership defect despite 58 intervening commits and 165 changed lines in the OpenCL translation unit.

## Open questions

- Whether maintainers prefer the narrow explicit-release patch or a later move-only event owner.
- Whether the correction should be submitted directly as a pull request or discussed in an issue first.
- Whether the 22 waits before blocking reads should later be removed in a separate optimization.

## Proposed issue title

`OpenCL: command events are waited but not released in tensor conversion/readback paths`

## Proposed issue body

The OpenCL backend requests command events from `clEnqueueNDRangeKernel()`, waits for them with `clWaitForEvents()`, and then leaves the local scope without releasing the application-owned event reference at 46 sites.

This is present at current `master` revision `505b1ed15ca80e2a19f12ff4ac365e40fb374053`.

Audited result:

- 51 direct `clWaitForEvents()` calls;
- 50 simple count-one waits;
- 4 simple waited events released in the same lexical scope;
- 46 simple waited events with no matching `clReleaseEvent()` or ownership transfer;
- 24 affected sites in `ggml_backend_opencl_buffer_set_tensor()`;
- 22 affected sites in `ggml_backend_opencl_buffer_get_tensor()`.

The proposed narrow fix adds `CL_CHECK(clReleaseEvent(evt));` immediately after each affected successful `CL_CHECK(clWaitForEvents(1, &evt));`.

A generated patch was mechanically checked against the exact current source: 46 releases inserted, every insertion immediately follows its matching wait, all 51 waits are preserved, and the post-patch report has zero unmatched simple waited events. No enqueue, read, conversion, or memory-object release is removed or reordered.

Possible removal of waits before blocking reads is intentionally excluded and should be reviewed separately.

## Proposed pull-request title

`opencl: release command events after synchronous waits`

## Proposed pull-request body

The OpenCL tensor conversion and readback paths request command events from `clEnqueueNDRangeKernel()`, wait for them with `clWaitForEvents()`, and then leave the local scope without releasing the application-owned event reference.

This change adds `clReleaseEvent(evt)` immediately after each affected successful wait. It preserves every existing wait and therefore does not alter synchronization or the ordinary synchronous tensor-set behavior.

Audited at llama.cpp revision `505b1ed15ca80e2a19f12ff4ac365e40fb374053`:

- 51 direct `clWaitForEvents()` calls;
- 46 unmatched local count-one waited events before the fix;
- 46 event releases added;
- zero unmatched simple waited events after the fix;
- all 51 waits preserved.

The affected sites are limited to 24 waits in `ggml_backend_opencl_buffer_set_tensor()` and 22 waits in `ggml_backend_opencl_buffer_get_tensor()`.

The patch changes event ownership only. Any future removal of waits before blocking reads should be reviewed separately.
