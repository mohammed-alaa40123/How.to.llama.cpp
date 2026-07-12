# Model tensor placement and data transfer

- Run time: 2026-07-12 17:50 Africa/Cairo
- Scope: pinned `load_tensors()`, buffer selection, mapping initialization, data population, progress, synchronization, and ownership
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Published `docs/foundations/model-tensor-placement.md` and added it to MkDocs Foundations navigation.

The bounded chapter covers:

- CPU and accelerator candidate buffer lists;
- input/repeating/output layer device assignment;
- per-tensor operation-aware buffer compatibility;
- one GGML metadata context per selected buffer type;
- `init_mappings(true, ...)` and used-range tracking;
- mapped host-pointer buffer creation;
- independently allocated CPU and accelerator buffers;
- mmap alias and mmap copy/upload paths;
- direct non-mmap host reads;
- four-slot pinned-buffer/event asynchronous upload;
- whole-tensor synchronous staging fallback;
- progress callbacks, cancellation, validation, trimming, and lifetimes;
- a placement decision table, measurement plan, source map, and truth labels.

## Verified

- The input layer is kept on CPU; repeating and output layers are assigned from `n_gpu_layers` and normalized device split points.
- CPU and accelerator buffer lists are preference/fallback lists. Final selection is per tensor after testing the operation against backend support.
- Architecture-specific tensor declarations are duplicated into one `ggml_context` per chosen buffer type.
- `init_mappings(true, ...)` creates one mapping per split file and computes total tensor bytes for progress.
- A default device buffer that supports `buffer_from_host_ptr` can wrap only the mapped ranges needed by tensors in that context.
- Mmap loading can alias mapped bytes or copy/upload from those bytes into independent storage.
- Non-mmap host destinations are read directly from the source file.
- Non-mmap accelerator destinations can use four pinned host buffers and events for asynchronous chunked uploads when the destination and device satisfy all capability checks.
- Unsupported asynchronous cases read a complete tensor into a temporary vector and call synchronous `ggml_backend_tensor_set()`.
- Events are synchronized before temporary resources are destroyed.
- Unused mapping fragments are trimmed, and mappings needed by model buffers are moved into `llama_model` ownership.

## Interpretation

- The model loader behaves like a placement compiler: architecture declarations, device choices, operation compatibility, and backend capabilities produce concrete storage choices.
- “Zero-copy loading” is branch-specific, not a property of an entire partially offloaded model.
- Prefetch can shift file activity earlier but does not guarantee pinned physical residency.
- A useful load benchmark must separate parsing, mapping, allocation, aliasing, reads, uploads, waits, and first-touch page faults.

## Historical

- Backend capabilities and upload paths can change after the pinned revision.
- Newer backends may expose additional host-pointer, shared-memory, or asynchronous-transfer behavior.

## Open questions

- Measure which backends and configurations enter each population branch.
- Count bytes aliased, directly read, synchronously copied, and asynchronously uploaded.
- Trace direct-I/O alignment/fallback behavior with concrete runtime evidence.
- Measure prefetch effects on first-token latency, storage reads, faults, and RSS.
- Link the interactive GGUF/graph tab to both canonical model-loading pages.

## Sources inspected

### Pinned llama.cpp source

- `src/llama-model.cpp`: candidate buffer lists, layer assignment, architecture tensor construction, backend-buffer allocation, and load dispatch.
- `src/llama-model-loader.cpp`: per-tensor compatibility, contexts, mappings, reads, uploads, validation, progress, and trimming.
- `src/llama-model-loader.h`: loader structures and API contracts.
- `src/llama-mmap.cpp`: platform mapping, prefetch, lock, and fragment behavior.
- `ggml/src/ggml-backend.cpp`: backend buffer/event interfaces used by the loader.

No new external secondary source was introduced, so `docs/reference/research-ledger.md` was intentionally unchanged.

## Validation

- Repository files were written through the GitHub contents API.
- The chapter was added to `mkdocs.yml`.
- README context map and living TODOs were updated; the placement slice is marked complete.
- Project state and concise research log were updated.
- CI and Pages were checked after the final durable commit; exact results are recorded below and in project state when available.

## Next priority

Build the GGML graph-construction chapter, then connect the interactive GGUF/graph tab to the GGUF and model-placement pages.
