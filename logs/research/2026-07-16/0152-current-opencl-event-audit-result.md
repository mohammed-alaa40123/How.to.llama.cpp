# Current-upstream OpenCL event audit result

- Run time: 2026-07-16 01:52 Africa/Cairo
- Documentation branch: `automation/backend-teardown-audit-method`
- Current upstream revision: `505b1ed15ca80e2a19f12ff4ac365e40fb374053`
- Workflow run: `29453611188`
- Evidence artifact: `opencl-lifecycle-current-upstream` (`8358479508`)
- Artifact digest: `sha256:e2293f8a6aeaaa173c0430f4714d0b83ac564c7e2250298b9a7863338a84c30d`

## Verified

The first current-upstream lifecycle audit completed successfully and preserved the exact OpenCL translation unit, lifecycle JSON, generated release-only patch, post-patch report, summary, and checksum manifest.

The current source reports the same bounded ownership shape as the pinned baseline:

| Metric | Current upstream |
|---|---:|
| Direct `clWaitForEvents()` calls | 51 |
| Direct `clReleaseEvent()` calls | 6 |
| Simple identifier waits | 50 |
| Released in the same scope | 4 |
| Unmatched in the same scope | 46 |
| Unmatched before same-queue blocking reads | 22 |
| Other unmatched waits | 24 |

The generated current-source release-only candidate inserts 46 releases and the post-patch report contains zero unmatched simple waited-event records. It preserves all waits and therefore does not change synchronization.

The direct lifecycle counts are also unchanged from the pinned report for the audited APIs: one context creation, one command-queue creation, 11 finishes, one flush, 23 kernel releases, 121 program releases, and 343 memory-object releases.

## Interpretation

The event-reference leak remains present at current upstream revision `505b1ed1`. The correction is still semantically applicable, but the upstream-ready artifact should be the patch generated from the exact current source rather than a textual application of the pinned patch.

The unchanged 22/24 split is strong evidence that recent OpenCL changes did not alter the reviewed synchronization categories. The release-only patch can therefore preserve the de facto synchronous tensor-set contract while fixing ownership independently.

## Historical

The pinned baseline `e3546c7948e3af463d0b401e6421d5a4c2faf565` first established 51 direct waits and 46 unmatched local command-event references. Current upstream is 58 commits ahead, yet the bounded counts remain identical.

## Open question

- Should the upstream contribution use 46 explicit `clReleaseEvent(evt)` calls or introduce a small move-only event owner?
- Should the correction be submitted directly as a pull request or first as an issue describing the measured current and pinned evidence?
- Should the public backend API document the ordinary tensor-set completion contract before any later wait-removal optimization is considered?

## Validation

- Read the complete README, project state, research log, research ledger, and latest detailed note before editing.
- Inspected the current-audit workflow implementation and final artifact.
- Verified the artifact checksum digest and exact resolved upstream SHA from GitHub Actions metadata.
- Confirmed the current release-only candidate reaches zero unmatched simple waits without removing synchronization.
- Confirmed final-head Documentation CI, pinned OpenCL lifecycle, and current-upstream OpenCL lifecycle runs all passed before this update.

## Next priority

Extract the generated current-source patch from artifact `8358479508`, review its 46 insertions for upstream style and branch context, and prepare an upstream-ready pull request or issue while preserving every existing wait.
