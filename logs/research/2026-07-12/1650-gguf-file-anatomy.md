# GGUF file anatomy and loader entry

- Run time: 2026-07-12 16:50 Africa/Cairo
- Scope: official GGUF physical layout plus the pinned loader's metadata/indexing phase
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Published `docs/foundations/gguf-file-anatomy.md` and added it to MkDocs Foundations navigation.

The bounded chapter covers:

- GGUF header, metadata, tensor descriptors, alignment, and tensor-data region;
- canonical upstream GGUF v3 diagram attribution;
- typed metadata and architecture/tokenizer/split keys;
- `gguf_init_from_file(..., no_alloc = true)` semantics;
- `llama_tensor_weight` source-file index and absolute-offset calculation;
- split discovery, indexing, duplicate rejection, and tensor-count validation;
- mmap/page-fault distinctions;
- CPU-mapped versus backend-owned accelerator storage;
- pinned source map and truth labels.

## Verified

- The official GGUF specification describes a self-describing, extensible, mmap-compatible binary format with typed key/value metadata.
- Its file-structure section publishes the canonical GGUF v3 diagram and attributes it to `@mishig25`.
- The project links to that upstream asset and attribution instead of copying the image.
- In the pinned loader, GGUF parsing uses `no_alloc = true`, producing tensor metadata before final model/backend storage is created.
- `llama_tensor_weight` resolves a tensor name, computes `gguf_get_data_offset + gguf_get_tensor_offset`, and rejects ranges outside the source file.
- Split files retain distinct file indexes while their tensors are merged into one name-indexed `weights_map`.
- The loader rejects duplicate tensor names, invalid split numbering, wrong split counts, and total tensor-count mismatches.
- Direct I/O and mmap are mutually resolved in the constructor: working direct I/O disables mmap; unavailable direct I/O falls back to mmap and a normal reopen.

## Interpretation

- `weights_map` is the format-to-runtime bridge: it answers where tensor bytes are stored, while later architecture and backend code decides where those bytes will be consumed.
- GGUF descriptor/data separation enables metadata-first inspection, mmap-backed host placement, and selective accelerator uploads.
- “Loaded” must be qualified as parsed, mapped, allocated, transferred, synchronized, or physically faulted into RAM.

## Historical

- GGUF succeeded the older GGML, GGMF, and GGJT file formats.
- The pinned loader recognizes GGUF versions 1, 2, and 3 and labels v3 latest for that revision.
- The official specification is a living document and may include conventions newer than the pinned implementation.

## Open questions

- Trace `llama_model::load_tensors()` and architecture-specific tensor creation.
- Trace `llama_model_loader::init_mappings()` and `load_all_data()` including prefetch, mlock, progress, cancellation, and explicit reads/uploads.
- Build a destination-buffer decision table across CPU, CPU_Mapped, CUDA, Metal, Vulkan, SYCL, and other backends.
- Verify big-endian behavior against a concrete file and pinned parser.
- Add runtime instrumentation for metadata parse time, mapping time, major/minor faults, storage reads, uploads, and synchronization.
- Link the interactive GGUF tab to this page.

## Source assessment

### Official GGUF specification

- Authority: official `ggml-org/ggml` repository.
- Revision caveat: living specification, not pinned to the llama.cpp baseline.
- Use: physical format and official diagram attribution.
- Status: deep-reviewed for the file-anatomy slice and recorded in the research ledger.

### Pinned llama.cpp source

- `src/llama-model-loader.h`: loader state, tensor-source records, mappings, contexts, and loading APIs.
- `src/llama-model-loader.cpp`: typed metadata access, constructor, split discovery, validation, and indexing.
- `src/llama-model.cpp`: next-stage architecture and backend tensor placement.
- `src/llama-mmap.cpp`: next-stage mapping, prefetch, and locking behavior.

## Validation

- Repository writes completed through the GitHub contents API.
- MkDocs navigation now includes `foundations/gguf-file-anatomy.md`.
- README TODOs were reordered: the physical-layout slice is complete; tensor placement/data transfer and explorer linking are now highest priority.
- Project state, concise research log, and research ledger were updated.
- Local strict MkDocs execution remains unavailable because the execution container cannot resolve `github.com` for a checkout.

## Next priority

Complete the model tensor-placement and transfer slice, then connect the interactive GGUF/graph tab to the canonical chapter.
