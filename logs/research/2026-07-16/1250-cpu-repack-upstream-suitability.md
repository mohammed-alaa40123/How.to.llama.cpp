# CPU_REPACK fixture upstream-suitability review

- Run time: 2026-07-16 12:50 Africa/Cairo
- Documentation branch: `automation/backend-teardown-audit-method`
- Pinned evidence revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream revision reviewed: `8ee54c8b32a1b0cf13c03fc5723142bc62c775f6`
- Bounded artifact: `docs/reference/upstream-cpu-repack-lifetime-fixture-proposal.md`

## Verified

The complete README, project state, research log, research ledger, and previous detailed note were read before editing.

Current upstream `tests/CMakeLists.txt` still defines `llama_build_and_test()`, registers `test-backend-ops.cpp`, and groups direct-backend tests under `if (NOT GGML_BACKEND_DL)`. Current `ggml/src/ggml-cpu/repack.h` still exposes the internal `ggml_backend_cpu_repack_buffer_type()` declaration.

The passing project fixture remains structurally compatible with an upstream two-file test proposal, provided it is guarded from dynamic-backend builds and reviewed against the exact submission head.

The required regression properties remain:

1. exact CPU_REPACK buffer identity;
2. non-null selected repack traits;
3. operation admission;
4. identical quantized inputs for reference and tested graphs;
5. NMSE at or below `1e-7`;
6. completed compute before teardown; and
7. CPU backend-wrapper destruction before retained repack-buffer destruction.

## Interpretation

The passing fixture is suitable to stage for upstream review as a dedicated test, but the project-specific generator and twenty-process evidence workflow should not be submitted with the first patch.

Cross-platform upstream testing may permit a clean skip when AVX2 is absent. That does not replace an authoritative sanitizer lane where AVX2 and successful CPU_REPACK admission are mandatory. Otherwise the regression could silently become permanently skipped.

The dedicated executable is preferable to folding the unusual destruction sequence into `test-backend-ops.cpp`, because the regression is about ownership and teardown rather than broad numerical operator coverage.

## Historical

The previous sequence moved from source-level ownership reasoning to a deterministic fixture, exact pinned compilation, and twenty passing AVX2 ASan/LSan processes. This run makes the subsequent upstream-suitability decision and stages the review text.

## Open question

- Whether current upstream commit `8ee54c8` still admits the exact Q4_0 `[32, 8]` case when compiled, rather than only retaining compatible APIs.
- Which llama.cpp CI runner can guarantee AVX2 and sanitizer execution.
- Whether maintainers prefer `tensor->extra` as path proof or a less internal observable.
- Whether to add repeated in-process execution before or after upstream submission.

## Validation

- Inspected the current project generator and living context.
- Inspected current upstream test registration and internal repack declaration at exact commit `8ee54c8`.
- Staged a complete upstream proposal with title, body, patch shape, guards, evidence scope, and open questions.
- Research ledger unchanged because the official llama.cpp source was already recorded as the active primary source.

## Next priority

Generate the two-file candidate against current upstream `8ee54c8`, compile it in a current-tree sanitizer workflow, and confirm that the minimal case still reaches CPU_REPACK before opening an upstream pull request.