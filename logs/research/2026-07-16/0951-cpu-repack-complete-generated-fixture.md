# Complete generated CPU_REPACK lifetime fixture

- Run time: 2026-07-16 09:51 Africa/Cairo
- Documentation branch: `automation/backend-teardown-audit-method`
- Pinned source revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Bounded artifact: replace the intentional status-2 generator boundary with a complete two-graph CPU_REPACK regression candidate

## Verified

The deterministic generator now emits a complete candidate `tests/test-cpu-extra-buffer-lifetime.cpp` rather than a placeholder. The generated source:

- creates independent no-allocation reference and tested GGML graphs;
- uses Q4_0 `[32, 8] × F32 [32, 1]`;
- explicitly allocates only the tested weight from `ggml_backend_cpu_repack_buffer_type()`;
- lets an ordinary CPU graph allocator allocate activation and output tensors;
- quantizes one deterministic F32 weight vector once and uploads identical Q4_0 bytes to both graphs;
- uploads identical deterministic F32 activation data;
- asserts exact repack buffer identity, non-null repack traits, and backend operation admission;
- computes both graphs, reads F32 outputs, and requires NMSE `<= 1e-7`;
- frees the tested CPU backend wrapper before the retained repack buffer;
- prints a success marker only after the repack path and numerical comparison complete.

Focused generator tests now enforce graph construction, allocation, deterministic shared inputs, compute, readback, NMSE, path proof, CMake registration, and teardown order. The former `INCOMPLETE` message and `return 2` boundary are forbidden.

## Interpretation

This closes the generator-level implementation gap. The artifact is now suitable for pinned-tree compilation and sanitizer execution. It is still a generated candidate patch, not runtime lifetime proof, until it compiles and runs against the exact pinned llama.cpp source on an AVX2-capable runner.

The two-graph design avoids comparing different logical inputs and prevents ordinary CPU fallback from being mistaken for CPU_REPACK execution. Exact buffer identity and `tensor->extra` are required path evidence in addition to output correctness.

## Historical

Earlier increments selected the integration point, minimal admitted shape, graph topology, NMSE threshold, and address-based per-tensor allocation API. This increment combines those decisions into the complete generated C++ body.

## Open question

- Confirm the generated candidate compiles against the pinned revision; API spelling and graph-overhead sizing remain subject to compiler validation.
- Run repeated ASan/LSan execution on a runner that proves AVX2 and successful CPU_REPACK admission.
- Decide whether the test should loop internally or use repeated CTest invocations in CI.

## Validation

- Read the complete README, project state, research log, research ledger, and latest detailed note before editing.
- Inspected pinned backend-op quantization, upload, readback, NMSE, graph, and allocation patterns.
- Ran the focused Python generator tests locally: 7 tests passed.
- Confirmed deterministic generated output and removal of the intentional status-2 boundary.
- Research ledger unchanged because no new external source was added or reclassified.

## Next priority

Add a pinned-source workflow that materializes the generated patch, compiles the dedicated target with AddressSanitizer and LeakSanitizer on an AVX2-confirmed runner, executes it repeatedly, and fails if the repack path is skipped or not admitted.
