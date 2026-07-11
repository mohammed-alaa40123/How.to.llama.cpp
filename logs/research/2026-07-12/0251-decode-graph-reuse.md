# Decode and graph-reuse trace

- Run time: 2026-07-12 02:51 Africa/Cairo
- Upstream baseline: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: `llama_decode` through scheduler submission; scheduler split internals intentionally deferred

## Verified

- `llama_decode()` delegates directly to `llama_context::decode()`.
- `decode()` initializes the batch allocator, reserves scheduler capacity, applies pending memory updates, initializes a memory batch context, and invokes `process_ubatch()` for each micro-batch.
- `process_ubatch()` reuses the previous graph only when graph reuse is enabled and every graph-result/input compatibility check accepts the new graph parameters.
- Pipeline-parallel reuse synchronizes before rewriting input tensors because the preceding asynchronous GPU execution may still read them.
- The rebuild branch resets graph/scheduler state, calls `model.build_graph()`, and calls `ggml_backend_sched_alloc_graph()`.
- `graph_compute()` selects batch versus single-token CPU threadpool/thread count and submits through `ggml_backend_sched_graph_compute_async()`.
- Reservation and allocation are distinct: reserve plans backend buffer capacity; alloc binds one concrete rebuilt graph.

## Interpretation

Graph reuse is a topology-and-shape cache. It does not reuse token values or outputs. Inputs are rewritten for every micro-batch, while compatible graph structure and allocations survive.

## Open question

Trace `ggml_backend_sched_graph_compute_async()` through split creation, cross-backend copies/events, synchronization, and backend execution.

## Artifact

- `docs/lifecycle/decode-graph-reuse.md`
- `mkdocs.yml`

## Evidence

- `src/llama-context.cpp`: `llama_decode`, `llama_context::decode`, `process_ubatch`, `graph_reserve`, `graph_params`, `graph_compute`
- `src/llama-graph.h/.cpp`: graph-input compatibility checks
