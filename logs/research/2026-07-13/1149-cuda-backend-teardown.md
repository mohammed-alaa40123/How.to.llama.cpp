# CUDA backend teardown audit

- Run time: 2026-07-13 11:49 Africa/Cairo
- Scope: CUDA backend wrapper destruction, stream/event/graph-resource lifetime, scheduler event and buffer independence, and backend-before-scheduler classification
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Added `docs/architecture/cuda-backend-teardown.md` and linked it under Architecture navigation.

## Verified

- `ggml_backend_cuda_free()` deletes the CUDA context and then the backend wrapper.
- The CUDA context destructor waits for graph capture to finish, then destroys its copy event, created streams, and cuBLAS handles.
- The graph-capture wait is not a general stream synchronization call.
- CUDA graph compute returns after enqueueing kernels or launching a CUDA graph; it does not synchronize the stream.
- `ggml_backend_cuda_synchronize()` synchronizes the current CUDA context stream.
- CUDA scheduler events are device-interface objects that own their own `cudaEvent_t`; their free callback does not access `ggml_backend_cuda_context`.
- CUDA registry and device objects are process-lifetime static registry state.
- CUDA scheduler buffers own a buffer context containing the device id and pointer; their free callback reaches `cudaFree` without using the backend wrapper.
- CUDA buffer types are static per-device registry objects.
- Context members such as pools, concurrent-event maps, and CUDA graph maps are destroyed after the destructor body, after the explicit stream-destruction loop.

## Interpretation

- Backend-before-scheduler destruction is structurally independent for ordinary CUDA scheduler events and buffers: later scheduler deleters retain the device/interface or buffer context they need.
- Queued-work completion is not fully proven by the llama.cpp source because the backend destructor does not explicitly synchronize before destroying streams and later releasing context-owned resources.
- Explicit synchronization before context destruction remains the clearest portable application rule.

## Historical

- CUDA graph storage, concurrent-stream optimization, VMM pools, copy-event ownership, stream count, and registry lifetime are revision-sensitive.
- HIP and MUSA builds share source but may have different runtime destruction guarantees.

## Open questions

- Whether every supported CUDA, HIP, and MUSA runtime safely handles the pinned stream/event/graph/allocation destruction order with queued work.
- Whether all lazily created concurrent streams are covered by the current single-stream synchronize callback.
- Whether pools, concurrent events, and CUDA graph maps should be cleared before stream destruction.
- Whether tests submit asynchronous CUDA work and immediately destroy `llama_context`.

## Sources inspected

Repository context:

- complete `README.md`;
- `docs/reference/project-state.md`;
- `docs/reference/research-log.md`;
- `docs/reference/research-ledger.md`;
- latest detailed note `logs/research/2026-07-13/1050-cpu-backend-teardown.md`;
- current `mkdocs.yml`.

Pinned upstream source:

- `ggml/src/ggml-cuda/ggml-cuda.cu`;
- `ggml/src/ggml-cuda/common.cuh`;
- `ggml/src/ggml-backend.cpp` through the prior scheduler teardown audit.

No new external secondary source passed the verification bar, so the research ledger was unchanged.

## Validation

- Connector-side inspection confirmed the backend free path, context destructor, asynchronous compute interface, explicit synchronize callback, device-event callbacks, static registry/device/buffer-type lifetime, and buffer `cudaFree` path.
- New page and navigation entry were written through the repository API.
- Local validation remains blocked because the execution environment cannot resolve `github.com` and has no usable checkout.
- GitHub Actions and Pages checks are performed after the context updates; exact results or blockers are recorded in project state and README TODOs.

## Next priority

Audit Metal teardown: command queues/buffers, shared/private allocations, event/fence objects, autorelease/Objective-C ownership, synchronization, and backend-before-scheduler safety.
