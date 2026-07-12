# Canonical `llama_model` object page

- Run time: 2026-07-12 21:08 Africa/Cairo
- Scope: document `llama_model` as the reusable loaded-model object and architecture-specific graph factory
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Published `docs/objects/llama-model.md` and added it to the Objects navigation.

The page covers:

- GGUF architecture dispatch to concrete model subclasses;
- common versus architecture-specific loading hooks;
- model identity, hyperparameters, vocabulary, model-level tensors, and `llama_layer` records;
- persistent model buffer, mapping, and device ownership;
- model tensor placement versus scheduler graph placement;
- `build_graph()` and `build_arch_graph()` delegation;
- model sharing across contexts and the lifetime contract;
- architecture-selected memory factories;
- teardown, source map, related pages, and truth labels.

## Verified

- `llama_model_create(loader, params)` obtains the GGUF architecture, rejects unknown values, and dispatches through `llama_model_mapping()` to a concrete subclass.
- `llama_model` and `llama_model_base` define common loading behavior while subclasses implement `load_arch_hparams()`, `load_arch_tensors()`, and `build_arch_graph()`.
- The model owns architecture and vocabulary state plus the lifetime of persistent model tensor storage, backend buffers, and retained mappings.
- Model-level fields and `layers` contain pointers to persistent GGML weight tensor metadata.
- Per-token activations and workspaces are created later during graph construction and scheduler allocation.
- Model tensor placement and scheduler node placement are distinct phases.
- `llama_context` stores a non-owning model reference, so the model must outlive every referencing context.
- `create_memory()` lets model architecture choose a compatible memory implementation while the context owns the mutable returned instance.

## Interpretation

- `llama_model` is best understood as a reusable loaded-model object and architecture-specific graph factory.
- `llama_layer` is a schema of persistent tensor roles rather than a record of one token's runtime execution.
- Sharing one model may avoid duplicate weight storage, but it does not make context mutation or backend execution automatically thread-safe.
- A retained mmap provides valid virtual addressability, not guaranteed physical residency.

## Historical

- Architecture registration, subclass organization, tensor names, offload logic, and memory factories change rapidly upstream. The page remains pinned to the stated revision.

## Open questions

- Document exact storage members and destruction order inside `llama_model::impl`.
- Locate the strongest explicit public contract for concurrent model sharing and destruction order.
- Add runtime evidence for mapped/read/uploaded bytes, page faults, and backend teardown synchronization.
- Link the interactive Model object layer when the minified asset can be safely fetched and replaced as a complete file.

## Sources inspected

- Complete repository README.
- `docs/reference/project-state.md`.
- `docs/reference/research-log.md`.
- `docs/reference/research-ledger.md`.
- Latest prior note: `logs/research/2026-07-12/1950-interactive-graph-moe-links.md`.
- Pinned `src/llama-model.h` and `src/llama-model.cpp`.
- Existing canonical GGUF, model-placement, graph-construction, and `llama_context` pages.
- Current MkDocs navigation and interactive explorer.

No new external source was introduced, so the research ledger was intentionally unchanged.

## Validation

- New page creation succeeded.
- MkDocs navigation update succeeded.
- README, project state, and research log were updated.
- Static source inspection confirmed the architecture dispatch, model fields, virtual loading hooks, graph-builder factory, and context/model lifetime boundary.
- Local checkout and `mkdocs build --strict` remain blocked because the execution container cannot resolve `github.com`.
- CI and Pages status are checked after the final durable commit; exact connector or network blockers are recorded when verification is unavailable.

## Next priority

Build the canonical memory-lifetime chapter and interactive overlay, then connect the Model object explorer layer to `objects/llama-model/`.
