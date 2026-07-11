# How.to.llama.cpp

**A source-guided, revision-pinned map of llama.cpp and GGML.**

How.to.llama.cpp explains how a request travels from a GGUF file to generated tokens: backend discovery, model loading, virtual memory, `llama_context`, GGML graph construction, backend scheduling, kernel execution, sampling, and teardown.

> **Initial upstream baseline:** [`e3546c7948e3af463d0b401e6421d5a4c2faf565`](https://github.com/ggml-org/llama.cpp/commit/e3546c7948e3af463d0b401e6421d5a4c2faf565)
>
> The baseline is intentionally pinned for reproducibility. Current upstream branches and commits are indexed separately so historical explanations are not silently mixed with newer behavior.

## Project goals

- Explain llama.cpp from a short end-to-end path down to individual subsystems and call chains.
- Keep every implementation claim tied to a source revision, file, function, PR, discussion, test, or runtime observation.
- Separate verified source behavior from interpretation, historical behavior, and open questions.
- Cover GGML tensors, operations, graphs, allocation, backend interfaces, scheduling, memory, concurrency, and kernels.
- Document CPU, CUDA, Metal, Vulkan, SYCL, OpenCL, RPC, and other backends using one consistent template.
- Build maintainable Mermaid figures and a large interactive inference animation whose nodes open source-level explanations.
- Retain research notes, decisions, unresolved questions, and logs so scheduled runs do not lose context.

## Current milestone

The repository currently contains:

1. a MkDocs Material site scaffold;
2. a verified top-level inference call chain;
3. a repository/source indexing framework;
4. a categorized external research ledger;
5. Mermaid architecture and sequence figures;
6. a clickable inference workflow prototype;
7. GitHub Pages deployment;
8. hourly context validation and scheduled upstream-index refresh workflows.

The next source-analysis priorities are maintained in [`docs/reference/project-state.md`](docs/reference/project-state.md).

---

<!-- SCHEDULED-RUN-INSTRUCTIONS:START -->
## Mandatory startup protocol for every scheduled run

**This section is the canonical startup instruction for automation and research agents. It must be read at the beginning of every run.**

A scheduled run must perform these steps in order:

1. Read this entire `README.md`, not only the scheduling section.
2. Read [`docs/reference/project-state.md`](docs/reference/project-state.md) for the current milestone, source revision, completed work, blockers, and next task.
3. Read the latest entries in [`docs/reference/research-log.md`](docs/reference/research-log.md).
4. Read [`docs/reference/research-ledger.md`](docs/reference/research-ledger.md) before adding a source, so references are not duplicated and their evidence quality is recorded consistently.
5. Inspect the relevant current files before editing them. Do not rely on a previous run's description of repository state.
6. Complete **one bounded, concrete increment** that leaves a reviewable artifact: source notes, a verified call path, a documentation section, a figure, a reference evaluation, a test, or an indexing improvement.
7. Distinguish every new claim as **Verified**, **Interpretation**, **Historical**, or **Open question**.
8. Update the canonical context before ending the run:
   - append the finding and evidence to `docs/reference/research-log.md`;
   - update `docs/reference/project-state.md` with completed work and the next highest-priority task;
   - update `docs/reference/research-ledger.md` when sources were added or re-evaluated;
   - update diagrams and source links when architecture documentation changed.
9. Store detailed per-run notes under `logs/research/YYYY-MM-DD/HHMM-topic.md` when the canonical research log would become too verbose.
10. Run the relevant validation commands and record failures honestly.

The bootstrap script enforces the context-loading portion:

```bash
./scripts/start_scheduled_run.sh <run-name>
```

It reads this README, project state, the canonical research log, and the latest detailed research note into a run-context bundle before work begins.
<!-- SCHEDULED-RUN-INSTRUCTIONS:END -->

## Scheduling plan

| Schedule | Mechanism | Responsibility | Output |
|---|---|---|---|
| Every hour | Research automation using the startup protocol above | Complete one concrete research or implementation increment; update state and logs | Documentation, diagrams, indexed notes, or research entries committed to the repository |
| Every hour at minute 23 UTC | `.github/workflows/hourly-context-check.yml` | Verify that README startup instructions, project state, logs, and scripts remain readable and internally consistent | GitHub Actions log and generated context bundle inside the job |
| Daily at 02:17 UTC | `.github/workflows/refresh-source-index.yml` | Mirror all llama.cpp refs, check out the pinned baseline, regenerate the source inventory, and open/update a PR | `data/generated/` and `docs/reference/generated-source-inventory.md` |
| Every push to `main` | `.github/workflows/pages.yml` | Build MkDocs with strict warnings and deploy the site | GitHub Pages site |
| Manual | All workflows support `workflow_dispatch` | Re-run deployment, context validation, or source indexing on demand | Corresponding Actions run |

The hourly context check does not pretend to replace source research. It verifies that the context needed by the real research run is present and readable. The research automation remains responsible for analysis and documentation changes.

---

## Implementation workflow

### 1. Select and pin the evidence scope

Record the exact llama.cpp revision, branch, PR, or discussion being analyzed. Do not write “current implementation” without a commit or date.

The pinned revision is stored in [`data/upstream.json`](data/upstream.json). The source mirror script honors `LLAMA_CPP_REV` when an alternative revision is intentionally selected.

### 2. Build a source map before writing prose

For a subsystem, record:

- public entry points;
- internal functions and virtual/interface calls;
- owning objects and data structures;
- input/output tensors and state mutations;
- memory allocation and lifetime;
- thread, queue, or backend context;
- synchronization boundaries;
- error, fallback, and configuration paths.

Use `scripts/index_upstream.py` for navigation, but never treat its regex output as a compiler-grade call graph. Macros, templates, function pointers, virtual dispatch, generated code, and backend registration require human verification.

### 3. Write layered documentation

Each major topic should eventually provide:

1. a five-minute explanation;
2. an end-to-end flow;
3. a detailed source call chain;
4. memory and concurrency notes;
5. backend-specific differences;
6. Mermaid or generated figures;
7. relevant PRs, discussions, papers, videos, and runtime evidence;
8. open questions and version caveats.

### 4. Update the interactive workflow

The interactive inference model lives in `docs/assets/interactive/inference-flow.html`. Each node should contain:

- a plain-language description;
- exact files and functions;
- inputs, outputs, and state changes;
- memory owner and lifetime;
- executing thread/backend;
- pinned source links;
- related diagrams and references.

Keep the interactive workflow data-driven so CPU-only, GPU-offload, multi-backend, prompt-processing, token-generation, and MoE paths can be represented without implying one universal runtime path.

### 5. Validate and log

Run the smallest relevant set:

```bash
python3 scripts/validate_project_context.py
python3 -m py_compile scripts/*.py
bash -n scripts/*.sh
mkdocs build --strict
```

`mkdocs build --strict` is also executed in the Pages workflow, so warnings fail deployment rather than silently producing a broken site.

## Repository and context map

| Location | Purpose | Update rule |
|---|---|---|
| `README.md` | Canonical operating manual and scheduled-run startup protocol | Read first on every run; update when process or layout changes |
| `docs/reference/project-state.md` | Current checkpoint: milestone, completed work, blockers, next task | Update at the end of every meaningful research run |
| `docs/reference/research-log.md` | Canonical chronological discoveries, decisions, and unresolved questions | Append concise evidence-backed entries |
| `logs/research/` | Detailed per-run notes and raw reasoning summaries that are too long for the canonical log | Use dated subdirectories and descriptive filenames |
| `docs/reference/research-ledger.md` | External sources and an assessment of what each source contributes | Deduplicate and label source quality/status |
| `docs/roadmap.md` | Full implementation and research plan | Update when scope, ordering, or deliverables change |
| `docs/reference/source-index.md` | Human-maintained guide to important source areas | Update after source-layout discoveries |
| `data/upstream.json` | Pinned upstream repository and revision metadata | Change only intentionally and explain why |
| `data/generated/` | Generated source inventory and ref metadata | Regenerate; do not hand-edit |
| `.upstream/` | Local mirror/worktree of llama.cpp | Generated locally and ignored by Git |
| `docs/assets/interactive/` | Interactive architecture/inference visualizations | Keep nodes linked to source and docs |
| `docs/assets/javascripts/` | Site-side behavior such as Mermaid initialization | Validate in the built site |
| `.github/workflows/` | Pages, hourly context validation, and source-refresh automation | Keep permissions minimal and schedules documented here |
| `scripts/` | Context bootstrap, validation, upstream mirroring, and indexing | Scripts must fail loudly and be safe to run repeatedly |
| GitHub Actions run logs | Build/deployment and scheduled-job output | Use for CI diagnostics; summarize durable findings in repository logs |
| `logs/runtime/` | Optional local profiler, benchmark, page-fault, memory, or backend traces | Ignored by default; commit only small curated evidence |

## Log format

Canonical research-log entries should contain:

```markdown
## YYYY-MM-DD HH:MM — Topic

**Scope**
- Revision, branch, PR, files, or experiment.

**Verified findings**
- Finding with pinned evidence.

**Interpretation**
- What the verified facts imply, explicitly labeled.

**Open questions**
- Remaining source or runtime checks.

**Artifacts changed**
- Documentation, diagrams, scripts, or data.

**Next step**
- One bounded task for the next run.
```

Detailed run notes use `logs/research/YYYY-MM-DD/HHMM-topic.md`. Large binaries, complete model files, full source mirrors, and unfiltered profiler captures should not be committed.

## Truth labels

- **Verified source behavior** — directly visible in the pinned source, official documentation, test, or reproducible runtime trace.
- **Interpretation** — a reasoned explanation connecting verified facts; useful but not an API guarantee.
- **Historical behavior** — tied to an older commit, branch, PR, or reverted design.
- **Open question** — needs additional source inspection, experimentation, or maintainer confirmation.

## Local preview

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Open the local URL printed by MkDocs. The direct interactive prototype is also available at `docs/assets/interactive/inference-flow.html`.

## Upstream source mirror and index

```bash
./scripts/update_upstream.sh
```

The script:

1. mirrors all refs from `ggml-org/llama.cpp`;
2. checks out the pinned revision in a temporary worktree;
3. exports branch/tag/ref metadata;
4. generates a machine-readable file/include/symbol inventory;
5. writes a human-readable inventory page.

Generated relationships are navigation hints and must be verified in source before being presented as runtime truth.

## GitHub Pages

The repository contains an Actions-based Pages deployment in `.github/workflows/pages.yml`.

After the repository files are pushed:

1. Open the repository on GitHub.
2. Open **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.
4. Open **Actions → Deploy documentation** and run the workflow manually, or push another commit to `main`.
5. After deployment succeeds, the site should be available at:
   `https://mohammed-alaa40123.github.io/How.to.llama.cpp/`

A failed strict MkDocs build prevents deployment. Inspect the failed job under the repository's **Actions** tab and fix the warning or error rather than disabling strict mode.

## Contribution model

Contributions should include:

- a pinned source link for implementation claims;
- a truth label;
- affected files, functions, objects, and backends;
- a diagram update when architecture changes;
- a research-log entry for major discoveries;
- the relevant validation results.

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

MIT for original project code and prose. Upstream llama.cpp content remains under its own license and is linked rather than copied in bulk.
