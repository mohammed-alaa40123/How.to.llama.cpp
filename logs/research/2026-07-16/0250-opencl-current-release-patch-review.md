# Current-upstream OpenCL release-only patch review

- Run time: 2026-07-16 02:50 Africa/Cairo
- Documentation branch: `automation/backend-teardown-audit-method`
- Current upstream revision: `505b1ed15ca80e2a19f12ff4ac365e40fb374053`
- Evidence workflow run: `29453611188`
- Evidence artifact: `8358479508`
- Machine-readable review: `data/opencl-current-event-release-review-505b1ed.json`

## Verified

The generated current-source patch contains exactly 46 insertions of:

```cpp
CL_CHECK(clReleaseEvent(evt));
```

Every insertion immediately follows the exact local statement:

```cpp
CL_CHECK(clWaitForEvents(1, &evt));
```

No wait, enqueue, read, conversion, or memory-object release is removed or reordered.

The 46 insertions split cleanly by enclosing function:

| Function | Insertions | Existing synchronization role |
|---|---:|---|
| `ggml_backend_opencl_buffer_set_tensor()` | 24 | Preserve synchronous conversion/expansion completion before ordinary tensor-set returns |
| `ggml_backend_opencl_buffer_get_tensor()` | 22 | Preserve the current explicit wait before the existing same-queue blocking read |

The post-patch lifecycle report records zero unmatched simple waited events while preserving all 51 direct `clWaitForEvents()` calls.

The complete insertion manifest records the current-source wait and insertion lines. It also verifies:

- `generated_insertions = 46`;
- `all_insertions_immediately_follow_matching_wait = true`;
- `waits_removed = 0`;
- `post_patch_unmatched_simple_waits = 0`;
- 24 synchronous set-completion sites;
- 22 blocking-read-follow-up sites.

## Interpretation

The explicit-release candidate is upstream-ready from an ownership and behavior-preservation perspective.

It is intentionally conservative:

```text
existing wait
    ↓
release the returned event reference
    ↓
continue with the original next statement
```

This fixes the command-event reference leak without changing the de facto synchronous `ggml_backend_tensor_set()` behavior and without combining ownership repair with the separate question of removing redundant readback waits.

A move-only event wrapper could reduce repetition, but introducing a new abstraction would enlarge the patch and obscure the narrow defect. For a first upstream correction, 46 explicit releases are easier to review because each change is local and mechanically paired with an existing wait.

## Historical

The pinned baseline and current upstream revision have the same bounded ownership shape: 46 unmatched simple waited-event references. The current source is 58 commits ahead of the baseline and has 165 changed OpenCL lines, so this review uses the regenerated current-source patch rather than textually rebasing the pinned patch.

## Open question

- Whether maintainers prefer the narrow explicit-release patch or a follow-up refactor introducing an event owner.
- Whether to submit the correction directly as a PR or open an issue first.
- Whether the 22 readback waits should later be removed in a separate optimization change; they remain untouched here.

## Upstream-ready PR summary

### Proposed title

`opencl: release command events after synchronous waits`

### Proposed body

The OpenCL tensor conversion and readback paths request command events from `clEnqueueNDRangeKernel()`, wait for them with `clWaitForEvents()`, and then leave the local scope without releasing the application-owned event reference.

This change adds `clReleaseEvent(evt)` immediately after each affected successful wait. It preserves every existing wait and therefore does not alter synchronization or the ordinary synchronous tensor-set behavior.

Audited at llama.cpp revision `505b1ed15ca80e2a19f12ff4ac365e40fb374053`:

- 51 direct `clWaitForEvents()` calls;
- 46 unmatched local count-one waited events before the fix;
- 46 event releases added;
- zero unmatched simple waited events after the fix;
- all 51 waits preserved.

The affected sites are limited to:

- 24 waits in `ggml_backend_opencl_buffer_set_tensor()`;
- 22 waits in `ggml_backend_opencl_buffer_get_tensor()`.

The patch changes event ownership only. Any future removal of waits before blocking reads should be reviewed separately.

## Validation

- Downloaded and extracted workflow artifact `8358479508`.
- Verified the artifact contains the exact current source, generated patch, baseline report, post-patch report, and checksum manifest.
- Counted 46 added `clReleaseEvent` statements in the generated patch.
- Matched every insertion to the immediately preceding local `clWaitForEvents(1, &evt)`.
- Classified all insertions by enclosing function and existing synchronization role.
- Confirmed the generated post-patch report reaches zero unmatched simple waited-event records without deleting waits.

## Next priority

Submit or stage the narrow current-source explicit-release patch upstream. Keep an event-wrapper refactor and any removal of redundant readback waits as separate follow-up changes.
