# Deterministic GGUF layout figure

## Run metadata

- Starting commit: `bcb7555ef8b4e80817b5b812c35db6b1c6f7b9a9`
- Assigned milestone: `FIG-01` — one authoritative deterministic figure from structured fixture data
- Learner outcome: distinguish GGUF header/metadata bytes, alignment, tensor descriptors and payload ranges without implying native inference or runtime graph construction

## Files and sources

- Input: `labs/fixtures/gguf/synthetic-v0.golden.json`
- Generator: `scripts/generate_gguf_layout_figure.py`
- Output: `media/generated/gguf-layout-deterministic-v0.svg`
- Manifest: `media/manifests/gguf-layout-deterministic-v0.json`
- Tests: `tests/test_generate_gguf_layout_figure.py`
- No external source, model, network download, paid API or learner data was used.

## Claims

- **Verified:** the input is the project-owned 428-byte GGUF v3 teaching fixture with 32-byte alignment, five metadata entries and two bounded F32 tensor payloads.
- **Verified:** the checked-in SVG is an exact byte-for-byte replay of the dependency-free generator output.
- **Verified:** input SHA-256 is `ae0fd013da8f7f463e79447978b5a2837e0a52b13029ad6bb23d2fcf3e150968`.
- **Verified:** output SHA-256 is `3482f28bde713b4bf335007df8f2a1b73e0aaee8e88186a5c6419063e1b3b178`; output size is 2526 bytes.
- **Interpretation:** a deterministic figure generated from hashed structured input is suitable as authoritative technical media because its transformation can be replayed and audited.
- **Open question:** independent llama.cpp/GGUF technical review is still required before broader correctness claims rely on this figure.

## Validation

The focused tests require:

1. exact generator-to-checked-in-SVG equality;
2. manifest input/output checksum and byte-count agreement;
3. accessible SVG title/description metadata;
4. explicit text stating that no model weights, native inference or runtime graph construction are represented.

The media manifest validator remains applicable and ordinary CI may regenerate this deterministic asset without credentials or API spending.

## Failures and human review

- No implementation failure was observed while constructing the bounded artifact.
- The manifest records Documentation Builder review, but independent domain review remains a separate `REVIEW-01` requirement.
- The figure intentionally does not visualize an executable GGML graph.

## Evidence produced

This increment supports or falsifies the EAAI claim that authoritative technical media can be derived reproducibly from repository-native structured evidence without depending on generative models. The claim fails if regeneration differs, hashes drift, accessibility metadata disappears or the figure inflates its evidence boundary.

## Next dependency

Wait for commit-scoped Documentation CI. After it passes, the Documentation Builder remains blocked on `VIEW-01` until the Validation Architect closes `TRACE-02`; the next dependency-safe implementation candidate is the browser GGUF lab only after the progress contract is integrated.
