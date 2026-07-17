# Adversarial EAAI reviewer notes

_Last reviewed: 2026-07-17 17:15 Africa/Cairo_

This review evaluates the prospective experience report and July 17-31 executable-learning roadmap. It does not authorize manuscript drafting, participant recruitment, personal-data collection, or educational-effectiveness claims.

## Overall recommendation

**Current recommendation: reject if submitted in the present state.**

The repository now contains a coherent set of deterministic contracts, validators, fixtures, and narrow interfaces. That is useful engineering evidence, but it is not yet an EAAI experience report. The submission would currently read as a sophisticated design-and-validation package with almost no demonstrated learner benefit, no measured native-tier reproducibility, no independent technical correctness review, and only a three-record retrospective sample for the scheduled-agent case study.

The central threat is **evidence inflation**: passing CI is repeatedly and correctly labelled as contract validation, but the project has accumulated enough polished infrastructure that a reader could still infer educational effectiveness, deployability, or workflow superiority that has not been measured.

## Fatal flaws at present

1. **No approved educational evaluation and no learner or expert-usefulness results.** The project cannot support its primary educational claim without a defensible evaluation pathway. A static-versus-viewer benchmark contract exists, but no approved comparison has been run.
2. **No independent technical correctness review.** The fixture, GGUF explanations, authored trace, source anchors, benchmark answer key, deterministic figure, and browser parser remain author-reviewed artifacts.
3. **No measured local-native or devcontainer Lab 0 evidence.** The schema is validated, but Ubuntu and cloud-container execution rows are absent. This prevents a reproducibility claim for two of the three tiers.
4. **The longitudinal agent case study is underpowered.** Three selected archetypes demonstrate schema coverage, not a longitudinal repository-native dataset, reliable coding, labor accounting, or a basis for general lessons.
5. **The integrated Week 2 demonstration is incomplete.** The current stack has independently validated components, but not a clean, measured, end-to-end learner path across setup, browser lab, viewer, progress, and evidence export.

Any one of these is enough to block manuscript integration. Together they make submission premature.

## Major concerns

### 1. The educational contribution may collapse into a tool collection

The repository has a fixture generator, browser parser, trace viewer, progress adapter, media manifests, validators, and benchmark schemas. The paper contribution must not be “we built many tools.” It needs a coherent educational mechanism:

- learners make a prediction;
- execute or inspect a bounded source-linked artifact;
- observe a falsifiable result;
- explain the result using evidence labels;
- transfer the distinction to a held-out path.

Required evidence: a frozen learning progression across Lab 0, Lab 1, and Executable Lecture 0, plus assessment items showing that the same conceptual distinctions recur rather than three disconnected demos.

### 2. Target audience remains broad

“Advanced undergraduate, graduate, and early-stage systems researchers” spans materially different prerequisites and goals. The current labs assume shell, Git, C/C++, Python, tensors, and introductory virtual memory. That may exclude many advanced undergraduates while being too basic for systems researchers.

Required evidence: choose one primary audience for evaluation, define exclusion criteria and prerequisite checks, and treat other audiences as transfer/generalization targets.

### 3. Lab 0 risks teaching command execution rather than systems reasoning

A successful `uv sync --locked`, CMake configure, Ninja build, and executable launch is setup evidence. It becomes educational only if learners can localize failures to environment, configure, compile, executable launch, model load, or inference and explain why those phases differ.

Required evidence: seeded failure tasks, diagnostic answer keys, explanations of ownership boundaries, and a checker that evaluates diagnosis rather than only command success.

### 4. Browser GGUF lab may overclaim native relevance

The current synthetic fixture and browser parser are appropriately bounded, but the learner may still generalize browser-derived structure to native parser behavior, `mmap`, page residency, graph creation, or inference.

Required evidence: persistent evidence-kind labels, at least one checkpoint explicitly rejecting a native-runtime inference, and an independent review that the synthetic subset does not teach false general rules about unsupported GGUF types or parser behavior.

### 5. Executable lecture is authored, not captured

The viewer currently demonstrates deterministic replay of source-derived/authored material. This is an interface prototype, not runtime instrumentation. “Executable lecture” can be misleading if execution means only stepping through a prepared trace.

Required evidence: either rename the initial artifact as an authored trace lecture, or add one faithfully captured/native-captured bounded path with a documented capture method, omissions, trace-size bound, and separation between captured values and explanatory inference.

### 6. Visual novelty remains an uncontrolled confound

The information-equivalent baseline is a strong design decision, but it has not been independently reviewed or executed. Navigation, highlighting, and visualization may increase engagement without improving code tracing.

Required evidence: correctness and transfer as primary outcomes, bounded completion time, confidence calibration, accessibility completion mode, and no attractiveness score presented as educational effectiveness.

### 7. Reproducibility claims are currently contractual

The local-native and cloud-container tiers have no measured rows. Codespaces/devcontainer compatibility is not established by configuration files alone. Tool versions, network conditions, cache state, architecture, and persistent-storage behavior can change results.

Required evidence: clean-environment runs with immutable revisions, exact commands, tool versions, wall-clock definitions, failure codes, offline/degraded classification, and retained logs. Report unsupported operating systems explicitly.

### 8. Agent case-study claims need denominator data

The retrospective sample contains one success, one CI repair, and one blocked reassignment. This is selected coverage, not a longitudinal analysis. It omits the denominator of all runs, duplicate work, abandoned branches, human editing time, API/tool costs, merge conflicts, maintenance burden, and false claims caught after generation.

Required evidence: a bounded but complete sampling frame, coding rules, missing-value policy, independent audit sample, counts of accepted/revised/rejected work, human-intervention categories, elapsed/active-time proxies, CI failures, and infrastructure costs.

### 9. Stacked draft PRs are an integration risk

The active work is spread across a long stacked chain with overlapping progress implementations. Passing commit-scoped CI does not prove that the final merge order will preserve all artifacts or that `main` and Pages contain the claimed integrated system.

Required evidence: explicit merge plan, conflict resolution for overlapping progress branches, integrated-head CI, deployed-site verification, and evidence links that resolve after merge.

## Component-specific review

### Three-tier platform

- **Browser/static:** defensible for bounded parsing, simulation, trace replay, and assessments. Must never be presented as native C++ execution.
- **Local native:** should be the authoritative runtime tier, but is currently unevidenced in a clean environment.
- **Cloud container:** useful as a reproducibility fallback, not as proof of zero setup, permanent storage, free compute, or performance equivalence.

Rejected alternative: claiming the three tiers are interchangeable implementations of the same runtime.

### Lab 0

Keep model-free build/launch mandatory and learner-provided model inference optional. Do not redistribute model weights. The report must separate time-to-ready from time-to-first-token and report the latter only when a lawful learner-provided model is used.

### Lab 1

The 428-byte project-owned fixture is legally and scientifically preferable to an opaque third-party “tiny model.” The main risk is external validity: it covers a small teaching subset. Document unsupported types and test misconceptions rather than claiming general GGUF mastery.

### Trace viewer

Source revision pinning, anchor validation, deterministic replay, bounded navigation, keyboard operation, reduced-motion support, and a static transcript are necessary. They are not evidence that the viewer improves comprehension. Native-captured and authored/source-derived traces must remain visually and semantically distinct.

### Progress storage

Local-first storage, versioned export/import, corruption recovery, and privacy minimization are appropriate. Do not add authentication, cross-device sync, telemetry, raw answers, or identity before a separate privacy/security/ethics decision. A successful parse must remain `in-progress`, not mastery.

### Media pipeline

Deterministic technical graphics must remain authoritative. Generative images, audio, or video are supplemental only. Reject any technical diagram whose correctness cannot be regenerated from structured source data. Ordinary CI must not call paid APIs or regenerate approved assets. Human approval, licensing notes, accessibility artifacts, hashes, stale detection, and accepted/revised/rejected records are mandatory but do not establish pedagogical value.

## Minor concerns

- `orchestrator-state.md` is stale relative to the active branch and understates completed work.
- The root README TODO list is also stale and can misdirect scheduled agents.
- “Predict-Discover-Explain” needs item-level operationalization, not only labels.
- Time-on-task instrumentation must distinguish active work from downloads/build waits.
- Accessibility validation is still mostly structural; real keyboard and screen-reader checks remain needed.
- The source-level documentation-gap claim must remain a hypothesis until a systematic audit is completed.

## Ranked required evidence

1. Independent llama.cpp/GGML correctness review of the fixture, Lab 1 explanations, trace, source anchors, figure, and benchmark key.
2. Measured clean Ubuntu 24.04 and devcontainer Lab 0 runs, with retained logs and failure diagnostics.
3. One integrated deployed or locally reproducible Week 2 demo on a single reviewed branch.
4. Approved evaluation pathway and execution of the frozen information-equivalent benchmark or an expert-evaluation substitute.
5. Expanded retrospective dataset with a complete sampling frame, coding rules, human labor, failures, costs, and independent audit.
6. One real or faithfully captured bounded trace, or an explicit narrowing of the claim to authored trace lectures.
7. Manual keyboard/screen-reader review and documented accessibility failures/fixes.
8. Merge and deployment verification after resolving stacked/overlapping PRs.

## EAAI framing judgment

The strongest defensible future contribution is not a generic llama.cpp tutorial. It is a source-revision-pinned educational environment that teaches evidence boundaries across file format, runtime, memory, and graph execution, paired with an auditable case study of human-supervised agents maintaining that environment.

That contribution becomes credible only after the project demonstrates educational or expert usefulness, independent correctness, measured reproducibility, and honest accounting of failed agent work and human supervision.