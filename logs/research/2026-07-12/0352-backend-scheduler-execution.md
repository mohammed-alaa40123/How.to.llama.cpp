# Backend scheduler split execution

- Run time: 2026-07-12 03:52 Africa/Cairo
- Upstream baseline: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: scheduler backend assignment, split construction, destination copies, event ordering, split submission, and synchronization

## Verified

- `ggml_backend_sched_alloc_graph()` selects `cur_copy`, advances `next_copy`, splits the graph, and allocates the augmented scheduler graph.
- Backend assignment is multi-pass and asserts that the final backend is CPU.
- A split is a contiguous graph interval, not a global grouping of all nodes assigned to one backend.
- New splits begin when backend placement changes and may also begin to reduce incompatible weight-copy lifetimes or avoid exceeding the split-input limit.
- Cross-backend sources receive destination-layout copies for each copy slot. Dependency views keep source storage alive; early copy nodes ensure destination storage is allocated before split execution.
- `ggml_backend_sched_compute_splits()` waits before overwriting the active copy slot, tries backend asynchronous tensor copy, and falls back to synchronized copy when necessary.
- User input tensors are copied immediately after synchronizing the destination slot so caller-owned memory cannot be overwritten before capture.
- Each split is submitted with `ggml_backend_graph_compute_async()` and records an event for the active backend/copy slot.
- `ggml_backend_sched_graph_compute()` synchronizes all registered backends after asynchronous submission.
- Host-resident `MUL_MAT_ID` weights use a specialized path that reads routing IDs and copies only selected consecutive expert ranges.

## Interpretation

- Copy-slot events are storage-reuse fences, not only performance markers.
- Scheduler-created destination tensors are temporary execution storage, not persistent model-owned weight replicas.
- The MoE path is a transfer-volume optimization rather than a long-lived expert cache.
- Scheduler-level asynchronous submission permits overlap but does not prove that a concrete backend implements asynchronous execution.

## Open questions

- Which pinned backend interfaces provide real asynchronous graph submission, peer copies, and device events?
- How do CPU threadpool completion, CUDA events/streams, Metal command buffers, Vulkan queues, SYCL queues, and RPC transport differ?
- Which later PRs materially changed event ordering or MoE partial-copy behavior?
- What prompt/decode overlap is measurable on representative hardware?

## Artifact

- `docs/lifecycle/backend-scheduler-execution.md`
- `mkdocs.yml`

## Evidence

- `ggml/src/ggml-backend.cpp`
  - `ggml_backend_sched_split_graph()`
  - `ggml_backend_sched_alloc_splits()`
  - `ggml_backend_sched_compute_splits()`
  - `ggml_backend_sched_alloc_graph()`
  - `ggml_backend_sched_graph_compute_async()`
  - `ggml_backend_sched_synchronize()`

## Validation plan

- Project context validator
- Python syntax compilation
- shell syntax checking
- strict MkDocs build
- GitHub Actions workflow inspection
- Pages HTTP/title check
