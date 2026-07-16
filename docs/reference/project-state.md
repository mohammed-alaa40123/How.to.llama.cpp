# Project state

_Last updated: 2026-07-16 11:58 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream OpenCL revision audited: `505b1ed15ca80e2a19f12ff4ac365e40fb374053`
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

## Latest concrete findings

### Verified

- Workflow run `29481384561` completed successfully on an Ubuntu 24.04 hosted runner with AVX2.
- The exact pinned llama.cpp revision was fetched, verified, compiled, and executed under AddressSanitizer and LeakSanitizer.
- All twenty separate fixture processes executed the `q4_0_8x8` CPU_REPACK path and printed `PASS: CPU_REPACK path executed; NMSE=3.82787e-16`.
- No run skipped, returned non-zero, or emitted an ASan/LSan diagnostic.
- The tested case was Q4_0 `[32, 8]` × F32 `[32, 1]` → F32 `[8, 1]`.
- The fixture proved exact repack-buffer identity, non-null traits, operation admission, synchronous compute, numerical agreement, and backend-wrapper-before-buffer teardown.
- Retained artifact `8368782428`, named `cpu-repack-lifetime-sanitizer-e3546c7`, has digest `sha256:ef4f0a36e27f7811b106e0a870c278724f1e620aed991807b7f2c3e443d1efaf` and expires on 2026-08-15.
- The canonical destruction-harness page now records the executable result and bounded ownership conclusion.

### Interpretation

- This is executable evidence that the admitted pinned CPU_REPACK buffer does not depend on the ordinary CPU backend-wrapper lifetime for the tested synchronous `MUL_MAT` destruction order.
- The stable NMSE `3.82787e-16` is far below the `1e-7` threshold and confirms that the optional path agreed numerically with ordinary CPU for identical quantized input bytes.
- The evidence is bounded to one admitted AVX2 shape and twenty process-level executions; it does not establish all layouts, concurrent use, or other optional CPU implementations.

### Historical

- Prior runs selected the minimal admitted shape, resolved graph and per-tensor allocation topology, generated the complete fixture, and added exact-revision sanitizer CI.
- Run `29481384561` closes that sequence with the first passing runtime artifact.

### Open questions

- Whether to propose the generated CPU_REPACK fixture upstream as a permanent regression target.
- Which hardware-gated extension should be next: ARM NEON+dotprod repack or KleidiAI.
- Whether to add repeated iterations inside one process in addition to the current twenty-process teardown coverage.
- Whether current upstream still admits the same minimal CPU_REPACK case without API adjustments.

## Immediate next task

```text
review upstream suitability of the passing CPU_REPACK fixture
  → compare the generated target with current upstream test conventions
  → decide whether to stage a permanent upstream regression patch
  → preserve exact path-proof and sanitizer requirements
  → begin one admitted ARM or KleidiAI lifetime extension
```

## In progress

- Manual/upstream submission of the reviewed 46-release OpenCL ownership correction; GitHub App write access to upstream is blocked.
- Source-index regeneration with pinned line-aware symbol inventory.
- Hardware-specific lifetime extensions for KleidiAI, AMX, SpacemiT, and ARM repack.
- Runtime overlays for mmap/page faults, scheduler copies, events, KV/recurrent growth, and backend queues.

## Publication and validation state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`.
- CPU_REPACK sanitizer workflow run `29481384561`: passed.
- Job `87565708592`: passed all setup, compile, twenty-process execution, and evidence-upload steps.
- Artifact `8368782428`: retained with the recorded SHA-256 digest.
- Added detailed note `logs/research/2026-07-16/1158-cpu-repack-first-passing-sanitizer-evidence.md`.
- Updated the CPU destruction-harness page, README living TODOs, this project checkpoint, and the concise research log.
- Research ledger unchanged: this increment used generated project evidence and the already-recorded pinned llama.cpp primary source.
- PR #1 was open and mergeable before the final context updates.
- Final-head workflow results must be checked after all context commits.

## Known blockers and caveats

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
