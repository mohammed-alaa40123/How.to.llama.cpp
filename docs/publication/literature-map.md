# EAAI literature map

_Last updated: 2026-07-17_

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

## Slice 2 — generated educational media and artifact provenance

### Question

Which current image, audio, realtime, video, and notebook services can be used as optional educational-media tools without making generated output authoritative technical evidence or an unreproducible CI dependency?

### Official capability and constraint map

| Service/source | Verified capability or constraint on 2026-07-17 | Reproducibility and governance implication |
|---|---|---|
| [OpenAI Images API](https://platform.openai.com/docs/api-reference/images-streaming) and [Responses image-generation tool](https://platform.openai.com/docs/api-reference/responses) | The API supports generated and edited images, including streamed partial images. Outputs are stochastic service results rather than source-revision-derived diagrams. | Record endpoint/tool, model identifier or snapshot when exposed, request parameters, prompt hash, input-asset hashes, output checksum, creation time, and human disposition. Never regenerate an approved asset on ordinary CI. |
| [OpenAI Audio API](https://platform.openai.com/docs/api-reference/audio) | The API supports text-to-speech and transcription. Custom voices require a consent recording and are limited to eligible customers. Transcription can return text and some caption-friendly formats depending on model. | Prefer built-in voices. Generated narration requires the exact source script, transcript, voice/model identifier, checksum, pronunciation review, and a text-equivalent lesson path. Do not treat an automatic transcript as reviewed captions. |
| [OpenAI Realtime API](https://platform.openai.com/docs/api-reference/realtime) | Realtime supports low-latency multimodal sessions over WebRTC, WebSocket, or SIP, including speech-to-speech and text/image/audio inputs and outputs. | Realtime is unsuitable as a canonical lesson artifact because session timing, outputs, connectivity, and model behavior are not deterministic. Restrict it to an optional demonstration after the static/browser lesson is complete; retain no learner audio by default. |
| [OpenAI Videos API](https://platform.openai.com/docs/api-reference/videos) | The API exposes asynchronous video-generation jobs with prompt, optional reference asset, model, duration, and size parameters. Current documented models include `sora-2` and `sora-2-pro`. | Video must be cached and review-gated. Store prompt/storyboard hash, input hashes, documented model name, parameters, output checksum, captions, transcript, static fallback, technical-claim declaration, and accepted/revised/rejected status. Generated motion cannot establish a call graph, tensor shape, ownership, timing, or memory fact. |
| [OpenAI business-data controls](https://openai.com/business-data/) and [API data controls](https://platform.openai.com/docs/models/default-usage-policies-by-endpoint) | API/business inputs and outputs are not used for training by default; retention and regional controls depend on account eligibility, endpoint, and configuration. | Do not infer zero retention. Before sending unpublished source, learner data, voices, or proprietary media, record the account policy and endpoint-specific retention setting. The project’s default prompts must contain only public repository material and project-authored assets. |
| [Gemini native image generation / Nano Banana](https://ai.google.dev/gemini-api/docs/image-generation) | Gemini provides text-and-image generation/editing through multiple image models. The official guide states that generated images include SynthID. The model family and preferred API path changed recently; Imagen deprecation is documented for 2026-08-17. | Treat model IDs and API versions as mutable deployment dependencies. Record exact model ID, API surface, prompt and inputs, output checksum, SynthID presence when detectable, and review state. Reverify before every generation run; do not encode “Nano Banana” alone as a reproducible model identifier. |
| [NotebookLM product capabilities](https://support.google.com/notebooklm/answer/16164461) | NotebookLM can generate grounded chats and derivative study artifacts from uploaded sources, including audio and visual study formats exposed through the product UI. | It can be an instructor-side ideation or review companion, but exported artifacts still need independent technical verification, accessibility review, provenance records, and local caching before use. |
| [NotebookLM Enterprise notebook API](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks) | The preview API currently documents notebook management operations such as create, retrieve, list, delete, and share. The verified page does not establish an API for deterministically generating, exporting, checksumming, or versioning every Audio/Video Overview or other derived artifact. | Reject NotebookLM as the canonical automated media pipeline. Reconsider only when an official supported API covers source ingestion, artifact generation, retrieval/export, version/model provenance, and lifecycle management needed by the manifest contract. |
| [NotebookLM privacy and copyright guidance](https://support.google.com/notebooklm/answer/17004255) and [public-notebook sharing warning](https://support.google.com/notebooklm/answer/16322204) | Google requires users to respect copyright. Public sharing may expose underlying sources even when a restricted chat view is used. Data handling varies by account/license. | Never upload restricted model files, confidential learner material, or sources that cannot be redistributed. Public-notebook presentation is not a privacy boundary. Record account class, source rights, sharing scope, and human approval. |

### Deterministic graphics versus generated media

| Educational use | Authoritative representation | Optional generated supplement | Reason |
|---|---|---|---|
| GGUF byte offsets, alignment and tensor ranges | Programmatically generated SVG/table from the fixture manifest | Decorative cover or analogy illustration | Exact positions must be recomputable and checksum-verifiable. |
| llama.cpp/GGML call graph | Revision-pinned source extraction plus deterministic graph layout | Nontechnical visual metaphor | A model-generated edge or missing call can silently falsify the explanation. |
| Tensor shapes and runtime objects | Trace-derived table/diagram with evidence labels | Introductory illustration with no numeric claims | Shapes and object states must correspond to the trace and source revision. |
| Memory ownership, mmap, residency and page faults | Deterministic state diagram plus captured/derived measurements | Context-setting animation | Generated imagery cannot establish OS state, ownership, or timing. |
| Narration | Reviewed script and transcript; audio is a rendering of that text | Generated voice | The text remains the accessible and reviewable source of truth. |
| Step-by-step video | Source-linked static trace, transcript and deterministic figures | Generated transition scenes or instructor summary | The learner must be able to verify every technical claim without viewing generated frames. |

### Design requirements derived from this slice

1. **No generative technical authority.** An architecture, call graph, tensor layout, pointer chain, memory event, benchmark, or timing claim must be generated from structured source/trace/fixture data or authored and independently reviewed—not inferred from an image/video model.
2. **Immutable artifact receipt.** Every external generation must emit a local receipt containing provider, endpoint/API surface, exact model identifier, parameters, UTC timestamp, prompt/storyboard hash, input checksums, output checksum, source revision, cost/usage record when available, and acceptance state.
3. **Manual generation only.** External generation is a manually triggered or separately approved workflow. Pull-request and push CI validates manifests and cached outputs but never calls paid media endpoints.
4. **Model drift is a first-class risk.** Friendly product labels are insufficient. Store exact documented IDs where available and flag an asset stale when its source revision, script, storyboard, prompt, input, generator model, or validation schema changes.
5. **Accessibility is upstream, not post-processing.** Images require meaningful alt text; narration requires the reviewed script/transcript; video requires captions, transcript, audio description when visually necessary, reduced-motion/static fallback, and keyboard-accessible controls.
6. **Privacy-minimized inputs.** Default generation inputs are public, project-owned, or licensed material. No learner identifiers, learner voice, raw learner code, unpublished model weights, secrets, or private repository content may be sent without a separate approved data pathway.
7. **Human review is claim-specific.** Review must separately record technical correctness, accessibility, licensing/redistribution, representation concerns, and whether the asset is accepted, revised, or rejected. Visual attractiveness is not an educational outcome.
8. **NotebookLM remains optional.** Use it only for instructor-side source-grounded exploration or manually reviewed supplements until an official artifact-generation/export API satisfies the same manifest and caching contract.

### Rejected alternatives

- **Rejected:** asking a generative image model to draw the canonical llama.cpp architecture and treating the result as a technical diagram.
- **Rejected:** storing only a prompt and provider name. This cannot reproduce or audit a mutable hosted model result.
- **Rejected:** using Realtime voice as the only lesson delivery path or storing learner audio by default.
- **Rejected:** regenerating images, narration, or video during ordinary CI.
- **Rejected:** using NotebookLM UI outputs as canonical build artifacts when the verified API does not expose the required generation/export/provenance lifecycle.

### EAAI framing implication

Generated media can support an experience report only as a documented instructional-design process: which assets were proposed, why deterministic evidence was retained, what reviewers corrected or rejected, what accessibility and licensing work was required, and what cost/maintenance burden resulted. The defensible outcome is not that generated media looked engaging. Any educational claim must be tied to comprehension, code-tracing, misconception, accessibility, or expert-use evidence.

## Next literature dependency

Complete a primary-literature slice on source-code comprehension and visualization outcomes, including evidence for code-tracing tasks and comparisons between interactive traces and static source/text. This should inform the baseline for `VIEW-01` and must not assume visual novelty implies learning benefit.
