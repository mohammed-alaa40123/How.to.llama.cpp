# Project state

_Last updated: 2026-07-16 05:51 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream OpenCL revision audited: `505b1ed15ca80e2a19f12ff4ac365e40fb374053`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Foundations deepening — source-backed lifetime regressions for optional CPU buffers**

## Completed foundations

- Canonical GGUF, model placement, `llama_model`, `llama_context`, graph/MoE, scheduler, memory-lifetime, backend, and inference-atlas pages.
- Source indexing, strict documentation CI, Pages deployment workflow, health checks, and durable run context.
- Generic scheduler plus CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL teardown audits.
- CPU repack, AMX, KleidiAI, and SpacemiT extra-buffer ownership comparison and destruction-harness specification.
- Complete pinned/current OpenCL event-ownership audit, generated 46-release correction, synchronous tensor-set contract analysis, and upstream proposal staging.

## Latest concrete findings

### Verified

- Pinned `ggml/src/ggml-cpu/CMakeLists.txt` always includes `ggml-cpu/repack.cpp` in the ordinary CPU backend target; there is no separate pinned `GGML_CPU_REPACK` build option.
- Pinned Q4_0 repack selection uses `q4_0_8x8_q8_0` when AVX2 is available and the weight row count `ne[1]` is divisible by eight.
- The smallest admitted x86 case is Q4_0 weight `[32, 8]` multiplied by F32 activation `[32, 1]`, producing F32 `[8, 1]`.
- Extra-buffer admission additionally requires a two-dimensional weight allocated from the exact `ggml_backend_cpu_repack_buffer_type()`, a non-null selected trait, host-addressable activation storage, and F32 activation type.
- The repack allocator delegates storage to ordinary CPU allocation, then replaces buffer identity and tensor init/set callbacks. Tensor initialization stores static repack traits in `tensor->extra`; upload performs the interleaved repack.

### Interpretation

- `Q4_0 [32, 8] × F32 [32, 1]` is the smallest bounded fixture that exercises repack initialization, upload, optional dispatch, synchronous compute, correctness comparison, and backend-wrapper-before-buffer teardown on common x86 AVX2 hardware.
- Buffer-type pointer identity and non-null traits are stronger path evidence than matching the diagnostic name `CPU_REPACK`.
- A non-AVX2 skip is not lifetime evidence; CI needs at least one runner whose logs confirm AVX2 and successful repack admission.

### Historical

- The previous run identified `tests/test-cpu-extra-buffer-lifetime.cpp` as the correct dedicated integration point and recommended reusing backend-op quantization, upload, graph, readback, and comparison helpers.
- The exact type and minimum dimensions were previously open; this run resolves them for the first x86 fixture.

### Open questions

- Whether GitHub-hosted Ubuntu formally guarantees AVX2 or only exposes it on current hosts.
- Whether to extract shared test helpers or duplicate a bounded subset for the first patch.
- Which existing Q4_0 comparison tolerance should be reused verbatim.
- Whether to add an ARM NEON+dotprod case immediately after x86.

## Immediate next task

```text
Implement tests/test-cpu-extra-buffer-lifetime.cpp
  → Q4_0 weight [32, 8]
  → F32 activation [32, 1]
  → assert AVX2, exact CPU_REPACK pointer identity, non-null traits, and supports_op
  → compare output against ordinary CPU
  → free tested CPU backend wrapper before retained repack buffer
  → repeat under ASan/LSan
  → add CMake target and AVX2-confirmed CI invocation
```

## In progress

- First CPU repack lifetime fixture implementation and sanitizer CI.
- Manual/upstream submission of the reviewed 46-release OpenCL ownership correction; GitHub App write access to upstream is blocked.
- Source-index regeneration with pinned line-aware symbol inventory.
- Hardware-specific lifetime extensions for KleidiAI, AMX, and SpacemiT.
- Runtime overlays for mmap/page faults, scheduler copies, events, KV/recurrent growth, and backend queues.

## Publication and validation state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`.
- Added detailed note `logs/research/2026-07-16/0551-cpu-repack-minimal-admitted-case.md`.
- Updated README living TODOs, this project checkpoint, and the concise research log.
- Research ledger unchanged: this increment used the already-recorded pinned llama.cpp primary source.
- Local compilation remains unavailable because a patch-capable upstream checkout is not mounted; GitHub-hosted CI is authoritative once source implementation lands.
- Final-head workflow results must be checked after all context commits.

## Known blockers and caveats

- **Hardware gate:** successful skip on a non-AVX2 runner does not validate repack lifetime ordering.
- **Path proof:** correct numerical output alone is insufficient because ordinary CPU fallback can produce the same answer.
- **Sanitizer scope:** process-static dispatch metadata should be documented separately, not hidden with broad leak suppression.
- **Upstream permission:** direct issue/PR creation in `ggml-org/llama.cpp` is blocked for the connected GitHub App.
- **Pages verification:** branch-added content cannot deploy until PR #1 merges; independent live response verification is still required.
- Mapping, allocation, residency, representation validity, command completion, event ownership, reset, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map and source-pinned end-to-end workflow.
- Deep GGUF/model-loading, model/context, graph, scheduler, memory, and teardown documentation.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays and executable lifetime regressions where source reasoning alone is insufficient.
