# CPU_REPACK fixture graph, allocation, and tolerance contract

- Run time: 2026-07-16 07:52 Africa/Cairo
- Documentation branch: `automation/backend-teardown-audit-method`
- Pinned source revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Bounded artifact: resolve the exact pinned no-allocation graph/allocation sequence and numerical error contract for the first CPU_REPACK lifetime fixture

## Verified

The pinned backend-op harness initializes a GGML context with `no_alloc = true`, creates the graph metadata, builds the operation, verifies backend support, allocates tensor storage, expands the forward graph, initializes tensors, and then compares backend execution. The relevant order is:

```text
ggml_init(no_alloc = true)
    → ggml_new_graph(ctx)
    → create weight, activation, and ggml_mul_mat(ctx, weight, activation)
    → verify ggml_backend_supports_op()
    → allocate tensor storage
    → ggml_build_forward_expand(graph, output)
    → upload inputs
    → execute and compare
```

For the dedicated lifetime fixture, one shared context cannot allocate the tested weight from CPU_REPACK while allocating activation/output from ordinary CPU storage through `ggml_backend_alloc_ctx_tensors()`. The fixture therefore needs explicit per-tensor allocation:

```text
weight buffer: ggml_backend_buft_alloc_buffer(repack_buft, ggml_nbytes(weight))
weight tensor: ggml_backend_tensor_alloc(repack_buffer, weight, 0)
activation/output: ordinary CPU buffer allocations, or separate no-alloc contexts allocated with the CPU backend
```

The important lifetime property is that `repack_buffer` is retained independently after `ggml_backend_free(tested_backend)`. Tensor metadata may be destroyed before the buffer, but the buffer must remain valid until its explicit free.

The pinned comparison contract in `test-backend-ops.cpp` is normalized mean squared error:

```text
NMSE = sum((reference - tested)^2) / sum(reference^2)
```

The base `test_case` threshold is `1e-7`. The ordinary `MUL_MAT` path does not need a looser Q4_0-specific threshold for comparing two executions that consume the same already-quantized Q4_0 bytes. Quantization error is common to both sides; the regression compares backend implementations, not Q4_0 output against an unquantized mathematical reference.

The fixture should therefore use:

```cpp
constexpr double max_nmse = 1e-7;
```

It should upload one deterministic F32 weight source, quantize it once with `ggml_quantize_chunk(GGML_TYPE_Q4_0, ...)`, upload the exact resulting byte vector to both ordinary and repack weights, and upload the same deterministic F32 activation to both graphs.

## Interpretation

The safest implementation is two independent no-allocation graphs with identical tensor shapes and input bytes:

```text
reference graph
  Q4_0 weight on ordinary CPU buffer
  F32 activation/output on ordinary CPU buffer

tested graph
  Q4_0 weight on exact CPU_REPACK buffer
  F32 activation/output on ordinary CPU buffers
```

This avoids relying on `ggml_backend_compare_graph_backend()` to duplicate a repacked weight whose physical representation differs from ordinary Q4_0 storage. It also makes the ownership boundary explicit and lets the tested backend wrapper be destroyed while the repack buffer is still retained.

The output comparison should occur before unusual teardown. The lifetime regression is then the destruction order itself, repeated under ASan/LSan:

```text
compute and compare
    → ggml_backend_free(tested_backend)
    → destroy tested graph/context metadata
    → ggml_backend_buffer_free(repack_buffer)
```

## Historical

The previous three increments selected the dedicated executable, the minimal admitted AVX2 case Q4_0 `[32, 8]` × F32 `[32, 1]`, and a deterministic patch generator. This increment resolves the generator's two remaining source-design questions: allocation topology and numerical tolerance.

## Open question

- The exact pinned signature and availability of `ggml_backend_tensor_alloc()` must be confirmed before emitting the final C++ body. If unavailable or unsuitable, the fixture should use separate contexts so `ggml_backend_alloc_ctx_tensors_from_buft()` can allocate the weight-only context from CPU_REPACK.
- The authoritative sanitizer runner still needs an explicit AVX2 feature check; a non-AVX2 skip is not runtime lifetime evidence.

## Validation

- Read the complete README, project state, research log, research ledger, and latest detailed note before editing.
- Inspected pinned `test-backend-ops.cpp` initialization, quantization, readback, NMSE, base threshold, no-allocation context, backend-support checks, allocation, graph expansion, and comparison flow.
- Confirmed the previous branch head had successful Documentation CI and pinned/current OpenCL workflows.
- No external source was added or reclassified; the research ledger remains unchanged.

## Next priority

Confirm the exact pinned per-tensor allocation API, then update the generator to emit the complete two-graph fixture with deterministic shared Q4_0 bytes, `1e-7` NMSE comparison, backend-before-repack-buffer teardown, and repeated sanitizer execution.
