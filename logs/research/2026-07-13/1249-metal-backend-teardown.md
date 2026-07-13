# Metal backend teardown audit

- Run time: 2026-07-13 12:49 Africa/Cairo
- Scope: backend-free synchronization, Objective-C command-resource ownership, scheduler event and buffer independence, and backend-before-scheduler classification
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Added `docs/architecture/metal-backend-teardown.md` and linked it under Architecture navigation.

## Verified

- `ggml_backend_metal_free()` calls `ggml_metal_synchronize(ctx)` before `ggml_metal_free(ctx)` and before freeing the backend wrapper.
- `ggml_metal_synchronize()` waits for `cmd_buf_last`, checks graph command-buffer status, checks retained extra command-buffer status, and releases completed extra buffers.
- `ggml_metal_free()` releases graph and extra command buffers, dynamic pipelines, the retained encoding block, the dispatch queue, and the context-owned copy event after synchronization.
- The pinned backend context obtains its command queue from the Metal device and does not own or release that device queue.
- Scheduler Metal events own an independent `MTLSharedEvent`; their concrete free function releases the event and does not use the backend context.
- Shared, private, and mapped scheduler buffers carry buffer-local contexts. Their free path removes the optional residency set, releases `MTLBuffer` objects, releases owned shared host allocation when applicable, and frees the wrapper.
- Mapped buffers do not own the mapped host bytes.
- Metal device, registry, and buffer-type objects are static registry state that outlive individual backend wrappers.

## Interpretation

- Backend-before-scheduler destruction is verified safe for ordinary pinned Metal resources because backend free establishes queued-work completion and later scheduler deleters retain valid device-level dependencies.
- This is a stronger teardown contract than the pinned CUDA-family path, whose backend destructor does not explicitly synchronize all streams first.
- Unified memory, storage mode, residency, wrapper ownership, and command completion are separate states.

## Historical

- Queue ownership, backend-free synchronization, event primitives, residency sets, shared/private defaults, and registry lifetime are revision-sensitive.

## Open questions

- Whether tests submit asynchronous Metal graph/copy/event work and immediately destroy `llama_context` under Metal API validation.
- Whether command-buffer failures discovered during final backend-free synchronization should be propagated more explicitly.
- Whether plugin unload ordering can invalidate static device state before outstanding scheduler resources in unusual embedding scenarios.
- Whether residency-set removal has measurable shutdown cost for very large mapped models.

## Sources inspected

Repository context:

- complete `README.md`;
- `docs/reference/project-state.md`;
- `docs/reference/research-log.md`;
- `docs/reference/research-ledger.md`;
- latest detailed note `logs/research/2026-07-13/1149-cuda-backend-teardown.md`;
- current `mkdocs.yml`;
- existing `docs/lifecycle/metal-backend-semantics.md`.

Pinned upstream source:

- `ggml/src/ggml-metal/ggml-metal.cpp`;
- `ggml/src/ggml-metal/ggml-metal-context.m`;
- `ggml/src/ggml-metal/ggml-metal-device.m`;
- prior generic scheduler and context teardown audits.

No new external secondary source passed the verification bar, so the research ledger was unchanged.

## Validation

- Connector-side inspection confirmed the backend-free synchronization path, Objective-C resource release sequence, static registry/device lifetime, event free path, and shared/private/mapped buffer free paths.
- New page, navigation entry, README TODO update, project-state update, research-log update, and this detailed note were written through the repository API.
- Local command validation remains blocked because the execution environment has no usable checkout.
- GitHub Actions and Pages checks are performed after this note; exact results or blockers are recorded in project state and README TODOs.

## Next priority

Audit Vulkan teardown: queue/device completion, command pools and buffers, fences/semaphores/events, allocator-backed buffers, synchronization, and backend-before-scheduler safety.
