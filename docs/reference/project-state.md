# Project state

_Last updated: 2026-07-18 05:00 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream OpenCL revision audited: `505b1ed15ca80e2a19f12ff4ac365e40fb374053`
- Current upstream CPU_REPACK suitability revision reviewed: `8ee54c8b32a1b0cf13c03fc5723142bc62c775f6`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Executable-learning Week 1 foundation — contracts, legal fixtures, schemas, and smallest vertical slice**

## Completed foundations

- Canonical GGUF, model placement, `llama_model`, `llama_context`, graph/MoE, scheduler, memory-lifetime, backend, and inference-atlas pages.
- Source indexing, strict documentation CI, Pages deployment workflow, health checks, and durable run context.
- Generic scheduler plus CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL teardown audits.
- First executable CPU_REPACK lifetime regression with exact path proof, numerical comparison, and repeated ASan/LSan evidence.
- Website UX review, task-oriented Architecture navigation, and generated-HTML accessibility validation.
- EAAI July 17-31 executable-learning plan and legal fixture decision.
- Deterministic synthetic GGUF package and bounded corruption variants.
- Lab 0 six-phase checker contract and semantic validator.
- Executable-trace, learner-progress, and media-manifest schemas and validators.
- Authoritative EAAI orchestration state, evidence backlog, roadmap, and readiness scorecard.
- Strict MkDocs integration, deterministic GGUF figure, immutable trace source anchors, and keyboard-operable trace viewer with passing commit-scoped CI.
- Browser-first GGUF Anatomy vertical slice with deterministic Python/browser agreement and passing Documentation CI run `29562479577`.

## Latest concrete findings

### Verified

- Ubuntu Lab 0 workflow run `29622240261` completed successfully on the PR head `712016f1522fd6f4f1184f9c37b76e3956b70c6a`.
- Documentation CI run `29622240365` also completed successfully for the same head.
- Artifact `8422651113`, `lab0-ubuntu-24.04-d895eddc1c5e69452d90571c4ccb5d80f410da07`, was retained with digest `sha256:2db76be20de63afb5ab080fbdca8354de60859d34d4f21970c5331f9f2871295` and expires on 2026-08-17.
- The retained report identifies Ubuntu 24.04/x86_64, Python 3.12.3, uv 0.8.0, CMake 3.31.6, Ninja 1.13.2, and GCC 13.3.0.
- The exact required `uv sync --locked` command passed with lock checksum `b332308fd26688b552acd6546a91ea95a3acd9e9d6457a1d3be97c59621f9ba3`.
- The runner detached llama.cpp at `e3546c7948e3af463d0b401e6421d5a4c2faf565`, configured with Ninja and `GGML_NATIVE=OFF`, built only `llama-cli` with two jobs, and launched `llama-cli --help`.
- The report recorded `setup_success=true`, `build_success=true`, `launch_success=true`, no diagnostics, no model, and `inference_state=not_attempted`.
- Monotonic model-free time to ready was 326,905 ms.
- The report recorded no model redistribution, secrets, personal paths, or learner data.
- A Codespaces-compatible Ubuntu 24.04 devcontainer definition and dedicated `LAB0-04` retained-evidence workflow now reuse the same parameterized Lab 0 runner and validator as the Ubuntu row.

### Interpretation

- The retained run provides bounded positive evidence for one clean Ubuntu local-native setup/build/launch row.
- The earlier failed report and the successful rerun demonstrate that retaining failed artifacts before semantic rejection improves reproducibility debugging.
- Reusing one runner and semantic validator reduces measurement drift between the local-native and cloud-container rows.
- The devcontainer implementation alone is not evidence that the container row succeeds; commit-scoped execution remains required.

### Historical

- The first retained Ubuntu run localized `UV_LOCK_DRIFT` before clone/configure/build/launch.
- A minimal dependency-free project entry in `uv.lock` corrected the locked-sync contract without weakening `uv sync --locked` or adding external Python dependencies.

### Open questions

- Whether the repository devcontainer completes the same bounded path and retains a semantically valid report in CI.
- Real macOS and WSL2 runs remain required before any cross-platform claim.
- Offline/degraded-mode behavior and cached rebuild behavior remain untested.
- Independent technical review and an approved educational evaluation pathway remain required.

## Immediate next task

```text
return to STACK-01 when the human canonical-progress decision exists
  → otherwise inspect the LAB0-04 devcontainer workflow and retained report
  → preserve the exact JSON artifact before semantic validation
  → make at most one phase-specific repair if it fails
  → do not claim inference, Codespaces service reliability or cross-platform reproducibility
```

## In progress

- Draft PR stack for the EAAI executable-learning foundation.
- `LAB0-04` measured devcontainer run and artifact validation.
- `DATA-01` retrospective agent-workflow extraction contract.
- `PROGRESS-02` progress export/import, migration, and corruption recovery.
- Current-tree CPU_REPACK regeneration and sanitizer validation.
- Website browser-level accessibility and deployed verification.

## Publication and validation state

- `docs/publication/orchestrator-state.md` and `docs/publication/evidence-backlog.md` remain authoritative.
- `CI-01`, `MEDIA-01`, `FIG-01`, `TRACE-02`, `VIEW-01`, and `LAB1-01` have passing commit-scoped CI evidence.
- `LAB0-03` has one retained, semantically valid, successful Ubuntu 24.04 model-free setup/build/launch record.
- `LAB0-04` now has an implementation and workflow, but no successful retained container report yet.
- No participant data, model, telemetry, credential, paid API call, generated media output, native instrumentation, inference, or manuscript prose was introduced.

## Known blockers and caveats

- **Canonical integration:** `STACK-01` still requires a human choice of progress implementation and merge order.
- **Execution-tier coverage:** the successful Ubuntu row does not cover devcontainer until `LAB0-04` passes, nor macOS, WSL2, browser execution, offline use, model loading, or inference.
- **Container reproducibility:** the Development Container base image tag and initial package acquisition still depend on external registries; the exact built image digest must be retained by CI or a later evidence increment before making a stronger image-reproducibility claim.
- **Lab 0 target:** the `llama-cli` command shape still requires independent technical review.
- **Educational effectiveness:** no learner-benefit claim is permitted before an approved evaluation pathway and baseline comparison.
- **Progress integration:** canonical progress implementation remains unresolved across overlapping branches.
- **Native acceptance:** the synthetic file is a format-teaching fixture and is not claimed to be a valid inference model.
- **Live-site verification:** Pages should be rechecked only after stacked changes merge to `main` and deploy.
- **Evidence retention:** artifact `8368782428` expires on 2026-08-15; successful Lab 0 artifact `8422651113` expires on 2026-08-17.
- **Upstream permission:** direct issue/PR creation in `ggml-org/llama.cpp` is blocked for the connected GitHub App.

## Definition of done for the executable-learning foundation phase

- Complete learning contracts and dependency-ordered July 17-31 plan.
- Legal fixture policy with no ambiguous model redistribution.
- Deterministic synthetic GGUF generator, manifest, golden output, and validators.
- Machine-readable trace, media-manifest, progress, Lab 0 phase, and reproducibility schemas.
- Authored sample trace with explicit evidence kinds and a narrow viewer shell.
- Lab 0 checker interface, model-free environment/build report, diagnostics, and timing contract.
- One deterministic technical figure from structured input.
- Accessibility fallbacks, reproducibility evidence, and CI gates for every introduced artifact.
