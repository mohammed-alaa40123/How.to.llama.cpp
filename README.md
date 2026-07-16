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
| Every push/PR | `.github/workflows/docs-ci.yml` | Validate context, links, scripts, tests, assets, strict MkDocs output, built-site accessibility structure, and representative Chromium routes |
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

- [ ] Inspect the three-way-classifier Chromium result and retained `diagnostics.jsonl`; keep explicit same-origin failures and functional Mermaid, route, viewport, focus, overflow, iframe, and reduced-motion checks strict.
- [ ] Verify the post-merge Pages deployment and audit the homepage, Architecture index, grouped navigation, search, diagrams, iframe interactions, keyboard access, card layout, and responsive behavior.
- [ ] Generate and compile the staged two-file CPU_REPACK lifetime candidate against current upstream `8ee54c8`, requiring AVX2, exact path admission, numerical agreement, and ASan/LSan-clean backend-before-buffer teardown.
- [ ] Open or manually stage the current-tree CPU_REPACK regression pull request after runtime validation; connected GitHub App upstream write permission may remain blocked.
- [ ] Add an admitted ARM NEON+dotprod or KleidiAI optional-buffer lifetime fixture with the same exact-path, numerical, teardown, and sanitizer requirements.
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

### Future improvements

- [ ] Vendor Mermaid locally or otherwise remove the production CDN dependency after measuring its browser and Pages impact.
- [ ] Add axe-core and explicit computed-contrast/focus-style checks to the representative browser route set after the smoke lane stabilizes.
- [ ] Audit standalone interactive explorers for complete keyboard operation, visible focus, text equivalents, and iframe/fullscreen fallbacks.
- [ ] Add an Inference lifecycle section index if deployed review confirms the same cross-section discoverability gap.
- [ ] Remove or explicitly explain the duplicate Foundations explorer navigation entry.
- [ ] Add text equivalents, legends, fullscreen/static fallbacks, and mobile variants for major diagrams and interactive explorers.
- [ ] Add repeated CPU_REPACK executions inside one process to complement the passing twenty-process teardown coverage.
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

- [x] Inspect the second representative Chromium failure: run `29509089935` again reached only the first browser case; successful local responses exposed the remaining empty-location-as-local assumption, so console diagnostics now use same-origin, cross-origin, and unlocated classes and retain per-case JSONL evidence.
- [x] Inspect the first representative Chromium smoke failure: run `29504440262` reached only the browser step; retained evidence showed a rendered homepage, visible skip-link focus, rendered Mermaid, and no local HTTP failure, so cross-origin diagnostics are now warnings while same-origin errors and functional Mermaid rendering remain strict.
- [x] Add a representative Chromium smoke lane for the homepage, Architecture index, a diagram-heavy page, and the interactive inference workflow at desktop and mobile widths, with failure screenshots retained by Documentation CI.
- [x] Inspect the first generated-site accessibility result: Documentation CI run `29496291134` passed strict MkDocs output and the accessibility structure validator without a Material-theme exception.
- [x] Add a dependency-free built-site accessibility structure check for language metadata, main landmarks, top-level headings, image alternatives, iframe titles, and button names, with focused tests and Documentation CI integration.
- [x] Add an Architecture section index with six goal-based entry points, concise summaries for all Architecture pages, and ordered paths for beginners, mmap/copy/page-fault research, scheduling, and teardown.
- [x] Group the flat Architecture navigation into Core architecture, Ownership and teardown, CPU optional buffers, and Accelerator backends without changing page routes.
- [x] Complete a structured website UX review covering information architecture, discoverability, diagrams, interaction, accessibility, consistency, and live-verification blockers.
- [x] Decide upstream suitability of the passing CPU_REPACK fixture and stage a narrow two-file proposal at `docs/reference/upstream-cpu-repack-lifetime-fixture-proposal.md`, reviewed against current upstream `8ee54c8`.
- [x] Preserve the first passing CPU_REPACK workflow evidence: run `29481384561`, twenty AVX2-confirmed ASan/LSan processes, stable NMSE `3.82787e-16`, no skip, and artifact `8368782428` with digest `sha256:ef4f0a36e27f7811b106e0a870c278724f1e620aed991807b7f2c3e443d1efaf`.
- [x] Update the CPU optional-buffer destruction-harness page with the executable CPU_REPACK result and bounded ownership conclusion.
- [x] Add a pinned-source AVX2-confirmed ASan/LSan workflow that materializes, compiles, and requires twenty non-skipped executions of the generated CPU_REPACK fixture.
- [x] Replace the generated CPU_REPACK fixture's intentional status-2 boundary with complete two-graph construction, deterministic shared Q4_0/F32 inputs, compute/readback, `1e-7` NMSE, exact path proof, and backend-before-buffer teardown.
- [x] Confirm the pinned per-tensor allocation API: allocate a backend buffer using `ggml_backend_buft_get_alloc_size()`, pass an aligned address from its base to `ggml_backend_tensor_alloc()`, and preserve explicit buffer ownership.
- [x] Resolve the pinned CPU_REPACK fixture's no-allocation graph/allocation topology and reuse the backend-op `1e-7` NMSE contract for identical quantized inputs.
- [x] Add a deterministic pinned-revision generator and structural tests for the CPU_REPACK lifetime fixture patch.
- [x] Select the first CPU repack regression's exact pinned case: Q4_0 `[32, 8]` × F32 `[32, 1]` on AVX2, with pointer-identity, trait, and operation-admission guards.
- [x] Identify `tests/test-cpu-extra-buffer-lifetime.cpp` as the dedicated integration point and reuse the backend-op harness approach.
- [x] Audit current upstream OpenCL ownership and generate/review a behavior-preserving 46-release patch preserving all waits.
- [x] Resolve the pinned OpenCL wait groups, synchronous tensor-set contract, event ownership, queue/context lifetime, and Adreno library lifetime.
- [x] Add source indexing, canonical GGUF/model/context/graph/scheduler/memory pages, inference atlas, teardown audit method, and CPU optional-buffer destruction specification.
<!-- PROJECT-TODOS:END -->

## Contribution and license

Implementation claims need pinned source links, truth labels, affected files/functions/backends, diagram updates when relevant, and honest validation results. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

Original project code and prose are MIT licensed. Upstream llama.cpp remains under its own license and is linked rather than copied.
