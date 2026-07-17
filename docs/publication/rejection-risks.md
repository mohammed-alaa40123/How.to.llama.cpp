# EAAI rejection risks

_Last reviewed: 2026-07-17 17:15 Africa/Cairo_

Severity meanings:

- **Fatal:** invalidates the central submission claim if unresolved.
- **Major:** likely rejection unless directly addressed with evidence.
- **Minor:** weakens clarity, reproducibility, or reviewer confidence.

## Fatal risks

| Rank | Risk | Why it is fatal | Required closure evidence | Owner / dependency |
|---|---|---|---|---|
| F1 | No educational or expert-usefulness evaluation | An EAAI experience report cannot rest on implementation and CI alone. | Approved pathway plus completed frozen assessment or defensible expert-evaluation alternative; correctness/transfer outcomes and limitations. | Human + Validation Architect; `EVAL-01`, `BASE-01` |
| F2 | No independent technical correctness review | All educational artifacts are produced and validated within the same project process. Systematic source errors could survive internal consistency checks. | Signed/dated review of fixture, parser, explanations, trace, anchors, figure, benchmark items and answer key; correction log. | Human reviewer; `REVIEW-01` |
| F3 | No measured native/cloud reproducibility | Two of three platform tiers are supported only by contracts, not executions. | Clean Ubuntu 24.04 and devcontainer model-free records with exact revisions, commands, versions, logs and time-to-ready. | Validation Architect; `LAB0-03`, `LAB0-04` |
| F4 | Agent case study lacks a longitudinal dataset | Three selected records cannot support general claims about scheduled-agent maintenance. | Bounded complete sampling frame, coding manual, missing-value rules, denominator counts, human/cost proxies and independent audit. | Validation Architect + Human; `DATA-01` |

## Major risks

| Rank | Risk | Reviewer challenge | Required evidence gate |
|---|---|---|---|
| M1 | Contribution is a collection of tools | What unifying learning mechanism connects setup, GGUF parsing and source tracing? | Cross-experience concept map and frozen progression showing prediction, execution/inspection, evidence-labelled explanation and transfer. |
| M2 | “Executable lecture” overstates authored replay | What exactly executes, and which values are captured? | One native/faithfully captured bounded trace or narrower naming/claims; capture provenance and omissions. |
| M3 | Visual novelty confounds comprehension | Could the viewer merely be more attractive? | Information-equivalent baseline execution with correctness/transfer primary; no attractiveness proxy. |
| M4 | Broad target audience | Are prerequisites and outcomes appropriate for one population? | One primary evaluation audience, prerequisite screener and explicit transfer populations. |
| M5 | Lab 0 is command-following | Does the lab teach diagnosis and phase ownership? | Seeded failures, explanation rubric and diagnosis scoring beyond command completion. |
| M6 | Browser simulation creates false native intuitions | Will learners infer `mmap`, residency, graphs or inference from a parser? | Explicit evidence-kind checks, misconception tasks and independent review of exclusions/unsupported types. |
| M7 | No integrated demonstration | Do individually passing branches compose? | Single integration branch, clean end-to-end acceptance script, integrated CI and deployed-site verification. |
| M8 | Stacked PR chain is operationally fragile | Which artifacts actually reach `main`, and how are overlapping branches resolved? | Dependency-ordered merge plan, conflict resolution, final commit map and post-merge link/Pages checks. |
| M9 | Human supervision and cost are underreported | Is the “agent” contribution actually hidden human labor? | Human decision/time categories, failed/duplicate generations, API/tool cost proxies, merge/maintenance effort. |
| M10 | Generalization is asserted rather than demonstrated | Why should llama.cpp-specific artifacts transfer? | Mechanism-level limits analysis and preferably one bounded replication outside llama.cpp. |
| M11 | Documentation-gap motivation is anecdotal | Is the claimed gap actually widespread? | Systematic documentation audit with predefined corpus and coding criteria; keep hypothesis until complete. |
| M12 | Accessibility evidence is structural only | Can keyboard and screen-reader users complete the tasks? | Manual keyboard, screen-reader, focus, contrast, reduced-motion and static-fallback review with defect log. |

## Minor risks

| ID | Concern | Required action |
|---|---|---|
| m1 | `orchestrator-state.md` is stale relative to the active stack. | Refresh the single source of truth before the next assignment. |
| m2 | Root README priorities are stale. | Reconcile TODOs with the evidence backlog to prevent duplicate work. |
| m3 | Time-to-ready may mix active work with download/build waiting. | Record phase timestamps and report active versus elapsed definitions. |
| m4 | Cloud persistence and cost expectations may be misunderstood. | Document ephemeral storage, prebuild/billing caveats and offline limits. |
| m5 | Progress schema may be mistaken for research instrumentation. | Keep local resume data separate from any consented research dataset. |
| m6 | Media lifecycle specimens are not technical figures. | Preserve the explicit non-evidence label and do not cite them for correctness. |
| m7 | Controlled taxonomies for rejection/revision reasons are absent. | Define a small coding vocabulary before larger retrospective extraction. |
| m8 | Unsupported GGUF field types are not central in the learner-facing story. | Publish the supported subset and failure behavior prominently. |

## Rejected alternatives

- Comparing the viewer with raw upstream source rather than information-equivalent static material.
- Calling model-free executable launch “inference.”
- Redistributing an unreviewed tiny model as a universal fixture.
- Treating JupyterLite/browser parsing as native llama.cpp execution.
- Using a generative image as authoritative technical evidence.
- Using attractiveness, page views, clicks or animation use as learning outcomes.
- Adding authenticated progress sync or telemetry before privacy, security, consent and ethics review.
- Inferring agent-workflow effectiveness from selected success stories.
- Starting manuscript integration because contracts and CI pass.

## Exact manuscript gate

Manuscript writing remains blocked until all fatal risks are closed and the following are simultaneously evidenced:

1. stable framing and one primary target audience;
2. integrated reproducible vertical slice;
3. independent technical correctness review;
4. approved and completed usefulness/evaluation pathway;
5. longitudinal retrospective dataset with human/cost disclosure;
6. at least one fair baseline comparison;
7. current official EAAI requirements;
8. no unresolved major concern that invalidates the central contribution.