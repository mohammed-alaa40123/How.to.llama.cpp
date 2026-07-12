# Project state

_Last updated: 2026-07-13 00:52 Africa/Cairo_

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
- Canonical memory-lifetime atlas covering storage, mappings, page faults/page cache/RSS, model buffers, KV/recurrent/hybrid state, graph allocations, scheduler copies, staging, outputs, synchronization, teardown, and runtime measurement requirements.
- Interactive memory-lifetime overlay: all eight memory entries expose owner, backing storage, validity/residency, synchronization, release/reclaim, and canonical atlas links.
- Static interactive-link validator covering literal HTML `href` values, JavaScript `page` records, and the foundations explorer's generated memory-atlas anchors.
- Fixture tests covering valid links, missing routes, missing anchors, dynamic/external link exclusion, and Markdown heading slug generation.
- Documentation CI integration for project context, interactive links, unit tests, script compilation, shell syntax, required assets, and strict MkDocs build.
- Expanded four-pass roadmap: file inventory, subsystem grouping, cross-file composition, and complete workflow reconstruction.

## In progress

- File-by-file Pass A for public API/examples, model/GGUF loader, and runtime context.
- Exact line-level source citations and generated source-link checking for the graph-construction chapter.
- Runtime evidence separating parsing, mapping/prefetch, page faults, reads, aliases, uploads, event waits, first-token access, KV/recurrent growth, activation peaks, and teardown.
- Architecture-specific graph-builder, prefill/decode, KV/recurrent, and MoE extensions to the explorer.
- Exact Metal shared/private buffer-level branches.

## Immediate next task

Begin file-by-file Pass A with the public API and minimal example group:

```text
include/llama.h
  -> examples/simple/simple.cpp
  -> public initialization, model/context, batch, decode, output, sampler, and teardown calls
  -> implementation entry points in src/llama.cpp, src/llama-model.cpp, and src/llama-context.cpp
  -> ownership, error paths, synchronization, and backend assumptions
  -> subsystem relationship diagram
```

Required deliverables:

1. one bounded public-API/examples inventory page;
2. a table of relevant files, symbols, callers, callees, owned/referenced objects, and teardown responsibilities;
3. a pinned end-to-end relationship diagram from example code to implementation entry points;
4. explicit Verified, Interpretation, Historical, and Open question sections;
5. README, project-state, research-log, and detailed-note updates;
6. CI and Pages verification after publication.

## Latest publication verification

- Interactive-link validator initial commit: `d388f49567da7feaf5df8c5874e8e3a986bd9ca0`.
- Fixture-test commit: `2157993ec6b26424b7566b1cdf2fad3c8d81cbca`.
- Documentation CI integration commit: `c0f1084f50f20834d9b21c95b07b1b97c3ff0936`.
- Dynamic-template handling fix: `880918c2169d0fb5efa30251c0c156357c44b457`.
- Detailed research note commit: `171b642a40e1026a99a1ae2019a0536e360db9ad`.
- The combined-status endpoint returned an empty status list for `171b642a40e1026a99a1ae2019a0536e360db9ad`.
- The commit-workflow endpoint returned no workflow runs for that commit and is documented as limited to pull-request-triggered runs.
- Public site: `https://mohammed-alaa40123.github.io/How.to.llama.cpp/`.
- Site-specific searches returned no indexed result; direct opening of the root, memory-atlas page, and explorer asset was rejected because those exact URLs were not present in search results.

## Known blockers and caveats

- **CI blocker:** the available combined-status and commit-workflow endpoints returned no records for the final research-note commit; the workflow endpoint does not reliably expose push-triggered Documentation CI, Pages deployment, or hourly-context runs. This is unverified status, not evidence of failure.
- **Pages blocker:** site-specific search returned no indexed project result, and direct browser opening was blocked by the safe-URL gate because the exact URLs were absent from search results. HTTP status and rendered content remain unverified.
- **Local validation blocker:** the execution environment has no confirmed checkout and may be unable to resolve `github.com`, so full repository commands and `mkdocs build --strict` remain delegated to Actions until a checkout is available.
- Static validation approximates Python-Markdown heading IDs; built-HTML validation is still required for plugin-generated or custom anchors.
- The validator intentionally ignores dynamically constructed template `href` values and currently handles the foundations explorer's separate memory anchors through an explicit asset rule.
- The official GGUF specification can evolve beyond the pinned implementation.
- Mmap host-pointer wrapping is conditional; “zero-copy model loading” is not a model-wide property.
- Mapping, allocation, residency, validity, ownership, and command completion are distinct states.
- Prefetch requests do not prove permanent physical residency.
- RSS is not a per-tensor residency oracle.
- Shared or unified memory does not itself prove host visibility, coherence, or command completion.
- Regex indexing cannot resolve macros, virtual dispatch, function pointers, generated code, or backend registration reliably.
- A conceptual layer stack is not a universal execution order for every architecture/backend combination.
- APIs named `async` do not prove host-visible overlap.

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
