# OpenCL `set_tensor` unresolved-wait grouping

- Run time: 2026-07-15 20:51 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Pinned source: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: turn the remaining 24 non-blocking-read waits into a reproducible lexical classification

## Verified

Added `scripts/classify_opencl_set_tensor_waits.py` and focused tests. The tool consumes the exact pinned OpenCL source and lifecycle report, excludes records already released or already classified as immediately followed by a same-queue blocking read, and classifies the next lexical statement.

The pinned result is:

```text
24 unresolved non-blocking-read waits
  21 → immediately followed by clReleaseMemObject(data_device)
   3 → nested scope exit
```

All 24 records are inside `ggml_backend_opencl_buffer_set_tensor()`.

The 21 `temporary_upload_buffer_release` sites wait for a conversion kernel and then release the temporary `data_device` input object. Under the already-reviewed OpenCL memory-object contract, queued commands retain memory objects they use, so the wait is not required merely to make `clReleaseMemObject(data_device)` safe.

The three `nested_scope_exit` sites wait for secondary expansion kernels. They do not release `data_device` on the next statement and therefore require separate caller/return-contract analysis rather than being grouped with temporary-input release.

Focused tests cover the two recognized groups, exclusion of released and blocking-read records, enclosing-function reporting, and an explicit `other` fallback.

## Interpretation

This narrows the synchronization question without claiming that 21 waits can immediately be removed. Their temporary-input lifetime justification is eliminated, but output readiness at synchronous `ggml_backend_tensor_set()` return remains a separate contract question.

The pinned public header distinguishes synchronous `ggml_backend_tensor_set()` from `ggml_backend_tensor_set_async()`, but it does not explicitly state whether a synchronous set must leave every device-side format-conversion kernel complete or only guarantee that caller-owned host input can be reused after return. The OpenCL backend exposes no async set callback, so removing waits requires a deliberate contract decision rather than relying only on same-queue ordering.

## Historical

The previous run generated a behavior-preserving patch that releases all 46 leaked event references while preserving every wait. Earlier analysis had split those waits into 22 immediate blocking-read cases and 24 other cases. This increment makes the second group reproducible and separates temporary-input release from scope-exit completion.

## Open questions

- Does the synchronous backend tensor-set contract require converted device output to be complete before return?
- Can the 21 temporary-input-release waits be removed while preserving host-input reuse and all later same-queue consumers?
- What exact operations follow the three nested-scope waits, and do two of them intentionally make an early-return branch synchronous?
- Should the classifier be added to the pinned workflow only after the semantic labels are reviewed and frozen?

## Validation

- `python3 -m unittest -v test_classify_opencl_set_tensor_waits.py`: 3 tests passed locally.
- Running the classifier against the exact source-bearing workflow artifact produced 24 records: 21 `temporary_upload_buffer_release`, 3 `nested_scope_exit`, 0 `other`.
- The prior branch head `37420fc514237ad357b174122c306c838a22877f` passed Documentation CI run `29434609772` and pinned OpenCL lifecycle run `29434609672`.
- New-head workflow results must be checked after the repository commits are complete.

## Next priority

Trace the three nested-scope waits and establish the synchronous tensor-set completion contract. Keep the already-generated release-only ownership patch independent from any synchronization-removal patch.
