# Project state

_Last updated: 2026-07-16 07:52 Africa/Cairo_

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

- The pinned backend-op harness creates `no_alloc = true` contexts, builds graph metadata, checks operation support, allocates storage, expands the graph, uploads inputs, and compares outputs.
- The base backend-op comparison uses normalized mean squared error with threshold `1e-7`.
- For this fixture, both reference and tested paths consume the exact same already-quantized Q4_0 bytes, so quantization error is common to both sides; no looser Q4_0-specific threshold is needed.
- A single ordinary `ggml_backend_alloc_ctx_tensors()` allocation cannot place only the tested weight in CPU_REPACK while leaving activation/output in ordinary CPU storage. The fixture needs explicit per-tensor allocation or separate weight-only and compute contexts.
- The safest topology is two independent no-allocation graphs: ordinary Q4_0/F32 reference storage and exact CPU_REPACK weight plus ordinary F32 activation/output storage for the tested graph.

### Interpretation

- Avoid `ggml_backend_compare_graph_backend()` for this regression because ordinary Q4_0 and CPU_REPACK store different physical weight representations.
- Quantize one deterministic F32 source once, upload the same Q4_0 byte vector to both weights, and compare final F32 outputs with NMSE `<= 1e-7`.
- Compare before unusual teardown, then free the tested CPU backend wrapper, destroy tested graph/context metadata, and free the retained repack buffer last under ASan/LSan.

### Historical

- Prior runs selected the dedicated executable, minimal Q4_0 `[32, 8]` × F32 `[32, 1]` AVX2 case, and deterministic patch generator.
- This run resolves the generator's graph/allocation design and numerical tolerance questions.

### Open questions

- Confirm the exact pinned signature and suitability of `ggml_backend_tensor_alloc()`; otherwise allocate a separate weight-only context with a buffer-type-specific context allocator.
- Whether GitHub-hosted Ubuntu exposes AVX2 consistently enough for authoritative sanitizer coverage.

## Immediate next task

```text
Confirm exact pinned per-tensor allocation API
  → update generator with two no-alloc graphs
  → allocate tested Q4_0 weight from exact CPU_REPACK buffer
  → allocate activation/output from ordinary CPU storage
  → quantize deterministic F32 weight once and upload identical Q4_0 bytes
  → upload identical deterministic F32 activation
  → prove buffer identity, non-null traits, and supports_op
  → execute both graphs and compare NMSE <= 1e-7
  → free tested backend wrapper before retained repack buffer
  → repeat under ASan/LSan on AVX2-confirmed CI
```

## In progress

- First CPU repack lifetime fixture implementation and sanitizer CI.
- Manual/upstream submission of the reviewed 46-release OpenCL ownership correction; GitHub App write access to upstream is blocked.
- Source-index regeneration with pinned line-aware symbol inventory.
- Hardware-specific lifetime extensions for KleidiAI, AMX, and SpacemiT.
- Runtime overlays for mmap/page faults, scheduler copies, events, KV/recurrent growth, and backend queues.

## Publication and validation state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`.
- Added detailed note `logs/research/2026-07-16/0752-cpu-repack-graph-allocation-contract.md`.
- Updated README living TODOs, this project checkpoint, and the concise research log.
- Research ledger unchanged: this increment used the already-recorded pinned llama.cpp primary source.
- Previous branch head `5ddbdc5b530eb0a6e2e22b962bd0d1df47d20978` passed Documentation CI plus pinned/current OpenCL workflows.
- Final-head workflow results must be checked after all context commits.

## Known blockers and caveats

- **Runtime proof:** the generated source remains intentionally incomplete and exits nonzero until graph/allocation integration is implemented.
- **Allocation API:** exact pinned per-tensor allocation signature still needs confirmation before emitting the final C++ body.
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
