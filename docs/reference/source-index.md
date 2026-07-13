# Initial source index

**Pinned upstream revision:** `e3546c7948e3af463d0b401e6421d5a4c2faf565`

This hand-reviewed index is the seed for an automatically generated full inventory.

## Top-level execution chain

| Stage | Public/visible entry | Deeper implementation targets |
|---|---|---|
| Backend discovery | `ggml_backend_load_all` | backend registry, dynamic loading, device registration |
| Model load | `llama_model_load_from_file` | `llama_model_load_from_file_impl`, `llama_model_load`, `llama_model_loader` |
| Architecture creation | internal model factory | architecture-specific `llama_model_*` subclasses |
| Model state load | model load methods | hparams, vocab, stats, tensors, placement/buffer types |
| Context create | `llama_init_from_model` | `llama_context` constructor, backend init, memory, scheduler reserve |
| Batch | `llama_batch_get_one` | batch allocator and microbatch construction |
| Decode | `llama_decode` | `llama_context::decode`, `process_ubatch` |
| Graph | model `build_graph` | architecture graph builder, memory context, output selection |
| Schedule | scheduler graph compute | backend assignment, splits, galloc, copy tensors, events |
| Execute | backend graph compute | CPU plan/thread pool/kernels or accelerator queues/kernels |
| Sample | `llama_sampler_sample` | sampler chain, logits access, token selection |

## High-priority files

| Path | Why it matters | Review status |
|---|---|---|
| `examples/simple/simple.cpp` | Minimal executable lifecycle | First pass complete |
| `include/llama.h` | Public API and core types | Pending |
| `src/llama.cpp` | Public API implementation and model-loading entry | First pass started |
| `src/llama-model-loader.cpp` | GGUF metadata/tensor loading | Pending deep read |
| `src/llama-model.cpp` / `.h` | Model object, architecture dispatch, graph entry | Pending deep read |
| `src/llama-context.cpp` / `.h` | Context creation, decode, graph lifecycle | Pending deep read |
| `src/llama-memory*` | KV/recurrent/hybrid memory | Pending |
| `src/llama-graph*` | Graph helper abstractions | Pending |
| `ggml/include/ggml.h` | Tensor/op/graph definitions | Pending |
| `ggml/src/ggml.c` | GGML core implementation | Pending |
| `ggml/src/ggml-alloc.c` | Graph allocator | Pending |
| `ggml/src/ggml-backend.cpp` | Backend abstraction and scheduler | First pass started |
| `ggml/include/ggml-cpu.h` | CPU plan/thread-pool API | Pending deep read |
| `ggml/src/ggml-cpu/` | CPU graph compute and kernels | Pending deep read |
| backend directories | Device-specific buffers, queues, kernels | Pending per backend |

## Generated symbol locations

`scripts/index_upstream.py` now emits two symbol views for every indexed source file:

- `symbols`: the original compact, deduplicated name list retained for compatibility;
- `symbol_locations`: an untruncated source-ordered list containing approximate symbol `name`, declaration `kind`, and 1-based `line`.

This makes very large translation units such as `ggml-opencl.cpp` navigable by symbol and source location without pretending to provide a compiler-grade call graph. Duplicate names are intentionally retained in `symbol_locations` because overloads and conditional-compilation branches can produce several useful navigation targets.

## Generated index limitations

`scripts/index_upstream.py` intentionally produces an approximate source inventory. Regex-detected symbols, line locations, and include relationships are useful navigation aids, but cannot resolve:

- preprocessor configurations;
- overloaded functions and templates;
- virtual dispatch;
- function pointers/backend interfaces;
- generated sources;
- platform-specific compilation;
- runtime plugin registration.

Human-reviewed call chains remain the source of documentation truth.
