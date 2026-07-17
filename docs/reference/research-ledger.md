# Research and references ledger

This ledger records sources worth reading. Inclusion does not imply endorsement or correctness. Every non-official source must be checked against a pinned revision.

## Official and primary sources

| Source | Type | Use in the project | Status |
|---|---|---|---|
| [`ggml-org/llama.cpp`](https://github.com/ggml-org/llama.cpp) source, examples, tests, docs | Primary source | Implementation truth and regression behavior | Active baseline |
| [`ggml-org/ggml` GGUF specification](https://github.com/ggml-org/ggml/blob/master/docs/gguf.md) | Official specification | File layout, typed metadata, alignment, tensor descriptors, split naming, and canonical v3 diagram | Deep review completed for file-anatomy slice; implementation differences remain pinned separately |
| [Canonical GGUF v3 diagram](https://github.com/ggerganov/ggml/assets/1991296/c3623641-3a1d-408e-bfaf-1b7c4e16aa63), attributed upstream to [@mishig25](https://github.com/mishig25) | Officially referenced figure | GGUF physical-layout explanation | Linked, not redistributed; attribution verified from specification |
| [Pinned llama.cpp OpenCL backend guide](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/docs/backend/OPENCL.md) | Official backend documentation | Intended hardware/OS scope, build paths, kernel deployment options, and known limitations | Reviewed for OpenCL build/lifetime foundation; teardown contracts still require source audit |
| [Khronos `clReleaseMemObject` reference](https://registry.khronos.org/OpenCL/specs/unified/refpages/man/html/clReleaseMemObject.html) | Official API specification | Memory-object reference-count deletion rule, queued-command retention, and parent/sub-buffer deletion ordering | Reviewed for pinned `transpose_2d()` enqueue-then-release classification |
| [Khronos `clEnqueueNDRangeKernel` reference](https://registry.khronos.org/OpenCL/specs/unified/refpages/man/html/clEnqueueNDRangeKernel.html) | Official API specification | Kernel enqueue semantics, optional completion events, and queue/event behavior | Reviewed for pinned nonblocking transpose classification |
| [Khronos OpenCL event-object specification](https://registry.khronos.org/OpenCL/specs/unified/html/OpenCL_API.html#event-objects) | Official API specification | `clWaitForEvents()` host synchronization, implicit event retain on command return, and required `clReleaseEvent()` reference decrement | Reviewed for Q4_0 conversion event-leak classification; specification v3.1.1 dated 2026-05-22 |
| [Khronos `clEnqueueReadBuffer` reference](https://registry.khronos.org/OpenCL/specs/unified/refpages/man/html/clEnqueueReadBuffer.html) | Official API specification | Blocking read completion and host-memory visibility | Reviewed for 22 redundant wait sites immediately preceding same-queue `CL_TRUE` reads |
| [Khronos `clCreateCommandQueue` reference](https://registry.khronos.org/OpenCL/specs/unified/refpages/man/html/clCreateCommandQueue.html) | Official API specification | In-order versus out-of-order queue execution properties | Reviewed to verify the pinned queue is in-order when the out-of-order property is absent |
| [Stanford CS336 Spring 2025 executable lectures](https://github.com/stanford-cs336/spring2025-lectures) | Primary educational repository, MIT | Trace-producing executable lectures and trace-viewer architecture | Reviewed for architecture pattern; license/source revision must be pinned before code adaptation |
| [JupyterLite kernel configuration](https://jupyterlite.readthedocs.io/en/stable/howto/configure/kernels.html) | Official documentation | Browser-kernel capability and limits | Reviewed for browser-tier boundary; not evidence of native llama.cpp execution |
| [JupyterLite browser storage](https://jupyterlite.readthedocs.io/en/stable/howto/configure/storage.html) | Official documentation | Local browser persistence mechanisms | Reviewed for local-only progress design; export/import and loss warnings still required |
| [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/) and [CLI reference](https://docs.astral.sh/uv/reference/cli/) | Official documentation | Locked Python tooling, offline/degraded behavior, reproducibility checks | Reviewed for Lab 0 Python environment contract; does not replace native toolchain pinning |
| [GitHub dev containers](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers) and [Codespaces prebuilds](https://docs.github.com/en/codespaces/prebuilding-your-codespaces/about-github-codespaces-prebuilds) | Official documentation | Cloud-container environment and optional prebuild behavior/cost boundary | Reviewed; devcontainer selected as fallback, prebuilds remain optional and budget-gated |
| [Binder reproducibility guidance](https://mybinder.readthedocs.io/en/latest/tutorials/reproducibility.html) | Official documentation | Repository-defined reproducible notebook environments | Reviewed as a lightweight fallback; rejected as default native llama.cpp environment |
| [MLSysBook interactive labs](https://mlsysbook.ai/labs/) | Primary educational project | Predict–Discover–Explain cycle, browser-first simulations, persistent design ledger | Reviewed for pedagogy pattern; implementation reuse requires license/source review |
| [Cornelissen, Zaidman, and van Deursen, trace-visualization controlled experiment](https://doi.org/10.1109/TSE.2010.47) | Primary controlled experiment | Static-source/text baseline design and correctness/time outcomes | Reviewed; historical effect sizes are not transferred to this project |
| [Wyrich, Bogner, and Wagner, 40-year code-comprehension experiment map](https://arxiv.org/abs/2206.11102) | Systematic mapping study | Task, measure, and construct-validity design cautions | Reviewed for benchmark freezing requirements |
| [Wyrich, contemporary source-code comprehension model](https://arxiv.org/abs/2310.11301) | Conceptual primary research | Explicit construct and operationalization | Reviewed; first evaluation limited to bounded path reconstruction and evidence classification |
| [Hassan and Zilles, tracing for understanding code](https://sigcse2023.sigcse.org/details/sigcse-ts-2023-papers/21/On-Students-Usage-of-Tracing-for-Understanding-Code) | Primary qualitative study | Prediction tasks and tracing-failure diagnostics | Reviewed for benchmark item design |
| [Park et al., code-readability eye-tracking experiment](https://doi.org/10.1007/s10664-024-10532-x) | Primary controlled experiment | Correctness, logical correctness, confidence, and visual-effort measures | Reviewed; confidence retained only as a secondary measure |
| [Thilderkvist and Dobslaw, remote eye-tracking limitations](https://doi.org/10.1016/j.infsof.2024.107502) | Primary remote-method validation | Privacy and validity limits of consumer-webcam eye tracking | Reviewed; webcam eye tracking rejected for the first evaluation |
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