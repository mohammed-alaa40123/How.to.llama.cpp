# CPU AMX extra-buffer lifetime increment

- Run time: 2026-07-14 04:50 Africa/Cairo
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: one optional CPU extra-buffer implementation, AMX

## Startup and inspection

Read the complete repository README first, then project state, research log, research ledger, and the latest detailed note. Inspected the active PR branch, MkDocs navigation, the reusable teardown worksheet, the CPU repack comparison page, and pinned `ggml/src/ggml-cpu/amx/amx.cpp`.

## Artifact

Added `docs/architecture/cpu-amx-extra-buffer-lifetime.md` and linked it after the CPU repack audit.

## Verified

- AMX is compiled only with `__AMX_INT8__` and `__AVX512VNNI__`; runtime buffer-type publication is gated by AMX tile-permission initialization.
- AMX allocates a dedicated aligned host allocation and stores it in `buffer->context`.
- The AMX buffer interface owns base lookup, tensor initialization, weight conversion/set, clear, and allocation release.
- `tensor->extra` points to a function-static AMX `tensor_traits` object.
- The AMX buffer type and its `extra_buffer_type` context are function-static/process-lifetime state.
- AMX dispatch remains inside synchronous ordinary CPU graph computation and introduces no independent queue or scheduler event.
- Buffer destruction does not dereference `ggml_backend_cpu_context`.

## Interpretation

AMX differs from the repack overlay because it owns a dedicated allocation and full buffer interface. Its teardown remains backend-wrapper-independent because the allocation owner is the buffer object and the dispatch metadata is static.

## Historical

The result is pinned. AMX admission, tile permission, supported formats, allocation APIs, and traits are platform- and revision-sensitive.

## Open questions

- Validate the `ggml_aligned_malloc()` plus `free()` allocator pairing on every supported platform, especially Windows.
- Test repeated AMX initialization across worker threads.
- Clarify intentionally unsupported `get_tensor` and `cpy_tensor` paths.
- Add ASan/LSan backend-free-before-buffer-free tests on AMX-capable hardware.

## Validation

Repository writes were made on `automation/backend-teardown-audit-method`. Local cloning still fails with `Could not resolve host: github.com`; local Python tests, strict MkDocs build, and `check_site.sh` therefore remain blocked. GitHub Actions and Pages are checked after durable context updates.

## Next priority

Finish the OpenCL teardown audit when complete source access becomes searchable; otherwise continue the optional CPU series with KleidiAI.