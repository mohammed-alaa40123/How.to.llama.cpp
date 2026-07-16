# Project state

_Last updated: 2026-07-16 08:51 Africa/Cairo_

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

- The pinned `ggml_backend_tensor_alloc()` signature is `(buffer, tensor, addr)`: its third argument is an address inside an already allocated backend buffer, not an offset.
- Pinned `ggml_tallocr_alloc()` queries backend-specific allocation size, obtains an aligned address from the buffer base, and passes that address to `ggml_backend_tensor_alloc()`.
- A one-weight CPU_REPACK fixture can allocate exactly one buffer using `ggml_backend_buft_get_alloc_size(repack_buft, tested_weight)`, use the buffer base as the aligned address, and initialize the tested weight directly.
- The generator now emits a concrete `allocate_single_tensor()` helper and focused tests enforce allocation-size, buffer-allocation, base-address, alignment, and initialization-status calls.
- The graph allocator recognizes externally buffered tensors as already allocated, so ordinary graph allocation can still own tested activation/output while leaving the repack weight untouched.

### Interpretation

- Direct per-tensor allocation is simpler and more explicit than a separate weight-only context for this bounded fixture.
- Use backend-specific allocation size rather than `ggml_nbytes(weight)`, because CPU_REPACK physical storage may differ from ordinary Q4_0 bytes.
- The resulting ownership split is exact: repack buffer owns the tested weight storage/traits; ordinary CPU allocation owns activation/output; the CPU backend wrapper executes but does not own the repack buffer.

### Historical

- Prior runs selected the dedicated executable, minimal Q4_0 `[32, 8]` × F32 `[32, 1]` AVX2 case, deterministic generator, two-graph topology, identical quantized inputs, and `1e-7` NMSE contract.
- This run closes the remaining allocation-API question and advances the generator from comments to a concrete allocation helper.

### Open questions

- Complete graph construction, ordinary activation/output allocation, deterministic quantization/upload, compute, readback, and NMSE comparison.
- Verify the final graph allocator does not replace or reinitialize the externally allocated repack weight.
- Whether GitHub-hosted Ubuntu exposes AVX2 consistently enough for authoritative sanitizer coverage.

## Immediate next task

```text
complete two no-alloc graphs
  → preallocate tested Q4_0 weight with allocate_single_tensor(repack_buft, ...)
  → allocate activation/output from ordinary CPU storage
  → quantize deterministic F32 weight once and upload identical Q4_0 bytes
  → upload identical deterministic F32 activation
  → prove buffer identity, non-null traits, and supports_op
  → execute both graphs and compare NMSE <= 1e-7
  → free tested backend wrapper before retained repack buffer
  → repeat under ASan/LSan on AVX2-confirmed CI
```

## In progress

- First CPU repack lifetime fixture graph execution and sanitizer CI.
- Manual/upstream submission of the reviewed 46-release OpenCL ownership correction; GitHub App write access to upstream is blocked.
- Source-index regeneration with pinned line-aware symbol inventory.
- Hardware-specific lifetime extensions for KleidiAI, AMX, and SpacemiT.
- Runtime overlays for mmap/page faults, scheduler copies, events, KV/recurrent growth, and backend queues.

## Publication and validation state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`.
- Added detailed note `logs/research/2026-07-16/0851-cpu-repack-per-tensor-allocation-api.md`.
- Updated the generator, focused tests, README living TODOs, this project checkpoint, and the concise research log.
- Research ledger unchanged: this increment used the already-recorded pinned llama.cpp primary source.
- Final-head workflow results must be checked after all context commits.

## Known blockers and caveats

- **Runtime proof:** the generated source still intentionally exits nonzero until graph execution and comparison are implemented.
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
