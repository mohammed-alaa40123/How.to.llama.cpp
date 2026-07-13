# Project state

_Last updated: 2026-07-13 03:50 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream reference used for the graph/MoE chapter: `6b4dc2116a92c5c8f2782bfe51fabe5ee66fb5ef`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Foundations deepening — interactive system map plus file-by-file subsystem synthesis**

Reconstruct llama.cpp from the source through a clickable system map and file-by-file analysis followed by subsystem grouping and end-to-end composition.

## Completed

- MkDocs Material site, strict documentation CI, Pages deployment, website health check, source indexing, and README-first scheduled-run context.
- Pinned decode, graph-reuse, backend-scheduler, copy-ring, split-allocation, synchronization, and CPU/accelerator backend documentation.
- Canonical `llama_context`, `llama_model`, GGUF anatomy, model placement, graph construction/MoE, and memory-lifetime pages.
- Large six-tab interactive foundations explorer with canonical object, graph, GGUF/model-loading, and memory routes.
- Static interactive-link validator, fixture tests, and Documentation CI integration.
- Four-pass roadmap: file inventory, subsystem grouping, cross-file composition, and workflow reconstruction.
- File-by-file Pass A public API/minimal-example inventory.
- File-by-file Pass A model/GGUF loader inventory.
- File-by-file Pass A runtime-context and memory inventory covering context construction, backend/scheduler/output ownership, polymorphic memory, KV slot planning, recurrent/hybrid variants, sequence mutation, state I/O, threads, synchronization, reset, and teardown.

## In progress

- Synthesize public API, loader, model, context, and memory groups into one subsystem relationship map.
- Enumerate every concrete `llama_memory_i` implementation and map model architectures to KV, recurrent, hybrid, iSWA, and specialized caches.
- Exact `llama_model` and `llama_context` member destruction ordering for retained mappings, buffers, scheduler, memory, graph results, outputs, and backends.
- Exact line-level source citations and generated source-link checking for the graph-construction chapter.
- Runtime evidence separating parsing, mapping/prefetch, faults, reads, aliases, uploads, memory updates, event waits, first-token access, KV/recurrent growth, activation peaks, and teardown.

## Immediate next task

Create one bounded subsystem synthesis page connecting:

```text
public API and minimal example
→ model/GGUF loader
→ llama_model publication
→ llama_context construction
→ polymorphic memory creation
→ batch/ubatch planning
→ graph build/reuse
→ scheduler execution
→ memory mutation and outputs
→ synchronization and teardown
```

Required deliverables:

1. one relationship diagram spanning the three completed Pass A groups;
2. explicit ownership transfer and non-ownership boundaries;
3. creation, decode, memory-update, output, and teardown call chains;
4. CPU-only, mmap, GPU-offload, multi-backend, KV, recurrent, and hybrid variants;
5. Verified, Interpretation, Historical, and Open question labels;
6. README, project-state, research-log, and detailed-note updates;
7. CI and Pages verification after publication.

## Latest publication verification

- Runtime-context/memory page commit: `53742731207cdbc73ca9dab674a002bb02c00780`.
- Navigation commit: `575776a9db0e2e4a05256b451cadc7f690ad36eb`.
- Local checkout validation failed on 2026-07-13 because `github.com` DNS resolution failed.
- CI and Pages checks remain to be completed against the final state commit for this increment.
- Public site: `https://mohammed-alaa40123.github.io/How.to.llama.cpp/`.

## Known blockers and caveats

- **Local validation blocker:** the execution environment cannot resolve `github.com`, preventing a fresh checkout and full `mkdocs build --strict`.
- **CI visibility caveat:** connector status interfaces may omit push-triggered Documentation CI, Pages, and hourly-context workflows; empty results mean unverified, not necessarily failed.
- **Pages verification caveat:** if direct access is unavailable, record the exact HTTP/search/DNS blocker rather than claiming deployment success.
- Static link validation approximates Python-Markdown IDs; built-HTML validation is still required for plugin-generated anchors.
- Mapping, allocation, residency, validity, ownership, and command completion are distinct states.
- Mmap host-pointer wrapping is conditional; model pages and context-owned KV/recurrent memory are separate lifetimes.
- Shared/unified memory does not prove coherence or queue completion.
- `async` APIs indicate submission semantics, not immediate host visibility.
- `llama_context` references, but does not own, `llama_model`.
- Attached thread pools are referenced resources and must outlive their use.
- Memory implementations and architecture mappings are revision-sensitive.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, and memory ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
