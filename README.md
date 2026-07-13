# How.to.llama.cpp

**A source-guided, revision-pinned map of llama.cpp and GGML.**

How.to.llama.cpp explains the path from a GGUF file to generated tokens: backend discovery, model loading, virtual memory, `llama_model`, `llama_context`, GGML graph construction, scheduling, kernels, outputs, sampling, and teardown.

> **Initial upstream baseline:** [`e3546c7948e3af463d0b401e6421d5a4c2faf565`](https://github.com/ggml-org/llama.cpp/commit/e3546c7948e3af463d0b401e6421d5a4c2faf565)
>
> Newer upstream refs are indexed separately. Baseline claims must not be silently rewritten as llama.cpp changes.

## What the project contains

- MkDocs Material documentation with source-pinned figures and tables.
- Beginner-readable and source-level inference walkthroughs.
- Canonical pages for GGUF, model loading, `llama_model`, `llama_context`, graph construction, graph reuse, schedulers, memory, synchronization, and backends.
- Clickable foundations and inference explorers.
- A research ledger for official docs, PRs, discussions, papers, talks, videos, blogs, and technical posts.
- Scripts for source mirroring, indexing, context loading, validation, and site health checks.
- GitHub Actions for hourly context validation, daily upstream indexing, strict documentation CI, and Pages deployment.

Current progress lives in [`docs/reference/project-state.md`](docs/reference/project-state.md).

---

<!-- SCHEDULED-RUN-INSTRUCTIONS:START -->
## Mandatory startup protocol

Every scheduled or manual research run must:

1. Read this entire `README.md` first.
2. Read [`docs/reference/project-state.md`](docs/reference/project-state.md).
3. Read [`docs/reference/research-log.md`](docs/reference/research-log.md).
4. Read [`docs/reference/research-ledger.md`](docs/reference/research-ledger.md) before adding sources.
5. Read the latest detailed note under `logs/research/`.
6. Inspect current repository files before editing.
7. Complete one bounded, reviewable artifact.
8. Label claims as **Verified**, **Interpretation**, **Historical**, or **Open question**.
9. Before finishing:
   - update this README TODO list;
   - update project state and research log;
   - update the research ledger when sources change;
   - run relevant validation;
   - inspect the latest GitHub Actions state;
   - verify the deployed Pages site;
   - fix failures when possible or record the exact blocker.
10. Store detailed notes under `logs/research/YYYY-MM-DD/HHMM-topic.md`.

Start a local run with:

```bash
./scripts/start_scheduled_run.sh <run-name>
```
<!-- SCHEDULED-RUN-INSTRUCTIONS:END -->

## Scheduling plan

| Schedule | Workflow | Responsibility |
|---|---|---|
| Every hour | Research automation | Complete one source-pinned increment; prioritize foundations, file-by-file analysis, subsystem synthesis, interactive explanations, and durable context updates |
| Daily | Website quality review | Review foundations, discoverability, source traceability, accessibility, cross-links, diagrams, and interaction opportunities |
| Hourly at minute 23 UTC | `.github/workflows/hourly-context-check.yml` | Validate context and scripts |
| Daily at 02:17 UTC | `.github/workflows/refresh-source-index.yml` | Refresh upstream source inventory through a PR |
| Every push/PR | `.github/workflows/docs-ci.yml` | Validate context, interactive routes/anchors, scripts, assets, tests, and `mkdocs build --strict` |
| Every push to `main` | `.github/workflows/pages.yml` | Build, deploy, and verify the public site |

## Implementation method

### Pin the evidence scope

Record the exact commit, branch, PR, discussion, test, or trace. Baseline metadata is in [`data/upstream.json`](data/upstream.json).

### Analyze files, then synthesize subsystems

For each relevant file, record purpose, major objects and functions, callers/callees, ownership, allocations/mappings/copies, threads and synchronization, error paths, backend differences, tests, and runtime evidence.

Then group files into public API, model/GGUF loading, runtime context, memory modules, GGML core, scheduler, CPU backend, accelerator backends, model architectures, and tools/tests. Explain how control, objects, memory, and synchronization cross those boundaries.

`scripts/index_upstream.py` is a navigation aid, not a compiler-grade call graph.

### Write layered documentation

A mature topic should include a five-minute explanation, end-to-end flow, source-level call chain, memory/concurrency notes, backend differences, figures or interactive diagrams, external references/runtime evidence, and version caveats/open questions.

### Validate

```bash
python3 scripts/validate_project_context.py
python3 scripts/validate_interactive_links.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m py_compile scripts/*.py tests/*.py
bash -n scripts/*.sh
mkdocs build --strict
./scripts/check_site.sh
```

Public site: `https://mohammed-alaa40123.github.io/How.to.llama.cpp/`

## Context map

| Location | Purpose |
|---|---|
| `README.md` | Operating manual and living TODOs |
| `docs/reference/project-state.md` | Current milestone, blockers, and next task |
| `docs/reference/research-log.md` | Concise chronological findings |
| `logs/research/` | Detailed per-run notes |
| `docs/reference/research-ledger.md` | External-source assessment |
| `docs/roadmap.md` | Full implementation, file-analysis, and subsystem-synthesis plan |
| `docs/foundations/interactive-system-map.md` | Large clickable foundations map and tabbed explorer |
| `docs/foundations/gguf-file-anatomy.md` | GGUF layout, metadata, descriptors, split indexing, loader entry, mmap, and ownership |
| `docs/foundations/model-tensor-placement.md` | Layer/device assignment, buffer selection, mappings, alias/read/upload paths, synchronization, and ownership |
| `docs/foundations/memory-lifetimes.md` | Ownership and lifetime atlas for mappings, page cache, model buffers, context state, graph allocations, copies, outputs, and teardown |
| `docs/objects/llama-model.md` | `llama_model` creation, architecture dispatch, tensor/layer schema, storage ownership, graph factory, sharing, and teardown |
| `docs/objects/llama-context.md` | `llama_context` creation, ownership, lifetime, memory, execution, synchronization, and teardown |
| `docs/ggml/graph-construction-and-moe.md` | Graph construction, MoE routing, graph reuse, router patch points, and per-layer LRU design |
| `docs/architecture/public-api-minimal-example.md` | Pass A public API/minimal-example map |
| `docs/architecture/model-gguf-loader-pass-a.md` | Pass A model/GGUF loader inventory |
| `docs/architecture/runtime-context-memory-pass-a.md` | Pass A runtime context and memory inventory |
| `docs/architecture/context-memory-implementations.md` | Exact concrete memory implementations and architecture factory mapping |
| `docs/architecture/backend-scheduler-pass-a.md` | Pass A scheduler assignment, splits, copy ring, validity, events, reuse, and teardown |
| `docs/architecture/system-ownership-and-execution-map.md` | Cross-subsystem ownership, execution, mutation, synchronization, and teardown synthesis |
| `docs/architecture/model-context-teardown-order.md` | Exact declaration order, reverse destruction, RAII ownership, synchronization caveats, and safe teardown |
| `docs/architecture/scheduler-teardown-core.md` | Exact scheduler free order, event and graph-buffer deleter chains, borrowed lifetime dependencies, and unresolved backend contracts |
| `docs/architecture/cpu-backend-teardown.md` | Ordinary CPU backend free path, synchronous execution contract, event/device lifetime, and backend-before-scheduler safety classification |
| `docs/reference/source-index.md` | Human-reviewed source areas |
| `data/upstream.json` | Pinned upstream metadata |
| `docs/assets/interactive/` | Interactive architecture assets |
| `scripts/validate_interactive_links.py` | Static validation for local routes and Markdown anchors in interactive assets |
| `.github/workflows/` | CI, Pages, context, and indexing automation |

<!-- PROJECT-TODOS:START -->
## Living TODO list

Keep unfinished work in priority order. Remove duplicates and move old completion history into the research log when this section grows.

### Highest priority

- [ ] Audit CUDA backend-context destruction, stream synchronization, event destruction, device/buffer-type lifetime, `cudaFree`, and CUDA graph resources; classify backend-before-scheduler destruction.
- [ ] Continue concrete teardown audits for Metal, Vulkan, SYCL, RPC, CANN, and OpenCL, including optional CPU extra-buffer implementations.
- [ ] Map each architecture-specific graph builder downcast to `llama_memory_context_i` subtypes and identify exact state tensors read and written.
- [ ] Add runtime evidence separating parsing, mapping/prefetch, page faults, direct reads, alias bytes, upload bytes, scheduler copy generations, event waits, memory-update graphs, first-token access, KV/recurrent growth, activation peaks, synchronization, and teardown.
- [ ] Add exact pinned line-level source citations to the graph-construction chapter once the generated source-link checker is ready.
- [ ] Expand the interactive explorer with architecture-specific graph builders, prefill/decode variants, KV/recurrent state, MoE, scheduler splits/copies, and runtime-measured overlays.
- [ ] Replace curated interactive metadata with generated versioned JSON shared by object pages, source maps, and visualizers.
- [ ] Verify the latest **Documentation CI**, **Deploy documentation**, and **Hourly research context check** runs after this increment.
- [ ] Verify the public Pages site returns HTTP 200 and renders `architecture/cpu-backend-teardown/` with expected How.to.llama.cpp content.

### Future improvements

- [ ] Add a sanitizer regression test that frees a CPU backend wrapper before its scheduler and then destroys the scheduler.
- [ ] Extend interactive-link validation to built HTML IDs, generated routes, non-HTML assets, and plugin-generated anchors.
- [ ] Add RAII guidance or an upstream example patch for deterministic cleanup on every minimal-example error path.
- [ ] Locate the strongest public contract for model sharing, context concurrency, thread safety, backend teardown synchronization, and destruction order.
- [ ] Prototype per-layer LRU expert-cache instrumentation using `(layer_id, expert_id)` keys and separate logical, OS-residency, and backend-copy validity fields.
- [ ] Prototype cache-aware routing by adding selection-only bias before `ggml_argsort_top_k()`.
- [ ] Quantify backend entry into mmap alias, mapped-copy, direct-read, synchronous-upload, and asynchronous-upload paths.
- [ ] Trace direct-I/O alignment/fallback behavior with runtime evidence.
- [ ] Extend the source index with per-file, object, symbol, subsystem, and caller/callee landing pages.
- [ ] Add dedicated mmap/page-fault, CPU-thread, backend-queue, KV-cache, recurrent-memory, MoE-routing, and scheduler-timeline visualizers.
- [ ] Trace exact Metal shared/private buffer-level set/get/copy branches.
- [ ] Extend backend comparisons to later scheduler-copy revisions and architecture-specific accelerators.
- [ ] Expand graph-reuse documentation with every specialized `can_reuse()` predicate.
- [ ] Add a searchable index for detailed research logs and commit-pinned link checking.

### Completed

- [x] Classify ordinary pinned CPU backend teardown: synchronous graph execution, no events/synchronize callback, static device lifetime, backend-independent scheduler buffers, and verified-safe backend-before-scheduler destruction.
- [x] Trace the pinned generic scheduler free chain: event destruction, graph allocator and backend-buffer destruction, host metadata release, borrowed backend/device/buffer-type dependencies, and the limits of the generic safety conclusion.
- [x] Trace exact `llama_model` and `llama_context` member declaration and reverse-destruction order, including retained mappings, backend buffers, scheduler, memory, graph results, outputs, backend instances, partial construction, and safe application teardown.
- [x] Enumerate every concrete `llama_memory_i` and primary `llama_memory_context_i` implementation at the pinned revision and map architecture factory decisions to no-memory, KV, iSWA, recurrent, hybrid, DSA, and DSV4 storage.
- [x] Complete file-by-file Pass A for backend scheduler internals: backend assignment, split creation, copy-ring allocation, destination validity, events, asynchronous submission, fallback synchronization, graph-allocation reuse, and teardown.
- [x] Synthesize the public API, model/GGUF loader, `llama_model`, `llama_context`, and memory Pass A work into one subsystem relationship map with ownership, mutation, synchronization, and teardown boundaries.
- [x] Complete file-by-file Pass A for runtime-context and memory files with construction, ownership, batch/microbatch memory planning, KV/recurrent/hybrid behavior, sequence mutation, state I/O, threads, synchronization, reset, and teardown.
- [x] Complete file-by-file Pass A for the model/GGUF loader group.
- [x] Complete file-by-file Pass A for the public API/minimal-example group.
- [x] Add CI validation for canonical local routes and section anchors embedded in interactive assets.
- [x] Publish the canonical memory-lifetime atlas and interactive ownership/lifetime overlay.
- [x] Publish canonical `llama_model`, `llama_context`, graph/MoE, model-placement, and GGUF-anatomy pages with explorer integration.
- [x] Add the six-tab foundations explorer and four-pass file-by-file/subsystem-synthesis roadmap.
- [x] Document scheduler execution, generic copy fallback, CPU/CUDA/Metal/Vulkan/SYCL semantics, and the central buffer compatibility matrix.
- [x] Add strict CI, Pages deployment health checking, source indexing, and durable scheduled-run context.
<!-- PROJECT-TODOS:END -->

## Contribution and license

Implementation claims need pinned source links, truth labels, affected files/functions/backends, diagram updates when relevant, and honest validation results. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

Original project code and prose are MIT licensed. Upstream llama.cpp remains under its own license and is linked rather than copied.
