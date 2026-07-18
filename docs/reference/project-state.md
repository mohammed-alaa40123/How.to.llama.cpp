# Project state

_Last updated: 2026-07-18 06:01 Africa/Cairo_

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
- Successful model-free Lab 0 setup/build/launch measurements for Ubuntu 24.04 local-native and Ubuntu 24.04 devcontainer tiers.

## Latest concrete findings

### Verified

- Ubuntu Lab 0 workflow run `29622240261` completed successfully and retained artifact `8422651113` with digest `sha256:2db76be20de63afb5ab080fbdca8354de60859d34d4f21970c5331f9f2871295`.
- Devcontainer Lab 0 workflow run `29626470197` completed successfully on head `ab1db83938176dc4fd766cf66fccf18e5b0e2116`.
- Devcontainer artifact `8424069914`, `lab0-devcontainer-ubuntu-24.04-6b5c02d78b36c6283fa40c3c4ccdbdd5c051ea55`, was retained with digest `sha256:2aaf62980561e141244b5552f4cd397cb7c9a4e1215b75c35a04fdc3ad7c3121` and expires on 2026-08-17.
- The container report identifies Ubuntu 24.04/x86_64, Python 3.12.3, uv 0.8.0, CMake 3.28.3, Ninja 1.11.1, and GCC 13.3.0.
- The exact required `uv sync --locked` command passed with lock checksum `b332308fd26688b552acd6546a91ea95a3acd9e9d6457a1d3be97c59621f9ba3`.
- The runner detached llama.cpp at `e3546c7948e3af463d0b401e6421d5a4c2faf565`, configured with Ninja and `GGML_NATIVE=OFF`, built only `llama-cli` with two jobs, and launched `llama-cli --help`.
- The container report recorded `setup_success=true`, `build_success=true`, `launch_success=true`, no diagnostics, no model, and `inference_state=not_attempted`.
- Container monotonic model-free time to ready was 280,753 ms; the earlier Ubuntu local-native row was 326,905 ms. These are environment observations, not a performance comparison.
- Documentation CI `29626470196` and the unchanged Ubuntu regression lane `29626470190` passed on the same head.
- The reports record no model redistribution, secrets, personal paths, telemetry, or learner data.

### Interpretation

- The retained runs provide bounded positive evidence for one clean Ubuntu local-native row and one clean Ubuntu devcontainer row using the same runner and semantic validator.
- Reusing one runner and validator reduces measurement drift, but the different tool versions and container image acquisition path remain part of the environment description.
- The shorter container time-to-ready must not be interpreted as a speed advantage because caches, runner allocation, image-build timing boundaries, and repeated-run state were not controlled.

### Historical

- The first retained Ubuntu run localized `UV_LOCK_DRIFT` before clone/configure/build/launch.
- A minimal dependency-free project entry in `uv.lock` corrected the locked-sync contract without weakening `uv sync --locked` or adding external Python dependencies.
- The devcontainer lane was introduced only after the local-native row passed and deliberately reused its measurement implementation.

### Open questions

- The Development Container base image tag and package sources are mutable; an exact built-image digest was not retained.
- Real Codespaces service opening, persistence and failure behavior remain untested.
- Real macOS and WSL2 runs remain required before any cross-platform claim.
- Offline/degraded-mode behavior and cached rebuild behavior remain untested.
- Independent technical review and an approved educational evaluation pathway remain required.

## Immediate next task

```text
return to STACK-01 when the human canonical-progress decision exists
  → otherwise begin DATA-01 retrospective extraction or PROGRESS-02 according to the orchestrator
  → do not duplicate Lab 0 environment lanes without a declared matrix need
  → do not claim inference, Codespaces service reliability, image reproducibility or cross-platform equivalence
```

## In progress

- Draft PR stack for the EAAI executable-learning foundation.
- `DATA-01` retrospective agent-workflow extraction contract.
- `PROGRESS-02` progress export/import, migration, and corruption recovery.
- Current-tree CPU_REPACK regeneration and sanitizer validation.
- Website browser-level accessibility and deployed verification.

## Publication and validation state

- `docs/publication/orchestrator-state.md` and `docs/publication/evidence-backlog.md` remain authoritative.
- `CI-01`, `MEDIA-01`, `FIG-01`, `TRACE-02`, `VIEW-01`, and `LAB1-01` have passing commit-scoped CI evidence.
- `LAB0-03` has one retained, semantically valid, successful Ubuntu 24.04 model-free setup/build/launch record.
- `LAB0-04` has one retained, semantically valid, successful Ubuntu 24.04 devcontainer model-free setup/build/launch record.
- No participant data, model, telemetry, credential, paid API call, generated media output, native instrumentation, inference, or manuscript prose was introduced.

## Known blockers and caveats

- **Canonical integration:** `STACK-01` still requires a human choice of progress implementation and merge order.
- **Execution-tier coverage:** the two successful rows do not cover macOS, WSL2, browser execution, offline use, model loading, inference or actual Codespaces service operation.
- **Container reproducibility:** the Development Container base image tag and initial package acquisition depend on external registries; the exact built image digest was not retained.
- **Timing comparison:** local-native and container time-to-ready values are not a controlled benchmark and must not be compared as performance results.
- **Lab 0 target:** the `llama-cli` command shape still requires independent technical review.
- **Educational effectiveness:** no learner-benefit claim is permitted before an approved evaluation pathway and baseline comparison.
- **Progress integration:** canonical progress implementation remains unresolved across overlapping branches.
- **Native acceptance:** the synthetic file is a format-teaching fixture and is not claimed to be a valid inference model.
- **Live-site verification:** Pages should be rechecked only after stacked changes merge to `main` and deploy.
- **Evidence retention:** artifact `8368782428` expires on 2026-08-15; Lab 0 artifacts `8422651113` and `8424069914` expire on 2026-08-17.
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
