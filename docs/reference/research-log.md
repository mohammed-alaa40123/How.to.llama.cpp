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
- Published the graph-construction/MoE chapter and explorer links.
- GGUF stores tensors and metadata, not an executable graph; architecture code rebuilds GGML operations over loaded tensors.

**Interpretation**

- `weights_map` joins physical GGUF layout to backend-aware tensor construction.
- Cache-aware routing should generally bias selection scores before top-k when expert weights should remain based on original probabilities.

## 2026-07-12 — Memory lifetimes and validation

**Verified**

- Published the memory-lifetime atlas and interactive owner/backing/validity/synchronization/release overlay.
- Mapping, allocation, residency, validity, command completion, and ownership are distinct states.
- Added static validation for local interactive routes and Markdown anchors, fixture tests, and Documentation CI integration.

**Interpretation**

- Logical cache admission, OS page residency, and backend-copy validity require separate measurements.

## 2026-07-13 01:52 — Public API and minimal example Pass A

**Verified**

- Published `docs/architecture/public-api-minimal-example.md`.
- Mapped `examples/simple/simple.cpp`, `include/llama.h`, `src/llama.cpp`, `src/llama-model.cpp`, and `src/llama-context.cpp`.
- Documented construction, ownership, batch views, synchronization assumptions, errors, and teardown.

**Open questions**

- Strongest contracts for model sharing, context concurrency, output visibility, and deterministic cleanup.

## 2026-07-13 02:51 — Model and GGUF loader Pass A

**Verified**

- Published `docs/architecture/model-gguf-loader-pass-a.md`.
- GGUF parsing uses `no_alloc=true`; split descriptors are merged into one source index before destination allocation.
- Buffer selection depends on expected operations and backend support.
- Cancellation is an explicit result distinct from exception unwinding.

**Interpretation**

- The loader is a transactional bridge from temporary parse/I/O state into persistent model-owned storage.

## 2026-07-13 03:50 — Runtime context and memory Pass A

**Verified**

- Published `docs/architecture/runtime-context-memory-pass-a.md` and added it to Architecture navigation.
- Inventoried `llama-context`, `llama-memory`, ordinary KV cache, recurrent memory, and specialized/hybrid memory files.
- `llama_context` references the model and owns runtime backends, scheduler state, persistent memory, output buffers, graph-result caches, and the reusable batch allocator.
- Context construction initializes model devices, accelerator and CPU backends, reserves output storage, and calls `model.create_memory()`.
- `llama_memory_i` defines batch preparation, worst-case simulation, pending updates, sequence operations, memory accounting, and state I/O.
- `llama_memory_context_i` carries temporary ubatch state; `apply()` is the intended mutation point.
- The ordinary KV cache separates cell/sequence metadata from backend-buffer-backed K/V tensors and maps each ubatch token to concrete cache cells before graph execution.
- Pending KV shifts/copies may be implemented as backend memory-update graphs and require synchronization before conflicting reuse or host state I/O.
- Recurrent and hybrid implementations use the same interface but have different state layouts and update semantics.

**Interpretation**

- A per-batch memory context behaves like a transaction plan: prepare candidate state, apply for the current ubatch, compute, and advance.
- Context memory should be documented as a polymorphic subsystem, not assumed to be one conventional KV ring.
- Successful asynchronous graph submission is not equivalent to host-visible outputs or serializable state.

**Historical**

- Unified/multi-stream KV behavior, recurrent/hybrid implementations, specialized caches, graph reuse, and output/sampler integration are revision-sensitive.

**Open questions**

- Enumerate every concrete `llama_memory_i` subclass and map each architecture to it.
- Verify exact destruction dependencies among scheduler, memory, graph results, output buffers, and backend instances.
- Measure KV/recurrent allocation, update-graph cost, scheduler copies, event waits, and state-save synchronization.

## 2026-07-13 05:52 — System ownership and execution synthesis

**Verified**

- Published `docs/architecture/system-ownership-and-execution-map.md` and added it to Architecture navigation.
- The synthesis connects application ownership, loader publication, persistent model storage, context-owned runtime state, polymorphic memory, graph construction, scheduler splits/copies, backend execution, output visibility, and teardown.
- Ownership, virtual addressability, physical residency, destination allocation, data validity, and queued-command completion are tracked as distinct states.
- The model must outlive every context; scheduler copies and events must outlive queued work; context teardown precedes model teardown.

**Interpretation**

- `llama_model_loader` is a transactional publisher, `llama_context` is a mutable execution session around a borrowed model, and the scheduler is an execution planner rather than the persistent owner of weights or sequence memory.
- The per-batch memory context is best understood as a transaction plan separating candidate state from committed mutation.

**Historical**

- Exact memory implementations, graph-reuse predicates, scheduler copy behavior, and backend synchronization remain revision-sensitive.

**Open questions**

- Exact model/context member destruction order, public concurrency contracts, output synchronization guarantees, architecture-to-memory mapping, and scheduler copy validity across graph reuse.

## 2026-07-13 06:49 — Backend scheduler Pass A

**Verified**

- Published `docs/architecture/backend-scheduler-pass-a.md` and added it to Architecture navigation.
- Inventoried scheduler construction, backend assignment, split construction, cross-backend dependency copies, graph allocation, execution, synchronization, reset, and teardown.
- `ggml_backend_sched` owns assignment metadata, split records, a temporary GGML context, graph-allocation state, per-backend/per-slot copy pointers, and backend events.
- Copy tensors are scheduler execution storage, not persistent model weights or context sequence memory.
- Destination allocation, current-generation data validity, and prior-consumer completion are separate states.
- User inputs are captured under a stricter lifetime assumption; ordinary internal copies can use asynchronous peer-copy support or synchronized fallback.
- Graph-allocation reuse preserves compatible placement/allocation structure, not input values, copy generations, outputs, or sequence state.

**Interpretation**

- A scheduler copy is valid only for a particular source-value generation and copy slot.
- Backend events are reuse fences for destination storage, not merely profiling markers.
- The pinned `MUL_MAT_ID` partial expert transfer reduces bytes but does not implement a persistent expert cache.

**Historical**

- PRs #20793 and #25319 provide design history but do not replace the pinned implementation.

**Open questions**

- Concrete async-copy and event behavior for every backend.
- Runtime overlap, fallback frequency, copy bytes, event waits, and graph-reallocation frequency.
- Exact later changes to scheduler copy validity and partial MoE transfers.

## 2026-07-13 07:50 — Concrete context-memory implementations

**Verified**

- Published `docs/architecture/context-memory-implementations.md` and added it to Architecture navigation.
- The pinned tree contains seven concrete persistent `llama_memory_i` implementations: ordinary KV, iSWA, DSA, DSV4, recurrent, hybrid, and hybrid-iSWA.
- Exact recurrent architectures are Mamba, Mamba2, RWKV6, RWKV6-Qwen2, RWKV7, and ARWKV7.
- Exact hybrid architectures are Jamba, Falcon H1, Plamo2, Granite Hybrid, LFM2/LFM2-MoE, Nemotron H variants, Qwen3-Next, Kimi Linear, and Qwen3.5 variants.
- DeepSeek 3.2 and DeepSeek 4 use dedicated DSA and DSV4 memories; SWA attention paths use iSWA wrappers.
- Encoder, embedding, selected audio-decoder, and diffusion architectures explicitly receive no persistent context memory.
- DSV4 combines raw iSWA state, compressed K-only stores, and persistent compressor state rather than behaving as one ordinary KV cache.

**Interpretation**

- The factory acts as an architecture-to-state-machine compiler combining architecture, context type, SWA, offload, and layer-filter decisions.
- Composite memories coordinate child plans; allocation, validity, and completion remain separate states.
- “KV cache size” is not a universal metric for recurrent, hybrid, or compressed-cache models.

**Historical**

- The class family, architecture predicates, MTP exception, DSV4 layout, and rollback support are revision-sensitive.

**Open questions**

- Map architecture-specific graph-builder downcasts and exact state tensors read/written.
- Measure bytes, update-graph cost, and synchronization per memory family.
- Trace exact model/context teardown ordering and public concurrency guarantees.

**Next step**

- Trace exact `llama_model` and `llama_context` member declaration and reverse-destruction order, including queued backend work and external lifetime requirements.
