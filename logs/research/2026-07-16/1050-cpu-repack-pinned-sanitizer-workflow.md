# Pinned CPU_REPACK sanitizer workflow

- Run time: 2026-07-16 10:50 Africa/Cairo
- Documentation branch: `automation/backend-teardown-audit-method`
- Pinned source revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Bounded artifact: `.github/workflows/cpu-repack-lifetime-sanitizer.yml`

## Verified

The new workflow performs one exact-revision compiler and lifetime-validation path:

1. checks out the documentation repository;
2. records `lscpu` output and fails unless `/proc/cpuinfo` exposes AVX2;
3. fetches and verifies the exact pinned llama.cpp commit;
4. imports the deterministic generator and writes its complete `CPP_SOURCE` into the pinned `tests/` tree;
5. inserts the generated CMake fragment at the pinned `test-backend-ops.cpp` marker;
6. configures a `RelWithDebInfo` build with AddressSanitizer, LeakSanitizer leak detection, and frame pointers;
7. compiles only `test-cpu-extra-buffer-lifetime`;
8. executes the binary twenty times;
9. fails if any execution emits `SKIP:` or if fewer than twenty exact CPU_REPACK success markers appear; and
10. uploads CPU capability, generated source, and sanitizer output as retained evidence.

The workflow is path-filtered to the generator, its focused tests, and the workflow itself. The first run is `29481384561`; it was queued at the initial status check.

## Interpretation

This closes the missing CI implementation boundary but does not yet constitute runtime proof. The first run is expected to expose any pinned API, CMake, include-path, graph-allocation, or sanitizer issue that source inspection could not resolve.

Failing rather than skipping on a non-AVX2 hosted runner is intentional. A green workflow must prove that the selected CPU_REPACK path was actually available and executed, not merely that the test binary exited successfully.

Twenty separate process executions exercise initialization and process teardown repeatedly and keep each sanitizer report isolated enough to identify deterministic lifetime failures. Internal looping can be considered later if process-start overhead becomes material.

## Historical

The preceding increment completed the generated two-graph C++ candidate with deterministic shared Q4_0/F32 inputs, exact path proof, `1e-7` NMSE, and backend-wrapper-before-buffer teardown. This increment moves that candidate into an exact pinned-tree compile-and-run workflow.

## Open question

- Whether the first hosted build accepts every generated pinned API spelling and internal include path.
- Whether `ubuntu-latest` currently exposes AVX2 to the runner consistently.
- Whether ASan/LSan reports process-static CPU dispatch allocations that require narrow documentation rather than suppression.
- Whether the externally allocated repack weight remains untouched by the ordinary graph allocator at runtime.

## Validation

- Read the complete README, project state, research log, research ledger, and latest detailed note before editing.
- Inspected the complete generator and the existing pinned OpenCL workflow's exact-revision fetch and artifact conventions.
- Confirmed the new workflow appeared in GitHub Actions as `Validate pinned CPU_REPACK lifetime fixture`, run `29481384561`.
- Research ledger unchanged because no new external source was added or reclassified.

## Next priority

Inspect the first workflow run. Correct compiler or runtime failures in the generated fixture or workflow, then preserve a passing AVX2-confirmed twenty-run ASan/LSan artifact as the first executable CPU_REPACK lifetime result.
