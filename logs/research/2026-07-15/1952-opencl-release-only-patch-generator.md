# OpenCL release-only event patch generator

- Run time: 2026-07-15 19:52 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Pinned source: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: convert the 46-site ownership audit into a behavior-preserving generated patch and CI proof

## Verified

Added `scripts/apply_opencl_event_release_fix.py`. The tool consumes the exact pinned source and its generated lifecycle report, then inserts:

```cpp
CL_CHECK(clReleaseEvent(evt));
```

immediately after every simple waited-event record classified as `unmatched_in_scope`.

The transformation is deliberately bounded:

1. It uses the exact `wait_line` and event identifier from the report.
2. It verifies that the source line still contains `clWaitForEvents(1, &event)`.
3. It rejects duplicate records for one line, stale line mappings, empty unmatched sets, and unexpected fix counts.
4. It preserves all waits and surrounding synchronization.
5. It can emit both a patched source file and a unified patch against `ggml/src/ggml-opencl/ggml-opencl.cpp`.

The pinned workflow now generates the release-only patch and re-runs lifecycle extraction over the patched source. Its acceptance contract is:

```text
50 simple identifier waits released in scope
0 simple identifier waits unmatched in scope
51 direct clWaitForEvents calls preserved
52 direct clReleaseEvent calls total
46 generated insertions
```

The existing baseline report remains unchanged and still records the reviewed ownership and synchronization split:

```text
4 released / 46 unmatched simple identifier waits
22 unmatched before same-queue blocking reads / 24 other unmatched
```

Focused unit tests cover insertion, preservation of indentation, already-released input rejection, stale line rejection, and duplicate-line rejection.

## Interpretation

This is a behavior-preserving patch generator, not yet an upstream submission. It closes the application-owned event-reference leaks while intentionally retaining every existing completion point. That separation keeps ownership repair independent from the later performance-oriented removal of 22 waits already proven redundant before blocking reads.

Generating the patch from the audited report reduces the risk of manually missing one of 46 repetitive sites. The strict source-line check also makes baseline drift visible rather than silently applying edits to the wrong location.

## Historical

The previous run made the 22/24 synchronization classification machine-readable. Before this increment, the proposed release-only correction existed only as a plan. The repository can now generate the concrete unified patch and prove the expected post-patch ownership counts in GitHub Actions.

## Open questions

- Whether upstream would prefer 46 explicit releases or a move-only event owner introduced in a separate refactor.
- Whether the generated patch should be proposed directly against the pinned historical revision or rebased onto current upstream after re-auditing changed sites.
- Which of the remaining 24 non-blocking-read waits are required by the backend `set_tensor` completion contract.
- Whether the 22 redundant waits should be removed in a second patch after the release-only correction lands.

## Validation

- Prior branch head `3a8bc45e134f291114cdfd9da954aa4840e3de45` passed Documentation CI run `29430361648` and pinned OpenCL report run `29430360856`.
- The source-bearing artifact from run `29430360856` contained the expected 46 unmatched simple waits and 22/24 follow-up split.
- Local patch generation against the preserved pinned source produced 46 insertions; `git apply --check` succeeded; the patched source retained 51 waits and contained 52 direct event-release calls.
- Final-head GitHub Actions results are checked separately after all durable-context updates.

## Next priority

Classify the remaining 24 waits against `set_tensor` return semantics and subsequent same-queue consumers, then decide whether to submit the generated release-only patch upstream before any synchronization cleanup.
