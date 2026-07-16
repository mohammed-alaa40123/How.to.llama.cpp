# Project state

_Last updated: 2026-07-16 12:50 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream OpenCL revision audited: `505b1ed15ca80e2a19f12ff4ac365e40fb374053`
- Current upstream CPU_REPACK suitability revision reviewed: `8ee54c8b32a1b0cf13c03fc5723142bc62c775f6`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Foundations deepening — executable lifetime regressions for optional CPU buffers**

## Completed foundations

- Canonical GGUF, model placement, `llama_model`, `llama_context`, graph/MoE, scheduler, memory-lifetime, backend, and inference-atlas pages.
- Source indexing, strict documentation CI, Pages deployment workflow, health checks, and durable run context.
- Generic scheduler plus CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL teardown audits.
- CPU repack, AMX, KleidiAI, and SpacemiT extra-buffer ownership comparison and destruction-harness specification.
- Complete pinned/current OpenCL event-ownership audit, generated 46-release correction, synchronous tensor-set contract analysis, and upstream proposal staging.
- First executable CPU_REPACK lifetime regression with exact path proof, numerical comparison, and repeated ASan/LSan evidence.
- Upstream-suitability decision and staged two-file CPU_REPACK regression proposal.

## Latest concrete findings

### Verified

- Current upstream commit `8ee54c8b32a1b0cf13c03fc5723142bc62c775f6` still defines `llama_build_and_test()` and groups direct-backend tests under `if (NOT GGML_BACKEND_DL)`.
- Current `ggml/src/ggml-cpu/repack.h` still declares the internal `ggml_backend_cpu_repack_buffer_type()` entry point.
- The passing fixture can be staged as a dedicated `tests/test-cpu-extra-buffer-lifetime.cpp` plus `tests/CMakeLists.txt` registration, guarded from dynamic-backend builds.
- The upstream candidate must retain exact buffer identity, non-null repack traits, operation admission, identical quantized inputs, `1e-7` NMSE, and backend-wrapper-before-buffer teardown.
- The proposal is recorded in `docs/reference/upstream-cpu-repack-lifetime-fixture-proposal.md`.

### Interpretation

- The fixture is suitable for upstream review as a narrow two-file test.
- The project-specific generator, retained-artifact machinery, and twenty-process workflow should remain outside the first upstream patch.
- A cross-platform test may skip when AVX2 is unavailable, but an authoritative sanitizer lane must require AVX2 and successful CPU_REPACK admission so the test cannot silently become permanently skipped.
- A dedicated executable is clearer than folding unusual destruction ordering into broad backend-op correctness tests.

### Historical

- Workflow run `29481384561` established the pinned executable evidence: twenty AVX2-confirmed ASan/LSan processes, stable NMSE `3.82787e-16`, no skips, and no sanitizer diagnostics.
- Prior runs selected the minimal shape, resolved graph/per-tensor allocation, generated the fixture, and preserved the first passing artifact.

### Open questions

- Whether current upstream `8ee54c8` still admits the exact Q4_0 `[32, 8]` case at runtime rather than merely retaining compatible APIs.
- Which upstream CI lane can guarantee AVX2 and sanitizer execution.
- Whether maintainers prefer `tensor->extra` or another observable for path proof.
- Whether repeated in-process execution belongs in the first upstream patch or a follow-up.

## Immediate next task

```text
generate the staged two-file fixture against current upstream 8ee54c8
  → compile with ASan/LSan
  → require AVX2 and real CPU_REPACK admission
  → confirm numerical and teardown behavior
  → update proposal with current-tree evidence
  → open or manually stage the upstream pull request
```

## In progress

- Manual/upstream submission of the reviewed 46-release OpenCL ownership correction; GitHub App write access to upstream is blocked.
- Current-tree regeneration and sanitizer validation of the CPU_REPACK lifetime candidate.
- Source-index regeneration with pinned line-aware symbol inventory.
- Hardware-specific lifetime extensions for KleidiAI, AMX, SpacemiT, and ARM repack.
- Runtime overlays for mmap/page faults, scheduler copies, events, KV/recurrent growth, and backend queues.

## Publication and validation state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`.
- CPU_REPACK sanitizer workflow run `29481384561`: passed.
- Job `87565708592`: passed all setup, compile, twenty-process execution, and evidence-upload steps.
- Artifact `8368782428`: retained with digest `sha256:ef4f0a36e27f7811b106e0a870c278724f1e620aed991807b7f2c3e443d1efaf`.
- Added `docs/reference/upstream-cpu-repack-lifetime-fixture-proposal.md` and detailed note `logs/research/2026-07-16/1250-cpu-repack-upstream-suitability.md`.
- Research ledger unchanged: this increment used the already-recorded official llama.cpp primary source.
- PR #1 was open and mergeable before these context updates.
- Final-head workflow results must be checked after all context commits.

## Known blockers and caveats

- **Current-tree runtime evidence:** source/API compatibility at `8ee54c8` is verified, but the fixture has not yet been compiled and executed against that exact current revision.
- **Evidence retention:** artifact `8368782428` expires on 2026-08-15; durable textual findings and digest are recorded, but long-term binary retention may require downloading or regenerating it.
- **Hardware scope:** the passing evidence is AVX2-specific and does not cover ARM, KleidiAI, AMX, or SpacemiT.
- **Path proof:** correct numerical output alone remains insufficient; future fixtures must preserve exact buffer identity, traits, and operation-admission checks.
- **Upstream permission:** direct issue/PR creation in `ggml-org/llama.cpp` is blocked for the connected GitHub App.
- **Pages verification:** branch-added content cannot deploy until PR #1 merges; independent live response verification is still required.
- Mapping, allocation, residency, representation validity, command completion, event ownership, reset, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map and source-pinned end-to-end workflow.
- Deep GGUF/model-loading, model/context, graph, scheduler, memory, and teardown documentation.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays and executable lifetime regressions where source reasoning alone is insufficient.