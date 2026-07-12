# How.to.llama.cpp

**A source-guided, revision-pinned map of llama.cpp and GGML.**

How.to.llama.cpp explains the path from a GGUF file to generated tokens: backend discovery, model loading, virtual memory, `llama_context`, GGML graph construction, scheduling, kernels, outputs, sampling, and teardown.

> **Initial upstream baseline:** [`e3546c7948e3af463d0b401e6421d5a4c2faf565`](https://github.com/ggml-org/llama.cpp/commit/e3546c7948e3af463d0b401e6421d5a4c2faf565)
>
> Newer upstream refs are indexed separately. Baseline claims must not be silently rewritten as llama.cpp changes.

## What the project contains

- MkDocs Material documentation with source-pinned figures and tables.
- Beginner-readable and source-level inference walkthroughs.
- Documentation for GGUF, model loading, context construction, graph reuse, schedulers, memory, synchronization, and backends.
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
| Daily | Website quality review | Navigate the live site; review foundations, tabs, discoverability, source traceability, accessibility, cross-links, diagrams, and interaction opportunities |
| Hourly at minute 23 UTC | `.github/workflows/hourly-context-check.yml` | Validate context and scripts |
| Daily at 02:17 UTC | `.github/workflows/refresh-source-index.yml` | Refresh upstream source inventory through a PR |
| Every push/PR | `.github/workflows/docs-ci.yml` | Validate context, scripts, assets, and `mkdocs build --strict` |
| Every push to `main` | `.github/workflows/pages.yml` | Build, deploy, and verify the public site |

## Implementation method

### Pin the evidence scope

Record the exact commit, branch, PR, discussion, test, or trace. Baseline metadata is in [`data/upstream.json`](data/upstream.json).

### Analyze files, then synthesize subsystems

For each relevant file, record:

- purpose and directory role;
- major objects, functions, interfaces, callbacks, and registration points;
- callers/callees recoverable from source;
- objects created, owned, referenced, mutated, and destroyed;
- allocations, mappings, copies, workspaces, and reclaim;
- threads, queues, events, barriers, and synchronization;
- error paths, fallbacks, build flags, and backend differences;
- tests, examples, PRs, discussions, and runtime evidence.

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
python3 -m py_compile scripts/*.py
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
| `docs/foundations/interactive-system-map.md` | Large clickable foundations map and tabbed system explorer |
| `docs/foundations/gguf-file-anatomy.md` | Canonical GGUF layout, typed metadata, tensor descriptors, split indexing, loader entry, mmap, and ownership foundation |
| `docs/foundations/model-tensor-placement.md` | Canonical layer/device assignment, per-tensor buffer selection, mappings, alias/read/upload paths, progress, synchronization, and ownership chapter |
| `docs/objects/llama-context.md` | Canonical `llama_context` creation, ownership, lifetime, memory, call-chain, synchronization, and teardown page |
| `docs/reference/source-index.md` | Human-reviewed source areas |
| `data/upstream.json` | Pinned upstream metadata |
| `data/generated/` | Generated source inventories |
| `docs/assets/interactive/` | Interactive architecture assets |
| `.github/workflows/` | CI, Pages, context, and indexing automation |
| `scripts/` | Bootstrap, validation, indexing, and health checks |

<!-- PROJECT-TODOS:START -->
## Living TODO list

Keep unfinished work in priority order. Remove duplicates and move old completion history into the research log when this section grows.

### Highest priority

- [ ] Create the GGML graph-construction chapter: op calls, output tensors as lazy nodes, source edges, graph expansion, insertion ordering, views, activations, allocation, reuse, and execution.
- [ ] Link the interactive graph-construction and graph-expansion cards to the canonical GGML chapter after publication.
- [ ] Build the memory-lifetime chapter and interactive overlay: GGUF bytes, mmap, page faults, page cache/RAM, model buffers, context state, KV/recurrent memory, activations, workspaces, scheduler copies, output buffers, and teardown.
- [ ] Add runtime evidence separating metadata parse, mapping/prefetch, major/minor faults, direct reads, alias bytes, upload bytes, event waits, and first-token access.
- [ ] Begin file-by-file Pass A with public API/examples, model/GGUF loader, and runtime context files; produce subsystem relationship diagrams after each group.
- [ ] Expand the interactive foundations explorer with architecture-specific graph-builder sublayers, prefill/decode variants, KV/recurrent state, MoE, and runtime-measured overlays.
- [ ] Replace curated interactive metadata with generated versioned JSON shared by object pages, source maps, and visualizers.
- [ ] Add CI validation for canonical local links embedded in interactive JavaScript and HTML assets.
- [ ] Verify the latest **Documentation CI**, **Deploy documentation**, and **Hourly research context check** runs after this increment.
- [ ] Verify the public Pages site returns HTTP 200 and renders the GGUF and model-placement chapters, canonical upstream diagram, linked `llama_context` page, and the new explorer links.

### Future improvements

- [ ] Quantify backend entry into the mmap host-pointer alias path for CPU-only, Metal, CUDA, Vulkan, and SYCL configurations.
- [ ] Trace direct-I/O alignment/fallback behavior with runtime evidence.
- [ ] Identify the first later upstream revision that registers or replaces SYCL scheduler `cpy_tensor_async`.
- [ ] Create the next canonical object page for `llama_model`.
- [ ] Add reusable page metadata for prerequisites, related objects, source symbols, and next pages.
- [ ] Extend the source index with per-file, object, symbol, subsystem, and caller/callee landing pages.
- [ ] Add a dedicated mmap/page-fault visualizer with conceptual and runtime-evidence modes.
- [ ] Add CPU-thread, backend-queue, KV-cache, MoE-routing, and scheduler-timeline visualizers.
- [ ] Add automated checks for truth labels, source maps, navigation metadata, iframe assets, and accessible interaction labels.
- [ ] Trace exact Metal shared/private buffer-level set/get/copy branches.
- [ ] Add runtime instrumentation separating generic heap staging, backend temporary staging, and host-forward staging.
- [ ] Measure mmap page faults, queue/fence waits, temporary RSS, and copy/compute overlap for representative prefill and decode runs.
- [ ] Compare Level Zero, OpenCL, and non-Intel SYCL runtime behavior.
- [ ] Validate Vulkan behavior on Android integrated GPUs by vendor.
- [ ] Extend the compatibility matrix to RPC, CANN, OpenCL, and Android-specific backends.
- [ ] Add a backend graph/event capability matrix.
- [ ] Trace later scheduler PRs that changed copy/event ordering.
- [ ] Determine whether newer revisions pool generic or backend staging allocations.
- [ ] Expand graph-reuse documentation with every specialized `can_reuse()` predicate.
- [ ] Add a searchable index for detailed research logs.
- [ ] Add commit-pinned link checking and backend profiler evidence.

### Completed

- [x] Link the interactive GGUF/graph tab to the canonical GGUF file-anatomy and model-tensor-placement pages with top-level navigation.
- [x] Publish the canonical model tensor-placement and transfer chapter covering device assignment, per-tensor buffer selection, mappings, mmap alias/copy branches, direct reads, asynchronous and synchronous uploads, progress, cancellation, validation, mapping trimming, ownership, and truth labels.
- [x] Publish the canonical GGUF file-anatomy foundation with official format structure, verified upstream figure attribution, typed metadata, tensor descriptors, split indexing, loader entry, mmap/page-fault distinctions, ownership, and truth labels.
- [x] Link the interactive **llama_context runtime** layer and **Construct context** workflow step to the canonical `llama_context` page through shared pinned metadata.
- [x] Create and publish the canonical `llama_context` object page with creation, ownership, lifetime, memory, mutation, call chain, synchronization, teardown, source map, related objects, and truth labels.
- [x] Add a large tabbed foundations explorer with hover summaries, clickable system layers, end-to-end code path, memory lifecycle, GGUF/graph explanation, synchronization timeline, and file-group map.
- [x] Update the roadmap with a four-pass file-by-file analysis and subsystem-synthesis program.
- [x] Add and publish the object-centred, searchable, interactive documentation quality roadmap and website review rubric.
- [x] Add website-quality review to the scheduling plan.
- [x] Enable GitHub Pages and publish the public documentation site.
- [x] Add exact pinned SYCL source/destination rows to the central buffer compatibility matrix.
- [x] Distinguish generic emergency staging from SYCL mmap/PVC staging and SYCL host-forward staging.
- [x] Complete Vulkan capability and transfer-path documentation and matrix rows.
- [x] Document CPU, CPU_Mapped, CUDA, Metal, Vulkan, and SYCL buffer/copy semantics.
- [x] Trace generic scheduler fallback and full host-staging behavior.
- [x] Trace decode, graph reuse, scheduler allocation, split execution, and synchronization.
- [x] Replace the broken scheduler Mermaid sequence with an accessible static SVG.
- [x] Add strict CI, Pages deployment health checking, source indexing, and durable scheduled-run context.
<!-- PROJECT-TODOS:END -->

## Contribution and license

Implementation claims need pinned source links, truth labels, affected files/functions/backends, diagram updates when relevant, and honest validation results. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

Original project code and prose are MIT licensed. Upstream llama.cpp remains under its own license and is linked rather than copied.