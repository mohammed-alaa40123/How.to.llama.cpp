# CPU SpacemiT IME extra-buffer lifetime increment

- Run time: 2026-07-14 06:50 Africa/Cairo
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: one optional CPU extra-buffer implementation, SpacemiT IME

## Startup and inspection

Read the complete repository README first, then project state, research log, research ledger, and the latest detailed KleidiAI note. Inspected the active PR branch, MkDocs navigation, the completed CPU repack/AMX/KleidiAI audits, and pinned `ggml/src/ggml-cpu/spacemit/ime.cpp` plus `spine_mem_pool.cpp`.

## Artifact

Added `docs/architecture/cpu-spacemit-ime-extra-buffer-lifetime.md` and linked it after the KleidiAI audit.

## Verified

- SpacemiT allocates a dedicated 64-byte-aligned buffer through `spine_mem_pool_alloc()` and frees it through `spine_mem_pool_free()`.
- Pool allocation/release is mutex-protected and tracked independently of `ggml_backend_cpu_context`.
- `tensor->extra` points to process-static IME1, IME2, or RVV traits selected during tensor initialization.
- The extra-buffer type and buffer-type metadata are function-static.
- Upload/repacking and graph execution are synchronous CPU work using the CPU threadpool and barriers.
- SpacemiT introduces no scheduler event or accelerator command queue.
- Worker setup can acquire thread-local TCM state; the paired clear-affinity hook explicitly releases the TCM lease.

## Interpretation

The weight-buffer teardown path is backend-wrapper-independent, like AMX with a custom allocator. However, SpacemiT also owns auxiliary per-thread TCM coordination outside `ggml_backend_buffer_t`. Therefore buffer destruction is verified independent, while complete thread/process teardown remains conditional on all worker cleanup hooks running.

## Historical

The result is pinned. IME1/IME2 admission, supported layouts, pool chunking, huge-page devices, TCM synchronization, thread binding, and callbacks are revision-sensitive.

## Open questions

- Prove every worker path releases acquired TCM state, including errors and threadpool destruction.
- Audit process-level Spine pool manager and mapped-chunk shutdown order.
- Add ASan/LSan and repeated threadpool/TCM teardown tests on supported hardware.
- Document null readback/copy and 2-D transfer behavior.
- Measure repacked and padded memory expansion, including MoE `MUL_MAT_ID` tensors.

## Validation

Repository writes were made on `automation/backend-teardown-audit-method`. Local cloning again failed with `Could not resolve host: github.com`; local validators, strict MkDocs build, and `check_site.sh` remain blocked. GitHub Actions and Pages are checked after durable context updates.

## Next priority

Finish the complete pinned OpenCL teardown audit. In parallel, add a cross-implementation CPU extra-buffer comparison and destruction test plan covering repack, AMX, KleidiAI, and SpacemiT.
