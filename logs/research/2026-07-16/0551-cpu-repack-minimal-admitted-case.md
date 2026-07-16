# Minimal admitted CPU repack `MUL_MAT` case

- Run time: 2026-07-16 05:51 Africa/Cairo
- Documentation branch: `automation/backend-teardown-audit-method`
- Pinned source revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Bounded artifact: exact tensor type, dimensions, feature gate, and admission assertions for the first CPU repack lifetime regression

## Verified

The pinned CPU backend always compiles `ggml-cpu/repack.cpp` into the ordinary CPU backend target. There is no separate `GGML_CPU_REPACK` build option in the pinned CPU CMake path. Runtime admission, rather than source inclusion, determines whether a tensor receives repack traits.

For `GGML_TYPE_Q4_0`, `ggml_repack_get_optimal_repack_type()` selects the `q4_0_8x8_q8_0` traits when both conditions hold:

```text
ggml_cpu_has_avx2() == true
weight->ne[1] % 8 == 0
```

The Q4_0 quantization block size is 32 values along `ne[0]`. Therefore the smallest ordinary two-dimensional weight shape satisfying the quantization and AVX2 row-interleave constraints is:

```text
weight:     GGML_TYPE_Q4_0, ne = [32, 8]
activation: GGML_TYPE_F32,  ne = [32, 1]
result:     GGML_TYPE_F32,  ne = [8, 1]
operation:  GGML_OP_MUL_MAT
```

The pinned extra-buffer admission path accepts this operation only when:

1. `op->op == GGML_OP_MUL_MAT`;
2. the weight has a buffer;
3. the weight is exactly two-dimensional;
4. the weight buffer type is exactly `ggml_backend_cpu_repack_buffer_type()`;
5. `ggml_repack_get_optimal_repack_type(weight)` returns non-null;
6. the activation buffer is host-addressable when it already has storage; and
7. the activation type is F32.

The repack buffer type has the stable public-facing name `CPU_REPACK`. Its allocator delegates storage allocation to the ordinary CPU buffer allocator, then replaces the buffer type and tensor initialization/upload callbacks. Tensor initialization stores the selected static repack traits pointer in `tensor->extra`; upload invokes those traits to repack the original Q4_0 bytes into the interleaved representation.

The extra-dispatch implementation then accepts only tensors whose weight buffer still points to the repack buffer type and whose trait selection remains non-null. This gives the fixture two independent path proofs:

```text
weight->buffer->buft == ggml_backend_cpu_repack_buffer_type()
weight->extra != nullptr
```

followed by:

```text
ggml_backend_supports_op(cpu_backend, mul_mat) == true
```

## Exact fixture contract

The first fixture should use one AVX2-gated case:

```text
Q4_0 [32, 8] × F32 [32, 1] -> F32 [8, 1]
```

Required execution and teardown order:

```text
create ordinary reference CPU backend
create CPU execution backend for the repack path
obtain ggml_backend_cpu_repack_buffer_type()
construct identical reference and repack MUL_MAT graphs
allocate reference weight in ordinary CPU storage
allocate tested weight from CPU_REPACK
allocate activations and outputs in ordinary CPU storage
quantize identical F32 weight values to Q4_0
upload through each buffer's set_tensor callback
assert repack buffer identity and non-null tensor traits
assert the tested backend supports the exact operation
compute both graphs synchronously
read and compare outputs
free the tested CPU backend wrapper
free graph and tensor metadata
free the retained CPU_REPACK buffer last
repeat multiple times under ASan and LSan
```

The test should print a clear skip only when `ggml_cpu_has_avx2()` is false. Once AVX2 is reported, failure to obtain repack traits or operation admission is a test failure, not a skip.

## Interpretation

`Q4_0 [32, 8] × F32 [32, 1]` is the smallest pinned x86 AVX2 case that exercises the ordinary repack buffer's initialization, upload, trait lookup, optional CPU dispatch, synchronous compute, and backend-wrapper-before-buffer destruction order.

The case is preferable to Q4_K or Q2_K for the first regression because its minimum quantization width is 32 rather than 256, and AVX2 admission is available on common x86-64 CI hardware. The fixture remains hardware-gated: a successful skip on a non-AVX2 runner is not lifetime evidence. CI should therefore include at least one runner whose logs confirm `ggml_cpu_has_avx2()` and `CPU_REPACK` admission.

The display name `CPU_REPACK` is useful for diagnostics, but identity should use the actual buffer-type pointer returned by `ggml_backend_cpu_repack_buffer_type()`. String matching alone would not prove that the tested tensor used the intended implementation.

## Historical

The previous increment selected `tests/test-cpu-extra-buffer-lifetime.cpp` as the dedicated integration point and recommended reusing the backend-op harness for quantization, upload, graph execution, readback, and numerical comparison. This increment closes the remaining type-and-shape question for the first x86 fixture.

## Open questions

- Whether GitHub's current Ubuntu hosted runner contract guarantees AVX2, rather than merely exposing it on current hosts.
- Whether the first implementation should duplicate a small bounded set of `test-backend-ops.cpp` helpers or extract a shared test utility.
- Which numerical tolerance from the existing Q4_0 backend-op cases should be reused verbatim.
- Whether a second ARM NEON+dotprod case should be added immediately after the x86 fixture to avoid platform-specific lifetime coverage.

## Validation

- Read the complete required startup files and latest detailed research note before editing.
- Inspected pinned `ggml/src/ggml-cpu/repack.cpp`, including trait instances, Q4_0 runtime selection, repack-buffer callbacks, extra-buffer `supports_op()`, and stable buffer-type identity.
- Inspected pinned `ggml/src/ggml-cpu/CMakeLists.txt` and confirmed that `repack.cpp` is included in the ordinary CPU source list without a separate repack option.
- Cross-checked the proposed shape against the Q4_0 block width, AVX2 row multiple, two-dimensional weight requirement, F32 activation requirement, and host-buffer admission rule.

No executable was compiled in this runtime because a patch-capable upstream checkout remains unavailable. The next implementation must compile and run the fixture on an AVX2-capable GitHub Actions host under ASan/LSan.

## Next priority

Implement `tests/test-cpu-extra-buffer-lifetime.cpp` with the exact Q4_0 `[32, 8]` case, add its CMake target, and run repeated backend-before-buffer teardown under ASan/LSan on an AVX2-confirmed runner.