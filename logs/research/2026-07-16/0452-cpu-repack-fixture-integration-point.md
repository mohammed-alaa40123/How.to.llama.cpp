# CPU repack lifetime fixture integration point

- Run time: 2026-07-16 04:52 Africa/Cairo
- Documentation branch: `automation/backend-teardown-audit-method`
- Pinned source revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current source cross-check: `505b1ed15ca80e2a19f12ff4ac365e40fb374053`
- Bounded artifact: implementation placement and reuse plan for the first admitted CPU repack `MUL_MAT` lifetime regression

## Verified

The complete required startup sequence was completed before editing: the root README, project state, concise research log, research ledger, and latest detailed note were read. The current documentation branch and relevant CPU lifetime documentation were inspected.

Current upstream `tests/test-backend-ops.cpp` already provides the reusable building blocks needed by the fixture:

1. `init_tensor_uniform()` creates deterministic-shaped host data, quantizes quantized tensor types with `ggml_quantize_chunk()`, and uploads through `ggml_backend_tensor_set()`.
2. `tensor_to_float()` reads backend tensors with `ggml_backend_tensor_get()` and dequantizes quantized formats through the registered type traits.
3. `test_case::eval()` constructs no-allocation GGML contexts, builds a graph, checks `ggml_backend_supports_op()`, allocates tensor storage through backend buffer APIs, initializes tensors, executes both backends, and compares outputs.
4. The existing test harness already models the correct correctness baseline: execute the same operation on the backend under test and a reference backend, then compare tensor values.

The CPU extra-dispatch path is separate from ordinary CPU fallback. `ggml_cpu_extra_compute_forward()` enumerates `ggml_backend_cpu_get_extra_buffer_types()`, obtains the implementation-specific `extra_buffer_type` from `buffer_type->context`, asks it for tensor traits, and returns only when one implementation's `compute_forward()` accepts and executes the operation. The analogous work-size path uses the same enumeration and trait lookup.

Therefore the first lifetime regression should not create a new standalone matrix-reference implementation. It should reuse the existing backend-op test infrastructure for data generation, quantization, graph construction, execution, and numerical comparison, while adding one narrow ownership-order mode.

## Recommended implementation shape

Add a dedicated executable beside `test-backend-ops`, rather than changing normal comparison-test teardown globally:

```text
tests/test-cpu-extra-buffer-lifetime.cpp
```

The executable should reuse or extract the following helpers from `test-backend-ops.cpp` into a small test utility module:

```text
init_tensor_uniform()
tensor_to_float()
error comparison helpers
small MUL_MAT graph construction
```

The first case should perform this exact sequence:

```text
create reference CPU backend
create CPU backend used for the extra-buffer path
enumerate ggml_backend_cpu_get_extra_buffer_types()
select the CPU repack buffer type explicitly
construct the smallest aligned quantized-weight × F32-activation MUL_MAT
require the selected buffer type's supports_backend / supports_op admission
allocate the weight tensor from that exact buffer type
allocate activation and output in ordinary CPU storage
initialize identical source values
execute reference and repack graphs synchronously
compare output within the quantized-format tolerance
free the CPU backend wrapper used for the repack execution
free graph/tensor metadata
free the repack buffer last
repeat in one process
```

The fixture must fail, not silently skip, when CPU repack is compiled and advertised but the chosen supposedly portable case is not admitted. A skip is acceptable only when the build does not expose the repack buffer type at all, and the reason must be printed explicitly.

## Admission guard

The fixture needs two independent checks:

1. **Buffer-type identity:** the selected buffer must be the repack implementation, not the ordinary CPU buffer returned as fallback.
2. **Operation admission:** the exact `MUL_MAT` node and tensor layout must be accepted through the same trait/support path used by normal placement.

Merely observing correct output is insufficient because ordinary CPU fallback could produce the same result while leaving the optional-buffer lifetime untested.

## Lifetime assertion

The ownership assertion starts only after synchronous graph compute and correctness comparison succeed:

```text
compute complete
    -> output comparison passed
    -> destroy repack execution backend wrapper
    -> retain optional buffer and tensor metadata long enough to expose stale callback/context use
    -> destroy tensor/graph contexts
    -> destroy optional repack buffer
```

ASan catches callback-table or buffer-context use-after-free. LSan checks that fixture-owned contexts, buffers, and wrappers are released. Process-static dispatch metadata should be documented separately rather than hidden with a broad leak suppression.

## Interpretation

The existing `test-backend-ops` machinery is the smallest stable implementation foundation, but the lifetime ordering should live in a dedicated executable. Adding backend-before-buffer destruction to the general comparison runner would make every operation participate in a specialized ownership test and would complicate failure attribution.

The first implementation increment should therefore be a focused source test plus one CMake target and sanitizer-enabled CI invocation. It should not attempt AMX, KleidiAI, or SpacemiT in the same patch.

## Historical

The existing documentation already specified the ownership contract and sanitizer matrix but left open which upstream test helper should be reused. This increment resolves that question: reuse the backend-op harness's quantization, upload, readback, graph, and comparison helpers; isolate the unusual destruction order in a dedicated lifetime executable.

## Open questions

- Which exact quantized format and dimensions are the smallest shape admitted by the pinned CPU repack traits on generic CI hardware?
- Is the repack buffer type exposed in the default CI build, or does the lifetime job need an explicit `GGML_CPU_REPACK=ON` configuration?
- Should helper extraction be accepted upstream, or should the first fixture duplicate a bounded subset to keep the initial patch independent?
- What stable implementation identifier should the test use to distinguish repack from other extra-buffer types without relying on display-name text?

## Validation

- Read and cross-checked `tests/test-backend-ops.cpp` at current revision `505b1ed1`, including quantized initialization, tensor readback/dequantization, support checks, backend allocation, graph construction, and comparison flow.
- Read and cross-checked `ggml/src/ggml-cpu/traits.cpp`, including the exact extra-buffer enumeration and trait-dispatch path.
- Confirmed that the proposed fixture preserves the documented synchronous-completion boundary and backend-wrapper-before-buffer destruction order.

No source code was compiled in this runtime because direct GitHub DNS access and a patch-capable checkout remain unavailable. GitHub-hosted CI remains the authoritative validation path once the fixture source is implemented.

## Next priority

Inspect the pinned CPU repack trait implementation to select one exact admitted tensor type and minimal dimensions, then add `test-cpu-extra-buffer-lifetime.cpp`, its CMake target, and an ASan/LSan CI job.