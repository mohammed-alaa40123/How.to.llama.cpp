# Synthetic GGUF v0 fixture implementation

- **Starting commit:** `a795a4d8bb7246578fc247f97a5b050b0088efe0`
- **Implementation ending commit:** `0df632d2fd66743ca3e4d55cba1b44a35bcada53`
- **Assigned milestone:** Week 1 legal/small fixture implementation for Lab 1 GGUF Anatomy
- **Learner outcome:** predict, parse, and explain GGUF metadata, tensor descriptors, alignment, relative offsets, absolute byte ranges, and corruption failures without downloading model weights
- **Source baseline:** `ggml-org/llama.cpp@e3546c7948e3af463d0b401e6421d5a4c2faf565`
- **Primary format source:** official `ggml-org/ggml` GGUF specification already recorded in `docs/reference/research-ledger.md`

## Increment

Added one deterministic, project-owned GGUF fixture package:

- `scripts/generate_synthetic_gguf.py`
- `labs/fixtures/gguf/synthetic-v0.manifest.json`
- `labs/fixtures/gguf/synthetic-v0.golden.json`
- `tests/test_generate_synthetic_gguf.py`

The generator emits a 428-byte little-endian GGUF v3 file with five metadata entries and two F32 demonstration tensors. The second tensor begins at relative offset 32, while tensor data begins at absolute file offset 384. Payload values are authored numeric examples, not trained weights and not valid inference content.

The committed source of truth is the generator, manifest, and golden parse. The binary and three corruption variants are regenerated deterministically:

- invalid magic;
- misaligned tensor offset;
- truncated final tensor payload.

## Truth labels

### Verified

- Repeated generation produced SHA-256 `688d0ef28c83d6972e291cc0342e695540eae8496b3ec8e92bdbb91e3982a564`.
- The golden parse reports GGUF v3, alignment 32, five metadata records, two tensor descriptors, data offset 384, and file size 428.
- Both tensor ranges are alignment-valid and bounded by the generated file.
- All three bounded corruption variants raise parser errors.
- The implementation performs no network download, model redistribution, paid API call, telemetry, or learner-data collection.

### Interpretation

- Committing generator plus manifest and golden output, while regenerating the tiny binary for tests/labs, keeps provenance and reviewability stronger than treating an opaque binary as the source of truth.
- The fixture is sufficient for the first browser GGUF lesson but is intentionally insufficient for llama.cpp inference.

### Historical

- The previous run selected a model-free Lab 0 path and a project-owned synthetic GGUF for Lab 1.

### Open question

- Browser/Python parser agreement is not yet implemented.
- Native `gguf_init_from_file` acceptance against the pinned llama.cpp revision is not yet part of ordinary CI.

## Validation performed before repository write

```text
python3 -m unittest discover -s tests -p 'test_*.py'
Ran 3 tests in 0.001s — OK

python3 scripts/generate_synthetic_gguf.py --check
688d0ef28c83d6972e291cc0342e695540eae8496b3ec8e92bdbb91e3982a564
```

These commands were executed against the exact file contents committed in this increment in an isolated local workspace.

## CI inspection and integration fix

Documentation CI run `29538414734` passed durable-context validation, interactive links, source-index tests, unit-test discovery, shell syntax, Python compilation, and required interactive assets. It failed only at `mkdocs build --strict` because the new executable-learning documentation pages were not represented in `mkdocs.yml` navigation. Commit `0df632d2fd66743ca3e4d55cba1b44a35bcada53` adds a bounded `Executable learning` navigation group for the legal fixture decision, two-week plan, literature map, and agent handoffs. A final-head workflow run had not appeared when this log was closed.

## Human review needs

- Confirm that `general.architecture = educational` is acceptable for the browser-only teaching fixture; it is not claimed to be a loadable llama.cpp model architecture.
- Review whether Week 2 should add a pinned native GGUF reader acceptance test or keep the first fixture validator Python/browser-only.

## Evidence produced

- deterministic generator;
- explicit manifest and source revision;
- golden parser output and whole-file checksum;
- alignment/range assertions;
- bounded corruption rejection tests;
- explicit non-model and non-inference boundary;
- CI evidence showing the focused Python/test lanes passed before a documentation-navigation integration failure;
- bounded MkDocs navigation repair.

## Next dependency

Add machine-readable trace, media-manifest, and learner-progress schemas with focused validators, unless the orchestrator ranks the Lab 0 checker interface first.
