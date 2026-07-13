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
- CPU-mapped addressability does not prove physical residency.

## 2026-07-12 — Documentation architecture and core objects

**Verified**

- Added the documentation-quality roadmap and six-tab foundations explorer.
- Published canonical `llama_context` and `llama_model` pages and linked their explorer entries.
- The context stores a non-owning model reference while owning mutable runtime state, scheduler resources, outputs, and memory modules.
- `llama_model` owns architecture/vocabulary state, persistent tensors, buffers, retained mappings, and architecture-specific graph dispatch.

## 2026-07-12 — GGUF, model placement, graph construction, and MoE

**Verified**

- Published canonical GGUF anatomy and model tensor-placement chapters.
- GGUF stores tensors and metadata, not an executable graph; architecture code rebuilds GGML operations over loaded tensors.
- Population paths include mapped alias, mapped copy/upload, direct read, asynchronous staging, and synchronous fallback.

**Interpretation**

- `weights_map` joins physical GGUF layout to backend-aware tensor construction.
- Cache-aware routing should generally bias selection scores before top-k when expert weights should remain based on original probabilities.

## 2026-07-12 — Memory lifetimes and validation

**Verified**

- Published the memory-lifetime atlas and interactive ownership overlay.
- Mapping, allocation, residency, validity, command completion, and ownership are distinct states.
- Added static validation for interactive routes and Markdown anchors, fixture tests, and Documentation CI integration.

## 2026-07-13 01:52–07:50 — File-by-file Pass A and subsystem synthesis

**Verified**

- Published Pass A pages for the public API/minimal example, model/GGUF loader, runtime context/memory, backend scheduler, and concrete context-memory implementations.
- Published the cross-subsystem ownership and execution map.
- The pinned tree contains ordinary KV, iSWA, DSA, DSV4, recurrent, hybrid, and hybrid-iSWA persistent memory implementations.
- Scheduler copy allocation, current-generation validity, and previous-consumer completion are separate states.

**Interpretation**

- The loader is a transactional publisher, `llama_context` is a mutable session around a borrowed model, and the scheduler is an execution planner.
- A per-batch memory context behaves like a transaction plan.

## 2026-07-13 08:50 — Model and context teardown order

**Verified**

- Published `docs/architecture/model-context-teardown-order.md`.
- `llama_model` retains mappings until tensor buffers and metadata are released.
- `llama_context` reverse destruction releases owning backend wrappers before the scheduler smart pointer.
- The context destructor contains no universal explicit synchronization call.

**Interpretation**

- Applications should establish an explicit synchronization boundary before destroying a context that may have queued accelerator work.

## 2026-07-13 09:49 — Scheduler core teardown dependencies

**Verified**

- Published `docs/architecture/scheduler-teardown-core.md`.
- Scheduler free destroys events, graph-allocation resources, and host metadata without a generic synchronize call.
- Event destruction dispatches through device interfaces; graph allocation frees concrete backend buffers.

**Interpretation**

- Teardown safety depends on concrete backend device, queue, buffer-type, allocator, and callback lifetimes.

## 2026-07-13 10:50 — Ordinary CPU backend teardown

**Verified**

- CPU graph execution is synchronous; the ordinary CPU backend exposes no async tensor methods, synchronize callback, or events.
- CPU device state is static and scheduler buffers are backend-wrapper independent.

**Interpretation**

- Backend-before-scheduler destruction is verified safe for ordinary pinned CPU resources.

## 2026-07-13 11:49 — CUDA backend teardown

**Verified**

- CUDA backend destruction releases context-owned streams, events, cuBLAS handles, graph state, and wrapper state.
- Scheduler CUDA events and buffers retain device- or buffer-local state independent of the individual backend context.

**Interpretation**

- Backend-before-scheduler destruction is structurally independent for ordinary CUDA scheduler resources, but queued-work completion remains conditional.

## 2026-07-13 12:49 — Metal backend teardown

**Verified**

- Metal backend free explicitly synchronizes before releasing command buffers and Objective-C resources.
- Scheduler events and buffers retain device-level or buffer-local state.

**Interpretation**

- Backend-before-scheduler destruction is verified safe for ordinary pinned Metal resources.

## 2026-07-13 13:52–14:50 — Vulkan command lifetime and teardown

**Verified**

- Vulkan command pools track reusable command buffers per context/device queue pairing.
- Synchronous helpers wait on fences before recycling command-pool state.
- Vulkan backend cleanup explicitly synchronizes before destroying context-owned submission resources.
- Scheduler events use persistent registry-device state; scheduler buffers retain shared device/buffer ownership.

**Interpretation**

- Backend-before-scheduler destruction is verified safe for ordinary pinned Vulkan resources.

**Open questions**

- The optional performance query pool still needs a focused ownership/destructor audit.

## 2026-07-13 15:49 — SYCL backend teardown

**Verified**

- Published `docs/architecture/sycl-backend-teardown.md` and linked it in Architecture navigation.
- `ggml_backend_sycl_free()` deletes the per-backend context and generic wrapper without an explicit queue wait.
- `ggml_backend_sycl_synchronize()` waits on `stream(device, 0)`, but backend free does not invoke it.
- Async tensor set/get and graph execution can enqueue work and return without host completion.
- The context borrows device-manager default-queue pointers and owns pools, scratchpads, flash-attention buffers, and optional executable graph state.
- Scheduler events own independent `sycl::event` objects.
- Ordinary scheduler buffers retain buffer-local device, allocation, queue, tensor-extra, and allocation-mode state.
- SYCL buffer-type objects are function-static and outlive individual backend wrappers.

**Interpretation**

- Backend-before-scheduler destruction is structurally independent for ordinary SYCL scheduler events and buffers.
- Queued-work completion remains conditional because backend free does not establish an explicit completion boundary before context-member destruction.
- The pinned SYCL contract is closer to CUDA than to Metal or Vulkan.

**Historical**

- Queue ownership, command graphs, async allocation extensions, DNNL, Level Zero, and split-buffer behavior are revision- and compiler-sensitive.

**Open questions**

- Whether queue/pool/USM/command-graph destruction provides a portable implicit wait.
- Whether queue-0 synchronization covers all multi-device and optional paths.
- Whether immediate-context-destruction regression tests exist or should be added.
