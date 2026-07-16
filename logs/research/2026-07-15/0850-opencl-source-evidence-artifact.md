# Preserve exact pinned OpenCL source with lifecycle report

- Run time: 2026-07-15 08:50 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: remove the remaining source-recovery blocker for queue/context ownership tracing by preserving the complete verified pinned translation unit beside the generated lifecycle report

## Startup and inspection

Read the complete repository README first, then `docs/reference/project-state.md`, `docs/reference/research-log.md`, `docs/reference/research-ledger.md`, and the latest detailed note. Inspected PR #1, the current OpenCL lifecycle workflow, the regenerated 558-call artifact, and the exact `clCreateContext` and `clCreateCommandQueue` context windows before editing.

## Artifact

Updated `.github/workflows/opencl-lifecycle-report.yml` so each successful run now uploads three mutually checkable files in the existing `opencl-lifecycle-pinned-e3546c7` artifact:

1. `opencl-lifecycle-pinned-e3546c7.json` — exact-line lifecycle inventory with bounded context;
2. `ggml-opencl-pinned-e3546c7.cpp` — the complete source file fetched from pinned revision `e3546c7948e3af463d0b401e6421d5a4c2faf565`;
3. `opencl-lifecycle-pinned-e3546c7.sha256` — SHA-256 entries for both report and preserved source.

The workflow now also verifies that the fetched checkout HEAD equals the full pinned revision, rejects an unexpectedly small source file, and requires exactly two checksum-manifest entries.

## Verified

- The previous report identified one direct `clCreateContext()` assigned to `shared_context` at pinned line 5545 and one direct `clCreateCommandQueue()` assigned to `backend_ctx->queue` at pinned line 5902.
- Three-line context windows identify those assignments but do not expose the declarations, enclosing owners, or final destruction paths.
- The previous artifact preserved only the JSON report, so the next ownership audit still depended on incomplete connector rendering of the large translation unit.
- The updated workflow preserves the exact source used to generate the report, not a separately downloaded or floating copy.
- The pinned checkout is now checked explicitly with `git rev-parse HEAD` before report generation.
- The artifact checksum manifest binds the preserved source and generated report for later review.

## Interpretation

This increment does not resolve queue/context ownership itself. It removes the evidence-access blocker that prevented a complete source-level trace of `shared_context`, `backend_ctx->queue`, scheduler events, optional Adreno library teardown, and enqueue-then-release sites. Future runs can inspect the exact source artifact locally without relying on truncated connector output.

## Historical

The repository-owned workflow already fetched the complete pinned translation unit and generated a reproducible report, but discarded the source before artifact upload. Earlier reviews could inspect bounded call windows only.

## Open questions

- Where is `shared_context` declared and what object or process lifetime owns it?
- Which destructor or free path owns `backend_ctx->queue`?
- Do scheduler event and buffer deleters remain valid after backend-wrapper destruction?
- When is the optional Adreno binary-library handle released relative to kernels?

## Validation

The workflow YAML was reviewed for pinned-revision verification, non-empty source validation, report validation, source-size validation, checksum generation, and artifact upload paths. GitHub-hosted Documentation CI and the pinned lifecycle workflow must be checked for commit `d679012a8dd6f8769114884294bff9d8a4e03265` and the final durable-state head.

Local clone-based validation remains blocked by `Could not resolve host: github.com`.

## Next priority

Download the regenerated artifact, verify both SHA-256 entries, search the complete pinned source for `shared_context` and `backend_ctx->queue`, and update the OpenCL and cross-backend teardown matrices with exact owner and destruction paths.
