# CPU optional extra-buffer comparison increment

- Run time: 2026-07-14 07:49 Africa/Cairo
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: synthesize the completed repack, AMX, KleidiAI, and SpacemiT IME audits into one reviewable comparison and destruction-test matrix

## Startup and inspection

Read the complete repository README first, then project state, research log, research ledger, and the latest detailed SpacemiT note. Inspected the active PR, MkDocs navigation, the four completed optional CPU extra-buffer pages, and the current TODO ordering before editing.

## Artifact

Added `docs/architecture/cpu-extra-buffer-comparison.md` and linked it after the four implementation-specific pages.

## Verified

- All four audited paths publish process-static buffer-type metadata and store process-static implementation traits in `tensor->extra`.
- All four execute through synchronous CPU graph computation and introduce no scheduler event or independent accelerator queue.
- Repack and KleidiAI retain ordinary CPU allocation/free ownership.
- AMX owns a dedicated aligned allocation through the buffer context.
- SpacemiT owns a dedicated Spine pool allocation through the buffer context.
- The state required by the audited weight-buffer free callbacks does not live in `ggml_backend_cpu_context`.

## Interpretation

The implementations split into an overlay family (repack and KleidiAI) and a dedicated-allocation family (AMX and SpacemiT). Backend-wrapper-independent weight-buffer destruction is common, but complete implementation shutdown differs: AMX retains platform allocator/tile-permission questions, while SpacemiT retains thread-local TCM and process-pool shutdown obligations.

## Historical

The matrix is pinned. Admission rules, callback tables, packing layouts, allocator APIs, worker hooks, and static-lifetime choices are revision-sensitive.

## Open questions

- Validate AMX allocation/free pairing and repeated tile-permission initialization.
- Validate null transfer/readback callbacks across optional buffer types.
- Validate KleidiAI concurrent initialization and packed-layout portability.
- Prove SpacemiT TCM release on every worker/error/threadpool-destruction path.
- Implement the comparison page's ASan/LSan/TSan destruction matrix.

## Validation

Repository files were updated on `automation/backend-teardown-audit-method`. The artifact includes a cross-implementation table, ownership diagram, common/different lifetime analysis, and a portable destruction-test matrix. CI and Pages are checked after the durable context updates.

## Next priority

Finish the complete pinned OpenCL teardown audit when the full translation unit is searchable. In parallel, implement the first portable CPU extra-buffer backend-free-before-buffer-free regression harness from the new matrix.
