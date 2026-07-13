# SYCL backend teardown increment

- Run time: 2026-07-13 15:49 Africa/Cairo
- Scope: backend free, queue completion, context members, scheduler event/buffer independence, and backend-before-scheduler classification
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Added `docs/architecture/sycl-backend-teardown.md` and linked it under Architecture navigation.

## Verified

- `ggml_backend_sycl_free()` deletes the per-backend context and generic wrapper without an explicit queue wait.
- `ggml_backend_sycl_synchronize()` waits on `stream(device, 0)`, but backend free does not call it.
- Async tensor set/get submit queue copies without waiting; graph compute can submit kernels or an executable SYCL command graph and return without a host wait.
- `ggml_backend_sycl_context` borrows device-manager default-queue pointers and owns pools, scratchpads, flash-attention buffers, and an optional executable graph through members.
- Scheduler events own independent `sycl::event` objects; event free ignores the device parameter and does not dereference the deleted backend context.
- Ordinary scheduler buffers retain a buffer-local device id, allocation pointer, default-queue pointer, tensor extras, and USM-system flag. Their deleter does not use the backend context.
- Buffer-type objects are function-static arrays whose contexts point to device-manager default queues.

## Interpretation

- Backend-before-scheduler destruction is structurally independent for ordinary SYCL events and buffers.
- Queued-work completion remains conditional because backend free does not establish an explicit completion boundary before destroying context-owned pools, scratchpads, graph state, and related resources.
- The pinned SYCL result is therefore closer to CUDA than to Metal or Vulkan.

## Historical

- Queue ownership, command-graph support, async allocation extensions, DNNL integration, Level Zero behavior, and split-buffer paths are revision- and compiler-sensitive.

## Open questions

- Whether every supported SYCL runtime gives a portable implicit-wait guarantee when pools, command graphs, USM allocations, or queue-related objects are destroyed.
- Whether waiting only on queue 0 covers all multi-device, split-buffer, DNNL, flash-attention, and communication paths.
- Whether backend free should wait on every referenced device-manager queue.
- Whether immediate-context-destruction regression tests exist or should be added.

## Sources inspected

Repository context:

- complete `README.md`;
- `docs/reference/project-state.md`;
- `docs/reference/research-log.md`;
- `docs/reference/research-ledger.md`;
- latest detailed note `logs/research/2026-07-13/1450-vulkan-backend-teardown.md`;
- current `mkdocs.yml`.

Pinned upstream source:

- `ggml/src/ggml-sycl/ggml-sycl.cpp`;
- `ggml/src/ggml-sycl/common.hpp`;
- prior generic scheduler and backend teardown audits.

No new external secondary source passed the verification bar, so the research ledger was unchanged.

## Validation

- Connector-side source inspection confirmed the free path, explicit synchronize callback, asynchronous submission paths, queue-pointer ownership, event independence, and buffer-local release state.
- Local validation was attempted, but cloning failed with `Could not resolve host: github.com`.
- GitHub Actions and Pages checks are performed after this note; exact results or blockers are recorded in project state and README TODOs.

## Next priority

Audit the pinned RPC backend teardown and transport/worker lifetime, then classify backend-before-scheduler destruction.
