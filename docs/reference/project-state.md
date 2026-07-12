# Project state

_Last updated: 2026-07-13 02:51 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream reference used for the graph/MoE chapter: `6b4dc2116a92c5c8f2782bfe51fabe5ee66fb5ef`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Foundations deepening — interactive system map plus file-by-file subsystem synthesis**

Reconstruct llama.cpp from the source in two complementary directions:

1. a large clickable system map explaining layers, code paths, memory, GGUF, graph construction, execution, synchronization, and MoE variants;
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
- Canonical `llama_context` and `llama_model` object pages plus interactive routes.
- Canonical GGUF file-anatomy and model tensor-placement/data-transfer chapters plus explorer links.
- Canonical GGML graph-construction and MoE chapter plus graph, expansion, routing, and reuse explorer links.
- Canonical memory-lifetime atlas and interactive ownership/lifetime overlay.
- Static interactive-link validator, fixture tests, and Documentation CI integration.
- Expanded four-pass roadmap: file inventory, subsystem grouping, cross-file composition, and complete workflow reconstruction.
- File-by-file Pass A public API/minimal-example inventory.
- File-by-file Pass A model/GGUF loader inventory covering construction order, split discovery, source offsets, file/mapping/buffer ownership, population paths, cancellation, synchronization, and partial cleanup.

## In progress

- File-by-file Pass A for runtime-context and memory groups.
- Exact `llama_model` implementation-member ownership and destruction ordering for retained mappings/buffers.
- Exact line-level source citations and generated source-link checking for the graph-construction chapter.
- Runtime evidence separating parsing, mapping/prefetch, page faults, reads, aliases, uploads, event waits, first-token access, KV/recurrent growth, activation peaks, and teardown.
- Architecture-specific graph-builder, prefill/decode, KV/recurrent, and MoE extensions to the explorer.
- Exact Metal shared/private buffer-level branches.

## Immediate next task

Continue file-by-file Pass A with runtime-context and memory implementations:

```text
src/llama-context.cpp
src/llama-context.h
src/llama-memory.cpp
src/llama-memory.h
src/llama-kv-cache.cpp
src/llama-kv-cache.h
recurrent and hybrid memory implementations
```

Required deliverables:

1. one bounded runtime-context/memory inventory page;
2. creation and mutation call chains;
3. ownership of scheduler, outputs, KV/recurrent/hybrid memory, graph caches, thread pools, and backend resources;
4. synchronization, reset, sequence-state, and teardown paths;
5. explicit Verified, Interpretation, Historical, and Open question sections;
6. README, project-state, research-log, and detailed-note updates;
7. CI and Pages verification after publication.

## Latest publication verification

- Loader inventory commit: `06ad84e7f226e0ea0e214361672d815c5f55bcaf`.
- Navigation commit: `5a6d224283f715d2db5247843401470739a0ce8b`.
- README TODO commit: `db9e344de0f1cf3722ef8e4dc937b434576c9afe`.
- Research-log commit: `870c937d2b39dacb10bb2e01e8ab51d34503001a`.
- Detailed-note commit checked for CI: `b53abbb704f9b569b39004ba1606a68b5cc56aea`.
- Combined status for `b53abbb704f9b569b39004ba1606a68b5cc56aea` returned an empty status list.
- The commit-workflow endpoint returned `workflow_runs: []`; it is limited to pull-request-triggered runs and cannot reliably expose these push workflows.
- Direct browser opening of the Pages root and `architecture/model-gguf-loader-pass-a/` was rejected by the safe-URL gate because those exact URLs were not present in prior search results.
- Local checkout validation remains blocked because the execution environment cannot resolve `github.com`.
- Public site: `https://mohammed-alaa40123.github.io/How.to.llama.cpp/`.

## Known blockers and caveats

- **CI visibility blocker:** for commit `b53abbb704f9b569b39004ba1606a68b5cc56aea`, combined status was empty and the commit-workflow endpoint returned no runs. Because that endpoint does not reliably expose push-triggered Documentation CI, Pages, or hourly-context workflows, status is unverified rather than failed.
- **Pages verification blocker:** direct opening of the site root and `architecture/model-gguf-loader-pass-a/` was blocked by the browser safe-URL gate; the container also cannot resolve GitHub hosts. HTTP status and rendered content remain unverified.
- **Local validation blocker:** the execution environment cannot resolve `github.com`, preventing a fresh checkout and full local `mkdocs build --strict`.
- Static validation approximates Python-Markdown heading IDs; built-HTML validation is still required for plugin-generated or custom anchors.
- The official GGUF specification can evolve beyond the pinned implementation.
- Mmap host-pointer wrapping is conditional; “zero-copy model loading” is not a model-wide property.
- Mapping, allocation, residency, validity, ownership, and command completion are distinct states.
- Prefetch requests do not prove permanent physical residency.
- RSS is not a per-tensor residency oracle.
- Shared or unified memory does not itself prove host visibility, coherence, or command completion.
- Regex indexing cannot resolve macros, virtual dispatch, function pointers, generated code, or backend registration reliably.
- A conceptual layer stack is not a universal execution order for every architecture/backend combination.
- APIs named `async` do not prove host-visible overlap.
- The minimal example is a control-flow skeleton; several early-return paths rely on process exit rather than deterministic cleanup.
- Loader cancellation is an explicit `false` return and must not be confused with exception unwinding.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible hover/click behavior.
- Source-pinned end-to-end code workflow.
- Deep GGUF and model-loading chapters.
- Canonical `llama_context` and `llama_model` ownership/lifetime pages.
- GGML tensor/op/graph-construction and execution chapter.
- Memory ownership and synchronization atlas plus interactive overlay.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.