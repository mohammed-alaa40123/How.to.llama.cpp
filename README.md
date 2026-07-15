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

`scripts/index_upstream.py` is a navigation aid, not a compiler-grade call graph. It emits source-ordered symbol locations with approximate declaration kinds, 1-based lines, optional revision-pinned file and symbol links, and bounded unsupported-syntax candidate counts for large translation units. `scripts/extract_opencl_lifecycle_calls.py` separately inventories selected OpenCL completion and release call sites with exact lines after masking C/C++ comments and quoted literals.

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
| `docs/architecture/cpu-extra-buffer-comparison.md` | Cross-implementation ownership comparison and portable destruction-test matrix |
| `docs/architecture/cpu-extra-buffer-destruction-harness.md` | Implementation-ready admitted-operation, lifetime-ordering, and sanitizer fixture |
| `docs/architecture/opencl-build-and-buffer-lifetimes.md` | OpenCL build composition, kernel deployment, and initial buffer ownership |
| `docs/reference/source-index.md` | Human-reviewed source areas and generated symbol-location/link format |
| `.github/workflows/docs-ci.yml` | Named validators, isolated unit-test suites, discovery guard, strict build, and actionable failure reporting |

<!-- PROJECT-TODOS:START -->
## Living TODO list

Keep unfinished work in priority order. Remove duplicates and move old completion history into the research log when this section grows.

### Highest priority

- [ ] Obtain the complete pinned `ggml-opencl.cpp` in CI or a checkout, run `scripts/extract_opencl_lifecycle_calls.py`, inspect every completion/release call in context, and finish the OpenCL teardown audit.
- [ ] Regenerate the pinned source inventory with line-aware `symbol_locations`, pinned source links, and unsupported-syntax counts for braced initializers, multiline initializers, and constructor function-try-blocks; use actual candidate volume to prioritize scanner work.
- [ ] Implement the first CPU repack regression fixture from `cpu-extra-buffer-destruction-harness.md`: admitted supported `MUL_MAT` → reference comparison → CPU backend free → repack buffer free under ASan/LSan.
- [ ] Extend the destruction fixture to KleidiAI, AMX, and SpacemiT hardware paths with explicit admission, allocator, initialization, TCM, and process-pool checks.
- [ ] Verify SpacemiT worker cleanup and process-level Spine pool, huge-page mapping, device-fd, and TCM synchronization shutdown.
- [ ] Validate KleidiAI null readback/copy callbacks, concurrent initialization, packed-layout portability, and packed-slot memory expansion.
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

- [ ] Extend OpenCL lexical masking only if pinned-source evidence requires raw-string, preprocessor-disabled-region, or macro-expansion handling.
- [ ] Pair OpenCL lifecycle release calls with creation/retention sites if the release-only inventory leaves ownership ambiguous.
- [ ] Define constructor function-try-block navigation line semantics and consider stateful extraction only if regenerated pinned-tree counts justify it.
- [ ] Evaluate multiline attributes, multiline constraints/returns, in-class special members, braced or multiline constructor initializer lists, defaulted/deleted definitions, literals, complex conversion operators, and export/declaration macros from the pinned tree before expanding the approximate source scanner further.
- [ ] Extend unsupported-syntax telemetry only after pinned-tree evidence identifies additional high-value missed forms.
- [ ] Upload or preserve validator output as Actions artifacts if isolated suites and verbose unittest output are still insufficient.
- [ ] Validate generated pinned blob URLs and line fragments during Documentation CI.
- [ ] Add sanitizer regression tests for backend-before-scheduler destruction.
- [ ] Extend interactive-link validation to built HTML IDs, generated routes, assets, and plugin-generated anchors.
- [ ] Add RAII guidance or an upstream example patch for deterministic cleanup on minimal-example error paths.
- [ ] Locate strong public contracts for model sharing, context concurrency, thread safety, backend synchronization, and destruction order.
- [ ] Prototype per-layer LRU expert-cache instrumentation with separate logical, OS-residency, and backend-copy validity.
- [ ] Prototype cache-aware routing before `ggml_argsort_top_k()`.
- [ ] Quantify mmap alias, mapped-copy, direct-read, synchronous-upload, and asynchronous-upload paths.
- [ ] Extend the source index with file, object, symbol, subsystem, and caller/callee landing pages.
- [ ] Add dedicated mmap/page-fault, CPU-thread, backend-queue, KV-cache, recurrent-memory, MoE-routing, and scheduler-timeline visualizers.
- [ ] Add a searchable detailed-research-log index and commit-pinned link checking.

### Completed

- [x] Isolate Documentation CI suites, diagnose `try : member(...) {` as a false ordinary-function record, add a bounded `FUNC_RE` guard, and pass full Documentation CI run `29380673982`.
- [x] Mask line comments, block comments, string literals, and character literals before extracting OpenCL lifecycle calls while preserving exact source lines.
- [x] Add a bounded exact-line OpenCL lifecycle-call extractor and focused tests for completion/wait and queue/context/program/kernel/event/buffer release APIs.
- [x] Add bounded constructor function-try-block telemetry for same-line and next-line `try` forms while keeping navigation extraction unchanged.
- [x] Audit constructor function-try-block behavior and confirm it produces neither a partial symbol record nor current unsupported-syntax telemetry.
- [x] Add bounded per-file and aggregate unsupported-syntax counters for braced and multiline constructor initializer candidates without emitting partial symbol records.
- [x] Protect the constructor-initializer scanner boundary with negative tests proving braced and multiline forms are not partially indexed.
- [x] Add explicit regression coverage for bounded same-line qualified delegating constructors with exact source lines.
- [x] Verify that the bounded same-line initializer-list rule already recognizes delegating constructors and remove the false unsupported-capability TODO.
- [x] Recognize bounded same-line out-of-class constructor initializer lists without weakening exact definition-line indexing.
- [x] Recognize bounded same-line qualified out-of-class constructor and destructor definitions while preserving exact definition lines.
- [x] Recognize bounded same-line C++ operator definitions, including qualified symbolic, call, subscript, and single-token conversion operators, while preserving exact definition lines.
- [x] Preserve exact function definition lines across preceding template lines and recognize bounded same-line C++20 `requires` clauses.
- [x] Recognize same-line C++ trailing-return function definitions while preserving exact definition lines.
- [x] Recognize same-line C++ attributes before function return types while preserving exact definition lines.
- [x] Recognize same-line C++ attributes before or after type keywords while preserving exact declaration lines.
- [x] Confirm the source-index type line-number fix and multiple-blank-line/namespace-indentation regression through successful full Documentation CI runs.
- [x] Diagnose and fix source-index type declarations reporting the preceding blank line instead of the declaration line.
- [x] Split Python unit tests into source-index and interactive-link suites while retaining full discovery coverage.
- [x] Split Documentation CI validation into named steps and enable verbose unittest output so failures identify the subsystem.
- [x] Specify an implementation-ready CPU optional-buffer destruction harness.
- [x] Synthesize CPU repack, AMX, KleidiAI, and SpacemiT IME into one ownership/completion comparison and portable test matrix.
- [x] Audit the pinned CPU repack, AMX, KleidiAI, and SpacemiT IME extra-buffer paths.
- [x] Add a reusable backend teardown audit method and cross-backend comparison matrix.
- [x] Add a guided end-to-end inference atlas.
- [x] Add line-aware, revision-pinned source-index links and tests.
- [x] Map pinned OpenCL build composition and initial `cl_mem` ownership.
- [x] Audit pinned CANN, RPC, SYCL, Vulkan, Metal, CUDA, ordinary CPU, and generic scheduler teardown.
- [x] Trace exact `llama_model` and `llama_context` declaration and reverse-destruction order.
- [x] Complete Pass A for public API, model/GGUF loading, runtime context/memory, and scheduler internals.
- [x] Publish canonical GGUF, model placement, model/context, graph/MoE, memory-lifetime, and system-ownership pages.
- [x] Add interactive explorers, validation, strict CI, Pages deployment, source indexing, and durable run context.
<!-- PROJECT-TODOS:END -->

## Contribution and license

Implementation claims need pinned source links, truth labels, affected files/functions/backends, diagram updates when relevant, and honest validation results. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

Original project code and prose are MIT licensed. Upstream llama.cpp remains under its own license and is linked rather than copied.
