# Research log

This is the concise chronological ledger. Detailed notes live under `logs/research/`.

## 2026-07-12 — Baseline and repository publication

**Verified**

- Baseline pinned to `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- The minimal path loads backends and a model, tokenizes, creates `llama_context`, decodes, samples, and feeds the next token back.
- The root README is the scheduled-run operating manual.
- CI includes context validation, source indexing, strict MkDocs validation, Pages deployment, and website health checking.

## 2026-07-12 02:51–12:52 — Decode, graph reuse, scheduler, and backend transfers

**Verified**

- `llama_decode()` delegates to `llama_context::decode()`.
- Reuse requires specialized compatibility checks; rebuild resets graph/scheduler state, calls `model.build_graph()`, and allocates through the backend scheduler.
- Allocation selects a copy-ring slot, assigns backends, builds splits, and allocates destination copies and dependency views.
- Execution waits before slot reuse, tries backend asynchronous copy, falls back to synchronized blocking copy, submits splits, and records events.
- CPU, CUDA, Metal, Vulkan, and SYCL execution/buffer/copy semantics are documented in the shared compatibility material.

**Interpretation**

- Reuse preserves compatible topology and allocation, not token values or outputs.
- Async-copy rejection is a correctness-preserving serialization point.
- CPU_Mapped addressability does not prove physical residency.

## 2026-07-12 13:52–15:49 — Documentation architecture and `llama_context`

**Verified**

- Added the object-centred documentation-quality roadmap and six-tab foundations explorer.
- Corrected the claim that mmap demand paging is equivalent to a universal application-level load-one-layer/free-one-layer policy.
- Published the canonical `llama_context` page for creation, ownership, lifetime, memory, mutation, decode, threading, synchronization, and teardown.
- The context stores a non-owning model reference while owning mutable runtime state, scheduler resources, outputs, and memory modules.
- Interactive Context entries link to the canonical page with top-level navigation.

## 2026-07-12 16:50–18:49 — GGUF and model tensor placement

**Verified**

- Published the canonical GGUF file-anatomy chapter with official format structure, canonical figure attribution, typed metadata, tensor descriptors, split indexing, loader entry, mmap/page-fault distinctions, and ownership.
- The loader computes a tensor’s absolute source-file offset from the GGUF data-region offset plus the tensor descriptor offset and validates bounds.
- Published model tensor placement and transfer documentation covering device assignment, per-tensor buffer compatibility, mappings, mmap alias/copy branches, direct reads, synchronous/asynchronous uploads, progress, synchronization, and retained ownership.
- The explorer links to both model-loading chapters.

**Interpretation**

- `weights_map` bridges file-format parsing and backend-aware construction.
- “Zero-copy model loading” applies only to the mapped host-pointer alias branch, not to an entire partially offloaded model.

## 2026-07-12 19:22–19:50 — Graph construction and MoE

**Verified**

- Published the canonical graph-construction and MoE chapter.
- Architecture code reconstructs a GGML graph over loaded tensors; GGUF does not store an executable graph.
- `build_moe_ffn()` separates router logits, selection probabilities, selected expert IDs, expert execution, and aggregation.
- The explorer links graph construction, graph expansion, MoE routing, the GGML graph layer, and graph reuse to the canonical chapter.

**Interpretation**

- Cache-aware routing should usually modify selection-only scores before top-k when the goal is to change expert choice without changing final expert weights.
- Per-layer expert residency should use `(layer_id, expert_id)` keys and tensor ranges or backend slices, not graph-node identity.

## 2026-07-12 21:08–21:51 — `llama_model` object and explorer integration

**Verified**

- Published `docs/objects/llama-model.md` and added it to Objects navigation.
- `llama_model_create(loader, params)` dispatches to an architecture-specific subclass.
- Common model mechanics and architecture hooks separate shared loading from `load_arch_hparams()`, `load_arch_tensors()`, and `build_arch_graph()`.
- The object owns architecture/vocabulary state and persistent tensor storage, backend buffers, and retained mappings.
- The interactive Model object layer routes to the canonical page.

**Interpretation**

- `llama_model` is a reusable loaded-model object and architecture-specific graph factory.
- `llama_layer` is a schema of persistent tensor roles, not a runtime activation layer.

## 2026-07-12 22:50–23:51 — Memory lifetime atlas and interactive overlay

**Verified**

- Published `docs/foundations/memory-lifetimes.md` and added it to navigation.
- The atlas separates GGUF storage, mappings, page-cache pages, model buffers, KV/recurrent/hybrid state, graph allocations, scheduler copies, staging, workspaces, outputs, queues, and events.
- Mapping, allocation, residency, validity, command completion, and ownership are distinct states.
- Replaced the Memory lifecycle tab's static cards with eight selectable records linked to canonical atlas sections.
- Each record exposes owner, backing, validity/residency, synchronization, and release/reclaim conditions.

**Interpretation**

- llama.cpp memory is better modeled as overlapping ownership and synchronization lifetimes than as one global cache.
- Logical expert-cache admission, OS page residency, and backend-copy validity require separate measurements.

## 2026-07-13 00:52 — Interactive route and anchor validator

**Verified**

- Added `scripts/validate_interactive_links.py` and fixture tests.
- The validator resolves literal HTML links, JavaScript page records, and memory-atlas anchors.
- Documentation CI now runs project-context validation, interactive-link validation, unit tests, Python compilation, shell syntax, required-asset checks, and strict MkDocs build.

**Open questions**

- Validate built HTML IDs and generated/plugin routes.
- Replace asset-specific rules with generated versioned metadata.

## 2026-07-13 01:52 — Public API and minimal example Pass A

**Verified**

- Published `docs/architecture/public-api-minimal-example.md` and added it to Architecture navigation.
- The page maps `examples/simple/simple.cpp`, `include/llama.h`, `src/llama.cpp`, `src/llama-model.cpp`, and `src/llama-context.cpp`.
- The pinned example loads backend registrations, creates model/context/sampler objects, tokenizes in two passes, optionally encodes, repeatedly decodes and samples, and frees sampler, context, then model.
- `llama_model_get_vocab()` returns a model-associated vocabulary reference rather than a separately freed object.
- `llama_batch_get_one()` is used as a caller-backed view over prompt-token or sampled-token storage.
- Model loading delegates through loader construction, architecture-specific model creation, device selection, metadata/vocabulary loading, and tensor loading.
- The page includes a subsystem relationship diagram, file/symbol/caller/callee table, ownership and synchronization matrix, error-path map, backend variants, and teardown responsibilities.

**Interpretation**

- The minimal example is an ownership and control-flow skeleton, not a complete production cleanup template.
- Prefill and one-token decode share `llama_decode()` but should be measured as distinct phases.
- `n_gpu_layers` is a placement request, not proof that a particular backend exists or every requested layer is offloaded.

**Historical**

- Public initialization, sampler, parameter, and batch APIs have changed across revisions; this inventory remains pinned to the baseline.

**Open questions**

- Strongest public contract for model sharing, context concurrency, and thread safety.
- Exact output-access synchronization guarantees.
- Deterministic RAII cleanup for every example error path.
- Process-level backend/global-resource shutdown requirements.

## 2026-07-13 02:51 — Model and GGUF loader Pass A

**Verified**

- Published `docs/architecture/model-gguf-loader-pass-a.md` and added it to Architecture navigation.
- The inventory covers `llama-model-loader`, model, mmap, and GGUF parser files.
- GGUF parsing uses `no_alloc=true`; tensor descriptors are indexed before destination payload allocation.
- Each tensor index entry preserves source split, absolute bounds-checked offset, and descriptor metadata.
- Split loading requires shard zero first, validates split count/index metadata, and rejects duplicate tensor names.
- Destination buffer selection depends on expected operations and backend support.
- Population paths include mapped host alias, mapped copy/upload, direct read, asynchronous staged upload, and synchronous fallback.
- Asynchronous staging slots and final uploads use events/synchronization before resource reuse or destruction.
- Cancellation is an explicit `false` result distinct from exception unwinding.

**Interpretation**

- The loader acts as a transactional bridge from temporary parse/I/O state to persistent model-owned storage.
- `weights_map` is the central join between GGUF physical layout and architecture/backend-aware tensor construction.
- A model is not fully loaded merely because metadata parsed or a mapping exists; destination bytes and required asynchronous work must be complete.

**Historical**

- Split conventions, direct-I/O support, buffer selection, and asynchronous upload behavior are revision-sensitive.

**Open questions**

- Exact model-member declaration/destruction order for retained mappings and buffers.
- Runtime cost split among parsing, mapping, faults, reads, validation, staging, upload, and synchronization.
- Backend-specific semantics of host-pointer wrapping.

**Next step**

- Continue Pass A with runtime-context and memory implementations, then synthesize public API, loader, model, and context ownership into one relationship map.