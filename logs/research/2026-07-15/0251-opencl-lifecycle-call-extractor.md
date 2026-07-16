# OpenCL lifecycle-call extractor

- Run time: 2026-07-15 02:51 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: create a bounded exact-line inventory aid for pinned OpenCL completion and release calls

## Startup and inspection

Read the complete repository README first, then project state, research log, research ledger, and the latest detailed note. Inspected the current source-index implementation, unsupported-syntax tests, PR state, and the pinned OpenCL blob before editing.

## Artifact

Added `scripts/extract_opencl_lifecycle_calls.py` and `tests/test_extract_opencl_lifecycle_calls.py`.

The extractor reports exact 1-based source lines for this bounded API set:

- completion/submission: `clFinish`, `clFlush`, `clWaitForEvents`;
- release: `clReleaseCommandQueue`, `clReleaseContext`, `clReleaseProgram`, `clReleaseKernel`, `clReleaseEvent`, and `clReleaseMemObject`.

It emits source-ordered call records and per-name totals as JSON. This is deliberately separate from the approximate C++ symbol index.

## Verified

- The pinned OpenCL blob remains `f283f65690af7790e163092207647d16dac9fb3e`.
- Direct line-ranged connector reads still return empty content for hidden ranges, but blob retrieval confirms the file is available and exposes the already-audited `ggml_cl_buffer` destructor calling `clReleaseMemObject`.
- The new extractor preserves physical source lines and distinguishes direct calls from similar non-call identifiers.
- Focused tests cover completion, queue/context/program/kernel/event/buffer release, source ordering, and false-positive resistance for similar identifiers.

## Interpretation

A call-site inventory is not a teardown proof, but it converts the large-translation-unit access problem into a bounded extraction task once the pinned blob is available in a checkout or CI workspace. Human review must still establish ownership, error paths, ordering, and whether every queued command is complete before release.

## Historical

Previous runs repeatedly attempted to recover the hidden teardown portion through line-ranged connector reads. This increment stops depending on connector rendering and adds a reusable tool that can operate on the complete pinned file during source-index regeneration.

## Open questions

- Which functions own each discovered queue, context, program, kernel, event, and buffer release?
- Does backend teardown call `clFinish`, wait on events, or otherwise guarantee command completion before releasing resources?
- Are all Adreno binary-kernel library handles released independently of backend/scheduler lifetime?
- Should the bounded extractor later cover creation calls to pair acquisitions and releases?

## Validation

The focused tests are committed. GitHub-hosted Documentation CI remains the authoritative full validation path because direct GitHub DNS resolution is blocked for a local checkout.

## Next priority

Run the extractor against pinned `ggml-opencl.cpp` during source regeneration, review every completion/release site in context, and update the OpenCL teardown matrix. If pinned-source recovery remains blocked, implement the admitted CPU repack backend-free-before-buffer-free ASan/LSan fixture.
