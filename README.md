# How.to.llama.cpp

**A source-guided, revision-pinned map of llama.cpp and GGML.**

How.to.llama.cpp explains the path from a GGUF file to generated tokens: backend discovery, model loading, virtual memory, `llama_model`, `llama_context`, GGML graph construction, scheduling, kernels, outputs, sampling, and teardown.

> **Initial upstream baseline:** [`e3546c7948e3af463d0b401e6421d5a4c2faf565`](https://github.com/ggml-org/llama.cpp/commit/e3546c7948e3af463d0b401e6421d5a4c2faf565)
>
> Newer upstream refs are indexed separately. Baseline claims must not be silently rewritten as llama.cpp changes.

## What the project contains

- MkDocs Material documentation with source-pinned figures and tables.
- Beginner-readable and source-level inference walkthroughs.
- Canonical pages for GGUF, model loading, `llama_model`, `llama_context`, graph construction and reuse, schedulers, memory, synchronization, and backends.
- Clickable foundations and inference explorers.
- A research ledger for official docs, PRs, discussions, papers, talks, videos, blogs, and technical posts.
- Scripts for source mirroring, indexing, context loading, validation, and site health checks.
- GitHub Actions for context validation, upstream indexing, strict documentation CI, pinned/current OpenCL evidence, and Pages deployment.

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
| Daily | Website quality review | Review discoverability, traceability, accessibility, diagrams, and interactions |
| Hourly at minute 23 UTC | `.github/workflows/hourly-context-check.yml` | Validate context and scripts |
| Daily at 02:17 UTC | `.github/workflows/refresh-source-index.yml` | Refresh upstream source inventory through a PR |
| Manual and extractor changes | `.github/workflows/opencl-lifecycle-report.yml` | Preserve and validate pinned OpenCL lifecycle evidence |
| Manual and current-audit changes | `.github/workflows/current-opencl-lifecycle-audit.yml` | Regenerate exact current-upstream OpenCL ownership evidence |
| Every push/PR | `.github/workflows/docs-ci.yml` | Validate context, links, scripts, tests, assets, and `mkdocs build --strict` |
| Every push to `main` | `.github/workflows/pages.yml` | Build, deploy, and verify the public site |

## Implementation method

### Pin the evidence scope

Record the exact commit, branch, PR, discussion, test, or trace. Baseline metadata is in [`data/upstream.json`](data/upstream.json).

### Analyze files, then synthesize subsystems

For each relevant file, record purpose, major objects/functions, callers/callees, ownership, allocations/mappings/copies, threads and synchronization, error paths, backend differences, tests, and runtime evidence. Then synthesize public API, model/GGUF loading, runtime context, memory, GGML core, scheduler, CPU, accelerator backends, model architectures, and tools/tests.

`scripts/index_upstream.py` is a navigation aid, not a compiler-grade call graph. OpenCL lifecycle scripts are bounded evidence tools, not general C++ ownership analyzers.

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
| `docs/lifecycle/inference-atlas.md` | Clickable end-to-end pipeline |
| `docs/foundations/gguf-file-anatomy.md` | GGUF layout, descriptors, mmap, and ownership |
| `docs/foundations/model-tensor-placement.md` | Layer/device assignment, mappings, uploads, and ownership |
| `docs/foundations/memory-lifetimes.md` | Ownership and lifetime atlas |
| `docs/objects/llama-model.md` | Persistent model state and teardown |
| `docs/objects/llama-context.md` | Mutable runtime state and lifetime |
| `docs/ggml/graph-construction-and-moe.md` | Graph construction, reuse, MoE routing, and cache design |
| `docs/architecture/backend-teardown-audit-method.md` | Reusable completion/ownership audit worksheet |
| `docs/architecture/cpu-extra-buffer-destruction-harness.md` | CPU optional-buffer lifetime fixture specification |
| `docs/architecture/opencl-build-and-buffer-lifetimes.md` | OpenCL lifecycle and ownership audit |

<!-- PROJECT-TODOS:START -->
## Living TODO list

Keep unfinished work in priority order. Remove duplicates and move old completion history into the research log when this section grows.

### Highest priority

- [ ] Implement `tests/test-cpu-extra-buffer-lifetime.cpp` using the pinned minimal admitted case: Q4_0 weight `[32, 8]` × F32 activation `[32, 1]`, assert `CPU_REPACK` pointer identity/traits/admission, compare against ordinary CPU, then free the CPU backend wrapper before the retained repack buffer under repeated ASan/LSan execution on an AVX2-confirmed runner.
- [ ] Add the fixture CMake target and sanitizer workflow; treat absence of AVX2 as an explicit skip, but fail when AVX2 is present and the pinned case is not admitted.
- [ ] Submit or manually stage the reviewed 46-release current-upstream OpenCL ownership correction; upstream GitHub App write permission is currently blocked.
- [ ] Decide whether a move-only OpenCL event owner is worthwhile after the narrow explicit-release correction.
- [ ] Decide whether deterministic OpenCL registry/process-exit teardown should be documented as an upstream improvement.
- [ ] Regenerate the pinned source inventory with line-aware `symbol_locations`, pinned links, and unsupported-syntax counts.
- [ ] Extend CPU extra-buffer lifetime fixtures to KleidiAI, AMX, and SpacemiT hardware paths.
- [ ] Verify SpacemiT worker cleanup and process-level Spine pool, huge-page mapping, device-fd, and TCM shutdown.
- [ ] Validate KleidiAI null readback/copy callbacks, concurrent initialization, packed-layout portability, and packed-slot expansion.
- [ ] Validate AMX allocator pairing, repeated tile-permission initialization, and disabled readback/copy paths.
- [ ] Verify CANN reset semantics with authoritative runtime documentation and a destruction-order matrix.
- [ ] Design and test real RPC synchronization/completion and shared-socket serialization.
- [ ] Verify SYCL all-queue and CUDA all-stream synchronization coverage.
- [ ] Determine Vulkan performance-query-pool ownership and persistent device teardown.
- [ ] Map architecture-specific graph-builder downcasts to `llama_memory_context_i` subtypes and exact state tensors.
- [ ] Add runtime evidence for page faults, copies, event waits, KV/recurrent growth, activation peaks, synchronization, and teardown.
- [ ] Verify latest Documentation CI, pinned/current OpenCL workflows, Pages deployment, and hourly context checks.
- [ ] Verify the public Pages site returns HTTP 200 and renders branch-added architecture pages after PR #1 merges.

### Future improvements

- [ ] Add an ARM NEON+dotprod CPU repack lifetime case after the x86 AVX2 fixture.
- [ ] Document ordinary `ggml_backend_tensor_set()` completion semantics explicitly or record a deliberate weaker contract.
- [ ] Rename the three OpenCL classifier records to `return_boundary_expansion_completion`.
- [ ] Add sanitizer regression tests for backend-before-scheduler destruction.
- [ ] Extend interactive-link validation to built HTML IDs, generated routes, assets, and plugin-generated anchors.
- [ ] Locate strong public contracts for model sharing, context concurrency, thread safety, backend synchronization, and destruction order.
- [ ] Prototype per-layer LRU expert-cache instrumentation with separate logical, OS-residency, and backend-copy validity.
- [ ] Prototype cache-aware routing before `ggml_argsort_top_k()`.
- [ ] Quantify mmap alias, mapped-copy, direct-read, synchronous-upload, and asynchronous-upload paths.
- [ ] Add dedicated mmap/page-fault, CPU-thread, backend-queue, KV-cache, recurrent-memory, MoE-routing, and scheduler-timeline visualizers.

### Completed

- [x] Select the first CPU repack regression's exact pinned case: Q4_0 `[32, 8]` × F32 `[32, 1]` on AVX2, with pointer-identity, trait, and operation-admission guards.
- [x] Identify `tests/test-cpu-extra-buffer-lifetime.cpp` as the dedicated integration point and reuse the backend-op harness approach.
- [x] Audit current upstream OpenCL ownership and generate/review a behavior-preserving 46-release patch preserving all waits.
- [x] Resolve the pinned OpenCL wait groups, synchronous tensor-set contract, event ownership, queue/context lifetime, and Adreno library lifetime.
- [x] Add source indexing, canonical GGUF/model/context/graph/scheduler/memory pages, inference atlas, teardown audit method, and CPU optional-buffer destruction specification.
<!-- PROJECT-TODOS:END -->

## Contribution and license

Implementation claims need pinned source links, truth labels, affected files/functions/backends, diagram updates when relevant, and honest validation results. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

Original project code and prose are MIT licensed. Upstream llama.cpp remains under its own license and is linked rather than copied.
