# Research log

This is the concise chronological ledger. Detailed notes live under `logs/research/`.

## 2026-07-12 — Milestone 0/1 start

**Verified**

- Baseline pinned to `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- The minimal example loads backends and a model, tokenizes, creates `llama_context`, decodes, samples, and feeds the next token back.
- Model loading dispatches architecture-specific construction, device preparation, metadata, vocabulary, statistics, and tensors.
- Load-time accounting explicitly acknowledges mmap-deferred page faults.

**Open questions**

- Complete graph-reuse predicates, memory-module selection, CPU work partitioning, backend combinations, and version-changing PRs.

## 2026-07-12 — Repository publication and durable scheduling context

**Verified**

- The root README is the scheduled-run operating manual.
- The startup script reads README, project state, research log, source ledger, and latest detailed note.
- CI includes hourly context validation, daily source indexing, strict documentation CI, and Pages deployment.

**Interpretation**

- Compact canonical state plus detailed per-run notes reduces context loss better than one unbounded README.

## 2026-07-12 01:54 Africa/Cairo — CI and Pages repair

**Verified**

- The corpus passed `mkdocs build --strict` in the repair environment.
- The interactive HTML asset had been omitted.
- CI was separated from deployment; Pages enablement is detected and deployed content receives an HTTP/title check.

**Blocker**

- Pages requires **Settings -> Pages -> Source: GitHub Actions**.

## 2026-07-12 02:51 Africa/Cairo — Decode and graph reuse

**Verified**

- `llama_decode()` delegates to `llama_context::decode()`.
- Decode prepares scheduler/memory state and processes `llama_ubatch` units.
- Graph reuse requires all specialized compatibility checks to accept new inputs.
- Pipeline-parallel reuse synchronizes before rewriting inputs.
- Rebuild resets graph/scheduler state, calls `model.build_graph()`, and allocates through the backend scheduler.
- `graph_compute()` selects the CPU threadpool and submits through the scheduler.

**Interpretation**

- Reuse preserves compatible topology and allocation, not token values or outputs.

## 2026-07-12 03:52 Africa/Cairo — Backend scheduler execution

**Verified**

- Allocation selects a copy-ring slot, assigns backends, builds contiguous splits, and allocates destination copies and dependency views.
- Execution waits before slot reuse, tries backend async copy, falls back to synchronized blocking copy, submits splits, and records events.
- Scheduler synchronization waits every backend.
- The pinned `MUL_MAT_ID` specialization copies only selected expert ranges.

**Interpretation**

- Copy-slot events are reuse fences.
- The MoE specialization reduces transfer volume but is not a persistent expert cache.

## 2026-07-12 04:51 Africa/Cairo — CPU and CUDA semantics

**Verified**

- CPU graph compute blocks inside `ggml_graph_compute()` and exposes no scheduler async-copy/event hooks.
- CUDA normally queues kernels or CUDA Graph launch without trailing stream synchronization.
- CUDA events provide device-side ordering.
- Ordinary CUDA buffer operations may use async primitives internally but synchronize before return.

**Interpretation**

- CPU threadpool parallelism is not scheduler-level asynchrony.
- An API name containing `async` does not prove host-visible overlap.

## 2026-07-12 05:50 Africa/Cairo — CUDA asynchronous copy branches

**Verified**

- The callback requires CUDA backend objects and CUDA device buffers with consistent devices.
- Same-stream copies use D2D ordering; cross-stream same-device copies add source event and destination wait; peer copies use `cudaMemcpyPeerAsync` when enabled.
- CPU/mmap, CUDA-host, mixed-backend, and device-mismatch pairs return `false`.
- Success means queued transfer and dependencies, not host-visible completion.

## 2026-07-12 06:49 Africa/Cairo — Metal backend semantics

**Verified**

- Ordinary Metal graph execution encodes and commits command buffers and returns without waiting.
- Async set/get/copy operations use retained blit command buffers.
- Metal-to-Metal copy signals a source event and queues a destination wait.
- Synchronization waits the last command buffer, checks status, releases completed extras, and preserves error state.

**Interpretation**

- Unified memory changes addressability and transfer cost, not completion or safe-reuse requirements.

## 2026-07-12 07:52 Africa/Cairo — Generic tensor-copy fallback

**Verified**

- Rejected or unavailable async copy synchronizes both source and destination backends.
- Blocking copy checks host-visible source, host-visible destination, destination direct-copy callback, then full `malloc -> get -> set -> free` staging.
- CPU/mmap-to-CUDA, CUDA-host-to-CUDA, and CPU/mmap-to-Metal avoid generic full-size heap staging but remain synchronized blocking paths.

**Interpretation**

- Async rejection is a correctness-preserving serialization point.
- File-backed accelerator copies can combine page faults, queue drains, and transfer latency.
- Avoiding generic heap staging does not imply zero-copy or overlap.

## 2026-07-12 08:52 Africa/Cairo — CPU, mmap, CUDA, and Metal buffer compatibility

**Verified**

- CPU and CPU_Mapped set/get are direct `memcpy()` operations and report host visibility.
- CPU_Mapped wraps an external pointer and does not free it.
- CUDA device buffers are not host-visible; set/get/direct-copy functions synchronize before return.
- CUDA blocking direct copy accepts same-device or peer CUDA-device sources.
- Metal command-buffer/event ordering remains required independently of storage mode.

**Interpretation**

- CPU_Mapped is an addressability property, not a physical-residency guarantee.
- CPU_Mapped accelerator transfers can include mmap faults and storage reads.

## 2026-07-12 09:11 Africa/Cairo — Backend scheduler figure repair

**Verified**

- Mermaid 11 displayed a syntax error for the scheduler sequence.
- The block was replaced with an accessible static SVG preserving allocation, split execution, async return, and later synchronization.

**Open question**

- Audit other complex Mermaid diagrams for renderer-specific failures.

## 2026-07-12 09:49 Africa/Cairo — Vulkan capability boundary

**Verified**

- Default Vulkan buffers leave `.is_host` unset.
- Vulkan advertises asynchronous execution, a dedicated host-buffer type, and events.
- Event state combines Vulkan events with timeline-semaphore-backed host synchronization.
- Graph execution inserts internal synchronization for overlapping hazardous tensor regions.

**Interpretation**

- Dedicated host-buffer support is distinct from device-buffer host visibility.
- Vulkan graph hazards and cross-backend scheduler ordering protect different boundaries.

## 2026-07-12 10:52 Africa/Cairo — Vulkan transfer path

**Verified**

- Vulkan memory-property preferences depend on UMA, host-memory preference, host-visible-VRAM policy, and system-memory fallback.
- Blocking writes use mapped coherent memory or staging plus a fence wait.
- Blocking reads use a host-read barrier on mapped UMA memory or staging plus a fence and deferred CPU copy.
- Same-device blocking copies wait a fence; cross-device copies stage through host-visible memory.
- Scheduler async copy accepts same-device Vulkan-device and Vulkan-registered-host sources, but rejects ordinary CPU/mmap and cross-device Vulkan sources.
- Backend async set/get remains queued only for registered host pointers; ordinary host pointers synchronize staging before return.

**Interpretation**

- Vulkan registration, not generic host visibility, enables queued host-to-device scheduler copies.
- UMA can remove staging without removing barrier and fence requirements.

## 2026-07-12 11:49 Africa/Cairo — SYCL buffer and transfer semantics

**Scope**

- Pinned SYCL device, optional system-USM, and host allocations; blocking and backend-async operations; cross-device copy fallbacks; scheduler callback registration.

**Verified**

- Default SYCL buffers allocate device memory unless large system-USM mode is enabled, the allocation is at least 1 GiB, and the device reports system-USM support.
- Default and split buffer types report `is_host == false`, including optional system-USM-backed allocations.
- The dedicated SYCL host-buffer type wraps aligned host memory with CPU operations and host visibility, falling back to ordinary CPU allocation on failure.
- Blocking `set_tensor` waits device queues; non-Windows builds make a full temporary host copy before the waited host-to-device copy as an mmap/PVC workaround.
- Blocking `get_tensor` waits the device-to-host queue copy.
- Direct SYCL-device copy waits both devices and uses Level Zero, SYCL peer access, or full host-forward staging.
- Backend async set/get callbacks enqueue stream-zero copies without waiting; backend synchronization waits that stream.
- A `ggml_backend_sycl_cpy_tensor_async()` helper exists, but the pinned backend interface explicitly installs `.cpy_tensor_async = NULL`.
- Scheduler graph-split tensor copies therefore take the synchronized generic fallback even for same-device SYCL buffers.

**Interpretation**

- System USM changes allocation mechanics but not the public GGML host-visibility contract.
- Non-Windows GGUF loading can combine mmap page faults, a full CPU copy, temporary RSS equal to the tensor, a device transfer, and a queue wait.
- Queue-based async set/get support does not imply scheduler tensor-to-tensor copy overlap.
- Peer access can avoid host staging while the blocking callback still establishes completion before return.

**Historical**

- These findings apply to `e3546c7948e3af463d0b401e6421d5a4c2faf565`; later revisions may register a replacement async-copy callback or change staging and dependency behavior.

**Open questions**

- Which revision first restores scheduler-level SYCL tensor-copy asynchrony.
- Whether the mmap/PVC staging workaround remains required on current runtimes.
- Runtime page-fault, temporary-RSS, queue-wait, and Level Zero versus OpenCL behavior.

**Artifacts changed**

- `docs/lifecycle/sycl-buffer-capabilities.md`
- `mkdocs.yml`
- `README.md`
- `docs/reference/project-state.md`
- `docs/reference/research-log.md`
- `logs/research/2026-07-12/1149-sycl-buffer-semantics.md`

**Validation**

- Connector-side reads verified the pinned allocation, buffer, copy, synchronization, and interface-registration branches.
- Local clone and strict MkDocs validation remain blocked because the execution environment cannot resolve `github.com`.
- Connected status interfaces returned no workflow runs for the latest commit, and the Pages site remains unverified until Pages is enabled.

**Next step**

- Add exact SYCL rows to the shared compatibility matrix and compare the first later upstream revision that restores scheduler async tensor copying.
