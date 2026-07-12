# Project state

_Last updated: 2026-07-13 01:52 Africa/Cairo_

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
- File-by-file Pass A public API/minimal-example inventory covering `examples/simple/simple.cpp`, `include/llama.h`, `src/llama.cpp`, `src/llama-model.cpp`, and `src/llama-context.cpp`, with relationship diagram, ownership, error paths, synchronization, backend assumptions, and teardown.

## In progress

- File-by-file Pass A for model/GGUF loader and runtime-context groups.
- Exact line-level source citations and generated source-link checking for the graph-construction chapter.
- Runtime evidence separating parsing, mapping/prefetch, page faults, reads, aliases, uploads, event waits, first-token access, KV/recurrent growth, activation peaks, and teardown.
- Architecture-specific graph-builder, prefill/decode, KV/recurrent, and MoE extensions to the explorer.
- Exact Metal shared/private buffer-level branches.

## Immediate next task

Continue file-by-file Pass A with the model/GGUF loader group:

```text
src/llama-model-loader.cpp
src/llama-model-loader.h
src/llama-model.cpp
src/llama-model.h
src/llama-mmap.cpp
src/llama-mmap.h
ggml/src/gguf.cpp
```

Required deliverables:

1. one bounded loader-file inventory page;
2. construction order and caller/callee table;
3. file descriptor, GGUF context, split-file, mmap, tensor-offset, buffer, and model ownership transitions;
4. cancellation and partial-construction cleanup paths;
5. explicit Verified, Interpretation, Historical, and Open question sections;
6. README, project-state, research-log, and detailed-note updates;
7. CI and Pages verification after publication.

## Latest publication verification

- Public API inventory commit: `2624123764db654bc32734d67f3b05cf68b4e74e`.
- Navigation commit: `3ac54a9861ca5ae9c91a65bb81779b9b5b560eb5`.
- Detailed note commit: `421d8d4a9d140fe6c6bdab5b1b1f343741a05874`.
- README living-TODO commit: `a20de8ec61f0426e7dd88a6715a2c6252a88ea31`.
- Research-log commit checked for CI: `484b4cd02d44691483903e0c2c8d1afeb2317395`.
- The combined-status endpoint returned an empty status list for `484b4cd02d44691483903e0c2c8d1afeb2317395`.
- The commit-workflow endpoint returned `workflow_runs: []`; that endpoint is limited and does not reliably expose push-triggered runs.
- Site-specific search returned no results for the Pages root or the new public-API page.
- Direct opening of both URLs was rejected by the browser safe-URL gate because the exact URLs were not present in search results.
- Local checkout validation is blocked because the execution environment cannot resolve `github.com`.
- Public site: `https://mohammed-alaa40123.github.io/How.to.llama.cpp/`.

## Known blockers and caveats

- **CI blocker:** for commit `484b4cd02d44691483903e0c2c8d1afeb2317395`, combined status was empty and the commit-workflow endpoint returned no runs. Because that workflow endpoint does not reliably expose push-triggered Documentation CI, Pages, or hourly-context runs, status is unverified rather than failed.
- **Pages blocker:** site-specific search returned no indexed result, and direct opening of the root and `architecture/public-api-minimal-example/` was blocked by the safe-URL gate. HTTP status and rendered content remain unverified.
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