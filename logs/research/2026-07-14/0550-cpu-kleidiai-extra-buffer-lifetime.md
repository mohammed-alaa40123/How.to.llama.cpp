# CPU KleidiAI extra-buffer lifetime increment

- Run time: 2026-07-14 05:50 Africa/Cairo
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: one optional CPU extra-buffer implementation, KleidiAI

## Startup and inspection

Read the complete repository README first, then project state, research log, research ledger, and the latest detailed AMX note. Inspected the active PR branch, MkDocs navigation, CPU repack and AMX audits, and pinned `ggml/src/ggml-cpu/kleidiai/kleidiai.cpp`.

## Artifact

Added `docs/architecture/cpu-kleidiai-extra-buffer-lifetime.md` and linked it after the AMX audit.

## Verified

- KleidiAI initialization is protected by the GGML critical section and process-static state.
- Allocation delegates to the ordinary CPU buffer type; KleidiAI replaces only the buffer type plus tensor initialization/upload callbacks and retains the ordinary CPU free callback.
- `tensor->extra` points to a function-static KleidiAI trait object.
- The extra-buffer type and buffer-type metadata are function-static.
- Q4_0/Q8_0 upload synchronously builds versioned packed slots and falls back to the original representation when no slot is available.
- Supported execution is limited to compatible `MUL_MAT` and `GET_ROWS` cases and remains in synchronous CPU graph computation.
- Buffer destruction does not require `ggml_backend_cpu_context`.

## Interpretation

KleidiAI is teardown-equivalent to the CPU repack overlay for backend-wrapper ownership, but has a richer packed representation and process-global feature/kernel policy. Ordinary CPU allocation ownership plus static metadata makes later buffer destruction independent of the deleted CPU backend wrapper.

## Historical

The conclusion is pinned. CPU-feature detection, SME policy, kernel chains, packed-header format, fallback behavior, and callbacks are revision-sensitive.

## Open questions

- Add ASan/LSan backend-free-before-buffer-free tests.
- Document null `get_tensor` and `cpy_tensor` behavior.
- Test concurrent initialization and global-context publication.
- Measure memory expansion from one versus two packed slots.
- Verify packed-layout portability assumptions across machines and feature sets.

## Validation

Repository writes were made on `automation/backend-teardown-audit-method`. Local cloning still fails with `Could not resolve host: github.com`; local validators, strict MkDocs build, and `check_site.sh` remain blocked. GitHub Actions and Pages are checked after durable context updates.

## Next priority

Finish the OpenCL teardown audit when complete source access becomes searchable; otherwise audit SpacemiT IME, the last remaining optional CPU extra-buffer path in the current series.
