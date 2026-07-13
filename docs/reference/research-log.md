# Research log

This is the concise chronological ledger. Detailed notes live under `logs/research/`.

## 2026-07-12 — Baseline, decode, scheduler, and backends

**Verified**

- Baseline pinned to `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- The minimal path loads backends/model, tokenizes, creates a context, decodes, samples, and feeds the next token back.
- Decode delegates to `llama_context::decode()`; graph reuse requires specialized compatibility checks.
- Scheduler allocation assigns backends, creates splits and copy-ring destinations, and execution uses events plus synchronized fallback copies.
- CPU, CUDA, Metal, Vulkan, and SYCL execution/buffer/copy semantics are documented.

**Interpretation**

- Reuse preserves compatible topology/allocation, not token values or outputs.
- CPU_Mapped addressability does not prove physical residency.

## 2026-07-12 — Documentation architecture and core objects

**Verified**

- Added the documentation-quality roadmap and six-tab foundations explorer.
- Published canonical `llama_context` and `llama_model` pages and linked their explorer entries.
- The context stores a non-owning model reference while owning mutable runtime state, scheduler resources, outputs, and memory modules.
- `llama_model` owns architecture/vocabulary state, persistent tensors, buffers, and retained mappings and dispatches architecture-specific graph construction.

## 2026-07-12 — GGUF, model placement, graph construction, and MoE

**Verified**

- Published canonical GGUF anatomy and model tensor-placement chapters.
- The loader computes absolute source offsets from the GGUF data-region offset plus tensor descriptor offset and validates bounds.
- Population paths include mapped alias, mapped copy/upload, direct read, asynchronous staging, and synchronous fallback.
- GGUF stores tensors and metadata, not an executable graph; architecture code rebuilds GGML operations over loaded tensors.

**Interpretation**

- `weights_map` joins physical GGUF layout to backend-aware tensor construction.
- Cache-aware routing should generally bias selection scores before top-k when expert weights should remain based on original probabilities.

## 2026-07-12 — Memory lifetimes and validation

**Verified**

- Published the memory-lifetime atlas and interactive owner/backing/validity/synchronization/release overlay.
- Mapping, allocation, residency, validity, command completion, and ownership are distinct states.
- Added static validation for local interactive routes and Markdown anchors, fixture tests, and Documentation CI integration.

## 2026-07-13 01:52 — Public API and minimal example Pass A

**Verified**

- Published `docs/architecture/public-api-minimal-example.md`.
- Mapped the public API, minimal example, facade, model, and context entry points.
- Documented construction, ownership, batch views, synchronization assumptions, errors, and teardown.

## 2026-07-13 02:51 — Model and GGUF loader Pass A

**Verified**

- Published `docs/architecture/model-gguf-loader-pass-a.md`.
- GGUF parsing uses `no_alloc=true`; split descriptors are merged before destination allocation.
- Buffer selection depends on expected operations and backend support.
- Cancellation is distinct from exception unwinding.

**Interpretation**

- The loader is a transactional bridge from temporary parse/I/O state into persistent model-owned storage.

## 2026-07-13 03:50 — Runtime context and memory Pass A

**Verified**

- Published `docs/architecture/runtime-context-memory-pass-a.md`.
- `llama_context` references the model and owns runtime backends, scheduler state, persistent memory, output buffers, graph-result caches, and the reusable batch allocator.
- `llama_memory_i` defines persistent memory behavior; `llama_memory_context_i` carries temporary ubatch state and `apply()` is the mutation boundary.
- Pending KV shifts/copies may be backend memory-update graphs and require synchronization before conflicting reuse or host state I/O.

**Interpretation**

- A per-batch memory context behaves like a transaction plan.
- Context memory is polymorphic, not one universal KV ring.

## 2026-07-13 05:52 — System ownership and execution synthesis

**Verified**

- Published `docs/architecture/system-ownership-and-execution-map.md`.
- The synthesis connects loader publication, persistent model storage, context runtime state, memory, graph construction, scheduler copies, execution, output visibility, and teardown.
- Ownership, addressability, residency, allocation, validity, and queued completion are distinct.

**Interpretation**

- `llama_model_loader` is a transactional publisher, `llama_context` is a mutable session around a borrowed model, and the scheduler is an execution planner.

## 2026-07-13 06:49 — Backend scheduler Pass A

**Verified**

- Published `docs/architecture/backend-scheduler-pass-a.md`.
- Inventoried assignment, splits, dependency copies, allocation, execution, synchronization, reset, and teardown.
- Scheduler copy allocation, current-generation validity, and previous-consumer completion are separate states.
- User inputs receive stricter lifetime handling; internal copies use async support or synchronized fallback.

**Interpretation**

- A scheduler copy is valid only for a particular source-value generation and copy slot.
- Events are reuse fences, not merely profiling markers.

## 2026-07-13 07:50 — Concrete context-memory implementations

**Verified**

- Published `docs/architecture/context-memory-implementations.md`.
- The pinned tree contains seven persistent implementations: ordinary KV, iSWA, DSA, DSV4, recurrent, hybrid, and hybrid-iSWA.
- Architecture predicates and no-memory branches are mapped exactly.
- DSV4 combines raw iSWA state, compressed K-only stores, and persistent compressor state.

**Interpretation**

- `create_memory()` acts as an architecture-to-state-machine compiler.
- “KV cache size” is not a universal metric for recurrent, hybrid, or compressed memory.

## 2026-07-13 08:50 — Model and context teardown order

**Verified**

- Published `docs/architecture/model-context-teardown-order.md` and added it to Architecture navigation.
- `llama_model::~llama_model()` explicitly deletes registered LoRA adapters; its `pimpl` owns retained mappings, lock objects, GGML tensor contexts, and backend buffers.
- `llama_model::impl` reverse destruction releases `ctxs_bufs`, then mapping locks, then retained mappings. Each context/buffer pair destroys backend buffers before its GGML metadata context.
- `llama_context::~llama_context()` reports scheduler allocation sizes and calls `ggml_opt_free(opt_ctx)` but contains no explicit `synchronize()` or `sched.reset()`.
- Reverse declaration order destroys device memory snapshots, output storage, graph results, metadata, and owning backend wrappers before the scheduler smart pointer; memory and adapters are destroyed later.
- The model reference and attached thread pools are borrowed and are not automatically freed by context destruction.

**Interpretation**

- The model `pimpl` is an RAII ownership capsule designed to keep file mappings alive until tensor buffers and metadata are gone.
- Applications should use an explicit synchronization boundary before destroying a context that may have queued accelerator work.
- Output pointers are borrowed views invalidated by output-buffer/context teardown.

**Historical**

- Declaration order, scheduler/backend deleters, and implicit synchronization behavior are revision-sensitive.

## 2026-07-13 09:49 — Scheduler core teardown dependencies

**Verified**

- Published `docs/architecture/scheduler-teardown-core.md` and added it to Architecture navigation.
- `ggml_backend_sched_free()` destroys scheduler events, then graph-allocation resources, then host scheduler metadata.
- The generic scheduler free path does not call `ggml_backend_sched_synchronize()`.
- `ggml_backend_event_free()` dispatches through the event's device interface.
- `ggml_gallocr_free()` releases scheduler-owned backend buffer chunks, whose generic wrapper invokes concrete `free_buffer` callbacks.
- The scheduler stores borrowed backend and buffer-type relationships and does not free the backend wrappers itself.

**Interpretation**

- Scheduler teardown requires device, buffer-type, allocator, queue, and callback state to remain valid beyond the lifetime of the scheduler struct itself.
- Explicit synchronization is a clear completion boundary, but it cannot repair a concrete backend object-lifetime violation.

## 2026-07-13 10:50 — Ordinary CPU backend teardown

**Verified**

- Published `docs/architecture/cpu-backend-teardown.md` and added it to Architecture navigation.
- CPU graph execution is synchronous; the ordinary CPU backend exposes no async tensor methods, synchronize callback, or events.
- The CPU device and device context are static registry objects that outlive individual backend wrappers.

**Interpretation**

- Backend-before-scheduler destruction is verified safe for the ordinary pinned CPU backend.

## 2026-07-13 11:49 — CUDA backend teardown

**Verified**

- Published `docs/architecture/cuda-backend-teardown.md` and added it to Architecture navigation.
- CUDA backend destruction deletes context-owned streams, events, cuBLAS handles, graph state, and wrapper state.
- Scheduler CUDA events and buffers retain device- or buffer-local state independent of the individual backend context.

**Interpretation**

- Backend-before-scheduler destruction is structurally independent for ordinary CUDA scheduler resources.
- Queued-work completion remains conditional because the pinned path lacks one explicit all-stream synchronization boundary before teardown.

## 2026-07-13 12:49 — Metal backend teardown

**Verified**

- Published `docs/architecture/metal-backend-teardown.md` and added it to Architecture navigation.
- `ggml_backend_metal_free()` explicitly synchronizes before releasing command buffers and Objective-C resources.
- Scheduler events and buffers retain device-level or buffer-local state.

**Interpretation**

- Backend-before-scheduler destruction is verified safe for ordinary pinned Metal resources.

## 2026-07-13 13:52 — Vulkan command and synchronization lifetimes

**Verified**

- Published `docs/architecture/vulkan-command-lifetime.md` and added it to Architecture navigation.
- Vulkan command pools are scoped per `(context, queue)` and `(device, queue)` pairing and track reusable command buffers.
- Synchronous read, copy, and memset helpers wait on a fence before recycling command-pool state.
- Binary semaphores, timeline semaphores, and Vulkan events are pooled.

**Interpretation**

- Command-pool reset is a reuse step after completion, not a synchronization mechanism.
- Graph compute submission does not itself imply host completion.

## 2026-07-13 14:50 — Vulkan backend teardown classification

**Verified**

- Published `docs/architecture/vulkan-backend-teardown.md` and added it to Architecture navigation.
- `ggml_backend_vk_free()` calls `ggml_vk_cleanup()` before deleting the Vulkan context and wrapper.
- Cleanup discards unsubmitted recording, explicitly calls `ggml_vk_synchronize()` for submitted work, and only then destroys graph synchronization state, temporary buffers, events, fences, descriptor pools, command pools, and transfer-queue synchronization objects.
- Scheduler Vulkan events are destroyed through persistent backend-device registry state and do not require the deleted per-backend context.
- Scheduler Vulkan buffers retain a buffer-local shared `vk_device` and `vk_buffer` and remain independently destructible.

**Interpretation**

- Backend-before-scheduler destruction is verified safe for the ordinary pinned Vulkan resources inspected in this audit.
- The Vulkan free path provides a stronger explicit completion boundary than the pinned CUDA-family path.

**Historical**

- Queue topology, transfer policy, event implementation, and device-registry lifetime are revision-sensitive.

**Open questions**

- The optional performance query pool is created/replaced during graph compute, but no explicit destruction call appeared in the inspected cleanup body.
- Immediate-destruction validation tests and full process-exit Vulkan device teardown remain to be audited.
