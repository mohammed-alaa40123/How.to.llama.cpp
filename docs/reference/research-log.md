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

**Open questions**

- Whether every pinned scheduler/backend deleter safely tolerates owning backend wrapper destruction before scheduler destruction.
- Which backend frees synchronize implicitly and which require caller synchronization.
- Whether stress tests cover immediate context destruction after asynchronous graph submission.

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

**Open questions**

- Whether each concrete backend keeps device and buffer-deleter state valid after its backend wrapper is freed.
- Which event and buffer destructors require live streams, queues, allocators, or backend contexts.
- Whether backend wrapper free synchronizes or invalidates scheduler-owned resources.

## 2026-07-13 10:50 — Ordinary CPU backend teardown

**Verified**

- Published `docs/architecture/cpu-backend-teardown.md` and added it to Architecture navigation.
- CPU graph execution calls `ggml_graph_compute()` synchronously before returning.
- The ordinary CPU backend exposes no async tensor methods, synchronize callback, or event record/wait callbacks.
- The CPU device advertises `async = false` and `events = false`; its event callbacks are null.
- The CPU device and device context are static registry objects that outlive individual backend wrappers.
- `ggml_backend_cpu_free()` deletes only the backend work allocation, CPU context, and wrapper.

**Interpretation**

- Scheduler-owned ordinary CPU buffers remain independently destructible after backend-wrapper deletion.
- Backend-before-scheduler destruction is verified safe for the ordinary pinned CPU backend.

## 2026-07-13 11:49 — CUDA backend teardown

**Verified**

- Published `docs/architecture/cuda-backend-teardown.md` and added it to Architecture navigation.
- `ggml_backend_cuda_free()` deletes the CUDA context and then the backend wrapper.
- The CUDA context destructor waits for active graph capture to finish, then destroys its copy event, streams, and cuBLAS handles without an explicit general stream synchronization call.
- CUDA graph compute returns after enqueueing kernels or launching a CUDA graph.
- Scheduler CUDA events own their own `cudaEvent_t` and are destroyed through static device-interface state without accessing the deleted backend context.
- Scheduler CUDA buffers own their device id and pointer and reach `cudaFree` through a buffer-local context; CUDA buffer types are static registry objects.
- Pools, concurrent events, and CUDA graph objects unwind after the context destructor body and its explicit stream-destruction loop.

**Interpretation**

- Backend-before-scheduler destruction is structurally independent for ordinary CUDA scheduler events and buffers.
- Queued-work completion remains conditional because the pinned source relies on CUDA-family runtime destruction semantics rather than explicitly synchronizing all created streams before teardown.
- Explicit synchronization before context destruction remains the clearest portable application boundary.

## 2026-07-13 12:49 — Metal backend teardown

**Verified**

- Published `docs/architecture/metal-backend-teardown.md` and added it to Architecture navigation.
- `ggml_backend_metal_free()` explicitly calls `ggml_metal_synchronize()` before releasing the backend context and wrapper.
- Synchronization waits for the last relevant command buffer, checks graph and extra command-buffer status, and releases completed extra command buffers.
- Context teardown then releases retained command buffers, dynamic pipelines, the encoding block, the dispatch queue, and the context-owned copy event.
- The Metal command queue is device-owned rather than backend-context-owned in the pinned design.
- Scheduler events own independent `MTLSharedEvent` objects and do not require a live backend context during destruction.
- Shared, private, and mapped scheduler buffers own buffer-local contexts and use static device state for residency-set and `MTLBuffer` cleanup.
- Mapped buffers do not own the underlying mapped host bytes.

**Interpretation**

- Backend-before-scheduler destruction is verified safe for ordinary pinned Metal resources because backend free establishes queued-work completion and later scheduler deleters retain valid device-level dependencies.
- Metal provides a stronger explicit teardown boundary than the pinned CUDA-family path.

## 2026-07-13 13:52 — Vulkan command and synchronization lifetimes

**Verified**

- Published `docs/architecture/vulkan-command-lifetime.md` and added it to Architecture navigation.
- Vulkan command pools are scoped per `(context, queue)` and `(device, queue)` pairing and track stable command-buffer records with reuse state.
- `ggml_vk_command_pool_cleanup()` resets a pool only under the explicit source precondition that command buffers are complete.
- Synchronous Vulkan buffer read, same-device copy, and GPU memset helpers submit with a device fence, wait indefinitely, reset the fence, and then recycle command-pool state.
- Deferred host copies in the read path happen after the fence wait.
- Binary semaphores, timeline semaphores, and Vulkan events are pooled and reused through context indices.
- Vulkan graph compute is submission-oriented and does not make a universal host-completion guarantee merely by returning.

**Interpretation**

- Command-pool reset is a reuse step after completion, not a synchronization mechanism.
- Fence waits are the clearest host completion boundary in the inspected synchronous helper paths.
- Timeline semaphores and events may establish device ordering without proving host completion.

**Open questions**

- The exact final backend/context free chain, queue coverage, synchronization-object destruction order, scheduler event/buffer independence, and backend-before-scheduler safety classification remain unresolved.

**Next step**

- Finish the exact Vulkan teardown chain and classify the pinned destruction order.
