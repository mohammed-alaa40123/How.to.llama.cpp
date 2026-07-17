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

## Slice 2 — EAAI-27 official venue requirements

### Question

What does the current official EAAI-27 call require, and which repository evidence gaps directly threaten an Experience Report and Innovative Practice submission?

### Verified official facts

| Source | Verified requirement | Repository implication |
|---|---|---|
| [Official EAAI-27 call](https://aaai.org/conference/aaai/aaai-27/eaai-27-call/) | Abstract deadline: **September 1, 2026, 11:59 PM UTC-12**; paper deadline: **September 8, 2026, 11:59 PM UTC-12**; notification: November 17, 2026; camera-ready: December 14, 2026; symposium: February 21-23, 2027 in Montréal. | Replace the prior “call unavailable” assumption. Keep a separate internal evidence-freeze date before September 1; do not borrow AAAI main-track July deadlines. |
| Official EAAI-27 call | EAAI-27 is explicitly about **teaching and learning about AI**. Work using AI to teach unrelated programming or systems topics is outside scope. | Frame GGML/llama.cpp internals as AI-practitioner education: model formats, inference graphs, runtime evidence, and responsible AI-systems engineering. A generic C++ debugging framing would weaken venue fit. |
| Official EAAI-27 call | Main-track Area 2 accepts Experience Reports and Innovative Practice describing design, development, use context, collected data, and rich reflection on what did or did not work and why. | Repository contracts and tools are insufficient alone. The submission needs actual use or an approved expert-usefulness pathway, retained failures/corrections, and a bounded longitudinal dataset. |
| Official EAAI-27 call | Area 2 contributions must be grounded in relevant literature, clearly articulate novelty, and provide insights valuable to the broader AI education community. | Keep the source-level documentation gap as a hypothesis until audited. Generalization must be mechanism-level—evidence labels, source pinning, deterministic replay, and supervised maintenance—not “llama.cpp is universally representative.” |
| Official EAAI-27 call | Review criteria include relevance, significance to the intended audience, prior work, novelty, technical soundness, clarity, evaluation of claims/results, and ethics/inclusivity. | Freeze one primary learner population, obtain independent technical review, complete accessibility checks, and evaluate only claims supported by approved evidence. |
| Official EAAI-27 call | Empirical authors are encouraged, though not required, to use SIGSOFT Empirical Standards. | Structure retrospective repository analysis and any learner/expert study with an explicit study type, sampling frame, variables, missing-data rules, threats to validity, and artifact availability. |
| Official EAAI-27 call | All submissions and supplementary materials are double-blind; papers are up to 7 pages plus up to 2 pages of references; supplementary material is separate and reviewers are not required to inspect it. | The main paper must carry the essential evidence and limitations. Public repository URLs, author-identifying logs, branch names, and acknowledgements need an anonymization plan; crucial claims cannot depend only on supplementary artifacts. |
| Official EAAI-27 call | In-person presentation is required for accepted papers. | Add a human planning blocker for presenter availability, travel funding, visa timing, and accessible demo fallback before submission commitment. |
| [Official AAAI-27 page](https://aaai.org/conference/aaai/aaai-27/) | The AAAI main-track July 21/28 deadlines are track-specific; the page links a separate EAAI-27 CFP. | Reject the earlier assumption that no official EAAI-27 call exists and reject using main-track dates for EAAI planning. |

Sources were checked on **2026-07-17**.

### EAAI framing implication

**Verified:** the prospective work is within scope only when it is presented as education about AI systems and inference internals, not as AI-assisted teaching of generic programming.

**Interpretation:** the strongest Area 2 framing is a coherent experience report about a source-linked executable environment plus the supervised repository-native process that maintained it. The multi-agent workflow is supporting experience evidence, not a substitute for educational use data.

**Open question:** whether an expert-usefulness evaluation without a classroom deployment will provide sufficient “context of use” and “data collected” for a competitive Area 2 submission. This requires an approved evaluation pathway and later reviewer judgment; the call does not guarantee adequacy.

### Concrete design requirement

Before manuscript drafting, create a versioned **double-blind evidence-release plan** that maps every intended claim to evidence that can appear in the seven-page paper, identifies which repository artifacts require anonymized snapshots, and records which essential results cannot be delegated to supplementary material.

### Rejected alternative

Do not position the project as a Model AI Assignment merely because it includes labs. The contribution currently spans a learning environment, trace viewer, reproducibility architecture, and longitudinal maintenance case study; forcing it into the assignment track would discard the experience-report evidence structure and would require separate track-specific instructions.

## Next literature dependency

Conduct the predefined systematic audit of official and community llama.cpp/GGML learning resources before strengthening the claimed gap between usage-oriented documentation and source-level systems understanding.