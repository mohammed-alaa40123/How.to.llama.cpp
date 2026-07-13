# Ordinary CPU backend teardown audit

- Run time: 2026-07-13 10:50 Africa/Cairo
- Scope: CPU backend free path, synchronous execution, event/device lifetime, scheduler-buffer independence, and backend-before-scheduler classification
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Added `docs/architecture/cpu-backend-teardown.md` and linked it under Architecture navigation.

## Verified

- `ggml_backend_cpu_graph_compute()` builds a CPU plan and calls `ggml_graph_compute()` directly.
- The CPU backend interface has null async tensor operations, null asynchronous copy, null synchronize, and null event record/wait entries.
- The CPU device advertises `async = false` and `events = false`.
- CPU device event creation, destruction, and synchronization callbacks are null.
- The CPU registry returns a function-local static device object and static device context.
- `ggml_backend_cpu_free()` deletes the work allocation, CPU backend context, and backend wrapper only.
- Generic scheduler-buffer destruction invokes buffer callbacks and does not call through the deleted CPU backend wrapper.

## Interpretation

- There is no queued CPU device work remaining after the CPU graph-compute callback returns.
- The scheduler creates no CPU events and therefore cannot require the deleted CPU backend context while freeing events.
- Ordinary CPU scheduler buffers remain independently destructible after the CPU backend wrapper is deleted.
- Backend-before-scheduler destruction is verified safe for the ordinary CPU backend at the pinned revision.

## Historical

- CPU async/event support, buffer types, optional optimized buffer implementations, and registry lifetime are revision-sensitive.

## Open questions

- Whether AMX, KleidiAI, repack, HBM, BLAS, and other optional CPU-adjacent buffer implementations preserve backend-independent destruction.
- Whether sanitizer coverage explicitly exercises backend-first CPU scheduler destruction.

## Sources inspected

Repository context:

- complete `README.md`;
- `docs/reference/project-state.md`;
- `docs/reference/research-log.md`;
- `docs/reference/research-ledger.md`;
- latest detailed note `logs/research/2026-07-13/0949-scheduler-core-teardown.md`;
- `docs/architecture/scheduler-teardown-core.md`;
- current `mkdocs.yml`.

Pinned upstream source:

- `ggml/src/ggml-cpu/ggml-cpu.cpp`;
- `ggml/src/ggml-backend.cpp`.

No new external secondary source was introduced, so the research ledger was unchanged.

## Validation

- Connector-side source inspection confirmed the CPU free path, synchronous compute callback, null async/synchronize/event interface entries, static device lifetime, and generic buffer-free path.
- New page, navigation, README TODO, project-state, and research-log updates were written through the repository API.
- Local command validation is unavailable because this environment has no usable checkout.
- GitHub Actions and Pages verification are performed after this note commit; exact results or blockers are recorded in project state and TODOs.

## Next priority

Audit CUDA backend teardown: context destruction, stream and CUDA graph resources, event destruction, buffer deallocation, device/buffer-type lifetime, implicit synchronization, and queued-work safety.
