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

## Design requirements derived from Slice 1

1. Every executable result must declare one of: `browser-derived`, `native-captured`, `source-derived`, or `authored-example`.
2. The browser lab must expose a visible native-runtime disclaimer and a downloadable text/table fallback.
3. The Lab 0 checker must report Python environment, compiler, CMake, Ninja, source revision, build result, smoke-test result, and timing as separate fields.
4. Local and devcontainer paths must invoke the same checker and expected-output contract.
5. Progress persistence must support JSON export/import and warn that browser or cloud workspace storage can disappear.
6. Prebuilds, Binder, authenticated sync, and paid cloud capacity are optional future enhancements, not Week 1 dependencies.

## Slice 2 — static-source/text baseline for the trace viewer

### Orchestrator question

What is a fair baseline and defensible outcome set for testing whether the executable lecture improves source-code tracing rather than merely adding visual novelty?

### Evidence map

| Source | Evidence type | Verified finding | Implication |
|---|---|---|---|
| [Cornelissen, Zaidman, and van Deursen, “A Controlled Experiment for Program Comprehension through Trace Visualization,” IEEE TSE 37(3), 2011](https://doi.org/10.1109/TSE.2010.47) | Primary controlled experiment | Eight program-comprehension tasks compared an IDE-only condition with IDE plus execution-trace visualization; the reported outcomes were solution correctness and time spent. | The project needs an information-equivalent static source/text control and must treat correctness and completion time as primary outcomes. Historical effect sizes are context-specific and must not be transferred to this viewer. |
| [Wyrich, Bogner, and Wagner, “40 Years of Designing Code Comprehension Experiments,” 2022](https://arxiv.org/abs/2206.11102) | Systematic mapping of 95 experiments | Code-comprehension studies use heterogeneous tasks and measures, creating comparability and construct-validity problems. | Freeze task definitions, scoring, source revision, time limits, exclusions, and analysis before collecting data. Do not use an undefined “understanding” score. |
| [Wyrich, “Source Code Comprehension: A Contemporary Definition and Conceptual Model,” 2023](https://arxiv.org/abs/2310.11301) | Conceptual research framework | The field often defines comprehension implicitly through tasks; the paper argues that the target construct and operationalization must be explicit. | State that the first evaluation measures bounded path reconstruction and evidence classification, not general mastery of llama.cpp or systems programming. |
| [Hassan and Zilles, “On Students’ Usage of Tracing for Understanding Code,” SIGCSE TS 2023](https://sigcse2023.sigcse.org/details/sigcse-ts-2023-papers/21/On-Students-Usage-of-Tracing-for-Understanding-Code) | Primary qualitative think-aloud study | Tracing can help learners explain code, but failures occur when learners do not trace, trace incorrectly, or choose inputs that do not expose behavior. | Include prediction-before-reveal tasks and distractors that diagnose incorrect transitions, not only recall of labels shown by the viewer. |
| [Park et al., “An Eye Tracking Study Assessing Source Code Readability Rules for Program Comprehension,” Empirical Software Engineering 29, 2024](https://doi.org/10.1007/s10664-024-10532-x) | Primary controlled eye-tracking study | Participants answered comprehension and logical-correctness questions and reported confidence; response correctness and visual effort were analyzed. | Confidence can be a secondary calibration measure, but it cannot replace correctness. Eye tracking is unnecessary for the first bounded evaluation. |
| [Thilderkvist and Dobslaw, “On current limitations of online eye-tracking to study the visual processing of source code,” Information and Software Technology 174, 2024](https://doi.org/10.1016/j.infsof.2024.107502) | Primary remote-method validation | Consumer-webcam eye-tracking data was inadequate for the intended remote comparison despite calibration and guidance. | Reject webcam eye tracking for the July evaluation plan; it adds privacy and validity risk without supporting the core claim. |

Sources were checked on 2026-07-17.

### Required baseline

The control condition must contain the **same evidence** as the viewer, without synchronized interaction:

- immutable source excerpts and source links;
- ordered call-stack and step table;
- runtime-object, tensor-shape, and memory-event text;
- evidence-kind labels;
- the complete static transcript;
- identical prediction and code-tracing questions.

The intervention condition may add only synchronized step navigation, coordinated highlighting, and the deterministic runtime visualization. Both conditions use the same trace revision, wording, task order, time limit, and accessibility fallback.

**Rejected alternative:** comparing the viewer against raw upstream source alone. That would confound information availability, curated explanation, and navigation, making a positive result uninterpretable.

### Bounded code-tracing task set

1. **Next-transition prediction:** choose the next function/phase before reveal.
2. **State reconstruction:** identify which runtime object or bounded field changed at a specified step.
3. **Call-stack reconstruction:** order three to five pinned frames or transitions.
4. **Evidence classification:** distinguish `native-captured`, `source-derived`, `authored-example`, `interpretation`, and `open-question` claims.
5. **Misconception diagnosis:** reject statements equating a GGUF file with an executable graph or mapped bytes with physically resident pages.
6. **Transfer item:** answer one structurally similar question using a held-out step or source excerpt not navigated during practice.

### Outcome contract

- **Primary:** task correctness using a frozen item-level answer key.
- **Co-primary or key secondary:** bounded completion time for correctly completed tasks; report timeouts separately.
- **Secondary:** confidence per answer, confidence–correctness calibration, perceived difficulty/cognitive load, navigation errors, and accessibility completion mode.
- **Process evidence:** step revisits, prediction revisions, and missing-data/fallback use only when locally consented and approved; no silent telemetry.
- **Not outcomes:** visual attractiveness, page views, animation use, or total clicks.

### Design requirement

Before any learner evaluation, add a versioned benchmark fixture containing both presentation conditions, exact tasks, answer keys, scoring rules, timeout behavior, source revision, and accessibility alternatives. Expert review must verify information equivalence and technical correctness. A pilot may test task clarity and timing, but no participant recruitment or personal-data collection begins without the approved evaluation/ethics pathway.

## EAAI framing implication

The defensible educational contribution is not “one-click llama.cpp” or “an animated source viewer.” It is a source-pinned learning design that makes evidence boundaries visible and tests bounded path reconstruction. The executable lecture remains an implementation artifact until it is compared against an information-equivalent static source/text condition using correctness and time, with confidence and cognitive load treated as secondary measures.

The broader gap between usage-oriented documentation and source-level systems understanding remains a **hypothesis** pending a systematic documentation audit.

## Next literature dependency

Continue `VENUE-01` monitoring for an official EAAI-27 call. If no new official call is available, the next distinct literature slice should examine longitudinal repository-native documentation maintenance and human-supervised agent-workflow evaluation baselines.