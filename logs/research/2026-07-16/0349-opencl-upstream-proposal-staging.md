# OpenCL upstream proposal staging

- Run time: 2026-07-16 03:49 Africa/Cairo
- Documentation branch: `automation/backend-teardown-audit-method`
- Audited llama.cpp revision: `505b1ed15ca80e2a19f12ff4ac365e40fb374053`
- Evidence workflow run: `29453611188`
- Evidence artifact: `8358479508`
- Staged proposal: `docs/reference/upstream-opencl-event-release-proposal.md`

## Verified

The required startup sequence was completed before editing: the complete root README, project state, concise research log, research ledger, and latest detailed note were read. Current repository state and PR #1 metadata were inspected.

The exact workflow artifact was downloaded and extracted. It contains the current OpenCL translation unit, lifecycle reports, checksum manifest, generated fixed source, and the 370-line release-only patch.

The generated patch contains 46 additions of:

```cpp
CL_CHECK(clReleaseEvent(evt));
```

All existing waits remain. The previously reviewed split remains 24 set-tensor sites and 22 get-tensor sites.

A duplicate search across open llama.cpp issues and all pull requests for `OpenCL clReleaseEvent clWaitForEvents event leak` returned no matching item.

The current llama.cpp head returned by the connector remains `505b1ed15ca80e2a19f12ff4ac365e40fb374053`, so the staged proposal still targets the exact current source used by the generated patch.

An attempt to create the upstream issue through the connected GitHub App failed with HTTP 403:

```text
Resource not accessible by integration
```

The complete issue and pull-request wording was therefore committed as `docs/reference/upstream-opencl-event-release-proposal.md` so it is reviewable and ready for manual submission or a future connector with write access.

## Interpretation

The bounded increment is complete: the project now contains a durable upstream-contribution package rather than only an internal research note. It includes the target revision, evidence counts, ownership/synchronization separation, proposed issue title/body, proposed PR title/body, and the exact permission blocker.

Creating the upstream issue automatically is blocked by integration permissions, not by unresolved technical evidence. The proposal should be submitted manually or through a GitHub identity with issue/PR write access to `ggml-org/llama.cpp`.

## Historical

The preceding run completed insertion-by-insertion review of the generated patch. This run moves that result into a dedicated upstream-facing artifact and verifies there is no obvious duplicate issue or PR under the searched terms.

## Open questions

- Whether maintainers prefer an issue first or a direct pull request.
- Whether a writable fork should carry the generated patch before submission.
- Whether the 22 readback waits should later be removed in a separate optimization.

## Validation

- Re-downloaded workflow artifact `8358479508`.
- Confirmed the artifact is unexpired and its published digest remains `sha256:e2293f8a6aeaaa173c0430f4714d0b83ac564c7e2250298b9a7863338a84c30d`.
- Extracted eight evidence files.
- Confirmed the generated patch is 370 lines and 16,725 bytes.
- Inspected the patch and verified it is addition-only around the existing waits.
- Searched llama.cpp issues and pull requests for an obvious duplicate.

## Publication and blockers

- Added `docs/reference/upstream-opencl-event-release-proposal.md` in commit `1c5e46faa247eeb28403dd3e3db284f91a3dd772`.
- Upstream issue creation is blocked by GitHub App permissions: HTTP 403 `Resource not accessible by integration`.
- Local checkout validation remains blocked by `Could not resolve host: github.com`.
- The README, project-state, and concise research-log updates still require patch-capable repository access; the connector only supports complete-file replacement for existing files.
- Pages verification remains blocked for branch-only content until PR #1 merges.

## Next priority

Submit the staged proposal manually or through a writable fork/identity. If upstream submission remains blocked, implement the first admitted CPU repack `MUL_MAT` lifetime fixture under ASan/LSan rather than repeating the OpenCL ownership analysis.
