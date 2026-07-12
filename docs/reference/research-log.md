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

## 2026-07-12 — Repository publication and durable context

**Verified**

- The root README is the scheduled-run operating manual.
- Startup reads README, project state, research log, source ledger, and latest detailed note.
- CI includes context validation, source indexing, strict MkDocs validation, Pages deployment, and website health checking.

## 2026-07-12 02:51 — Decode and graph reuse

**Verified**

- `llama_decode()` delegates to `llama_context::decode()`.
- Decode prepares scheduler and memory state and processes `llama_ubatch` units.
- Reuse requires specialized compatibility checks; pipeline-parallel reuse synchronizes before rewriting inputs.
- Rebuild resets graph/scheduler state, calls `model.build_graph()`, and allocates through the backend scheduler.

**Interpretation**

- Reuse preserves compatible topology and allocation, not token values or outputs.

## 2026-07-12 03:52–12:52 — Scheduler and backend transfer semantics

**Verified**

- Allocation selects a copy-ring slot, assigns backends, builds splits, and allocates destination copies and dependency views.
- Execution waits before slot reuse, tries backend async copy, falls back to synchronized blocking copy, submits splits, and records events.
- Scheduler synchronization waits every backend.
- Missing/rejected async copy synchronizes source and destination; blocking fallback checks host-visible paths, direct-copy callbacks, then full heap staging.
- CPU graph compute is threadpool-backed and blocking at the backend interface.
- CUDA queues graph work, while ordinary set/get/copy callbacks establish completion before return.
- Metal uses command buffers and event ordering; explicit synchronization establishes host-visible completion.
- Vulkan registered-host and compatible same-device paths can use scheduler async copy; ordinary CPU/mmap and unsupported cross-device paths are rejected.
- SYCL explicit backend operations may queue work, but the pinned scheduler interface installs no `cpy_tensor_async` callback; backend-specific temporary or host-forward staging can still occur.
- The shared compatibility matrix records CPU, CPU_Mapped, CUDA, Metal, Vulkan, and SYCL paths.

**Interpretation**

- Async rejection is a correctness-preserving serialization point.
- No generic heap staging does not imply zero-copy, no backend staging, or host-visible overlap.
- CPU_Mapped addressability does not prove physical residency.

**Historical**

- Backend callback registration, staging, USM, events, and copy ordering may change in later revisions.

**Open questions**

- Identify the first later SYCL scheduler-copy revision and gather runtime page-fault, RSS, queue-wait, and overlap evidence.

## 2026-07-12 09:11 — Scheduler figure repair

**Verified**

- A deployed Mermaid renderer failure was replaced with an accessible static SVG preserving allocation, split execution, asynchronous return, and later synchronization.

## 2026-07-12 13:52 — Documentation quality and interaction roadmap

**Verified**

- Added object-centred documentation, clickable source exploration, synchronized diagrams, memory/execution visualizers, navigation contracts, and pinned-version/backend comparisons.
- Added a ten-part object-page contract and website review rubric.
- Published the roadmap and daily website-quality review responsibility.

**Interpretation**

- Stable metadata shared by diagrams, object pages, and symbol pages is the maintainable path to synchronized interactions.

## 2026-07-12 14:55 — Interactive foundations and file-by-file plan

**Verified**

- Added a six-tab foundations explorer covering system layers, end-to-end code flow, memory lifecycle, GGUF/graph construction, execution/synchronization, and file groups.
- Added hover/click details with representative symbols, ownership, synchronization, and pinned source links.
- Corrected the claim that mmap demand paging is equivalent to a universal application-level “load one layer, execute, free it” policy.
- Expanded the roadmap with file inventory, subsystem grouping, cross-file composition, and complete-workflow reconstruction.

**Interpretation**

- No single linear diagram can explain API control flow, object ownership, virtual memory, graph construction, and backend synchronization simultaneously.

## 2026-07-12 15:05 — Canonical `llama_context` object page

**Verified**

- Added a source-pinned page for context creation, ownership, lifetime, memory, mutation, decode, threading, synchronization, and teardown.
- The context stores a non-owning model reference while owning mutable runtime state, scheduler resources, outputs, and memory modules.
- The model must outlive every referencing context.

**Interpretation**

- `llama_context` is the mutable execution session around a reusable loaded model.

**Open questions**

- Locate an explicit public thread-safety contract and map every concrete memory-module selection and cleanup guarantee.

## 2026-07-12 15:49 — Interactive Context link

**Verified**

- The interactive `llama_context runtime` layer and `Construct context` workflow step link to the canonical page.
- `target="_top"` prevents canonical pages from opening inside the explorer iframe.
- The explorer centralizes pinned upstream, source-root, and documentation-root metadata.

**Historical**

- This is the first interactive node-to-canonical-object-page bridge.

## 2026-07-12 16:50 — GGUF file anatomy and loader entry

**Verified**

- Published `docs/foundations/gguf-file-anatomy.md` in the Foundations navigation.
- The official GGUF specification defines a self-describing typed format with header/counts, key/value metadata, tensor descriptors, alignment padding, and a tensor-data region.
- The canonical GGUF v3 diagram is linked from the official specification and attributed there to `@mishig25`; the asset is referenced rather than redistributed.
- The pinned loader calls `gguf_init_from_file(..., no_alloc = true)` before creating final tensor payload storage.
- `llama_tensor_weight` records the source split and computes an absolute source-file offset as data-region offset plus tensor-descriptor offset, then validates bounds.
- The loader unifies tensors from all splits into a name-indexed `weights_map`, while retaining each source-file index and rejecting duplicates/count mismatches.
- mmap-backed virtual addressability is distinct from physical page residency; accelerator placement may require separate backend-owned storage and transfer.

**Interpretation**

- `weights_map` is the bridge between format parsing and backend-aware model construction: it separates where bytes live in GGUF files from where execution consumes them.
- “Model loaded” is ambiguous unless metadata parsing, mapping, allocation, transfer, and first-touch faults are measured separately.

**Historical**

- GGUF replaced GGML/GGMF/GGJT file formats; the pinned loader recognizes versions 1–3.
- The current official specification can evolve beyond the pinned implementation.

**Open questions**

- Trace `model.load_tensors()`, buffer selection, `init_mappings()`, `load_all_data()`, prefetch/direct-I/O behavior, backend uploads, and progress accounting.
- Add runtime evidence separating parse time, mmap setup, faults, storage reads, transfers, and synchronization.
- Link the interactive GGUF tab to the canonical chapter.

**Artifacts changed**

- `docs/foundations/gguf-file-anatomy.md`
- `mkdocs.yml`
- `README.md`
- `docs/reference/project-state.md`
- `docs/reference/research-log.md`
- `docs/reference/research-ledger.md`
- `logs/research/2026-07-12/1650-gguf-file-anatomy.md`

**Next step**

- Complete the backend-placement and data-transfer half of model loading, then connect the GGUF explorer tab to the canonical page.

## 2026-07-12 17:50 — Model tensor placement and data transfer

**Verified**

- Published `docs/foundations/model-tensor-placement.md` and added it to Foundations navigation.
- `load_tensors()` assigns the input layer to CPU and repeating/output layers using `n_gpu_layers` plus normalized device split points.
- Candidate buffer types are ordered per CPU or accelerator device, but the final selection is per tensor after operation/backend compatibility checks.
- Destination tensor metadata is grouped into one GGML context per selected buffer type.
- `init_mappings(true, ...)` creates one mmap per source split, initializes used-range tracking, and computes total tensor bytes for progress.
- Mmap loading can either wrap mapped bytes through `buffer_from_host_ptr` or copy/upload from the mapped address into independently allocated storage.
- Non-mmap accelerator loading can use four pinned host staging buffers plus events and asynchronous tensor sets; unsupported configurations use a whole-tensor host staging vector and synchronous set.
- Upload events are synchronized before staging resources are freed; retained mappings are moved into model ownership.

**Interpretation**

- The loader acts like a placement compiler: architecture declarations, device assignment, operation compatibility, and backend capabilities become concrete tensor storage choices.
- “Zero-copy loading” applies only to the mapped host-pointer alias branch and is not a model-wide property under partial offload.
- Prefetch can move I/O earlier but does not guarantee permanent physical page residency.

**Historical**

- Buffer capabilities, host-pointer wrapping, and asynchronous upload paths may differ in later revisions and backends.

**Open questions**

- Measure branch entry and bytes aliased/read/uploaded for CPU, Metal, CUDA, Vulkan, and SYCL configurations.
- Trace direct-I/O alignment and fallback behavior at runtime.
- Link the interactive GGUF/graph tab to both model-loading chapters.

**Artifacts changed**

- `docs/foundations/model-tensor-placement.md`
- `mkdocs.yml`
- `README.md`
- `docs/reference/project-state.md`
- `docs/reference/research-log.md`
- `logs/research/2026-07-12/1750-model-tensor-placement.md`

**Next step**

- Build the GGML graph-construction chapter and connect the GGUF/graph explorer tab to the canonical model-loading pages.

## 2026-07-12 18:49 — Interactive GGUF and model-loading links

**Verified**

- The explorer's GGUF container card now links to the canonical GGUF file-anatomy chapter.
- The tensor registration and placement card now links to the canonical model-placement chapter.
- Both routes use top-level navigation so canonical pages open outside the iframe.
- The pinned baseline and the six existing explorer views remain intact.

**Interpretation**

- Readers can now move from the compact format/placement distinction to the two detailed source-pinned chapters without conflating on-disk GGUF structure with runtime backend residency.

**Historical**

- This is the second canonical-documentation integration in the explorer after the `llama_context` bridge.

**Open questions**

- Move hard-coded local routes into generated versioned metadata and validate them in CI.
- Link graph-construction cards after the canonical GGML chapter is published.

**Artifacts changed**

- `docs/assets/interactive/llama-foundations-explorer.html`
- `README.md`
- `docs/reference/project-state.md`
- `docs/reference/research-log.md`
- `logs/research/2026-07-12/1849-interactive-gguf-links.md`

**Next step**

- Build the canonical GGML graph-construction chapter and connect its graph cards.

## 2026-07-12 19:22 — GGML graph construction, MoE routing, and per-layer LRU design

**Verified**

- Published `docs/ggml/graph-construction-and-moe.md` and added it to Foundations navigation.
- Current upstream OLMoE tensor loading creates dense attention tensors plus `ffn_gate_inp`, `ffn_gate_exps`, `ffn_down_exps`, and `ffn_up_exps` per layer.
- Current upstream OLMoE graph construction loops over layers, builds attention, residuals, FFN norm, and calls `build_moe_ffn()` before final norm/output projection and `ggml_build_forward_expand()`.
- `process_ubatch()` reuses the previous graph only if graph reuse is enabled and `res->can_reuse(gparams)` succeeds; otherwise it resets the graph result and scheduler, calls `model.build_graph()`, and allocates through the backend scheduler.
- `build_moe_ffn()` computes router logits, probabilities, selection probabilities, top-k selected experts, expert weights, expert `mul_mat_id` paths, and aggregation.

**Interpretation**

- GGUF stores named tensor data and metadata, not an executable graph. The graph is reconstructed by architecture code over loaded model tensors.
- A graph-reuse hit reuses compatible topology/allocation but still recomputes values for the current ubatch.
- Cache-aware routing should usually bias `selection_probs` before top-k if the goal is to affect expert choice without changing final expert weights.
- A per-layer LRU should key on `(layer_id, expert_id)` and track expert tensor ranges or backend tensor slices, not whole-graph nodes.

**Historical**

- The graph/MoE chapter uses current upstream layout under `src/models/`; older pinned baseline layouts may organize architecture files differently.

**Open questions**

- Add generated line-level source links for every statement in the graph chapter.
- Link the interactive graph-construction, graph-expansion, and MoE cards to the new chapter.
- Prototype post-compute selected-expert logging and compare global LRU versus per-layer LRU offline.

**Artifacts changed**

- `docs/ggml/graph-construction-and-moe.md`
- `mkdocs.yml`
- `README.md`
- `docs/reference/project-state.md`
- `docs/reference/research-log.md`

**Next step**

- Link the interactive explorer's graph/MoE cards to the new canonical chapter and add line-level source metadata.

## 2026-07-12 19:50 — Interactive graph construction and MoE integration

**Verified**

- The explorer's Graph construction card links to section 2 of the canonical graph chapter.
- The Graph expansion card links to section 3.
- A new MoE router and selected experts card links to section 5 and names `logits`, `selection_probs`, `selected_experts`, and `MUL_MAT_ID` explicitly.
- The GGML computation graph system layer and Build or reuse graph workflow step link to the canonical chapter root.
- All canonical routes use top-level navigation, preserving normal MkDocs navigation outside the iframe.

**Interpretation**

- Separating router logits, selection scores, chosen IDs, and final expert weights makes the cache-aware routing patch point precise.
- Per-layer cache residency belongs to expert tensor storage and should use `(layer_id, expert_id)` keys rather than graph-node identity.

**Historical**

- This is the third canonical-documentation bridge in the foundations explorer.

**Open questions**

- Generate versioned route and anchor metadata instead of hard-coding it.
- Add built-site CI validation for interactive links and anchors.
- Add exact generated line-level source citations to the graph chapter.

**Artifacts changed**

- `docs/assets/interactive/llama-foundations-explorer.html`
- `README.md`
- `docs/reference/project-state.md`
- `docs/reference/research-log.md`
- `logs/research/2026-07-12/1950-interactive-graph-moe-links.md`

**Next step**

- Build the canonical `llama_model` object page and link the Model object explorer layer to it.