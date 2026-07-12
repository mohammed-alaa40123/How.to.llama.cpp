# `llama_model`

> **Evidence scope — Verified:** llama.cpp commit [`e3546c7948e3af463d0b401e6421d5a4c2faf565`](https://github.com/ggml-org/llama.cpp/tree/e3546c7948e3af463d0b401e6421d5a4c2faf565). Claims and source links on this page describe that revision unless explicitly labelled otherwise.

`llama_model` is the long-lived, reusable representation of one loaded model. It combines architecture identity, hyperparameters, vocabulary, named GGML weight tensors, layer structures, device-placement metadata, backend buffers, retained mappings, model metadata, and architecture-specific graph construction. One model can be referenced by multiple `llama_context` instances, but every referencing context requires the model to remain alive.

## Prerequisites

- [GGUF file anatomy](../foundations/gguf-file-anatomy.md)
- [Model tensor placement](../foundations/model-tensor-placement.md)
- [`llama_context`](llama-context.md)
- [GGML graph construction and MoE](../ggml/graph-construction-and-moe.md)

## Five-minute explanation

Loading starts with `llama_model_loader`, which identifies the GGUF architecture. `llama_model_create(loader, params)` dispatches to an architecture-specific C++ subclass. The model then loads common metadata, architecture hyperparameters, vocabulary, tensor statistics, tensor metadata, placement decisions, and tensor bytes.

The resulting object is more than a collection of weights. It is the stable bridge between storage and execution:

```text
GGUF metadata and tensor descriptors
  -> architecture-specific llama_model subclass
  -> hparams, vocabulary, model-level tensors, layer tensor fields
  -> selected devices and backend buffer types
  -> model-owned backend buffers and retained mappings
  -> build_graph(params)
  -> architecture-specific build_arch_graph(params)
  -> GGML graph consumed by a llama_context scheduler
```

A context does not duplicate this model state. It holds a non-owning reference and adds mutable inference-session resources: KV or recurrent memory, scheduler state, graph reuse, outputs, CPU thread-pool attachment, and other runtime state.

## Creation and loading path

**Verified:** architecture dispatch is explicit. `llama_model_create(llama_model_loader &, params)` obtains `ml.get_arch()`, rejects an unknown architecture, and calls `llama_model_create(arch, params)`. The architecture switch constructs a concrete subclass such as `llama_model_llama`, `llama_model_olmoe`, or another registered implementation.

```text
llama_model_load_from_file(...)
  -> llama_model_loader
      -> read GGUF architecture
      -> llama_model_create(loader, params)
          -> llama_model_create(arch, params)
              -> llama_model_mapping(arch, params)
                  -> new architecture-specific llama_model_* subclass
      -> load_stats()
      -> load_hparams()
          -> load_arch_hparams()
      -> load_vocab()
      -> load_tensors()
          -> load_arch_tensors()
          -> allocate/map/read/upload tensor storage
```

Pinned source:

- [`llama_model_mapping()` and `llama_model_create()`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/src/llama-model.cpp#L41-L333)
- [`llama_model` virtual loading interface](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/src/llama-model.h#L535-L737)

**Interpretation:** this is a two-level design. Common model mechanics live in `llama_model` and `llama_model_base`; architecture subclasses supply architecture-specific hyperparameters, tensor registration, and graph construction.

## What the object contains

The public struct layout makes the major categories visible.

| Category | Representative members | Ownership and role |
|---|---|---|
| Identity | `type`, `arch`, `name` | Owned values describing model family and size/type classification |
| Architecture configuration | `hparams` | Owned parsed hyperparameters used by loading, memory selection, graph construction, and runtime validation |
| Vocabulary | `vocab` | Owned tokenizer/vocabulary state shared by contexts and public token APIs |
| Model-level tensors | `tok_embd`, `output_norm`, `output`, classifier or architecture-specific fields | Non-owning tensor pointers into model-owned GGML metadata and backing buffers |
| Per-layer tensor map | `std::vector<llama_layer> layers` | Owned layer records containing pointers to attention, FFN, MoE, recurrent, convolutional, and architecture-specific tensors |
| GGUF metadata | `gguf_kv` | Owned string metadata retained for later inspection |
| Placement | `devices`, model parameters, split state | Owned device-selection and tensor-placement metadata |
| Tensor lookup/statistics | `tensors_by_name` | Owned name-to-tensor references used by internal tooling and quantization statistics |
| Adapter association | `loras` | Tracks associated adapters; adapter objects are not implied to be model-owned by this container alone |
| Load accounting | `t_load_us`, `t_start_us` | Owned timing counters |
| Hidden implementation state | `pimpl` | Owned implementation data, including storage objects not exposed in the public member list |

**Verified:** the central declaration is [`struct llama_model`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/src/llama-model.h#L535-L693). The `layers` vector contains `llama_layer` records whose fields include dense attention/FFN tensors, MoE router and expert tensors, recurrent/SSM tensors, and architecture extensions.

## Tensor registration and layer structures

Architecture subclasses implement `load_arch_tensors()`. They call common tensor-creation helpers and assign returned `ggml_tensor *` objects into model-level fields or one element of `layers`.

For a transformer-like layer, the stable C++ object may hold pointers such as:

```text
layers[il].attn_norm
layers[il].wq / wk / wv / wo
layers[il].ffn_norm
layers[il].ffn_gate / ffn_up / ffn_down
layers[il].ffn_gate_inp
layers[il].ffn_gate_exps / ffn_up_exps / ffn_down_exps
```

These pointers are tensor metadata handles. Their bytes may be:

- aliases into a retained file mapping;
- contained in CPU-owned backend buffers;
- copied into host/shared storage;
- uploaded into accelerator-owned buffers;
- split according to model and backend configuration.

See [Model tensor placement](../foundations/model-tensor-placement.md) for the detailed branches.

**Interpretation:** `llama_layer` is a source-level architecture schema, not a runtime activation object. Its pointers identify reusable model weights. Per-token activations are created later in a GGML graph and allocated by the context scheduler.

## Buffer, mapping, and device ownership

`llama_model` owns the loaded model’s storage lifetime. Exact storage objects are managed through implementation state and RAII containers, while public tensor pointers refer into that storage.

The ownership boundary is:

```text
llama_model_loader
  temporarily owns parsing, source-file, staging, and loading machinery
      -> successful load transfers or establishes required storage
llama_model
  owns backend buffers and retained mappings needed by its tensors
llama_context
  references model tensors but owns compute, sequence-memory, and output state
OS / backend runtime
  owns lower-level physical pages, device allocations, queues, and driver resources
```

**Verified:** loading retains mappings when mapped model buffers depend on them, while temporary mappings/staging resources are released after synchronization and transfer completion.

**Interpretation:** model ownership does not guarantee physical RAM residency. A retained mmap keeps a valid virtual mapping and file association; file-backed pages can still fault in, remain in page cache, or be reclaimed by the operating system.

## Device placement and offload

The model records participating devices and exposes placement helpers such as:

- `dev_layer(il)` and `dev_output()`;
- `select_buft(il)`;
- `n_gpu_layers()` and `tensor_split()`;
- `memory_breakdown()`.

Placement is decided during model loading, before a context executes a graph. The later graph builder uses those model tensors, while the context scheduler assigns operation nodes and temporary tensors across compatible backends.

**Verified:** model tensor placement and scheduler graph placement are related but distinct:

1. the model decides where persistent weight tensors live;
2. graph construction references those tensors and creates operation/activation tensors;
3. the scheduler assigns graph nodes, allocates temporary storage, and inserts cross-backend copies when needed.

**Open question:** runtime evidence is still needed to quantify how frequently representative CPU, Metal, CUDA, Vulkan, and SYCL configurations enter mmap alias, mapped-copy, direct-read, synchronous-upload, and asynchronous-upload branches.

## Graph-builder delegation

`llama_model::build_graph(params)` is the common model-level graph entry. The architecture subclass implements `build_arch_graph(params)` and returns an architecture-specific graph context. That builder creates the layer-by-layer GGML operations and eventually expands the output dependencies into a `ggml_cgraph`.

```text
llama_context::process_ubatch()
  -> model.build_graph(graph_params)
      -> architecture-specific build_arch_graph(graph_params)
          -> reference model tensors and context inputs/memory
          -> create GGML operation tensors
          -> expand final outputs into ggml_cgraph
  -> context scheduler allocates and executes graph
```

**Verified:** the model owns architecture and weights, but the graph is built for context-provided runtime parameters and mutable memory/input state. The returned graph is not the model itself.

**Interpretation:** `llama_model` acts as a reusable graph factory. A graph-reuse hit may preserve compatible topology and allocation inside a context, but the model remains the stable source of architecture-specific construction and persistent tensors.

## Relationship to `llama_context`

| `llama_model` | `llama_context` |
|---|---|
| Long-lived and reusable | Mutable inference session |
| Owns architecture, vocabulary, weight metadata, model buffers, retained mappings | Owns scheduler, sequence memory, graph-result caches, outputs, runtime backends, and batch state |
| Determines persistent tensor placement | Determines runtime execution configuration and temporary allocation |
| Supplies `build_graph()` and `create_memory()` factories | Calls those factories and mutates their returned runtime state |
| May be shared by multiple contexts | Holds a non-owning reference to one model |

**Verified:** `llama_context` stores `const llama_model & model`. Therefore destroying the model before its contexts creates dangling references and invalid tensor/storage access.

**Interpretation:** sharing a model can avoid duplicate weight storage, but it does not make contexts or backend execution automatically thread-safe. Each context has mutable state, and shared backend/model access still follows backend and API synchronization contracts.

## Memory-module factory

`llama_model::create_memory(params, cparams)` selects or constructs the model-compatible mutable memory implementation. Depending on architecture this may be a KV cache, recurrent memory, hybrid memory, or specialized variant.

This boundary is important:

- the model knows architectural memory requirements;
- the context owns the returned mutable memory instance;
- weight tensors remain model-owned;
- token-history state is context-owned.

## Teardown

The public model-freeing API ultimately destroys the `llama_model`. Its virtual destructor releases architecture-specific state and the model’s owned implementation resources. RAII-managed backend buffers, mappings, metadata contexts, vocabulary data, layer vectors, and other containers are then released.

Correct order:

```text
finish or destroy every llama_context that references the model
  -> destroy adapters/resources whose lifetime depends on model tensors
  -> llama_model_free(model)
```

**Verified:** the destructor is virtual, so deleting through a base `llama_model *` invokes the architecture subclass destructor.

**Open question:** a future API-contract pass should locate the strongest explicit public statement about concurrent model sharing and destruction ordering, rather than relying only on source-level references and examples.

## Truth labels

### Verified

- GGUF architecture selects a concrete `llama_model` subclass.
- Common loading calls architecture-specific hyperparameter and tensor loaders.
- The model owns architecture/vocabulary state and the lifetime of persistent tensor storage.
- `layers` and model-level fields hold pointers to persistent weight tensor metadata.
- `build_graph()` delegates to an architecture-specific graph builder.
- A context references, rather than owns, its model.
- The model must outlive every referencing context.

### Interpretation

- `llama_model` is best understood as a reusable loaded-model object and architecture-specific graph factory.
- `llama_layer` describes persistent weight roles, not one token’s runtime layer execution.
- mmap validity, physical residency, and backend residency are separate properties.
- Weight placement and scheduler node placement are distinct phases.

### Historical

- Architecture registration, model subclass layout, tensor names, split/offload logic, and memory factories evolve rapidly. Later upstream source must not be used to silently rewrite claims pinned here.
- Older llama.cpp revisions organized architecture-specific loading and graph code differently; this page describes the pinned `src/models/` era only.

### Open question

- Add generated line-level citations for every architecture-specific example.
- Document exact ownership fields inside `llama_model::impl` in a dedicated storage-internals appendix.
- Verify explicit model-sharing/thread-safety guarantees in public documentation.
- Measure storage branch entry, bytes mapped/read/uploaded, page faults, and teardown synchronization at runtime.

## Source map

| Question | Pinned source |
|---|---|
| Architecture dispatch and model creation | [`src/llama-model.cpp`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/src/llama-model.cpp#L41-L333) |
| Model fields, loading interface, graph/memory factories | [`src/llama-model.h`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/src/llama-model.h#L535-L737) |
| Layer tensor schema, including dense, MoE, recurrent, and architecture-specific fields | [`src/llama-model.h`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/src/llama-model.h#L226-L534) |
| GGUF parsing and source tensor records | [`src/llama-model-loader.cpp`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/src/llama-model-loader.cpp) |
| Architecture subclasses | [`src/models/`](https://github.com/ggml-org/llama.cpp/tree/e3546c7948e3af463d0b401e6421d5a4c2faf565/src/models) |
| Context ownership and model reference | [`src/llama-context.h`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/src/llama-context.h) |

## Related pages

- [GGUF file anatomy](../foundations/gguf-file-anatomy.md)
- [Model tensor placement](../foundations/model-tensor-placement.md)
- [`llama_context`](llama-context.md)
- [GGML graph construction and MoE](../ggml/graph-construction-and-moe.md)
- [Backend scheduler execution](../lifecycle/backend-scheduler-execution.md)
