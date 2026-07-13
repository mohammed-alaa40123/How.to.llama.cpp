# CANN backend teardown increment

- Run time: 2026-07-13 17:51 Africa/Cairo
- Scope: backend/context free, device and stream synchronization, events, allocator buffers, registry lifetime, and backend-before-scheduler classification
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Added `docs/architecture/cann-backend-teardown.md` and linked it under Architecture navigation.

## Verified

- `ggml_backend_cann_free()` calls `aclrtSynchronizeDevice()`, then `aclrtResetDevice(cann_ctx->device)`, then deletes the CANN context and backend wrapper.
- The public CANN synchronize callback waits only on the context default stream, while backend free uses a device-wide completion call.
- The CANN context owns up to eight lazy streams, an optional copy event, a memory pool, rope and tensor caches, and optional ACL graph-cache state.
- The context destructor destroys copy-event and stream handles; C++ member destruction later releases graph/cache/pool allocations.
- The CANN pool interface explicitly warns that operators are asynchronous and allocations must remain valid until completion.
- Scheduler CANN events own independent `aclrtEvent` handles and use a registry device object rather than the per-backend context.
- Scheduler CANN buffers own buffer-local device pointers and free them through their own context.
- CANN registry/device objects are function-static process state and outlive individual backend wrappers.
- The current upstream file inspected on 2026-07-13 retains the same reset-before-context-delete order as the pinned baseline.

## Interpretation

- Device-wide synchronization establishes a queued-work completion boundary before teardown.
- Backend-before-scheduler destruction is structurally independent for ordinary event and buffer objects.
- The pinned order is still teardown-order conditional because the device is reset before context and scheduler destructors later call `aclrtDestroyEvent`, `aclrtDestroyStream`, and `aclrtFree`.
- Source inspection alone cannot prove whether those calls are valid, redundant, or invalid after `aclrtResetDevice()`.
- CANN therefore differs from Metal/Vulkan: it explicitly synchronizes, but its device-reset placement introduces a separate resource-validity question.

## Historical

- The reset-before-context-delete order remains present in the current upstream file inspected during this run.
- Graph mode, stream count, event flags, allocator policy, and reset semantics are CANN-version-sensitive.

## Open questions

- What exact lifecycle guarantees does the supported CANN runtime provide after `aclrtResetDevice()`?
- Does reset destroy or invalidate streams, events, and allocations?
- Should context-owned resources be destroyed before reset?
- Can scheduler events and buffers safely release ACL resources after backend free reset the device?
- Does freeing one backend disrupt another backend instance using the same device?
- Which tests cover one versus multiple CANN contexts and immediate graph-compute → teardown?

## Sources inspected

Repository context:

- complete `README.md`;
- `docs/reference/project-state.md`;
- `docs/reference/research-log.md`;
- `docs/reference/research-ledger.md`;
- latest detailed note `logs/research/2026-07-13/1649-rpc-backend-teardown.md`;
- current `mkdocs.yml`.

Pinned upstream source:

- `ggml/src/ggml-cann/ggml-cann.cpp`;
- `ggml/src/ggml-cann/common.h`.

Current upstream comparison:

- `ggml/src/ggml-cann/ggml-cann.cpp` on the default branch, inspected 2026-07-13.

Official CANN documentation searches did not return a directly accessible authoritative contract for post-reset resource destruction in this environment, so no new ledger item was added.

## Validation

- Connector-side source inspection confirmed the free, synchronization, event, buffer, context-member, and registry paths.
- Local clone and command validation failed because the execution environment could not resolve `github.com`.
- GitHub Actions and Pages checks are performed after this note; exact results or blockers are recorded in project state and README TODOs.

## Next priority

Audit pinned OpenCL teardown and optional CPU extra-buffer implementations, while separately creating a CANN runtime test plan for reset-before-resource-destruction.