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
