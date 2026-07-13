# Runtime context and memory Pass A

- Run time: 2026-07-13 03:50 Africa/Cairo
- Scope: bounded file-by-file inventory of runtime context and polymorphic memory
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Added `docs/architecture/runtime-context-memory-pass-a.md` and linked it under Architecture navigation.

The page maps:

- `src/llama-context.cpp` and `.h`;
- `src/llama-memory.cpp` and `.h`;
- `src/llama-kv-cache.cpp` and `.h`;
- recurrent and specialized/hybrid memory implementations.

It includes construction and ownership, batch-to-ubatch memory planning, KV slot allocation, recurrent/hybrid variants, sequence mutation, state I/O, thread pools, synchronization, reset, teardown, backend/OS variants, and truth labels.

## Verified

- `llama_context` stores a non-owning reference to `llama_model` and owns mutable runtime resources.
- Context members include the memory module, scheduler, runtime backends, output buffer, graph-result caches, batch allocator, and optional per-sequence device-memory copies.
- Construction initializes device, accelerator, and CPU backends, records supported thread-control hooks, reserves output storage, and calls `model.create_memory()`.
- `llama_memory_i` defines `init_batch()`, `init_full()`, `init_update()`, sequence mutation, memory accounting, and state serialization.
- `llama_memory_context_i` yields ubatches and makes `apply()` the designated state-mutation boundary.
- `llama_kv_cache` separates cell/sequence metadata from K/V tensors allocated in backend buffers.
- `slot_info` maps tokens and streams to concrete KV-cell indices before execution.
- Cache shifts and stream copies can require a backend memory-update graph and synchronization.
- Recurrent and hybrid memory use the same interface but do not share the ordinary KV ring's exact storage/update semantics.

## Interpretation

- The temporary memory context behaves like a transaction plan for one logical batch.
- Context memory is a polymorphic subsystem; “the KV cache” is not a sufficient universal model.
- Graph submission success does not by itself guarantee host-visible output or safely serializable state.
- Model mmap/page-cache behavior and context-owned KV/recurrent storage are independent lifetimes.

## Historical

- Unified and multi-stream KV, iSWA, recurrent/hybrid memory, specialized architecture caches, graph reuse, and backend output handling are revision-sensitive.

## Open questions

- Enumerate every concrete memory implementation and map architectures to constructors.
- Confirm exact reverse-destruction dependencies with failure-injection tests.
- Find the strongest upstream contract for sharing a model across contexts and concurrent access to one context.
- Measure memory allocation, update graphs, scheduler copies, waits, host state-save costs, and teardown.

## Sources inspected

Repository context:

- complete `README.md`;
- `docs/reference/project-state.md`;
- `docs/reference/research-log.md`;
- `docs/reference/research-ledger.md`;
- latest detailed note `logs/research/2026-07-13/0251-model-gguf-loader-pass-a.md`;
- current `mkdocs.yml`.

Pinned upstream:

- `src/llama-context.cpp` and `.h`;
- `src/llama-memory.cpp` and `.h`;
- `src/llama-kv-cache.cpp` and `.h`;
- recurrent and specialized memory headers/source.

No new external secondary source was introduced, so the research ledger remained unchanged.

## Validation

Repository writes and connector-side re-fetch are the durable validation available in this environment.

A local clone failed with:

```text
fatal: unable to access 'https://github.com/mohammed-alaa40123/How.to.llama.cpp.git/': Could not resolve host: github.com
```

Therefore the local validation suite and `mkdocs build --strict` could not run. CI and Pages were checked after publication; unavailable connector/browser results are recorded as blockers rather than interpreted as failures.

## Next priority

Synthesize the completed public API, loader/model, context, and memory Pass A groups into one subsystem relationship map with creation, decode, mutation, output, synchronization, and teardown paths.
