# OpenCL queue/context ownership-call inventory increment

- Run time: 2026-07-15 07:52 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: expand the exact-line OpenCL lifecycle report and inspect the regenerated pinned artifact for direct queue/context ownership transitions

## Startup and inspection

Read the complete README first, then project state, research log, research ledger, and the latest detailed note. Inspected the current extractor, focused test suite, PR metadata, first-pass OpenCL lifecycle findings, generated artifact, workflow results, and the OpenCL lifetime page before editing.

## Artifact

Expanded `scripts/extract_opencl_lifecycle_calls.py` to recognize these additional direct ownership-transition APIs:

- `clCreateContext`
- `clCreateContextFromType`
- `clRetainContext`
- `clCreateCommandQueue`
- `clCreateCommandQueueWithProperties`
- `clRetainCommandQueue`

Updated `tests/test_extract_opencl_lifecycle_calls.py` with exact-line, source-order, lexical-masking, and similar-identifier regressions. Updated `docs/architecture/opencl-build-and-buffer-lifetimes.md` with the regenerated 558-call inventory and two exact creation assignments.

## Verified

- The lifecycle matcher now spans direct creation, retention, completion, and release calls for command queues and contexts.
- Existing comment/literal masking, exact 1-based line calculation, optional original-source context, and source ordering remain unchanged.
- GitHub Actions run `29390227929` succeeded and uploaded artifact `8332938429` for the exact pinned revision.
- The regenerated report contains 558 selected direct calls.
- Exactly one `clCreateContext(...)` call appears at pinned line 5545; its result is assigned to `shared_context` after constructing platform properties from `default_device->platform->id`.
- Exactly one `clCreateCommandQueue(...)` call appears at pinned line 5902; its result is assigned to `backend_ctx->queue` after optional profiling flags are added.
- The report contains zero direct `clCreateContextFromType`, `clCreateCommandQueueWithProperties`, `clRetainContext`, `clRetainCommandQueue`, `clReleaseContext`, or `clReleaseCommandQueue` calls.
- Final-head Documentation CI run `29390352407` passed.
- Final-head pinned OpenCL report run `29390352399` passed.
- PR #1 remains open and mergeable at head `883cb806c1690918ee11568f5dd4c39e2c1860f1`.

## Interpretation

The ownership gap is narrower. The context is created into a variable named `shared_context`, while the queue is stored directly in `backend_ctx->queue`. The asymmetric direct-call result—one create for each handle type, no retain, and no release—makes wrapper destruction, global/process-lifetime policy, or an omitted generated/macro path the next review target. It is not proof of a leak.

Three context lines are sufficient to identify both assignments but not the declaration lifetime of `shared_context` or the destructor/free behavior of `backend_ctx`.

## Historical

The first complete pinned report classified 556 selected completion/release calls but did not inventory direct queue/context creation or retention. This increment expands that report to 558 calls and locates the two direct creation sites.

## Open questions

- Where is `shared_context` declared, and is its lifetime intentionally process-wide?
- Which destructor or free path owns `backend_ctx->queue`?
- Why are there no direct context/queue release calls in the translation unit?
- Do scheduler events and buffers retain the required underlying OpenCL objects independently of the backend wrapper?
- Should enclosing-function metadata be added only for these two ownership sites?

## Validation

Both final-head GitHub-hosted workflows passed: Documentation CI `29390352407` and pinned report generation `29390352399`. Local checkout validation remains unavailable because direct GitHub DNS resolution is blocked in this runtime.

The production Pages site could not be independently verified: public search returned no indexed result, direct URL opening remained blocked by the available safety mechanism, and branch-only content cannot appear before PR #1 merges.

## Next priority

Locate the declarations and destruction paths for `shared_context` and `backend_ctx->queue`, then verify scheduler event/buffer deleter independence and update the OpenCL row in the backend teardown comparison matrix.
