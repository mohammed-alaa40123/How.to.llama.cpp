# Research log

## 2026-07-12 — Milestone 0/1 start

**Pinned baseline**

- Commit: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Reason: first connector-verified revision used to ground the initial call trace.
- Caution: upstream evolves rapidly; this is a documentation baseline, not a claim that all pages describe the newest commit indefinitely.

**Verified findings**

- The minimal example loads dynamic backends before loading a model.
- It loads the model, tokenizes the prompt, constructs `llama_context`, repeatedly calls decode, samples a token, and feeds a one-token batch back into the loop.
- The model-loading path constructs a loader and architecture-specific model object, selects devices, then loads hyperparameters, vocabulary, statistics, and tensors.
- A source comment explicitly accounts for mmap-deferred page faults in load-time measurement.
- Backend tensor async APIs can fall back to synchronization and synchronous data movement when the backend interface does not implement the async method.

**Interpretations to validate**

- Treat `llama_context` as the active inference runtime boundary, but document its exact ownership graph before presenting this as a formal invariant.
- Treat graph construction, allocation, backend placement, copies, and execution as separate conceptual phases even when some code paths fuse their orchestration.

**Open questions**

- Exact graph reuse compatibility checks at the pinned revision.
- Prompt versus token-generation scheduler reservation strategy.
- Complete memory-module selection by architecture.
- Scheduler copy/event ordering for every backend combination.
- CPU thread-pool work partitioning for major operations and `MUL_MAT_ID`.
- Branches/PRs that materially changed these paths.

**Artifacts created**

- MkDocs project scaffold.
- End-to-end Mermaid diagram.
- Interactive SVG inference explorer prototype.
- Upstream mirror and source-index scripts.
- Pages and refresh workflows.

## 2026-07-12 — Repository publication and durable scheduling context

**Scope**

- Documentation repository: `mohammed-alaa40123/How.to.llama.cpp`
- Process and automation infrastructure rather than upstream runtime behavior.

**Verified changes**

- The root README is now the canonical scheduled-run operating manual.
- Every scheduled workflow invokes `scripts/start_scheduled_run.sh`, which reads the complete README, project state, research log, ledger, and latest detailed research note before work begins.
- `scripts/validate_project_context.py` checks that the durable context contract remains intact.
- GitHub Actions now includes an hourly context check, a daily source-index refresh, and strict MkDocs Pages deployment.

**Interpretation**

- Keeping a small project-state checkpoint plus a concise canonical research log should reduce context loss more effectively than placing every raw note in one growing README.

**Open questions**

- Whether the hourly research executor should eventually create one PR per increment or batch related increments into milestone PRs.
- Whether detailed research logs need a generated index page once their count grows.

**Artifacts changed**

- `README.md`
- `docs/reference/project-state.md`
- `logs/README.md`
- `scripts/start_scheduled_run.sh`
- `scripts/validate_project_context.py`
- `.github/workflows/hourly-context-check.yml`
- `.github/workflows/refresh-source-index.yml`
- `.github/workflows/pages.yml`

**Next step**

- Trace `llama_decode` through context graph construction/reuse and backend scheduler execution at the pinned revision.

## 2026-07-12 01:54 Africa/Cairo — CI and Pages repair

**Scope**

- Repository automation and deployment health for `mohammed-alaa40123/How.to.llama.cpp`.

**Verified findings**

- The documentation corpus builds locally with `mkdocs build --strict`.
- The published repository was missing `docs/assets/interactive/inference-flow.html`, even though the documentation and README referenced it.
- The Pages workflow previously called `actions/configure-pages` unconditionally. The action documents that enabling Pages requires a token stronger than the standard `GITHUB_TOKEN`; therefore a repository with Pages disabled can fail after a successful MkDocs build.
- The repaired workflow separates strict documentation CI from deployment, detects whether Pages is enabled, skips deployment cleanly when it is not, and performs an HTTP/title health check after a successful deployment.

**Interpretation**

- The reported failure was deployment-configuration related rather than a reproducible MkDocs content failure. Independent CI makes that distinction visible.

**Open questions**

- Confirm the new Documentation CI and Deploy documentation runs finish successfully on GitHub.
- Enable Pages in repository settings and confirm the live site returns HTTP 200 with the expected title.

**Artifacts changed**

- `.github/workflows/docs-ci.yml`
- `.github/workflows/pages.yml`
- `scripts/check_site.sh`
- `scripts/validate_project_context.py`
- `docs/assets/interactive/inference-flow.html`
- `README.md`
- `docs/reference/project-state.md`

**Next step**

- Enable GitHub Pages, rerun deployment, verify the website, then continue the pinned `llama_decode` scheduler trace.

## 2026-07-12 02:51 Africa/Cairo — Decode and graph-reuse trace

**Scope**

- Pinned path from the public decode API through graph compatibility, rebuild/allocation, and scheduler submission.

**Verified findings**

- `llama_decode()` delegates directly to `llama_context::decode()`.
- `decode()` initializes the batch allocator, reserves scheduler capacity, applies pending memory work, initializes the active memory batch context, and processes one `llama_ubatch` at a time.
- `process_ubatch()` reuses the previous graph only when graph reuse is enabled and all graph-result/input compatibility checks accept the new graph parameters.
- Pipeline-parallel graph reuse synchronizes before rewriting inputs because a previous asynchronous GPU execution may still read those tensors.
- The rebuild branch resets graph and scheduler state, calls `model.build_graph()`, and allocates the concrete graph with `ggml_backend_sched_alloc_graph()`.
- `graph_compute()` selects the batch or single-token CPU threadpool and submits through `ggml_backend_sched_graph_compute_async()`.
- Scheduler reserve and per-graph allocation are distinct: reserve plans buffer capacity; allocation binds a rebuilt graph into that capacity.

**Interpretation**

- Graph reuse is a topology-and-shape cache, not a token-value or output cache. Compatible graph structure and allocations survive while input tensors are rewritten for each micro-batch.

**Open question**

- Trace scheduler splitting, inter-backend copies/events, split submission, and synchronization after `ggml_backend_sched_graph_compute_async()`.

**Artifacts changed**

- `docs/lifecycle/decode-graph-reuse.md`
- `mkdocs.yml`
- `docs/reference/project-state.md`
- `README.md`
- `logs/research/2026-07-12/0251-decode-graph-reuse.md`

**Next step**

- Document the scheduler split/copy/event execution path at the same pinned revision.
