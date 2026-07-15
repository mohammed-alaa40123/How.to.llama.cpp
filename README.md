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
- GitHub Actions for hourly context validation, daily upstream indexing, strict documentation CI, pinned OpenCL lifecycle/source evidence, and Pages deployment.

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
| Manual and extractor-related PR changes | `.github/workflows/opencl-lifecycle-report.yml` | Fetch exact pinned OpenCL source, generate the lifecycle report, preserve both with checksums |
| Every push/PR | `.github/workflows/docs-ci.yml` | Validate context, links, scripts, tests, assets, and `mkdocs build --strict` |
| Every push to `main` | `.github/workflows/pages.yml` | Build, deploy, and verify the public site |

## Implementation method

### Pin the evidence scope

Record the exact commit, branch, PR, discussion, test, or trace. Baseline metadata is in [`data/upstream.json`](data/upstream.json).

### Analyze files, then synthesize subsystems

For each relevant file, record purpose, major objects and functions, callers/callees, ownership, allocations/mappings/copies, threads and synchronization, error paths, backend differences, tests, and runtime evidence. Then synthesize public API, model/GGUF loading, runtime context, memory, GGML core, scheduler, CPU, accelerator backends, model architectures, and tools/tests.

`scripts/index_upstream.py` is a navigation aid, not a compiler-grade call graph. It emits source-ordered symbol locations with approximate declaration kinds, 1-based lines, optional revision-pinned file and symbol links, and bounded unsupported-syntax candidate counts. `scripts/extract_opencl_lifecycle_calls.py` inventories selected OpenCL ownership, completion, and release calls after masking comments and quoted literals. `.github/workflows/opencl-lifecycle-report.yml` now preserves the exact pinned translation unit, generated JSON report, and SHA-256 manifest in one artifact.

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
| `docs/lifecycle/inference-atlas.md` | Clickable end-to-end pipeline and audience-specific reading paths |
| `docs/foundations/interactive-system-map.md` | Clickable foundations map |
| `docs/foundations/gguf-file-anatomy.md` | GGUF layout, descriptors, mmap, and ownership |
| `docs/foundations/model-tensor-placement.md` | Layer/device assignment, mappings, upload paths, and ownership |
| `docs/foundations/memory-lifetimes.md` | Ownership and lifetime atlas |
| `docs/objects/llama-model.md` | `llama_model` construction, storage, graph factory, and teardown |
| `docs/objects/llama-context.md` | `llama_context` runtime state and lifetime |
| `docs/ggml/graph-construction-and-moe.md` | Graph construction, reuse, MoE routing, and cache design |
| `docs/architecture/backend-teardown-audit-method.md` | Reusable completion/ownership audit worksheet and runtime matrix |
| `docs/architecture/backend-teardown-comparison.md` | Cross-backend completion, resource-independence, and safety matrix |
| `docs/architecture/opencl-build-and-buffer-lifetimes.md` | OpenCL build, source-backed lifecycle inventory, ownership, Adreno library lifetime, and remaining gaps |
| `docs/architecture/cpu-extra-buffer-destruction-harness.md` | Implementation-ready admitted-operation, lifetime-ordering, and sanitizer fixture |
| `docs/reference/source-index.md` | Human-reviewed source areas and generated symbol-location/link format |
| `.github/workflows/docs-ci.yml` | Named validators, isolated unit-test suites, discovery guard, strict build, and actionable failures |
| `.github/workflows/opencl-lifecycle-report.yml` | Exact pinned-source recovery, lifecycle extraction, checksum validation, and artifact preservation |

<!-- PROJECT-TODOS:START -->
## Living TODO list

Keep unfinished work in priority order. Remove duplicates and move old completion history into the research log when this section grows.

### Highest priority

- [ ] Classify OpenCL enqueue-then-release groups that rely on object-retention semantics rather than explicit waits.
- [ ] Decide whether deterministic OpenCL registry/process-exit teardown should be documented as an upstream improvement; include explicit Adreno handle ownership, invalid-symbol cleanup, repeated registration, and shared-library unload behavior.
- [ ] Fix the OpenCL artifact SHA-256 manifest to use artifact-root basenames so `sha256sum -c` works directly after download.
- [ ] Regenerate the pinned source inventory with line-aware `symbol_locations`, pinned links, and unsupported-syntax counts; use actual candidate volume to prioritize scanner work.
- [ ] Implement the first CPU repack regression fixture: admitted supported `MUL_MAT` → reference comparison → CPU backend free → repack buffer free under ASan/LSan.
- [ ] Extend the destruction fixture to KleidiAI, AMX, and SpacemiT hardware paths with explicit admission, allocator, initialization, TCM, and process-pool checks.
- [ ] Verify SpacemiT worker cleanup and process-level Spine pool, huge-page mapping, device-fd, and TCM shutdown.
- [ ] Validate KleidiAI null readback/copy callbacks, concurrent initialization, packed-layout portability, and packed-slot expansion.
- [ ] Validate AMX allocator pairing, repeated tile-permission initialization, and disabled readback/copy paths.
- [ ] Verify CANN reset semantics with authoritative runtime documentation and a destruction-order test matrix.
- [ ] Design and test a real RPC synchronization/completion command and shared-socket serialization.
- [ ] Verify SYCL all-queue and CUDA all-stream synchronization coverage.
- [ ] Determine Vulkan performance-query-pool ownership and persistent device teardown.
- [ ] Add asynchronous-destruction regression tests for accelerator and RPC backends.
- [ ] Map architecture-specific graph-builder downcasts to `llama_memory_context_i` subtypes and exact state tensors.
- [ ] Add runtime evidence for parsing, mapping, page faults, copies, event waits, KV/recurrent growth, activation peaks, synchronization, and teardown.
- [ ] Verify the latest **Deploy documentation** and **Hourly research context check** runs.
- [ ] Verify the public Pages site returns HTTP 200 and renders branch-added architecture pages after PR #1 merges.

### Future improvements

- [ ] Add enclosing-function metadata only for lifecycle groups that remain ambiguous after source review.
- [ ] Extend OpenCL lexical masking only if pinned-source evidence requires raw strings, disabled preprocessor regions, or macro expansion.
- [ ] Add sanitizer regression tests for backend-before-scheduler destruction.
- [ ] Extend interactive-link validation to built HTML IDs, generated routes, assets, and plugin-generated anchors.
- [ ] Locate strong public contracts for model sharing, context concurrency, thread safety, backend synchronization, and destruction order.
- [ ] Prototype per-layer LRU expert-cache instrumentation with separate logical, OS-residency, and backend-copy validity.
- [ ] Prototype cache-aware routing before `ggml_argsort_top_k()`.
- [ ] Quantify mmap alias, mapped-copy, direct-read, synchronous-upload, and asynchronous-upload paths.
- [ ] Extend the source index with file, object, symbol, subsystem, and caller/callee landing pages.
- [ ] Add dedicated mmap/page-fault, CPU-thread, backend-queue, KV-cache, recurrent-memory, MoE-routing, and scheduler-timeline visualizers.
- [ ] Add a searchable detailed-research-log index and commit-pinned link checking.

### Completed

- [x] Resolve the optional Adreno binary-library lifetime: the raw handle is lost, the library remains process-lifetime, invalid-symbol loads are not closed, and close-before-kernel ordering is absent rather than unsafe.
- [x] Preserve the complete exact pinned OpenCL translation unit and SHA-256 manifest beside the generated lifecycle report.
- [x] Resolve pinned OpenCL queue/context ownership: shared context and per-device backend context/queue persist in static process-lifetime device state; wrapper free finishes the queue and drops only a reference.
- [x] Verify pinned OpenCL scheduler events are unsupported and buffer deleters use buffer-local `cl_mem` ownership rather than the destroyed backend wrapper.
- [x] Add direct context/queue creation and retention APIs to the lifecycle extractor with exact-line tests.
- [x] Inspect the complete pinned lifecycle artifact and classify local completion, cross-device synchronization, and temporary wait-before-release paths.
- [x] Add a GitHub-hosted pinned OpenCL report workflow, bounded source context, lexical masking, focused tests, and CI coverage.
- [x] Add bounded source-index support and regressions for attributes, trailing returns, constraints, operators, special members, initializer lists, delegating constructors, and unsupported constructor syntax telemetry.
- [x] Add a reusable backend teardown audit method, cross-backend comparison, CPU optional-buffer lifetime audits, and an implementation-ready destruction harness.
- [x] Publish canonical GGUF, model placement, model/context, graph/MoE, memory-lifetime, scheduler, teardown, and inference-atlas pages.
<!-- PROJECT-TODOS:END -->

## Contribution and license

Implementation claims need pinned source links, truth labels, affected files/functions/backends, diagram updates when relevant, and honest validation results. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

Original project code and prose are MIT licensed. Upstream llama.cpp remains under its own license and is linked rather than copied.