# Current-upstream OpenCL change-surface audit

- Run time: 2026-07-16 00:52 Africa/Cairo
- Documentation branch: `automation/backend-teardown-audit-method`
- Pinned baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream head inspected: `505b1ed15ca80e2a19f12ff4ac365e40fb374053`
- Scope: determine whether the generated 46-release correction can be treated as directly applicable to current upstream

## Verified

The current upstream head is 58 commits ahead of the pinned baseline, with the pinned revision as the merge base. Across that range, `ggml/src/ggml-opencl/ggml-opencl.cpp` changed by 165 lines: 106 additions and 59 deletions.

The latest upstream commit itself is OpenCL-specific and modifies the same translation unit. It adds Adreno A6x detection and disables selected Adreno MoE kernels on A6x, A7x, and unknown Adreno devices because some compilers miscompile the repack kernels. It does not present itself as event-lifetime work.

Recent OpenCL commits in the interval focus on:

- Adreno MoE-kernel eligibility;
- flash-attention compiler compatibility;
- OpenCL 2.x buffer creation;
- out-of-bounds and unaligned GEMV fixes;
- integer dot-product feature gating;
- Adreno dense and MoE prefill optimizations;
- Q6_K layout/alignment handling.

The current source blob is still the same large `ggml-opencl.cpp` translation unit and retains the pinned fatal `CL_CHECK` macro shape. However, the connector could not expose the complete 24,576-line blob as a locally processable file in this run, so the exact current counts of `clWaitForEvents()` and `clReleaseEvent()` were not recomputed.

## Interpretation

The pinned 46-release patch must not be declared current-upstream-ready merely because no recent commit title mentions event ownership. The OpenCL file has changed enough that line-based patch application is unsafe, and the recent Adreno/MoE work overlaps the same `set_tensor` and kernel-selection area audited in the baseline.

The correct rebase unit is semantic rather than textual:

```text
current exact source
    -> rerun lifecycle extractor
    -> pair waited events
    -> preserve required synchronization
    -> generate releases from current unmatched records
    -> validate zero unmatched simple events
```

The compare result narrows the problem: only 58 commits separate the baseline from current head, and the OpenCL translation unit changed by 165 lines. A current-source CI audit is therefore bounded and preferable to manually rebasing 46 insertions.

## Historical

The pinned baseline has 51 direct waits, of which 46 local command-event references lack release or ownership transfer. The repository already generates and validates a behavior-preserving release-only patch for that exact revision.

## Open question

- Does current head `505b1ed15ca80e2a19f12ff4ac365e40fb374053` still contain the same 46 unmatched simple events?
- Did the 165-line OpenCL diff add, remove, or relocate any waited-event sites?
- Should the existing evidence workflow gain a second, non-pinned current-upstream job that records counts without freezing them until human review?
- If the current leak remains, should the correction be submitted as explicit releases or as a small event owner?

## Validation

- Read the complete README, project state, research log, research ledger, and latest detailed note before editing.
- Resolved the current llama.cpp head and exact commit metadata.
- Compared the pinned baseline to current head and inspected the OpenCL file-level change count.
- Reviewed recent OpenCL commit subjects and the exact latest OpenCL commit diff.
- Confirmed PR #1 remains open and mergeable before this increment.

## Blocker

The GitHub connector returned the current source blob metadata and an initial content window but could not provide the complete large blob as a downloadable local file. Direct raw-file access and local cloning also failed because GitHub DNS resolution is unavailable in the runtime. Therefore, this increment records a verified change-surface audit but does not claim a current leak count.

## Next priority

Extend the OpenCL evidence workflow with a current-upstream audit job that fetches an explicit resolved master SHA, reruns the existing lifecycle extractor and release generator, uploads the exact current source and JSON evidence, and reports counts without treating them as a frozen regression until reviewed.