# Model and context teardown order

- Run time: 2026-07-13 08:50 Africa/Cairo
- Scope: exact declaration order, reverse C++ destruction, RAII ownership, queued-work caveats, and safe public teardown
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Added `docs/architecture/model-context-teardown-order.md` and linked it under Architecture navigation.

## Verified

- `llama_model::~llama_model()` explicitly deletes each pointer in `loras`.
- Model storage ownership is concentrated in `llama_model::impl`: retained mappings, mapping/buffer locks, GGML metadata contexts, and backend buffers.
- `impl` reverse destruction releases `ctxs_bufs` before lock objects and retained mappings.
- Each `ctxs_bufs` pair destroys the backend-buffer vector before the GGML context.
- `llama_context` borrows `llama_model`; attached thread pools are also borrowed.
- `llama_context::~llama_context()` inspects scheduler buffer sizes and calls `ggml_opt_free(opt_ctx)`.
- The context destructor body does not explicitly synchronize queued work and does not explicitly reset the scheduler.
- Reverse declaration order releases `mem_storage`, `buf_output`, graph results, backend metadata, and owning `backends` before `sched`; persistent memory and adapters are released later.
- Constructor failure only unwinds fully constructed members; the complete class destructor body is not called when construction did not finish.

## Interpretation

- Model `pimpl` is an RAII capsule that keeps retained mappings alive until model buffers and tensor metadata are gone.
- Explicit application synchronization before context destruction is the clearest portable completion boundary for accelerator work.
- Logit and embedding pointers are borrowed views whose lifetime ends no later than output-buffer/context destruction.

## Historical

- Member order, scheduler ownership, backend deleters, and synchronization behavior are revision-sensitive.

## Open questions

- Does `ggml_backend_sched_free` require live backend instances while freeing events, buffers, or copy slots?
- Which concrete backend frees synchronize implicitly?
- Is the pinned `backends`-before-`sched` reverse order deliberately safe or an untested lifetime hazard?
- Are there tests for destroying a context immediately after asynchronous compute?

## Sources inspected

Repository context:

- complete `README.md`;
- `docs/reference/project-state.md`;
- `docs/reference/research-log.md`;
- `docs/reference/research-ledger.md`;
- latest detailed note `logs/research/2026-07-13/0750-context-memory-implementations.md`;
- current `mkdocs.yml`.

Pinned upstream source:

- `src/llama-model.h`;
- `src/llama-model.cpp`;
- `src/llama-context.h`;
- `src/llama-context.cpp`.

No new external secondary source was introduced, so the research ledger was unchanged.

## Validation

- Connector-side page creation, navigation update, README update, project-state update, and research-log update succeeded.
- Local strict validation remains blocked because the execution environment cannot resolve `github.com` and has no usable checkout.
- CI and Pages checks are performed after this note commit; exact blockers are recorded in project state and TODOs if verification is unavailable.

## Next priority

Trace `ggml_backend_sched_free`, scheduler event/buffer deleters, and concrete backend destruction to resolve whether the pinned context member order safely destroys owning backend wrappers before the scheduler.
