# Research log

This is the concise chronological ledger. Detailed notes live under `logs/research/`.

## 2026-07-12 — Milestone 0/1 start

**Pinned baseline**

- Commit: `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- Purpose: reproducible source baseline; newer refs are indexed separately.

**Verified**

- The minimal example loads dynamic backends, loads the model, tokenizes, creates `llama_context`, decodes, samples, and feeds the next token back into the loop.
- Model loading constructs a loader and architecture-specific model, prepares devices, then loads hyperparameters, vocabulary, statistics, and tensors.
- mmap-deferred page faults are explicitly acknowledged in load-time accounting.

**Open questions**

- Complete graph-reuse predicates, memory-module selection, CPU work partitioning, backend combinations, and version-changing PRs.

## 2026-07-12 — Repository publication and durable scheduling context

**Verified**

- The root README is the scheduled-run operating manual.
- `scripts/start_scheduled_run.sh` reads README, project state, research log, ledger, and latest detailed note.
- CI includes hourly context validation, daily source-index refresh, strict documentation CI, and Pages deployment.

**Interpretation**

- Compact canonical state plus detailed per-run notes reduces context loss better than one unbounded README.

## 2026-07-12 01:54 Africa/Cairo — CI and Pages repair

**Verified**

- The corpus passed `mkdocs build --strict` in the repair environment.
- The interactive HTML asset had been omitted from the repository.
- Pages configuration could fail after a valid build when Pages was disabled.
- CI was separated from deployment; Pages enablement is detected; deployed content receives an HTTP/title check.

**Blocker**

- Pages still requires the one-time **Settings -> Pages -> Source: GitHub Actions** selection.

## 2026-07-12 02:51 Africa/Cairo — Decode and graph reuse

**Verified**

- `llama_decode()` delegates to `llama_context::decode()`.
- Decode prepares scheduler/memory state and processes `llama_ubatch` units.
- `process_ubatch()` reuses a graph only when all compatibility checks accept the new inputs.
- Pipeline-parallel reuse synchronizes before rewriting inputs.
- Rebuild resets graph/scheduler state, calls `model.build_graph()`, and allocates with `ggml_backend_sched_alloc_graph()`.
- `graph_compute()` selects the CPU threadpool and submits through the backend scheduler.

**Interpretation**

- Graph reuse preserves compatible topology/allocation, not token values or outputs.

## 2026-07-12 03:52 Africa/Cairo — Backend scheduler execution

**Verified**

- Allocation chooses a copy-ring slot, assigns backends, builds contiguous splits, and allocates destination copies/dependency views.
- Execution waits before reusing a destination slot, tries backend async copy, falls back to synchronized blocking copy, submits each split, and records events.
- Scheduler sync waits every backend.
- The pinned `MUL_MAT_ID` specialization copies only selected expert ranges.

**Interpretation**

- Copy-slot events are reuse fences.
- The MoE specialization is a transfer optimization, not a persistent expert cache.

## 2026-07-12 04:51 Africa/Cairo — CPU and CUDA semantics

**Verified**

- CPU graph compute blocks inside `ggml_graph_compute()` and leaves async-copy/event hooks unset.
- CUDA normally queues kernels or CUDA Graph launch without trailing stream synchronization.
- CUDA events create device-side ordering.
- Ordinary CUDA buffer operations may use async primitives internally but synchronize before return.

**Interpretation**

- CPU threadpool parallelism is not scheduler-level asynchrony.
- API names containing `async` do not prove host-visible overlap.

## 2026-07-12 05:50 Africa/Cairo — CUDA asynchronous copy branches

**Verified**

- The pinned callback requires CUDA backend objects and CUDA device buffers with consistent devices.
- Same-stream copies use D2D ordering; cross-stream same-device copies add source event/destination wait; peer devices use `cudaMemcpyPeerAsync` when enabled.
- CPU/mmap, CUDA-host, mixed backend, and device-mismatch pairs return `false`.
- Successful return means queued transfer/dependencies, not host-visible completion.

## 2026-07-12 06:49 Africa/Cairo — Metal backend semantics

**Verified**

- Ordinary Metal graph execution encodes and commits command buffers and returns without waiting.
- Async set/get/copy operations use retained blit command buffers.
- Metal-to-Metal copy signals a source event and queues a destination wait.
- Synchronization waits `cmd_buf_last`, checks all command-buffer status, releases completed extras, and preserves an error state after failure.

**Interpretation**

- Unified memory changes addressability and transfer cost, not completion or safe-reuse requirements.

## 2026-07-12 07:52 Africa/Cairo — Generic tensor-copy fallback

**Scope**

- Pinned generic path after backend asynchronous-copy capability is absent or rejects a tensor pair.

**Verified**

- `ggml_backend_tensor_copy_async()` synchronizes both source and destination backends before the blocking fallback.
- `ggml_backend_tensor_copy()` first uses a host-visible source pointer, then a host-visible destination pointer, then the destination buffer's optional direct `cpy_tensor` callback.
- If neither side is host-visible and direct copy fails, GGML allocates the full tensor size with `malloc()`, performs blocking source `get_tensor`, destination `set_tensor`, and frees the staging allocation.
- CPU/mmap-to-CUDA and CUDA-host-to-CUDA avoid the generic heap buffer because their source buffers are host-visible, but they still cross the synchronized blocking path.
- CPU/mmap-to-Metal likewise enters the destination `set_tensor` path after both backends have been synchronized.
- Fallback completion is stronger than accepted async submission: queued prior work is drained and the blocking copy has returned.

**Interpretation**

- Async rejection is a correctness-preserving serialization point that may remove overlap on both sides of a split.
- CPU/mmap accelerator copies can combine page faults, queue drains, and transfer latency.
- Unsupported device-to-device pairs can transiently duplicate the full tensor in pageable host memory.
- Avoiding generic heap staging does not imply zero-copy or asynchronous transfer.

**Historical**

- Newer revisions may add specialized transfers, reusable staging pools, or different event/ownership rules.

**Open questions**

- Exact destination-buffer `cpy_tensor` support matrix across CPU, CUDA, Metal, Vulkan, SYCL, RPC, and Android backends.
- Runtime page-fault, overlap, and temporary-RSS evidence for prefill and token decode.

**Artifacts changed**

- `docs/lifecycle/generic-copy-fallback.md`
- `mkdocs.yml`
- `docs/reference/project-state.md`
- `README.md`
- `logs/research/2026-07-12/0752-generic-copy-fallback.md`

**Next step**

- Trace concrete buffer-level `set_tensor`, `get_tensor`, and `cpy_tensor` implementations and build a backend buffer-pair compatibility matrix.

## 2026-07-12 08:52 Africa/Cairo — CPU, mmap, CUDA, and Metal buffer compatibility

**Scope**

- Concrete buffer-level host visibility, ownership, set/get, direct blocking copy, staging, and completion semantics.

**Verified**

- CPU and CPU_Mapped set/get operations are direct `memcpy()` calls.
- CPU_Mapped wraps an external aligned pointer and does not free it.
- CPU and CPU_Mapped report host visibility; CPU destination direct copy accepts host-visible sources.
- CUDA device buffers do not report host visibility.
- CUDA device set/get issue H2D/D2H copies and synchronize before returning.
- CUDA blocking direct copy accepts CUDA device sources, uses same-device or peer transfer, and synchronizes before return.
- Generic host-visible branches avoid full-tensor heap staging.
- Metal command-buffer/event ordering remains required independently of shared/private storage mode.

**Interpretation**

- `CPU_Mapped` is an addressability property, not a physical-residency guarantee.
- CPU_Mapped-to-accelerator transfer time can include mmap page faults and storage reads.
- Avoiding generic heap staging does not imply zero-copy or asynchronous overlap.

**Historical**

- Newer backends may add staging pools, registered-host paths, unified-memory specializations, or broader direct-copy support.

**Open questions**

- Exact Metal shared/private buffer-level branch table.
- Concrete Vulkan, SYCL, RPC, CANN, and Android-compiled-backend matrices.
- Runtime evidence for page faults, synchronization stalls, overlap, and temporary RSS.

**Artifacts changed**

- `docs/lifecycle/buffer-compatibility.md`
- `mkdocs.yml`
- `docs/reference/project-state.md`
- `README.md`
- `logs/research/2026-07-12/0852-buffer-compatibility.md`

**Next step**

- Trace Vulkan and SYCL buffer interfaces and extend the compatibility matrix.