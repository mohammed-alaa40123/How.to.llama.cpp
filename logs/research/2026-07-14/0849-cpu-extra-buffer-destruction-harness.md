# CPU optional extra-buffer destruction harness increment

- Run time: 2026-07-14 08:49 Africa/Cairo
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: convert the completed CPU optional-buffer comparison into an implementation-ready, reviewable regression-harness specification

## Startup and inspection

Read the complete repository README first, then project state, research log, research ledger, and the latest detailed note. Inspected the active PR, MkDocs navigation, CPU optional-buffer comparison, CI workflow, latest failed Documentation CI run, and current TODO ordering before editing.

## Artifact

Added `docs/architecture/cpu-extra-buffer-destruction-harness.md` and linked it after the CPU extra-buffer comparison.

## Verified

- CPU repack is the first portable target because it uses ordinary CPU allocation/free ownership, process-static traits, and synchronous CPU graph execution.
- The test must prove actual optional-buffer admission and supported operation dispatch rather than silently exercising ordinary CPU fallback.
- Output correctness and backend-free-before-buffer-free ordering are separate assertions.
- The fixture must retain tensor, graph, context, and buffer owners explicitly and release them deterministically.
- ASan/LSan cover UAF, invalid free, double free, and fixture leaks; TSan belongs in a separate initialization/concurrency target.

## Interpretation

A tiny deterministic `MUL_MAT` fixture is stronger for this ownership question than a full model because it makes admission, allocation owner, synchronous completion, and destruction order visible. The same fixture can be extended in stages to KleidiAI, AMX, and SpacemiT while preserving implementation-specific gates and auxiliary teardown obligations.

## Historical

The fixture requirements are pinned to the optional CPU buffer interfaces and admission behavior at the selected revision. Callback tables, tensor formats, feature gates, and upstream test helpers are revision-sensitive.

## Open questions

- Select the smallest upstream test helper for constructing a quantized `MUL_MAT` graph.
- Decide whether the executable belongs beside backend tests or in a dedicated optional-buffer lifetime target.
- Separate intentional process-static metadata from real LSan leaks.
- Define explicit SpacemiT process-pool shutdown before attempting process-lifetime validation.

## Validation and CI

The latest checked Documentation CI run `29307346854` failed in `Validate project context, interactive links, and scripts`. Checkout and startup-context reading succeeded; dependency installation and strict MkDocs build were skipped. The connector returned the job log only partially, still without the final failing assertion. Local cloning again failed with `Could not resolve host: github.com`.

## Next priority

Implement the repack fixture in the pinned llama.cpp test tree or a project-owned patch, run it under ASan/LSan, then extend the same ordering contract to KleidiAI, AMX, and SpacemiT hardware paths.
