# OpenCL transpose call-site audit

- Run time: 2026-07-15 12:49 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Pinned source: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: every call to `transpose_2d()`, `transpose_2d_as_8b()`, `transpose_2d_as_16b()`, and `transpose_2d_as_32b()` in pinned `ggml/src/ggml-opencl/ggml-opencl.cpp`

## Verified

The complete source-bearing Actions artifact was downloaded from successful workflow run `29402771146` (artifact `8337746583`) and inspected locally.

`transpose_2d()` and its three typed wrappers expose `bool blocking = true`. A balanced-parenthesis call-site scan found:

- 8 calls to `transpose_2d_as_8b()`;
- 42 calls to `transpose_2d_as_16b()`;
- 3 calls to `transpose_2d_as_32b()`;
- no direct external calls to `transpose_2d()` beyond the three wrappers;
- **zero call sites that pass `false`**;
- all 53 typed-wrapper calls omit the final argument and therefore use `blocking=true`.

Every reachable pinned caller therefore follows:

```text
transpose kernel enqueue
  -> copy enqueue with event
  -> clWaitForEvents(copy event)
  -> clReleaseEvent
  -> clReleaseMemObject(trans)
  -> return to caller only after copy completion
```

The previously analyzed `blocking=false` branch exists in source but is not reachable from any pinned call site.

## Interpretation

For the pinned revision, caller-side synchronization tracing for `transpose_2d(..., false)` is unnecessary because that mode has no callers. The live behavior is stronger than the local retention-only argument: all current callers wait for the copy to finish before the helper returns and before the temporary sub-buffer reference is released.

The nonblocking branch remains locally safe under OpenCL command-retention rules, but it should be documented as **dormant capability**, not as an active execution path.

The exposed boolean adds review surface without current use. A future cleanup could remove the parameter and branch, or add a regression test that explicitly records whether nonblocking use is introduced.

## Historical

The preceding case study correctly classified the nonblocking branch in isolation, then left caller tracing open. Complete-source inspection now closes that question by proving the pinned tree never selects the branch.

## Open questions

- Did a historical or newer llama.cpp revision use `blocking=false`, explaining why the branch remains?
- Should source-index or lifecycle tooling emit dormant-branch/call-site summaries for bounded helpers with constant default arguments?
- Which temporary quantization image or sub-buffer release group should be classified next?

## Next priority

Classify one temporary quantization image/sub-buffer release group, separating explicit wait-before-release, same-queue command retention, host-storage lifetime, and cross-queue dependencies.
