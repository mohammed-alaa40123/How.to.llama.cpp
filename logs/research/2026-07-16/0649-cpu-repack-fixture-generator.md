# CPU repack lifetime fixture patch generator

- Run time: 2026-07-16 06:49 Africa/Cairo
- Documentation branch: `automation/backend-teardown-audit-method`
- Pinned source revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Bounded artifact: deterministic, revision-scoped generator and structural tests for the first CPU_REPACK lifetime fixture patch

## Verified

- Added `scripts/generate_cpu_repack_lifetime_fixture.py`.
- The generator emits a candidate patch adding `tests/test-cpu-extra-buffer-lifetime.cpp` and its `tests/CMakeLists.txt` registration.
- The generated skeleton encodes the pinned minimal shape Q4_0 `[32, 8]` × F32 `[32, 1]`, the AVX2 gate, exact `ggml_backend_cpu_repack_buffer_type()` lookup, mandatory buffer/trait/admission assertions, and backend-before-buffer teardown order.
- Added `tests/test_generate_cpu_repack_lifetime_fixture.py` with deterministic-output, revision-scope, shape, CMake, path-proof, teardown-order, and false-success prevention checks.
- The skeleton deliberately exits with status 2 after API-surface setup. It cannot be mistaken for successful sanitizer lifetime evidence before graph/allocation integration is compiled against the pinned source.

## Interpretation

This is a bounded implementation step between source reasoning and an executable upstream regression. It converts the fixture contract into deterministic patch material while preserving an explicit failure boundary: structural CI can verify that the intended hardware gate, path proof, dimensions, and destruction order are present, but only a pinned-tree C++ build and sanitizer run can establish runtime correctness.

The generator approach is safer than committing an uncompiled C++ test as if it were complete. It also makes source drift visible because the output is labelled with the exact pinned revision and requires review before application.

## Historical

The previous run selected Q4_0 `[32, 8]` × F32 `[32, 1]` as the smallest admitted AVX2 case and identified the dedicated test executable and CMake integration point. This run materializes those decisions into reproducible candidate patch output.

## Open question

- Which exact no-allocation graph/allocation helper sequence compiles cleanly at the pinned revision while allowing the repack buffer to outlive the tested CPU backend wrapper?
- Which Q4_0 numerical tolerance should be copied from the existing backend-op test cases?
- Does the selected hosted sanitizer runner expose AVX2 consistently enough to make a skip exceptional rather than normal?

## Validation

- Read the complete README, project state, research log, research ledger, and latest detailed note before editing.
- Inspected pinned `tests/CMakeLists.txt`, `tests/test-backend-ops.cpp`, `ggml/include/ggml-cpu.h`, and `ggml/src/ggml-cpu/repack.h`.
- Confirmed that `llama_build_and_test()` is the existing test registration helper and that the repack buffer type is declared only in the internal CPU repack header.
- Added focused Python tests that are discovered by the repository's existing `python3 -m unittest discover -s tests -p 'test_*.py'` validation.

Runtime C++ compilation remains pending because no patch-capable pinned llama.cpp checkout is mounted in this environment.

## Next priority

Replace the intentional status-2 skeleton boundary with the exact pinned graph, allocation, deterministic Q4_0 upload, reference comparison, and repeated sanitizer execution; then add an AVX2-confirmed workflow job.
