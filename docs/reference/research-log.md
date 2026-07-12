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

**Open questions**

- Locate an explicit public thread-safety contract and map every concrete memory-module cleanup guarantee.

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

## 2026-07-12 21:08 — Canonical `llama_model` object page

**Verified**

- Published `docs/objects/llama-model.md` and added it to the Objects navigation.
- `llama_model_create(loader, params)` reads the GGUF architecture and dispatches to an architecture-specific `llama_model_*` subclass.
- Common model mechanics and virtual architecture hooks separate shared loading behavior from `load_arch_hparams()`, `load_arch_tensors()`, and `build_arch_graph()`.
- The object owns architecture and vocabulary state plus the lifetime of persistent model tensor storage, backend buffers, and retained mappings.
- `layers` and model-level fields hold pointers to persistent GGML weight tensor metadata; per-token activations are created later in context-built graphs.
- Persistent weight placement and scheduler graph-node placement are separate phases.
- `build_graph()` delegates architecture-specific graph construction for context-provided inputs and mutable memory.
- A `llama_context` stores a non-owning model reference; the model must outlive every referencing context.
- `create_memory()` expresses the boundary where model architecture selects a compatible memory implementation while the context owns the returned mutable state.

**Interpretation**

- `llama_model` is a reusable loaded-model object and architecture-specific graph factory.
- `llama_layer` is a schema of persistent tensor roles, not a runtime activation layer.
- Sharing a model can avoid duplicate weight storage but does not make context mutation or backend execution automatically thread-safe.

**Historical**

- Architecture registration, subclass layout, tensor names, split/offload logic, and memory factories evolve quickly; later upstream behavior must remain separately labelled.

**Open questions**

- Document the exact storage members inside `llama_model::impl`.
- Find the strongest public model-sharing and destruction-order contract.
- Measure mapped/read/uploaded bytes, page faults, and teardown synchronization by backend.

## 2026-07-12 21:51 — Interactive `llama_model` explorer link

**Verified**

- The interactive **Model object** system layer now routes to `objects/llama-model/`.
- The shared canonical-page renderer uses `target="_top"`, so navigation exits the iframe and opens the normal MkDocs page.
- The pinned baseline and all existing explorer layers, workflows, GGUF/graph cards, memory cards, synchronization entries, and source links were preserved.
- Both major runtime objects, `llama_model` and `llama_context`, now have canonical explorer routes.

**Interpretation**

- The explorer now provides a cleaner progressive-disclosure path from the persistent loaded-model layer to the detailed architecture, ownership, sharing, graph-factory, and teardown explanation.

**Historical**

- This closes the integration blocker left by the initial `llama_model` object-page increment.

**Open questions**

- Validate interactive routes automatically against built MkDocs output.
- Replace curated JavaScript metadata with generated versioned records.
- Build the memory-lifetime chapter and connect the memory cards to canonical sections.

**Artifacts changed**

- `docs/assets/interactive/llama-foundations-explorer.html`
- `README.md`
- `docs/reference/project-state.md`
- `docs/reference/research-log.md`
- `logs/research/2026-07-12/2151-interactive-model-link.md`

**Next step**

- Build the canonical memory-lifetime chapter and interactive overlay.