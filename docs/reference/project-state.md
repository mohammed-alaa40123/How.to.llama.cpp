# Project state

_Last updated: 2026-07-12 16:50 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Policy: baseline claims stay pinned; newer refs are documented separately.

## Active milestone

**Foundations deepening — interactive system map plus file-by-file subsystem synthesis**

Return to the foundations and reconstruct llama.cpp from the pinned source in two complementary directions:

1. a large clickable system map that explains layers, code paths, memory, GGUF, graph construction, execution, and synchronization;
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
- Canonical `llama_context` object page covering creation, ownership, lifetime, memory, mutation, call chain, synchronization, teardown, source map, backend/version differences, and truth labels.
- Interactive **llama_context runtime** layer and **Construct context** workflow step now link to the canonical object page through shared pinned metadata.
- Canonical GGUF file-anatomy chapter covering official format structure, the attributed upstream diagram, typed metadata, tensor descriptors, alignment, split indexing, loader entry, mmap/page-fault distinctions, ownership, backend consequences, and truth labels.
- Expanded implementation roadmap with four passes: file inventory, subsystem grouping, cross-file composition, and complete workflow reconstruction.

## In progress

- Second GGUF/model-loader slice: `model.load_tensors()`, buffer selection, mappings, prefetch, reads/uploads, direct I/O, and progress accounting.
- Generated versioned metadata shared by interactive nodes, object pages, and source maps.
- GGML op insertion, tensor-as-node semantics, graph expansion, activation allocation, reuse, and execution.
- Memory atlas and interactive runtime overlays for mmap/page faults, RAM/RSS, backend copies, KV/recurrent state, and workspaces.
- File-by-file Pass A for public API/examples, model/GGUF loader, and runtime context.
- Architecture-specific graph-builder, prefill/decode, KV/recurrent, and MoE extensions to the explorer.
- Exact Metal shared/private buffer-level branches.
- Runtime evidence for page faults, queue/fence waits, temporary RSS, and copy/compute overlap.

## Immediate next task

Complete the second GGUF/model-loading slice and connect the chapter to the explorer:

```text
model.load_tensors(loader)
  -> architecture tensor creation
  -> destination buffer-type selection
  -> loader.init_mappings()
  -> CPU_Mapped alias or explicit read
  -> backend upload/copy
  -> progress accounting
  -> mapping and buffer ownership
```

Required deliverables:

1. exact pinned `load_tensors()` and `load_all_data()` call chain;
2. buffer-placement decision table for CPU, CPU_Mapped, and accelerator destinations;
3. `init_mappings()` prefetch and file-range behavior;
4. direct-I/O versus mmap behavior;
5. links from the interactive GGUF tab to the detailed page;
6. runtime-measurement plan for parse, mapping, faults, reads, and uploads.

After GGUF/model loading, build the GGML graph-construction chapter. The next object page remains `llama_model`.

## Latest publication verification

- GGUF chapter commit: `ef30870f936825cb1aad2875ad3ee3e98020c432`.
- Durable detailed-note commit: `2078f721f56ddaf889eb23ddf8e8b8125c35e1c1`.
- The combined-status query for that commit returned no status records.
- The available commit-workflow query returned no runs and is documented to filter to pull-request-triggered runs, so push-triggered Documentation CI and Pages remain unverified.
- The public site is configured at `https://mohammed-alaa40123.github.io/How.to.llama.cpp/`.
- A direct browser open was rejected because the URL had no prior search result; site-specific search returned no indexed project result.
- The execution container also failed DNS resolution for `github.com`, preventing checkout, local `mkdocs build --strict`, and direct curl-based Pages verification.

## Known blockers and caveats

- **CI blocker:** the connected commit-workflow endpoint does not expose all push-triggered runs, and the final commit currently has no combined status records.
- **Pages blocker:** the browser requires an indexed/search-returned URL before direct opening, project-specific search returned no site result, and the execution container cannot resolve GitHub hosts.
- **Local validation blocker:** no repository checkout is available because `github.com` DNS resolution fails in the execution container.
- The canonical diagram is linked from the official GGUF specification and attributed to @mishig25; it is not copied into this repository.
- The official GGUF specification can evolve beyond the pinned llama.cpp implementation. Format statements and implementation statements must remain clearly separated.
- The interactive explorer does not yet link its GGUF tab to the new canonical chapter.
- The interactive explorer centralizes baseline/source/docs roots in one JavaScript metadata object, but does not yet consume generated versioned JSON.
- Regex indexing cannot resolve macros, virtual dispatch, function pointers, generated code, or backend registration reliably.
- A conceptual layer stack is not a universal execution order for every model architecture or backend combination.
- "Layer-by-layer loading and freeing" must not be stated as a universal llama.cpp policy.
- APIs named `async` do not prove host-visible overlap.
- CPU_Mapped addressability does not imply physical residency or fault-free access.
- Accelerator unified/shared/system memory does not by itself imply GGML host visibility, command completion, or safe reuse.
- The `llama_context` page infers external serialization for concurrent mutation; a future pass should locate an explicit public thread-safety contract or preserve this as an open question.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible hover/click behavior.
- Source-pinned end-to-end code workflow.
- Deep GGUF and model-loading chapter.
- Canonical `llama_context` ownership/lifetime page.
- GGML tensor/op/graph-construction and execution chapter.
- Memory ownership and synchronization atlas.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
