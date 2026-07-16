# CPU_REPACK fixture per-tensor allocation API

- Run time: 2026-07-16 08:51 Africa/Cairo
- Documentation branch: `automation/backend-teardown-audit-method`
- Pinned source revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Bounded artifact: confirm the exact pinned per-tensor allocation contract and encode it into the deterministic fixture generator and tests

## Verified

The pinned public declaration is:

```cpp
enum ggml_status ggml_backend_tensor_alloc(
    ggml_backend_buffer_t buffer,
    struct ggml_tensor * tensor,
    void * addr);
```

The third argument is an address inside an already allocated backend buffer, not a byte offset. The pinned allocator demonstrates the required sequence:

```text
query backend-specific allocation size
    → allocate backend buffer
    → obtain aligned address from the buffer base plus allocator offset
    → call ggml_backend_tensor_alloc(buffer, tensor, addr)
```

For the one-weight CPU_REPACK fixture, one tensor per buffer is sufficient and makes ownership explicit:

```text
alloc_size = ggml_backend_buft_get_alloc_size(repack_buft, tested_weight)
repack_buffer = ggml_backend_buft_alloc_buffer(repack_buft, alloc_size)
addr = ggml_backend_buffer_get_base(repack_buffer)
ggml_backend_tensor_alloc(repack_buffer, tested_weight, addr)
```

The generator now emits `allocate_single_tensor()`, verifies the buffer base and alignment, checks `GGML_STATUS_SUCCESS`, and keeps the intentional nonzero boundary until graph execution is implemented. Focused tests now require every API step.

The graph allocator can treat a tensor with an externally assigned `tensor->buffer` as already allocated. Therefore, the tested graph can preallocate only its Q4_0 weight from CPU_REPACK and use an ordinary CPU graph allocator for activation and output.

## Interpretation

Direct per-tensor allocation is suitable and simpler than creating a separate weight-only context. It provides the exact ownership boundary needed by the regression:

```text
repack buffer owns tested weight storage and repack traits
ordinary graph allocation owns tested activation/output
CPU backend wrapper executes the graph but does not own repack buffer
```

This design allows the tested backend wrapper to be freed before the retained repack buffer without mixing storage ownership.

The helper deliberately uses the backend-specific allocation-size query rather than `ggml_nbytes(weight)`, because CPU_REPACK may require a physical layout size different from ordinary Q4_0 bytes.

## Historical

The previous run established the two-graph topology, identical quantized inputs, and `1e-7` NMSE contract, but left the exact allocation API unresolved. This increment closes that question and advances the generator from API-surface comments to a concrete allocation helper.

## Open question

- Complete graph construction, ordinary activation/output allocation, deterministic quantization/upload, compute, readback, and NMSE comparison in the generated C++ fixture.
- Confirm that the final graph allocator does not replace or reinitialize the externally allocated repack weight.
- Add repeated ASan/LSan execution on a runner that explicitly proves AVX2 and successful CPU_REPACK admission.

## Validation

- Read the complete README, project state, research log, research ledger, and latest detailed note before editing.
- Inspected the pinned `ggml-backend.h` declaration and the pinned `ggml_tallocr_alloc()` implementation.
- Updated the deterministic generator with the exact address-based API and backend-specific allocation sizing.
- Updated focused generator tests to enforce allocation-size, buffer-allocation, base-address, alignment, initialization-status, path-proof, and teardown tokens.
- Research ledger unchanged because no new source category was added; the pinned llama.cpp source was already active.

## Next priority

Replace the remaining intentional status-2 boundary with complete graph execution and numerical comparison, while preserving the now-verified per-tensor CPU_REPACK allocation and backend-before-buffer teardown order.
