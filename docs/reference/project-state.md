# Project state

_Last updated: 2026-07-12 19:22 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream reference used for the graph/MoE chapter: `6b4dc2116a92c5c8f2782bfe51fabe5ee66fb5ef`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Foundations deepening — interactive system map plus file-by-file subsystem synthesis**

Return to the foundations and reconstruct llama.cpp from the source in two complementary directions:

1. a large clickable system map that explains layers, code paths, memory, GGUF, graph construction, execution, synchronization, and MoE variants;
2. file-by-file analysis followed by subsystem grouping and end-to-end composition.

## Completed

- MkDocs Material site, strict documentation CI, Pages deployment, website health check, source indexing, and README-first scheduled-run context.
- Minimal end-to-end path and initial model-loading trace.
- Pinned decode, graph-reuse, backend-scheduler, copy-ring, split-allocation, and synchronization documentation.
- CPU, CUDA, Metal, Vulkan, and SYCL execution/buffer/copy documentation plus shared compatibility matrix.
- Generic tensor-copy fallback and blocking copy decision tree.
- Accessible static scheduler SVG replacing a Mermaid renderer failure.
- Object-centred, searchable, and interactive documentation quality roadmap.
- Large interactive foundations explorer with system, code-path, memory, GGUF/graph, execution/synchronization, and file-map tabs.
- Canonical `llama_context` object page and interactive links.
- Canonical GGUF file-anatomy chapter covering format structure, split indexing, loader entry, mmap/page-fault distinctions, ownership, and truth labels.
- Canonical model tensor-placement and data-transfer chapter covering device assignment, per-tensor buffer selection, mapping initialization, host-pointer aliasing, explicit reads, synchronous/asynchronous uploads, progress, cancellation, validation, trimming, and ownership.
- Interactive GGUF/graph cards now link directly to both canonical model-loading chapters with top-level navigation.
- Canonical GGML graph-construction and MoE chapter covering GGUF tensor storage, layer-to-graph construction, graph expansion, graph reuse, router-logit patch points, `selected_experts_in`, and per-layer LRU cache design.
- Expanded implementation roadmap with four passes: file inventory, subsystem grouping, cross-file composition, and complete workflow reconstruction.

## In progress

- Linking graph-construction, graph-expansion, and MoE explorer cards to the canonical graph-construction chapter.
- Adding exact line-level source citations and generated source-link checking to the graph-construction chapter.
- Memory atlas and interactive runtime overlays for mmap/page faults, RAM/RSS, backend copies, KV/recurrent state, and workspaces.
- Runtime evidence separating parsing, mapping/prefetch, page faults, direct reads, alias bytes, upload bytes, event waits, and first-token access.
- File-by-file Pass A for public API/examples, model/GGUF loader, and runtime context.
- Architecture-specific graph-builder, prefill/decode, KV/recurrent, and MoE extensions to the explorer.
- Exact Metal shared/private buffer-level branches.

## Immediate next task

Connect the new graph-construction chapter into the interactive foundations explorer:

```text
GGUF/graph tab
  -> graph construction card
  -> graph expansion card
  -> MoE router / selected experts card
  -> canonical docs/ggml/graph-construction-and-moe.md
```

Required deliverables:

1. clickable explorer links to the new canonical chapter;
2. update node labels for router logits, selection bias, `selected_experts`, and per-layer LRU cache key `(layer_id, expert_id)`;
3. add line-level citation placeholders or generated source-link metadata;
4. update README TODOs and research log;
5. verify Documentation CI / Pages status if the connector exposes it.

The next canonical object page remains `llama_model`.

## Latest publication verification

- Latest graph-construction chapter commit: `1a41185dec68a64f25500af56e0e31844137191f`.
- Navigation update commit: `f31ee820ef6727b2e36782e158056e4f8da2c763`.
- README TODO/context update commit: `ffc7ff7ef55d72d5435618c8296d91ebe77c954d`.
- The GitHub connector exposes commit/file fetch but not reliable push-triggered workflow inspection in this environment.
- Public site: `https://mohammed-alaa40123.github.io/How.to.llama.cpp/`.

## Known blockers and caveats

- **CI blocker:** connector workflow-run access has repeatedly returned no push-triggered runs, so latest push workflow status must be checked in the GitHub UI or by a later environment that exposes check runs.
- **Pages blocker:** if the site lags the latest commit, rerun **Deploy documentation** from the Actions tab.
- **Local validation blocker:** the execution container has previously failed to resolve `github.com`, so this run used connector-side source fetches rather than a local clone.
- The official GGUF specification can evolve beyond the pinned llama.cpp implementation.
- Mmap host-pointer wrapping is conditional; “zero-copy model loading” is not a model-wide property under partial offload or incompatible buffer types.
- Prefetch requests do not prove permanent physical residency.
- CPU_Mapped addressability does not imply physical residency or fault-free access.
- Accelerator unified/shared/system memory does not by itself imply GGML host visibility, command completion, or safe reuse.
- Regex indexing cannot resolve macros, virtual dispatch, function pointers, generated code, or backend registration reliably.
- A conceptual layer stack is not a universal execution order for every model architecture or backend combination.
- APIs named `async` do not prove host-visible overlap.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible hover/click behavior.
- Source-pinned end-to-end code workflow.
- Deep GGUF and model-loading chapters.
- Canonical `llama_context` ownership/lifetime page.
- GGML tensor/op/graph-construction and execution chapter.
- Memory ownership and synchronization atlas.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
