# Pinned OpenCL lifecycle first-pass classification

- Run time: 2026-07-15 06:49 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: inspect the first complete pinned lifecycle artifact and convert it into a bounded OpenCL teardown classification

## Startup and inspection

Read the complete README first, then project state, research log, research ledger, and the latest detailed note. Inspected the current OpenCL lifetime page, PR state, commit-scoped workflow results, and the uploaded `opencl-lifecycle-pinned-e3546c7` artifact before editing.

## Artifact

Updated `docs/architecture/opencl-build-and-buffer-lifetimes.md` with:

- the exact 556-call inventory;
- first-pass roles for each selected API;
- verified shared-free and cross-device synchronization ordering;
- a conditional teardown classification;
- narrowed ownership and scheduler-lifetime questions.

## Verified

- GitHub Actions run `29385330482` succeeded and uploaded artifact `8331189030` for pinned revision `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- Documentation CI run `29385330547` succeeded for the preceding head.
- The report contains 556 selected direct calls: 343 `clReleaseMemObject`, 121 `clReleaseProgram`, 51 `clWaitForEvents`, 23 `clReleaseKernel`, 11 `clFinish`, 6 `clReleaseEvent`, and 1 `clFlush`.
- It contains no direct `clReleaseCommandQueue` or `clReleaseContext` calls.
- The shared OpenCL `free()` path calls `clFinish(queue)` before decrementing `ref_count`; on the final reference it releases pooled image/sub-buffer views and clears those pools.
- The cross-device synchronization path enqueues marker events on peer queues, flushes those queues, enqueues a destination-queue barrier waiting on the collected events, and releases the event references.
- Several temporary conversion/readback paths wait for kernel events before releasing temporary memory objects; selected readback paths use blocking reads and/or `clFinish()`.

## Interpretation

The shared `free()` path has strong local evidence for queued-work completion before final-reference pooled-memory release. That is enough to move OpenCL from “not classified” to “conditional with verified local completion evidence.” It is not enough to claim global backend-before-scheduler safety because the final queue/context owner, scheduler-resource independence, optional binary-library lifetime, and many enqueue-then-release sites remain unresolved.

The absence of direct queue/context release calls is an ownership question, not proof of a leak. Those objects may be process-scoped, wrapper-owned, or released through code outside the selected direct-call inventory.

## Historical

Earlier runs had a tested extractor and context windows but could inspect only truncated source content. The GitHub-hosted workflow removed that source-recovery blocker and made this first complete pinned report review possible.

## Open questions

- Locate command-queue and OpenCL-context creation and final ownership.
- Determine whether scheduler events and buffers can outlive the backend wrapper safely.
- Classify enqueue-then-release groups that rely on OpenCL object-retention semantics rather than explicit waits.
- Resolve optional Adreno binary-library handle lifetime.
- Add enclosing-function metadata only for report groups that remain ambiguous after source inspection.

## Validation

The documentation change is committed on the PR branch. Commit-scoped Documentation CI and lifecycle-report workflow results for the new head must be checked before the next run closes. The preceding head passed both workflows.

## Next priority

Locate queue/context creation and final ownership in the pinned translation unit, then update the cross-backend teardown matrix with the resulting OpenCL resource-independence classification.
