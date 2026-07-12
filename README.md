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

A mature topic should include:

1. a five-minute explanation;
2. an end-to-end flow;
3. a source-level call chain;
4. memory and concurrency notes;
5. backend differences;
6. figures or interactive diagrams;
7. external references and runtime evidence;
8. version caveats and open questions.

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
| `docs/reference/documentation-quality-roadmap.md` | Object-centred, searchable, and interactive documentation plan |
| `docs/foundations/interactive-system-map.md` | Large clickable foundations map and tabbed explorer |
| `docs/foundations/gguf-file-anatomy.md` | Canonical GGUF layout, metadata, descriptors, split indexing, loader entry, mmap, and ownership |
| `docs/foundations/model-tensor-placement.md` | Layer/device assignment, buffer selection, mappings, alias/read/upload paths, synchronization, and ownership |
| `docs/foundations/memory-lifetimes.md` | Canonical ownership and lifetime atlas for storage, mappings, page cache, model buffers, context state, graph allocations, copies, outputs, synchronization, and teardown |
| `docs/objects/llama-model.md` | Canonical `llama_model` creation, architecture dispatch, tensor/layer schema, storage ownership, graph factory, sharing, and teardown |
| `docs/objects/llama-context.md` | Canonical `llama_context` creation, ownership, lifetime, memory, execution, synchronization, and teardown |
| `docs/ggml/graph-construction-and-moe.md` | Graph construction, MoE routing, graph reuse, router patch points, and per-layer LRU design |
| `docs/reference/source-index.md` | Human-reviewed source areas |
| `data/upstream.json` | Pinned upstream metadata |
| `data/generated/` | Generated source inventories |
| `docs/assets/interactive/` | Interactive architecture assets |
| `scripts/validate_interactive_links.py` | Static validation for local routes and Markdown section anchors embedded in interactive assets |
| `.github/workflows/` | CI, Pages, context, and indexing automation |
| `scripts/` | Bootstrap, validation, indexing, and health checks |

<!-- PROJECT-TODOS:START -->
## Living TODO list

Keep unfinished work in priority order. Remove duplicates and move old completion history into the research log when this section grows.

### Highest priority

- [ ] Begin file-by-file Pass A with public API/examples, model/GGUF loader, and runtime context files; produce subsystem relationship diagrams after each group.
- [ ] Add exact pinned line-level source citations to the graph-construction chapter once the generated source-link checker is ready.
- [ ] Add runtime evidence separating parsing, mapping/prefetch, page faults, direct reads, alias bytes, upload bytes, event waits, first-token access, KV/recurrent growth, activation peaks, and teardown.
- [ ] Expand the interactive explorer with architecture-specific graph-builder sublayers, prefill/decode variants, KV/recurrent state, MoE, and runtime-measured overlays.
- [ ] Replace curated interactive metadata with generated versioned JSON shared by object pages, source maps, and visualizers.
- [ ] Verify the latest **Documentation CI**, **Deploy documentation**, and **Hourly research context check** runs after this increment.
- [ ] Verify the public Pages site returns HTTP 200 and renders the interactive memory overlay plus `foundations/memory-lifetimes/` with expected How.to.llama.cpp content.

### Future improvements

- [ ] Extend interactive-link validation to generated routes, built HTML IDs, non-HTML assets, and MkDocs plugin-generated anchors.
- [ ] Trace every concrete `llama_memory_i` implementation and map architectures to KV, recurrent, and hybrid memory.
- [ ] Document exact ownership members inside `llama_model::impl`.
- [ ] Locate the strongest explicit public contract for model sharing, thread safety, backend teardown synchronization, and destruction order.
- [ ] Prototype per-layer LRU expert-cache instrumentation using `(layer_id, expert_id)` keys and separate logical, OS-residency, and backend-copy validity fields.
- [ ] Prototype cache-aware routing by adding selection-only bias before `ggml_argsort_top_k()`.
- [ ] Quantify backend entry into mmap alias, mapped-copy, direct-read, synchronous-upload, and asynchronous-upload paths.
- [ ] Trace direct-I/O alignment/fallback behavior with runtime evidence.
- [ ] Add reusable page metadata for prerequisites, related objects, source symbols, and next pages.
- [ ] Extend the source index with per-file, object, symbol, subsystem, and caller/callee landing pages.
- [ ] Add dedicated mmap/page-fault, CPU-thread, backend-queue, KV-cache, MoE-routing, and scheduler-timeline visualizers.
- [ ] Trace exact Metal shared/private buffer-level set/get/copy branches.
- [ ] Measure mmap page faults, queue/fence waits, temporary RSS, and copy/compute overlap for representative prefill and decode runs.
- [ ] Extend backend comparisons to RPC, CANN, OpenCL, Android-specific backends, and later scheduler-copy revisions.
- [ ] Expand graph-reuse documentation with every specialized `can_reuse()` predicate.
- [ ] Add a searchable index for detailed research logs and commit-pinned link checking.

### Completed

- [x] Add CI validation for canonical local routes and section anchors embedded in interactive HTML/JavaScript assets, with valid/invalid fixture tests and actionable asset/route/anchor errors.
- [x] Connect all eight memory-lifecycle explorer entries to the canonical atlas and add an accessible ownership/lifetime overlay with owner, backing, validity/residency, synchronization, and release fields.
- [x] Publish the canonical memory-lifetime atlas covering GGUF storage, virtual mappings, page faults/page cache/RSS, model buffers, KV/recurrent/hybrid state, graph allocations, scheduler copies, backend staging, outputs, prefill/decode differences, synchronization, teardown, runtime measurements, and truth labels.
- [x] Link the interactive **Model object** layer to `objects/llama-model/` with top-level navigation.
- [x] Publish the canonical `llama_model` object page with architecture dispatch, common/architecture loading boundaries, tensor and layer schemas, persistent storage ownership, device placement, graph-builder delegation, context sharing, memory factory, teardown, source map, and truth labels.
- [x] Add `llama_model` to top-level Objects navigation.
- [x] Link graph-construction, graph-expansion, MoE routing, GGML graph, and graph-reuse explorer entries to the canonical graph chapter.
- [x] Publish canonical graph-construction/MoE, model-placement, GGUF anatomy, and `llama_context` chapters.
- [x] Add the six-tab foundations explorer and four-pass file-by-file/subsystem-synthesis roadmap.
- [x] Document scheduler execution, generic copy fallback, CPU/CUDA/Metal/Vulkan/SYCL semantics, and the central buffer compatibility matrix.
- [x] Add strict CI, Pages deployment health checking, source indexing, and durable scheduled-run context.
<!-- PROJECT-TODOS:END -->

## Contribution and license

Implementation claims need pinned source links, truth labels, affected files/functions/backends, diagram updates when relevant, and honest validation results. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

Original project code and prose are MIT licensed. Upstream llama.cpp remains under its own license and is linked rather than copied.
