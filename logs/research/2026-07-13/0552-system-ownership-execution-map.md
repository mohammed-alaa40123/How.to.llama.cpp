# System ownership and execution synthesis

- Run time: 2026-07-13 05:52 Africa/Cairo
- Scope: bounded cross-subsystem synthesis of the three completed Pass A groups and canonical model/context/memory pages
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Added `docs/architecture/system-ownership-and-execution-map.md` and linked it under Architecture navigation.

The page connects:

```text
public API and application ownership
→ temporary GGUF/model loader state
→ publication into llama_model
→ non-owning model reference from llama_context
→ context-owned KV/recurrent/hybrid memory
→ per-batch memory planning and apply boundary
→ architecture graph construction or compatible reuse
→ scheduler assignment, splits, dependency copies, and events
→ backend execution
→ output visibility and sampling
→ synchronization and teardown
```

## Verified

- The application owns returned model, context, and sampler handles.
- The loader owns temporary parse, file, mapping, staging, and partial-allocation state until successful publication.
- `llama_model` owns persistent architecture/vocabulary state, weight tensors, backend buffers, and retained mappings.
- `llama_context` borrows the model and owns mutable execution state, scheduler resources, outputs, and polymorphic memory.
- `llama_memory_context_i::apply()` is the documented mutation boundary between candidate per-batch planning and committed state changes.
- Scheduler-managed split graphs, copy destinations, and events have lifetimes distinct from model weights and context sequence memory.
- Context destruction must precede model destruction.

## Interpretation

- `llama_model_loader` is a transactional publisher.
- `llama_context` is a mutable execution session around a borrowed persistent model, not a second model copy.
- The scheduler is an execution planner and owner of scheduling resources rather than the persistent owner of weights or sequence state.
- The per-batch memory context behaves like a transaction plan.
- Ownership, virtual addressability, physical residency, destination allocation, data validity, and command completion must be measured separately.

## Historical

- API fields, memory implementations, graph-reuse predicates, scheduler split/copy logic, backend event behavior, and architecture mappings are revision-sensitive.
- Historical scheduler PRs remain useful for rationale but cannot replace pinned source behavior.

## Open questions

- Exact reverse member-destruction order in `llama_model` and `llama_context`.
- Strongest public contract for model sharing, context concurrency, and output synchronization.
- Complete architecture-to-`llama_memory_i` mapping.
- Destination-copy validity and invalidation across graph reuse.
- Runtime evidence separating page faults, reads, uploads, scheduler copies, event waits, memory-update graphs, output synchronization, and teardown.

## Sources inspected

Repository context:

- complete `README.md`;
- `docs/reference/project-state.md`;
- `docs/reference/research-log.md`;
- `docs/reference/research-ledger.md`;
- latest detailed note `logs/research/2026-07-13/0350-runtime-context-memory-pass-a.md`;
- current `mkdocs.yml`;
- current public API, loader, and runtime-context Pass A pages.

Pinned upstream source links used in the artifact:

- `examples/simple/simple.cpp`;
- `include/llama.h`;
- `src/llama.cpp`;
- `src/llama-model-loader.cpp`;
- `src/llama-model.cpp`;
- `src/llama-context.cpp`;
- `src/llama-memory.h`;
- `src/llama-kv-cache.cpp`;
- `ggml/src/ggml-backend.cpp`.

No new external secondary source was introduced, so `docs/reference/research-ledger.md` remained unchanged.

## Validation

- Repository writes succeeded.
- Connector-side re-fetch confirmed the new page, pinned baseline, ownership diagram, ownership table, construction path, encode/decode sequence, scheduler boundary, memory-state distinctions, teardown order, source map, and truth labels.
- The available commit-workflow lookup returned no runs for the research-log commit; that endpoint filters to pull-request-triggered runs and cannot verify push-triggered Documentation CI, Pages, or hourly context workflows.
- Direct browser opening of the Pages root and new route was rejected by the safe-URL gate because those exact URLs were absent from prior search results.
- No local checkout was available, so the project validation commands and `mkdocs build --strict` could not be executed locally.

## Next priority

Complete file-by-file Pass A for backend scheduler internals: backend assignment, split creation, cross-backend dependencies, copy-ring destination allocation and validity, events, asynchronous submission, synchronized fallback copies, graph-allocation reuse, and teardown across CPU and accelerator backends.
