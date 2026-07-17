# EAAI literature map

_Last updated: 2026-07-18_

This file records verified primary or official sources that constrain the executable-learning architecture. It is not paper prose. Claims about a gap between usage-oriented documentation and source-level systems understanding remain a **hypothesis** until a systematic documentation audit is completed.

## Slice 1 — executable lectures and three-tier lab delivery

### Question

Which delivery architecture best supports the first two-week vertical slice: browser-only labs, local native execution, or a cloud development container?

### Evidence map

| Source | Evidence type | Verified capability or constraint | Implication for How.to.llama.cpp |
|---|---|---|---|
| [Stanford CS336 Spring 2025 executable lectures](https://github.com/stanford-cs336/spring2025-lectures) | Primary repository, MIT license | Lecture programs are executed to produce JSON traces and cached images; a React/Vite frontend consumes those traces. The repository explicitly separates executable lectures from non-executable PDFs. | Reuse the architectural pattern—authoritative trace artifact plus narrow viewer—not the implementation wholesale. Pin the license and source revision before adapting code or schemas. |
| [JupyterLite kernel configuration](https://jupyterlite.readthedocs.io/en/stable/howto/configure/kernels.html) | Official documentation | JupyterLite kernels execute in the browser and are constrained compared with ordinary Jupyter kernels; Python support commonly uses Pyodide or Xeus-based kernels. | Browser labs are appropriate for GGUF parsing, calculations, simulations, and formative checkpoints, but must not claim to execute the native llama.cpp C++ runtime. |
| [JupyterLite browser storage](https://jupyterlite.readthedocs.io/en/stable/howto/configure/storage.html) | Official documentation | JupyterLite stores settings, contents, and workspaces using browser-supported persistent storage drivers. | Local progress is feasible without an account, but export/import, schema versioning, corruption recovery, and storage-loss warnings are still required. Browser persistence is not a research-data backend. |
| [uv locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/) | Official documentation | `uv` resolves dependencies into a lockfile; `uv sync` installs from it; `--locked` fails rather than updating an out-of-date lockfile. | Use `uv sync --locked` and `uv run --locked` for Python lab tooling. Treat this as Python-environment reproducibility only; CMake/Ninja and the native compiler remain separate dependencies. |
| [uv CLI reference](https://docs.astral.sh/uv/reference/cli/) | Official documentation | `--offline` disables network access and uses locally cached data; `--locked` asserts that the lockfile remains unchanged. | Add an explicit degraded/offline test and report which artifacts must already be cached. Do not promise first-run offline setup. |
| [GitHub: introduction to dev containers](https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers) | Official documentation | Codespaces creates a development environment from a repository `.devcontainer` configuration and can provide project-specific tools and runtimes. | A devcontainer is the reproducible cloud and local-container fallback for native builds, not the canonical source of truth. Keep commands identical to local setup where possible. |
| [GitHub Codespaces prebuilds](https://docs.github.com/en/codespaces/prebuilding-your-codespaces/about-github-codespaces-prebuilds) | Official documentation | Prebuilds can reduce startup time for large or complex repositories, but consume storage and may incur charges; updates rely on GitHub Actions. | Do not require prebuilds for the first release. Measure cold container setup first, then consider prebuilds only if setup exceeds the project’s acceptable threshold and budget is approved. |
| [Binder reproducibility guidance](https://mybinder.readthedocs.io/en/latest/tutorials/reproducibility.html) | Official documentation | Binder emphasizes pinned dependencies and repository-defined environments for reproducible launches. | Binder is a possible lightweight notebook fallback, but it is not the default for native llama.cpp compilation because resource, persistence, startup, and lifecycle guarantees are weaker than a dedicated devcontainer path. |
| [MLSysBook interactive labs](https://mlsysbook.ai/labs/) | Primary educational project | Labs use a Predict–Discover–Explain cycle, require a committed prediction before exploration, run browser-first, retain a browser-based design ledger, and provide an offline path. | Adopt the pedagogical sequence and persistent decision record as design requirements. Do not copy simulations or claims without license and source review. |

Sources were checked on 2026-07-17. Because platform behavior, product limits, and billing can change, implementation decisions that depend on current service details must be reverified before deployment.

## Comparison for the first vertical slice

| Criterion | Browser/static tier | Local native tier | Cloud devcontainer tier |
|---|---|---|---|
| Setup burden | Lowest after site load | Highest and platform-dependent | Medium; container creation replaces much manual setup |
| Native llama.cpp C++ | **No** for ordinary JupyterLite/Pyodide path | **Yes** | **Yes**, subject to container resources |
| Suitable initial tasks | GGUF parsing, alignment, simulations, prediction checkpoints, trace replay | Build, smoke test, real source/runtime experiments | Reproducibility fallback, instructor/demo environment, clean-room verification |
| Persistence | Browser storage; deletion and quota risks | Filesystem under learner control | Workspace persistence depends on service lifecycle and user account |
| Reproducibility boundary | Static assets and pinned browser packages | Locked Python plus explicitly pinned native toolchain and llama.cpp revision | Devcontainer image/configuration plus repository and dependency pins |
| Cost | Static hosting and client resources | Learner-owned machine | Potential metered compute/storage |
| Offline use | Possible after assets are cached, but not guaranteed on first load | Strongest after dependencies and source are present | Generally network- and provider-dependent |
| Security boundary | No secrets; untrusted input must remain sandboxed | Native code executes on learner machine | Repository/container permissions and secrets require explicit minimization |
| Accessibility | Must provide keyboard operation and static text/table fallback | Terminal transcripts and copyable commands | Same as local plus browser/editor accessibility constraints |
| Progress sync | Local only for MVP | Export/import file | Do not treat workspace state as canonical progress |

## Decision recommendation

**Verified:** no single tier satisfies all learning and reproducibility requirements.

**Interpretation:** use a shared lesson contract with three deliberately unequal tiers:

1. **Browser-first for concepts and checkpoints.** Lab 1 should parse a tiny legal GGUF fixture, expose calculations and byte layout, and persist a local decision record. It must display a permanent label that it is not running native llama.cpp.
2. **Local native as the authoritative execution path.** Lab 0 and runtime experiments should use `uv sync --locked` for Python tooling, CMake/Ninja plus a compiler for C++, and a pinned llama.cpp revision.
3. **Devcontainer as the reproducibility fallback.** The same commands and checker should run inside the container. Codespaces-specific prebuilds remain optional and budget-gated.

**Rejected alternative:** do not present browser, local, and cloud environments as interchangeable implementations of the same runtime. This would blur simulation, trace replay, and native evidence, creating a correctness risk for both learners and the EAAI case study.

## Design requirements derived from this slice

1. Every executable result must declare one of: `browser-derived`, `native-captured`, `source-derived`, or `authored-example`.
2. The browser lab must expose a visible native-runtime disclaimer and a downloadable text/table fallback.
3. The Lab 0 checker must report Python environment, compiler, CMake, Ninja, source revision, build result, smoke-test result, and timing as separate fields.
4. Local and devcontainer paths must invoke the same checker and expected-output contract.
5. Progress persistence must support JSON export/import and warn that browser or cloud workspace storage can disappear.
6. Prebuilds, Binder, authenticated sync, and paid cloud capacity are optional future enhancements, not Week 1 dependencies.

## EAAI framing implication

The defensible educational contribution is not “one-click llama.cpp.” It is a source-pinned learning design that makes the evidence boundary visible: learners can distinguish browser simulation, authored explanation, deterministic source-derived structure, and real native execution. Evaluation should test whether this distinction improves code-tracing and systems reasoning, not merely whether setup succeeds.

## Slice 2 — official generative-media capability and lifecycle boundaries

### Question

Can current image, speech, realtime, video, Gemini image, or NotebookLM APIs satisfy the repository's authoritative technical-asset lifecycle, or should they remain optional reviewed supplements?

### Official capability map

| Service | Official capability verified on 2026-07-18 | Reproducibility and governance implication |
|---|---|---|
| [OpenAI Images API](https://platform.openai.com/docs/api-reference/images-streaming) | Image generation/editing can return final bytes and usage metadata; streaming can emit partial and completed images. | Store the exact prompt/storyboard, model identifier, API parameters, returned checksum and usage record. Partial outputs are previews, not accepted assets. Model output remains non-deterministic and cannot be the authoritative architecture diagram. |
| [OpenAI text-to-speech](https://platform.openai.com/docs/api-reference/audio) | `/v1/audio/speech` generates audio from text with selected model, voice, format and speed. Custom voices require an audio sample and a consent recording and are limited to eligible customers. | Use built-in voices only unless a separate consent/licensing review approves a custom voice. Commit the transcript as authoritative, retain the exact voice/model/settings and checksum, and require caption/transcript parity review. |
| [OpenAI Realtime API](https://platform.openai.com/docs/api-reference/realtime) | Realtime supports low-latency WebRTC/WebSocket/SIP sessions with speech-to-speech and text/image/audio I/O. Instructions guide behavior but are not guaranteed to be followed. | Reject Realtime as a canonical build dependency or deterministic narration generator. It may support an optional live companion, but session output must not replace reviewed scripts, traces or captions. |
| [OpenAI Videos API](https://platform.openai.com/docs/api-reference/videos) | `/v1/videos` accepts a prompt and optional reference asset and creates an asynchronous video job using a named video model. | Video must be manually triggered, cost-capped, cached and reviewed frame-by-frame for technical claims. Store prompt, reference hashes, model/version, duration, size, job metadata, output checksum and transcript/captions. Do not regenerate on ordinary pushes. |
| [OpenAI API data controls](https://platform.openai.com/docs/models/default-usage-policies-by-endpoint) | Official endpoint tables document retention and Zero Data Retention eligibility differences across images, audio, realtime and videos. | Every generation run needs a recorded data-classification decision. Do not upload private learner data, unpublished review identities or restricted model artifacts. Reverify endpoint retention before each approved generation batch. |
| [Gemini image generation](https://ai.google.dev/gemini-api/docs/image-generation) | The Gemini API exposes Nano Banana image-generation/editing models; generated images include SynthID. Google documents model-specific resolution, grounding, batch and lifecycle differences. | Record the exact model code rather than the marketing family name, plus prompt, inputs, grounding setting, output checksum and SynthID-preserving handling. Grounded or high-fidelity text rendering does not make a generated technical diagram factual evidence. |
| [NotebookLM Enterprise notebook API](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks) | A preview API can create, retrieve, list, delete and share Enterprise notebooks; it requires Enterprise setup/licenses and is governed by Pre-GA terms. | NotebookLM may be an optional companion workspace, not a canonical CI dependency. Notebook management alone does not provide the repository's manifest, deterministic asset build, approval, checksum and stale-asset lifecycle. |
| [NotebookLM Enterprise source API](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks-sources) | The preview API can add and manage sources including files, raw text, web content and YouTube sources, with additional authorization requirements for some Google content. | Source ingestion introduces privacy, licensing, mutable-web and authorization risks. Any experiment must use an allowlist and retained source snapshot; no learner data or unpublished review material may be uploaded. |

### Verified boundaries

- API availability does not imply deterministic replay. Exact prompt and parameters can be retained while output bytes still vary across calls or model updates.
- OpenAI API keys must remain server-side secrets; browser labs and ordinary static-site builds must never receive generation credentials.
- Gemini's SynthID is useful provenance metadata but does not establish technical correctness, license clearance or accessibility.
- NotebookLM Enterprise now has preview notebook/source-management APIs, but the official surfaces reviewed here do not replace this repository's required acceptance/revision/rejection ledger or deterministic technical-figure pipeline.

### Interpretation for the EAAI case study

The defensible design is a two-layer media system:

1. **Authoritative layer:** deterministic SVG, Mermaid, D3, Graphviz or trace-derived figures generated from structured repository data and validated against source revisions.
2. **Supplemental layer:** optional illustrations, narration, live companions or short videos generated only after a reviewed storyboard exists and accepted only after technical, accessibility, licensing/privacy and provenance review.

Generated media may be evaluated for engagement, accessibility preference or explanatory support. It must not be counted as evidence that a GGML data structure, memory transition, call edge, tensor shape or runtime event is correct.

### Concrete design requirement

Every optional generation adapter must default to a **dry-run manifest mode** and require an explicit manual approval token or workflow dispatch before network/API execution. A generation record must include provider, exact model/version, generator version, prompt/storyboard hashes, input hashes, source revision, parameters, usage/cost record, output checksum, captions/transcript, license/privacy notes and human-review state. Ordinary pushes validate cached artifacts only.

### Rejected alternative

Do not use a generative image or video model to draw the canonical llama.cpp/GGML architecture, source call graph, tensor layout, memory-residency transition or benchmark result. Visual plausibility and text-rendering quality are not source-level correctness guarantees.

### Limitations and revalidation triggers

- Product names, model identifiers, availability, retention, pricing and preview status can change; reverify official documentation before an approved generation batch.
- This slice verifies documented capabilities and restrictions only. It does not test output quality, factuality, accessibility, latency or cost.
- No paid API call, NotebookLM workspace, generated asset or learner data was used in this review.

## Next literature dependency

Retain the predefined `DOC-AUDIT-01` search-result frame and complete independent double-coding before strengthening the source-level documentation-gap hypothesis. A separate future slice should review empirical evidence on multimodal explanations and generated-diagram factuality rather than inferring educational benefit from API capability.