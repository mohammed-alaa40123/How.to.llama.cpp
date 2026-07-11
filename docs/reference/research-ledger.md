# Research and references ledger

This ledger records sources worth reading. Inclusion does not imply endorsement or correctness. Every non-official source must be checked against a pinned revision.

## Official and primary sources

| Source | Type | Use in the project | Status |
|---|---|---|---|
| [`ggml-org/llama.cpp`](https://github.com/ggml-org/llama.cpp) source, examples, tests, docs | Primary source | Implementation truth and regression behavior | Active baseline |
| [`ggml-org/ggml` GGUF specification](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md) | Official specification | File-format chapter | Located; deep review pending |
| llama.cpp PRs and discussions | Design history | Rationale, regressions, alternatives, synchronization details | Ongoing |
| Backend vendor APIs/docs | Primary technical docs | Streams, buffers, events, driver behavior | Per-backend research pending |

## High-value llama.cpp design threads found

| Item | Why it matters | Research caution |
|---|---|---|
| [PR #25319 — asynchronous scheduler memory copies](https://github.com/ggml-org/llama.cpp/pull/25319) | Explains graph splits, copy dependencies, and proposed asynchronous behavior | Verify final status and exact merged/reverted behavior |
| [PR #20793 — scheduler synchronization and pipeline parallelism](https://github.com/ggml-org/llama.cpp/pull/20793) | Shows how subtle event/copy ordering affects correctness and performance | Historical behavior may differ from pinned baseline |
| [PR #21160 — cross-backend profiler](https://github.com/ggml-org/llama.cpp/pull/21160) | Potential source for visualizing split-level execution | Verify current integration and data model |
| [PR #22691 — token-tiered placement planning](https://github.com/ggml-org/llama.cpp/pull/22691) | CPU/GPU scheduling under VRAM constraints; links to a paper | Newer branch/feature may not represent baseline |

## Papers and technical reports found in the first pass

| Work | Topic | Potential chapter |
|---|---|---|
| [*Optimization of Armv9-Based General Matrix Multiplication Based on Llama.cpp*](https://arxiv.org/abs/2406.10816) | CPU kernels and Arm optimization | CPU backend / kernels |
| [*Production-Grade Local LLM Inference on Apple Silicon*](https://arxiv.org/search/?query=Production-Grade+Local+LLM+Inference+on+Apple+Silicon&searchtype=all) | Measurement and optimization methodology | Metal, memory, benchmarking |
| [*Llamas on the Web: Memory-Efficient, Performance-Portable, and Multi-Precision LLM Inference with WebGPU*](https://arxiv.org/abs/2605.20706) | Portability and GPU execution | Backend comparison |
| [*ProfInfer: An eBPF-based Fine-Grained LLM Inference Profiler*](https://arxiv.org/abs/2601.20755) | Runtime profiling | Observability / validation |
| [*Which Quantization Should I Use?*](https://arxiv.org/abs/2601.14277) | Quantization choices and tradeoffs | Quantization chapter |
| [*Mind the Gap: Exploiting the GGUF Quantization Attack Surface*](https://arxiv.org/search/?query=Mind+the+Gap+GGUF+Quantization+Attack+Surface&searchtype=all) | Format/quantization security | GGUF and trustworthiness |
| [*vla.cpp*](https://arxiv.org/search/?query=vla.cpp&searchtype=all) | Extending llama.cpp-style inference to VLA models | Architecture extension case study |

## Community explanations to locate and verify

- Source walkthrough repositories and annotated forks.
- Maintainer talks or interviews about GGML and llama.cpp architecture.
- YouTube deep dives that show source rather than only CLI usage.
- Blog/Medium series about GGUF, quantization, mmap, schedulers, and backends.
- Technical posts by backend contributors explaining PR rationale.
- Conference slides, podcasts, and social threads with implementation details.

!!! warning "First-pass gap"
    General web and video searches produced noisy results. No YouTube item has yet passed the verification bar for this ledger. Future passes should search by maintainer/contributor name, exact symbol, PR number, and conference title rather than broad “llama.cpp tutorial” queries.

## Evaluation rubric

Each external source receives scores for:

1. revision/date clarity;
2. direct source references;
3. author expertise or contributor involvement;
4. technical depth;
5. reproducibility;
6. agreement with current source;
7. usefulness of figures/explanations;
8. license and quotation constraints.
