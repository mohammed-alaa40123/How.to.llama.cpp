# OpenCL queue/context ownership-call inventory increment

- Run time: 2026-07-15 07:52 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: expand the exact-line OpenCL lifecycle report so the next pinned artifact can reveal direct queue/context creation and retention sites as well as releases

## Startup and inspection

Read the complete README first, then project state, research log, research ledger, and the latest detailed note. Inspected the current extractor, focused test suite, PR metadata, first-pass OpenCL lifecycle findings, and the current living TODO order before editing.

## Artifact

Expanded `scripts/extract_opencl_lifecycle_calls.py` to recognize these additional direct ownership-transition APIs:

- `clCreateContext`
- `clCreateContextFromType`
- `clRetainContext`
- `clCreateCommandQueue`
- `clCreateCommandQueueWithProperties`
- `clRetainCommandQueue`

Updated `tests/test_extract_opencl_lifecycle_calls.py` with exact-line, source-order, lexical-masking, and similar-identifier regressions for the new calls.

## Verified

- The lifecycle matcher now spans direct creation, retention, completion, and release calls for command queues and contexts.
- Existing comment/literal masking, exact 1-based line calculation, optional original-source context, and source ordering remain unchanged.
- `clCreateContextFromType` has dedicated coverage.
- Call-shaped text inside comments and literals remains excluded.
- Similar identifiers such as `create_clCreateContext(...)` remain excluded because the matcher requires a word boundary at the API name.
- The repository-owned OpenCL workflow is already configured to rerun when the extractor or its tests change, so the next artifact will report the pinned translation unit without requiring another workflow edit.

## Interpretation

This increment does not resolve ownership by itself. It removes a blind spot in the generated evidence: a report containing zero direct releases can now be compared against direct creation and retention sites. If the regenerated pinned report also contains zero direct creation calls, wrapper constructors, generated code, globals, or process-lifetime ownership become the higher-probability review targets.

## Historical

The first complete pinned report classified 556 selected completion/release calls but did not inventory direct queue/context creation or retention. That made the absence of `clReleaseCommandQueue()` and `clReleaseContext()` difficult to interpret. This increment makes the next report symmetric enough for a bounded ownership audit.

## Open questions

- How many direct queue/context creation and retention calls appear in pinned revision `e3546c7948e3af463d0b401e6421d5a4c2faf565`?
- Which enclosing object owns each returned handle?
- Are queue/context objects wrapper-owned or deliberately process-scoped?
- Do scheduler events and buffers retain the required underlying OpenCL objects independently of the backend wrapper?
- Should creation/retention and release records be automatically paired after the regenerated report is inspected?

## Validation

The extractor and focused tests were committed. Documentation CI and the pinned OpenCL lifecycle-report workflow must be checked on the final head. Local checkout validation remains unavailable in this runtime, so GitHub-hosted workflows are authoritative.

## Next priority

Inspect the regenerated pinned lifecycle artifact, map direct queue/context ownership calls to enclosing objects, and update the OpenCL row in the backend teardown comparison matrix.
