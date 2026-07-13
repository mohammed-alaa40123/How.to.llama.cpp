# Context memory implementations

- Run time: 2026-07-13 07:50 Africa/Cairo
- Scope: exact pinned inventory of concrete context-memory implementations and architecture factory decisions
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Added `docs/architecture/context-memory-implementations.md` and linked it under Architecture navigation.

The page maps:

```text
llama_model::create_memory()
→ no persistent memory
→ ordinary KV
→ iSWA
→ recurrent
→ hybrid
→ hybrid-iSWA
→ DeepSeek DSA
→ DeepSeek V4 compressed memory
→ per-batch/update context
→ apply, graph state writes, sequence operations, state I/O, and teardown
```

## Verified

- Seven concrete persistent `llama_memory_i` implementations exist at the pinned revision: `llama_kv_cache`, `llama_kv_cache_iswa`, `llama_kv_cache_dsa`, `llama_kv_cache_dsv4`, `llama_memory_recurrent`, `llama_memory_hybrid`, and `llama_memory_hybrid_iswa`.
- Each has a primary `llama_memory_context_i` implementation. DSV4 additionally has a generic raw sub-context and a non-interface compressed helper context.
- Recurrent architectures are exactly Mamba, Mamba2, RWKV6, RWKV6-Qwen2, RWKV7, and ARWKV7.
- Hybrid architectures are exactly Jamba, Falcon H1, Plamo2, Granite Hybrid, LFM2/LFM2-MoE, Nemotron H/Nemotron H MoE, Qwen3-Next, Kimi Linear, Qwen3.5, and Qwen3.5-MoE.
- DeepSeek 3.2 selects DSA; DeepSeek 4 selects DSV4.
- Attention architectures with SWA use iSWA; hybrid architectures with SWA use hybrid-iSWA.
- BERT-family encoders, embedding models, WavTokenizer decoder, and diffusion architectures listed in the factory receive `nullptr` memory.
- `apply()` is the generic interface's designated mutation boundary.
- DSV4 owns raw iSWA state, compressed CSA/HCA/LID caches, and persistent compressor-state stores.

## Interpretation

- `create_memory()` behaves as an architecture-to-state-machine compiler combining architecture, context type, SWA, offload, rollback, sharing, reuse, and layer-filter decisions.
- Composite memories coordinate child memory objects and child context plans; they are not one flat tensor layout.
- “KV cache size” cannot describe recurrent snapshots or DSV4 compressed state accurately.

## Historical

- The implementation family, architecture sets, MTP exception, DSV4 layout, rollback support, and unified-cache behavior are revision-sensitive.

## Open questions

- Which architecture graph builders downcast to each concrete context, and which state tensors they read or write.
- Runtime allocation, update graph, copy, and synchronization costs per family.
- Later fixes for DSV4 unified mode and the token-position/buffer-validity conflation noted in the pinned header.
- Exact public concurrency and serialization guarantees.

## Sources inspected

Repository context:

- complete `README.md`;
- `docs/reference/project-state.md`;
- `docs/reference/research-log.md`;
- `docs/reference/research-ledger.md`;
- latest detailed note `logs/research/2026-07-13/0649-backend-scheduler-pass-a.md`;
- current `mkdocs.yml`.

Pinned upstream source:

- `src/llama-memory.h`;
- `src/llama-model.cpp`;
- `src/llama-arch.cpp`;
- `src/llama-kv-cache.h`;
- `src/llama-kv-cache-iswa.h`;
- `src/llama-kv-cache-dsa.h`;
- `src/llama-kv-cache-dsv4.h`;
- `src/llama-memory-recurrent.h`;
- `src/llama-memory-hybrid.h`;
- `src/llama-memory-hybrid-iswa.h`.

No new external secondary source was introduced, so the research ledger was unchanged.

## Validation

- Connector-side file creation and updates succeeded.
- Re-fetch, commit status, workflow visibility, and Pages checks are performed after this note commit.
- Local strict validation is unavailable without a usable repository checkout.

## Next priority

Trace exact `llama_model` and `llama_context` declaration and reverse-destruction order, including smart-pointer cleanup, explicit synchronization, queued backend dependencies, retained mappings, model buffers, and safe application teardown.
