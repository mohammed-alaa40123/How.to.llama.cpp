# CPU repack extra-buffer lifetime increment

- Run time: 2026-07-14 03:51 Africa/Cairo
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: one optional CPU extra-buffer implementation, `GGML_USE_CPU_REPACK`

## Startup and inspection

Read the complete repository README first, then project state, research log, research ledger, and the latest detailed note. Inspected the active PR branch, MkDocs navigation, the reusable teardown worksheet, and pinned `ggml-cpu.cpp`, `traits.h`, `traits.cpp`, and `repack.cpp`.

## Artifact

Added `docs/architecture/cpu-repack-extra-buffer-lifetime.md` and linked it after the ordinary CPU teardown page.

## Verified

- CPU extra-buffer types are collected in a function-static registry.
- The repack buffer type and its `extra_buffer_type` context are function-static/process-lifetime state.
- Repack allocation delegates to the ordinary CPU buffer type, then overrides selected tensor callbacks; it does not replace the ordinary free callback.
- `tensor->extra` points to function-static repack trait objects.
- CPU graph execution is synchronous and the backend exposes no async tensor, synchronize, or event callbacks.
- `ggml_backend_cpu_free()` owns only backend work data, the CPU backend context, and the generic wrapper.

## Interpretation

For audited repack allocations, buffer destruction and trait lookup are independent of `ggml_backend_cpu_context`; command completion follows the ordinary synchronous CPU contract. This does not automatically classify AMX, KleidiAI, or SpacemiT IME.

## Historical

The classification is pinned. Newer revisions may change allocation callbacks, trait ownership, or execution behavior.

## Open questions

- Audit AMX, KleidiAI, and SpacemiT IME with the same worksheet.
- Add ASan/LSan destruction tests that free the CPU backend wrapper before repack buffers.
- Decide whether process-lifetime extra-buffer contexts need an explicit shutdown policy.

## Validation

Repository writes were made on `automation/backend-teardown-audit-method`. Local checkout validation remains blocked by DNS failure resolving `github.com`. GitHub Actions and Pages were checked after the context updates.

## Next priority

Finish the pinned OpenCL teardown audit when complete source access is available; otherwise continue the optional CPU extra-buffer series with AMX.
