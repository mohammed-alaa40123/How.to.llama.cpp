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
9. Before finishing, update this README TODO list, project state, research log, and the research ledger when sources change; run relevant validation; inspect GitHub Actions; verify Pages; fix failures when possible or record exact blockers.
10. Store detailed notes under `logs/research/YYYY-MM-DD/HHMM-topic.md`.

Start a local run with:

```bash
./scripts/start_scheduled_run.sh <run-name>
```
<!-- SCHEDULED-RUN-INSTRUCTIONS:END -->

## Scheduling plan

| Schedule | Workflow | Responsibility |
|---|---|---|
| Every hour | Research automation | Complete one source-pinned increment and durable context update |
| Daily | Website quality review | Review discoverability, source traceability, accessibility, diagrams, and interactions |
| Hourly at minute 23 UTC | `.github/workflows/hourly-context-check.yml` | Validate context and scripts |
| Daily at 02:17 UTC | `.github/workflows/refresh-source-index.yml` | Refresh upstream source inventory through a PR |
| Every push/PR | `.github/workflows/docs-ci.yml` | Validate context, links, scripts, tests, assets, and `mkdocs build --strict` |
| Every push to `main` | `.github/workflows/pages.yml` | Build, deploy, and verify the public site |

## Implementation method

### Pin the evidence scope

Record the exact commit, branch, PR, discussion, test, or trace. Baseline metadata is in [`data/upstream.json`](data/upstream.json).

### Analyze files, then synthesize subsystems

For each relevant file, record purpose, major objects and functions, callers/callees, ownership, allocations/mappings/copies, threads and synchronization, error paths, backend differences, tests, and runtime evidence. Then synthesize public API, model/GGUF loading, runtime context, memory, GGML core, scheduler, CPU, accelerator backends, model architectures, and tools/tests.

`scripts/index_upstream.py` is a navigation aid, not a compiler-grade call graph. It emits source-ordered symbol locations with approximate declaration kinds, 1-based lines, and optional revision-pinned file and symbol links for large translation units.

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
| `docs/roadmap.md` | Full implementation and synthesis plan |
| `docs/foundations/interactive-system-map.md` | Clickable foundations map |
| `docs/foundations/gguf-file-anatomy.md` | GGUF layout, descriptors, mmap, and ownership |
| `docs/foundations/model-tensor-placement.md` | Layer/device assignment, mappings, upload paths, and ownership |
| `docs/foundations/memory-lifetimes.md` | Ownership and lifetime atlas |
| `docs/objects/llama-model.md` | `llama_model` construction, storage, graph factory, and teardown |
| `docs/objects/llama-context.md` | `llama_context` runtime state and lifetime |
| `docs/ggml/graph-construction-and-moe.md` | Graph construction, reuse, MoE routing, and cache design |
| `docs/architecture/system-ownership-and-execution-map.md` | Cross-subsystem ownership/execution synthesis |
| `docs/architecture/model-context-teardown-order.md` | Exact model/context destruction order |
| `docs/architecture/scheduler-teardown-core.md` | Generic scheduler free chain and dependencies |
| `docs/architecture/cpu-backend-teardown.md` | Ordinary CPU teardown classification |
| `docs/architecture/cuda-backend-teardown.md` | CUDA teardown and conditional completion |
| `docs/architecture/metal-backend-teardown.md` | Metal explicit synchronization and teardown |
| `docs/architecture/vulkan-backend-teardown.md` | Vulkan explicit synchronization and teardown |
| `docs/architecture/sycl-backend-teardown.md` | SYCL queue, event, buffer, and teardown classification |
| `docs/architecture/rpc-backend-teardown.md` | RPC client/server ownership, remote completion, and teardown |
| `docs/architecture/cann-backend-teardown.md` | CANN device synchronization, reset ordering, and resource lifetimes |
| `docs/architecture/opencl-build-and-buffer-lifetimes.md` | OpenCL build composition, kernel deployment, and initial buffer ownership |
| `docs/reference/source-index.md` | Human-reviewed source areas and generated symbol-location/link format |
| `docs/assets/interactive/` | Interactive architecture assets |
| `.github/workflows/` | CI, Pages, context, and indexing automation |

<!-- PROJECT-TODOS:START -->
## Living TODO list

Keep unfinished work in priority order. Remove duplicates and move old completion history into the research log when this section grows.

### Highest priority

- [ ] Regenerate the pinned source inventory with line-aware `symbol_locations` and pinned source links, then use it to finish the OpenCL backend/context free, queue completion, scheduler-resource, program/kernel/context, and binary-library teardown audit.
- [ ] Audit optional CPU extra-buffer implementations and classify their deleter independence from ordinary CPU backend wrappers.
- [ ] Verify CANN reset semantics with authoritative runtime documentation and a test matrix: destroy streams/events/buffers before versus after `aclrtResetDevice`, one versus two contexts, and scheduler-resource release after backend free.
- [ ] Design and test a real RPC synchronization/completion command; verify immediate graph-compute → remote-buffer-free and graph-compute → connection-close behavior on CPU and accelerator servers.
- [ ] Verify shared RPC socket serialization under concurrent backend/buffer users and document transport error/reconnect semantics.
- [ ] Verify whether SYCL synchronization covers every queue used by multi-device, split-buffer, DNNL, flash-attention, command-graph, and communication paths; determine whether backend free should wait explicitly.
- [ ] Verify whether `ggml_backend_cuda_synchronize()` covers every lazily created concurrent stream and whether context pools/events/graphs should be cleared before stream destruction.
- [ ] Determine whether the pinned Vulkan performance query pool has an explicit owner/destructor or represents a cleanup leak; audit persistent Vulkan device/process-exit teardown.
- [ ] Add asynchronous-destruction regression tests for CUDA-family, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL backends.
- [ ] Map architecture-specific graph-builder downcasts to `llama_memory_context_i` subtypes and exact state tensors.
- [ ] Add runtime evidence separating parsing, mapping/prefetch, page faults, direct reads, alias/upload bytes, scheduler copy generations, event waits, memory-update graphs, KV/recurrent growth, activation peaks, synchronization, and teardown.
- [ ] Add exact pinned line-level source citations to the graph-construction chapter once generated source-link checking is ready.
- [ ] Expand the interactive explorer with architecture-specific builders, prefill/decode variants, KV/recurrent state, MoE, scheduler splits/copies, and runtime overlays.
- [ ] Replace curated interactive metadata with generated versioned JSON shared by object pages, source maps, and visualizers.
- [ ] Verify the latest **Documentation CI**, **Deploy documentation**, and **Hourly research context check** runs after this increment.
- [ ] Verify the public Pages site returns HTTP 200 and renders `reference/source-index/` with expected How.to.llama.cpp content.

### Future improvements

- [ ] Validate generated pinned blob URLs and line fragments during Documentation CI.
- [ ] Add sanitizer regression tests for backend-before-scheduler destruction.
- [ ] Extend interactive-link validation to built HTML IDs, generated routes, assets, and plugin-generated anchors.
- [ ] Add RAII guidance or an upstream example patch for deterministic cleanup on minimal-example error paths.
- [ ] Locate strong public contracts for model sharing, context concurrency, thread safety, backend synchronization, and destruction order.
- [ ] Prototype per-layer LRU expert-cache instrumentation with separate logical, OS-residency, and backend-copy validity.
- [ ] Prototype cache-aware routing before `ggml_argsort_top_k()`.
- [ ] Quantify mmap alias, mapped-copy, direct-read, synchronous-upload, and asynchronous-upload paths.
- [ ] Trace direct-I/O alignment/fallback behavior with runtime evidence.
- [ ] Extend the source index with file, object, symbol, subsystem, and caller/callee landing pages.
- [ ] Add dedicated mmap/page-fault, CPU-thread, backend-queue, KV-cache, recurrent-memory, MoE-routing, and scheduler-timeline visualizers.
- [ ] Expand graph-reuse documentation with every specialized `can_reuse()` predicate.
- [ ] Add a searchable detailed-research-log index and commit-pinned link checking.

### Completed

- [x] Add revision-pinned file and `#L<line>` symbol URLs to the generated source inventory, derive them from the selected llama.cpp revision, and cover URL generation with regression tests.
- [x] Add untruncated, source-ordered symbol records with approximate declaration kind and 1-based line numbers to the generated source inventory, while retaining the legacy compact symbol list and adding regression tests.
- [x] Map pinned OpenCL build composition, kernel deployment modes, official platform scope, and the initial `cl_mem` RAII ownership path.
- [x] Audit pinned CANN teardown: backend/context free, device-wide synchronization, reset ordering, events, allocator buffers, registry lifetime, scheduler-resource independence, and conditional teardown classification.
- [x] Audit pinned RPC teardown: client/backend free, shared socket lifetime, remote buffer release, server dispatch/completion, session cleanup, and backend-before-scheduler classification.
- [x] Audit pinned SYCL teardown: backend/context free, queue wait behavior, command graphs, context-owned pools and scratchpads, scheduler event independence, buffer-local allocation ownership, static buffer types, and conditional queued-work safety classification.
- [x] Finish pinned Vulkan teardown and command-lifetime audits.
- [x] Audit pinned Metal, CUDA, ordinary CPU, and generic scheduler teardown.
- [x] Trace exact `llama_model` and `llama_context` declaration and reverse-destruction order.
- [x] Enumerate concrete context-memory implementations and architecture factory decisions.
- [x] Complete Pass A for public API, model/GGUF loading, runtime context/memory, and scheduler internals.
- [x] Publish canonical GGUF, model placement, model/context, graph/MoE, memory-lifetime, and system-ownership pages.
- [x] Add interactive explorers, validation, strict CI, Pages deployment, source indexing, and durable run context.
<!-- PROJECT-TODOS:END -->

## Contribution and license

Implementation claims need pinned source links, truth labels, affected files/functions/backends, diagram updates when relevant, and honest validation results. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

Original project code and prose are MIT licensed. Upstream llama.cpp remains under its own license and is linked rather than copied.
