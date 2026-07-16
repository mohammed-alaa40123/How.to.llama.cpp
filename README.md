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
- GitHub Actions for context validation, upstream indexing, strict documentation CI, generated-site browser smoke checks, pinned/current OpenCL evidence, CPU_REPACK sanitizer evidence, and Pages deployment.

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
| CPU_REPACK fixture changes | `.github/workflows/cpu-repack-lifetime-sanitizer.yml` | Compile and repeatedly execute the pinned fixture under ASan/LSan on AVX2 |
| Every push/PR | `.github/workflows/docs-ci.yml` | Validate context, links, scripts, tests, assets, strict MkDocs output, accessibility structure, and representative Chromium routes |
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
./scripts/prepare_mermaid_asset.sh
mkdocs build --strict
python3 scripts/validate_built_site_accessibility.py site
python3 -m http.server 8000 --directory site
BASE_URL=http://127.0.0.1:8000 node scripts/validate_browser_smoke.mjs
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
| `docs/architecture/index.md` | Audience-based Architecture reading paths and page summaries |
| `docs/architecture/backend-teardown-audit-method.md` | Reusable completion/ownership audit worksheet |
| `docs/architecture/cpu-extra-buffer-destruction-harness.md` | CPU optional-buffer lifetime fixture specification and executable evidence |
| `docs/architecture/opencl-build-and-buffer-lifetimes.md` | OpenCL lifecycle and ownership audit |

<!-- PROJECT-TODOS:START -->
## Living TODO list

Keep unfinished work in priority order. Remove duplicates and move old completion history into the research log when this section grows.

### Highest priority

- [ ] Inspect the corrected Mermaid generated-SVG detector result across the full four-route by two-viewport matrix.
- [ ] If visible rendering is recognized but `pageerror: Object` remains, preserve the exact Mermaid rejection object before deciding whether it is a real site failure.
- [ ] Fix or explicitly classify the external GitHub releases-API 404 observed in browser diagnostics.
- [ ] Verify the post-merge Pages deployment and audit the homepage, Architecture index, grouped navigation, search, diagrams, iframe interactions, keyboard access, card layout, and responsive behavior.
- [ ] Generate and compile the staged two-file CPU_REPACK lifetime candidate against current upstream `8ee54c8`, requiring AVX2, exact path admission, numerical agreement, and ASan/LSan-clean backend-before-buffer teardown.
- [ ] Open or manually stage the current-tree CPU_REPACK regression pull request after runtime validation; connected GitHub App upstream write permission may remain blocked.
- [ ] Add an admitted ARM NEON+dotprod or KleidiAI optional-buffer lifetime fixture with the same exact-path, numerical, teardown, and sanitizer requirements.
- [ ] Submit or manually stage the reviewed 46-release current-upstream OpenCL ownership correction; upstream GitHub App write permission is currently blocked.
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

### Future improvements

- [ ] Add a pinned checksum for the prepared Mermaid asset after the first successful same-origin browser run establishes the exact bytes.
- [ ] Add axe-core and explicit computed-contrast/focus-style checks after the representative browser matrix stabilizes.
- [ ] Audit standalone interactive explorers for complete keyboard operation, visible focus, text equivalents, and iframe/fullscreen fallbacks.
- [ ] Add an Inference lifecycle section index if deployed review confirms the same discoverability gap.
- [ ] Remove or explicitly explain the duplicate Foundations explorer navigation entry.
- [ ] Add text equivalents, legends, fullscreen/static fallbacks, and mobile variants for major diagrams and interactive explorers.
- [ ] Add repeated CPU_REPACK executions inside one process to complement the passing twenty-process teardown coverage.
- [ ] Document ordinary `ggml_backend_tensor_set()` completion semantics explicitly or record a deliberate weaker contract.
- [ ] Decide whether a move-only OpenCL event owner is worthwhile after the narrow explicit-release correction.
- [ ] Decide whether deterministic OpenCL registry/process-exit teardown should be documented as an upstream improvement.
- [ ] Rename the three OpenCL classifier records to `return_boundary_expansion_completion`.
- [ ] Add sanitizer regression tests for backend-before-scheduler destruction.
- [ ] Extend interactive-link validation to built HTML IDs, generated routes, assets, and plugin-generated anchors.
- [ ] Locate strong public contracts for model sharing, context concurrency, thread safety, backend synchronization, and destruction order.
- [ ] Prototype per-layer LRU expert-cache instrumentation with separate logical, OS-residency, and backend-copy validity.
- [ ] Prototype cache-aware routing before `ggml_argsort_top_k()`.
- [ ] Quantify mmap alias, mapped-copy, direct-read, synchronous-upload, and asynchronous-upload paths.
- [ ] Add dedicated mmap/page-fault, CPU-thread, backend-queue, KV-cache, recurrent-memory, MoE-routing, and scheduler-timeline visualizers.

### Completed

- [x] Inspect the first same-origin Mermaid Chromium result: run `29521791301` retained a screenshot with a visibly rendered flowchart while the detector reported zero; correct the detector to recognize generated Mermaid SVGs while preserving exact source-diagram counts.
- [x] Move Mermaid from browser-runtime CDN loading to a pinned build-time local asset shared by Documentation CI and Pages after the full readiness bound still produced zero SVGs.
- [x] Inspect the third representative Chromium failure: run `29513543532` reached the real Mermaid assertion and failed `0 of 1` about 2.6 seconds after browser start; the validator now waits for the exact SVG postcondition for up to 15 seconds while preserving a hard bounded failure.
- [x] Inspect the second representative Chromium failure and replace empty-location-as-local with same-origin, cross-origin, and unlocated diagnostic classes plus per-case JSONL evidence.
- [x] Inspect the first representative Chromium failure and keep same-origin errors and functional Mermaid rendering strict while treating external diagnostics as warnings.
- [x] Add a representative Chromium smoke lane for four routes at desktop and mobile widths with retained failure evidence.
- [x] Add and validate a dependency-free built-site accessibility structure guard.
- [x] Add an Architecture section index and task-oriented navigation grouping.
- [x] Complete a structured website UX review.
- [x] Decide upstream suitability of the passing CPU_REPACK fixture and stage a narrow two-file proposal.
- [x] Preserve twenty passing AVX2-confirmed CPU_REPACK ASan/LSan processes with stable NMSE `3.82787e-16`.
- [x] Audit current upstream OpenCL ownership and generate a behavior-preserving 46-release correction.
- [x] Add source indexing, canonical GGUF/model/context/graph/scheduler/memory pages, inference atlas, teardown audit method, and CPU optional-buffer destruction specification.
<!-- PROJECT-TODOS:END -->

## Contribution and license

Implementation claims need pinned source links, truth labels, affected files/functions/backends, diagram updates when relevant, and honest validation results. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

Original project code and prose are MIT licensed. Upstream llama.cpp remains under its own license and is linked rather than copied.
