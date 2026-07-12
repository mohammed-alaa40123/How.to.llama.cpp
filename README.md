# How.to.llama.cpp

**A source-guided, revision-pinned map of llama.cpp and GGML.**

How.to.llama.cpp explains the full path from a GGUF file to generated tokens: backend discovery, model loading, virtual memory, `llama_context`, GGML graph construction, scheduling, kernels, outputs, sampling, and teardown.

> **Initial upstream baseline:** [`e3546c7948e3af463d0b401e6421d5a4c2faf565`](https://github.com/ggml-org/llama.cpp/commit/e3546c7948e3af463d0b401e6421d5a4c2faf565)
>
> Newer upstream refs are indexed separately. Baseline claims must not be silently rewritten as llama.cpp changes.

## What the project contains

- MkDocs Material documentation with Mermaid figures.
- A beginner-readable end-to-end inference path.
- Source maps for llama.cpp, GGML, schedulers, memory, backends, and concurrency.
- A clickable inference-flow explorer.
- A research ledger for official docs, PRs, discussions, papers, talks, videos, blogs, and technical posts.
- Scripts for upstream mirroring, source indexing, context loading, validation, and website health checking.
- Hourly context validation, daily upstream indexing, strict documentation CI, and Pages deployment.

Current progress and the next source-analysis task live in [`docs/reference/project-state.md`](docs/reference/project-state.md).

---

<!-- SCHEDULED-RUN-INSTRUCTIONS:START -->
## Mandatory startup protocol for every scheduled run

Every scheduled or manual research run must:

1. Read this entire `README.md` first.
2. Read [`docs/reference/project-state.md`](docs/reference/project-state.md).
3. Read the newest entries in [`docs/reference/research-log.md`](docs/reference/research-log.md).
4. Read [`docs/reference/research-ledger.md`](docs/reference/research-ledger.md) before adding sources.
5. Read the latest detailed note under `logs/research/`, when present.
6. Inspect current repository files before editing; never rely only on an earlier run summary.
7. Complete one bounded, reviewable increment: source notes, a verified call chain, a documentation section, a diagram, a reference evaluation, a test, or an indexing improvement.
8. Label claims as **Verified**, **Interpretation**, **Historical**, or **Open question**.
9. Before ending the run:
   - update `docs/reference/research-log.md`;
   - update `docs/reference/project-state.md`;
   - update `docs/reference/research-ledger.md` when sources changed;
   - update diagrams and source links when architecture changed;
   - update the living README TODO list by marking completed work, adding future improvements, removing duplicates, and preserving priority order;
   - inspect the latest GitHub Actions result and the deployed Pages website;
   - fix failures when possible, otherwise record the exact blocker in project state and the TODO list.
10. Store long run notes under `logs/research/YYYY-MM-DD/HHMM-topic.md`.
11. Run the relevant validation commands and report failures honestly.

Start a run with:

```bash
./scripts/start_scheduled_run.sh <run-name>
```

The bootstrap reads this README, project state, the canonical research log, the source ledger, and the latest detailed research note into one run-context bundle.
<!-- SCHEDULED-RUN-INSTRUCTIONS:END -->

## Scheduling plan

| Schedule | Workflow | Responsibility |
|---|---|---|
| Every hour | Research automation | Complete one documentation/research increment; update README TODOs, state, logs, Actions status, and website status |
| Hourly at minute 23 UTC | `.github/workflows/hourly-context-check.yml` | Validate that durable context and scripts remain readable |
| Daily at 02:17 UTC | `.github/workflows/refresh-source-index.yml` | Mirror llama.cpp refs and refresh generated source inventory through a PR |
| Every push/PR | `.github/workflows/docs-ci.yml` | Validate context, scripts, interactive assets, and `mkdocs build --strict` |
| Every push to `main` | `.github/workflows/pages.yml` | Build; deploy when Pages is enabled; verify HTTP 200 and project title |
| Manual | `workflow_dispatch` | Re-run CI, context checks, indexing, or deployment |

## Implementation method

### 1. Pin the evidence scope

Record the exact commit, branch, PR, discussion, test, or runtime trace being analyzed. The baseline metadata is in [`data/upstream.json`](data/upstream.json).

### 2. Map the subsystem before writing prose

For each topic, record:

- public entry points and internal functions;
- interfaces, virtual calls, callbacks, and runtime dispatch;
- owning objects and lifetimes;
- tensors, inputs, outputs, and state mutations;
- allocation, mappings, copies, and reclaim behavior;
- threads, queues, events, barriers, and synchronization;
- error paths, fallbacks, configuration branches, and backend differences.

`scripts/index_upstream.py` is a navigation aid, not a compiler-grade call graph. Macros, templates, function pointers, virtual dispatch, generated code, and backend registration require human verification.

### 3. Write layered documentation

Each mature topic should include:

1. a five-minute explanation;
2. an end-to-end flow;
3. a source-level call chain;
4. memory and concurrency notes;
5. backend-specific differences;
6. Mermaid or generated figures;
7. external references and runtime evidence;
8. version caveats and open questions.

### 4. Maintain the interactive workflow

The interactive asset is [`docs/assets/interactive/inference-flow.html`](docs/assets/interactive/inference-flow.html). Each node should eventually show:

- plain-language purpose;
- exact files and symbols;
- inputs, outputs, state changes, and memory owner;
- executing thread/backend;
- pinned source links;
- related docs, diagrams, PRs, and experiments.

### 5. Validate

```bash
python3 scripts/validate_project_context.py
python3 -m py_compile scripts/*.py
bash -n scripts/*.sh
mkdocs build --strict
./scripts/check_site.sh  # after Pages is enabled and deployed
```

## Context and log map

| Location | Purpose |
|---|---|
| `README.md` | Canonical operating manual, scheduling contract, and living TODOs |
| `docs/reference/project-state.md` | Current milestone, completed work, blockers, and next task |
| `docs/reference/research-log.md` | Concise chronological findings and decisions |
| `logs/research/` | Detailed per-run notes |
| `docs/reference/research-ledger.md` | External sources and evidence-quality assessment |
| `docs/roadmap.md` | Full implementation and research plan |
| `docs/reference/source-index.md` | Human-reviewed important source areas |
| `data/upstream.json` | Pinned upstream metadata |
| `data/generated/` | Regenerated source inventories; do not hand-edit |
| `.upstream/` | Local llama.cpp mirror/worktree; ignored by Git |
| `docs/assets/interactive/` | Clickable architecture and inference visualizations |
| `.github/workflows/` | CI, Pages, context, and source-index automation |
| `scripts/` | Bootstrap, validation, indexing, and health checks |
| `logs/runtime/` | Optional large runtime traces; ignored by default |

Canonical research entries should include scope, verified findings, interpretation, open questions, artifacts changed, validation, and one next step.

<!-- PROJECT-TODOS:START -->
## Living TODO list

Every run maintains this list. Keep unfinished items in priority order and move old completed history into the research log when this section grows.

### Highest priority

- [ ] Enable **Settings → Pages → Build and deployment → Source: GitHub Actions**.
- [ ] Rerun **Deploy documentation** and confirm its build, deploy, and website-verification jobs succeed.
- [ ] Confirm **Documentation CI** and **Hourly research context check** succeed on the latest documentation commits; connected status interfaces may not expose complete push-run conclusions.
- [ ] Confirm the live site returns HTTP 200 and contains `How.to.llama.cpp`; direct verification remains blocked until Pages is enabled and publicly reachable.
- [ ] Trace SYCL buffer host, USM, and device allocation semantics.
- [ ] Trace SYCL blocking set/get/direct-copy callbacks, scheduler `cpy_tensor_async` acceptance, queue/event ordering, and return-time completion.
- [ ] Add exact SYCL source/destination rows to `docs/lifecycle/buffer-compatibility.md`.
- [ ] Trace exact Metal shared/private buffer-level copy branches below the wrapper layer.
- [ ] Add runtime instrumentation for page faults, synchronization bubbles, transfer overlap, direct-copy acceptance, backend staging, heap staging, and temporary RSS.

### Future improvements

- [ ] Validate Vulkan behavior on Android integrated GPUs and record memory-type, staging, queue-family, and fence-latency differences by vendor.
- [ ] Add Vulkan runtime counters for registered-host fast paths versus ordinary-host synchronizing staging.
- [ ] Extend the buffer matrix to RPC, CANN, OpenCL, SYCL, and Android-compiled backend combinations.
- [ ] Add backend-specific runtime traces proving copy/compute overlap during prompt processing and token decode.
- [ ] Add a matrix for CPU, CUDA, Metal, Vulkan, SYCL, RPC, and Android GPU graph/event capabilities.
- [ ] Trace later scheduler PRs that changed copy/event ordering and compare them with the pinned baseline.
- [ ] Determine whether newer revisions pool or reuse generic and backend-specific host staging allocations.
- [ ] Compare newer Metal changes affecting queue ownership, `cmd_buf_last`, copy events, and error propagation.
- [ ] Expand graph-reuse documentation with a table of every `llm_graph_input_*::can_reuse()` predicate.
- [ ] Expand the interactive workflow to separate prefill, token decode, CPU-only, GPU offload, multi-backend, and MoE paths.
- [ ] Add direct source and documentation links to every interactive node.
- [ ] Add an index page for detailed research logs.
- [ ] Add commit-pinned link checking.
- [ ] Add backend-specific runtime validation and profiler evidence.

### Completed setup

- [x] Complete the pinned Vulkan transfer-path trace: memory-property selection, blocking set/get, same-device and cross-device blocking copies, backend async set/get fallbacks, scheduler async-copy acceptance, fence completion, and registered-host behavior.
- [x] Add exact Vulkan source/destination rows to `docs/lifecycle/buffer-compatibility.md`.
- [x] Document the pinned Vulkan capability boundary: non-host-visible default buffers, dedicated host-buffer support, async/events flags, queue/event state, backend synchronization, and graph hazard tracking.
- [x] Replace the broken backend-scheduler Mermaid sequence with a static accessible SVG and explanatory caption.
- [x] Document concrete CPU and CPU_Mapped host visibility, ownership, `memcpy()` set/get, and direct-copy behavior.
- [x] Document CUDA-device blocking set/get/direct-copy behavior, same-device/peer branches, and completion semantics.
- [x] Build a representative CPU/mmap/CUDA/Metal source-buffer × destination-buffer compatibility matrix.
- [x] Add a runtime-validation schema for page faults, synchronization bubbles, overlap, direct-copy acceptance, heap staging, and RSS deltas.
- [x] Trace the generic scheduler fallback after `cpy_tensor_async` is absent or returns `false`: synchronize source and destination, invoke blocking tensor copy, and establish completion.
- [x] Document the blocking copy decision tree: host-source pointer, host-destination pointer, destination-buffer direct copy, then full-tensor `malloc → get → set → free` staging.
- [x] Document CPU/mmap-to-CUDA, CUDA-host-to-CUDA, and CPU/mmap-to-Metal fallback paths, including page-fault, synchronization, ownership, and host-visibility caveats.
- [x] Trace the pinned Metal graph-submission path, command-buffer lifecycle, asynchronous blit set/get/copy operations, event signal/wait ordering, and explicit host synchronization boundary.
- [x] Build a CUDA-versus-Metal capability table, including discrete-memory and unified-memory caveats.
- [x] Document that Metal shared/unified memory changes addressability and transfer cost but does not imply command completion, safe reuse, or host visibility.
- [x] Trace `ggml_backend_cuda_cpy_tensor_async()` branch by branch, including CUDA backend/buffer eligibility, device consistency, same-backend D2D, same-device cross-backend D2D, peer copies, event ordering, and every false-return fallback.
- [x] Document that CPU/mmap and CUDA host buffers are outside the pinned CUDA device-copy callback, and that successful return means queued dependency rather than host-visible completion.
- [x] Compare pinned CPU and CUDA graph submission, thread/stream completion, event semantics, synchronization, and synchronous buffer-operation behavior.
- [x] Build a true-async versus fallback table for CPU, CUDA, and scheduler-level APIs.
- [x] Trace `ggml_backend_sched_graph_compute_async` through backend assignment, graph splitting, destination copies, copy-slot events, backend split submission, and synchronization.
- [x] Document CPU-only versus multi-backend scheduler behavior, copy ownership, immediate user-input capture, fallback synchronization, and the pinned MoE partial-copy path.
- [x] Trace `llama_decode → llama_context::decode → process_ubatch → graph_compute → ggml_backend_sched_graph_compute_async` at the pinned revision.
- [x] Document graph-reuse compatibility, scheduler reservation versus allocation, thread selection, and the pipeline-parallel input synchronization boundary.
- [x] Repair Pages handling so disabled Pages does not fail a valid MkDocs build.
- [x] Add independent strict Documentation CI and a post-deployment website health check.
- [x] Publish and validate the interactive workflow HTML asset.
- [x] Create the public repository and initial MkDocs site.
- [x] Add README-first scheduled-run context loading.
- [x] Add project state, canonical research log, detailed-log layout, and source ledger.
- [x] Add hourly context validation and daily upstream-index workflows.
<!-- PROJECT-TODOS:END -->

## GitHub Pages enablement

The workflow cannot enable Pages with the standard `GITHUB_TOKEN`. Enable it once in the UI:

1. Open the repository.
2. Open **Settings → Pages**.
3. Under **Build and deployment**, choose **GitHub Actions** as the source.
4. Open **Actions → Deploy documentation → Run workflow**.
5. After success, visit `https://mohammed-alaa40123.github.io/How.to.llama.cpp/`.

The final workflow job checks for HTTP 200 and the expected project title.

## Contribution and license

Implementation claims need pinned source links, truth labels, affected files/functions/backends, diagram updates when relevant, and validation results. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

Original project code and prose are MIT licensed. Upstream llama.cpp remains under its own license and is linked rather than copied in bulk.
