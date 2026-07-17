# llama.cpp/GGML documentation-gap audit protocol

_Last updated: 2026-07-17 21:59 Africa/Cairo_

## Purpose and claim boundary

**Open Question:** Existing llama.cpp/GGML learning resources may emphasize installation, command use, model conversion, or API examples more often than revision-pinned explanations of source-level execution, ownership, memory, graph construction, and backend scheduling.

This protocol tests that hypothesis. It does not assume the gap exists, and it does not permit convenience-selected examples to support a novelty claim.

## Audit question

Across a predefined sample of official and community learning resources, what fraction provides enough evidence for an advanced undergraduate or beginning graduate learner to reconstruct a bounded source-level path and distinguish file format, mapped bytes, runtime graph, backend execution, and token generation?

## Intended learner and educational problem

- **Learner:** advanced undergraduate or beginning graduate learner who can read C/C++ and Python but is new to llama.cpp/GGML internals.
- **Prerequisite:** basic systems programming, virtual-memory concepts, and tensor terminology.
- **Learning objective:** identify which resources support source-path reconstruction rather than only usage-oriented task completion.
- **Predicted misconception:** a successful CLI walkthrough or GGUF metadata display necessarily explains native loading, graph construction, memory residency, or backend execution.
- **Executable action:** independently code each sampled resource against the frozen rubric.
- **Observable output:** a versioned audit batch containing inclusion decisions, evidence anchors, rubric values, coder disagreements, and adjudication.
- **Formative assessment:** coders must justify each `source_path_reconstruction` rating with a stable anchor or mark the field unavailable.
- **Source revision:** every repository resource requires an immutable commit; web pages require an archived or dated capture plus retrieval date.
- **Validation method:** JSON Schema plus semantic validator, duplicate detection, sampling-frame checks, and independent coding before adjudication.
- **Accessibility fallback:** the audit artifact is plain JSON/Markdown; no visual-only evidence is required.

## Predefined sampling frame

The first audit batch must use all four strata below. A stratum may be reported as empty only after retaining the exact search queries and zero-result evidence.

1. **Official project material:** `ggml-org/llama.cpp` and `ggml-org/ggml` documentation, examples, wiki/discussions explicitly linked by maintainers, and official talks linked from project-controlled surfaces.
2. **Primary educational repositories:** executable lectures, labs, notebooks, or courses whose repository and license are identifiable.
3. **Contributor-authored technical explanations:** material by identifiable llama.cpp/GGML maintainers or contributors, with the contribution relationship recorded.
4. **Community tutorials and walkthroughs:** independently authored articles, videos, notebooks, or repositories discovered by the frozen search process.

### Search process

For every stratum, retain:

- exact query string;
- search surface;
- UTC retrieval timestamp;
- result rank inspected;
- canonical URL;
- inclusion/exclusion decision and reason;
- immutable revision, publication date, or archived capture where available.

The initial batch uses the first 20 unique results per query after deduplication. Search queries must include both usage-oriented and source-oriented terms, for example:

- `llama.cpp tutorial`
- `llama.cpp source code walkthrough`
- `GGML graph construction explanation`
- `GGUF loading source walkthrough`
- `llama.cpp mmap scheduler backend internals`

Queries may be expanded only in a new versioned protocol; they must not be changed after coding begins.

## Inclusion and exclusion

Include a resource when it is publicly accessible, substantially educational, and contains material about llama.cpp, GGML, or GGUF implementation/use.

Exclude only with one frozen reason:

- duplicate or mirror;
- inaccessible or removed;
- non-educational announcement;
- unrelated despite query match;
- language unsupported by the audit team;
- license or access terms prevent retained analysis.

Do not exclude a weak resource because it lacks source depth; absence of depth is an audit result.

## Frozen coding rubric

Each included resource receives categorical values with evidence anchors:

| Dimension | Values | Interpretation |
|---|---|---|
| revision clarity | `immutable`, `dated_only`, `mutable`, `absent` | Whether implementation claims can be tied to a stable source state |
| source references | `line_or_symbol`, `file_only`, `repository_only`, `none` | Precision of source linkage |
| execution-path coverage | `reconstructable`, `partial`, `usage_only`, `none` | Whether a bounded call/data path can be reconstructed |
| runtime evidence | `native_captured`, `source_derived`, `authored_only`, `none` | Strongest evidence kind used |
| conceptual boundaries | `explicit`, `partial`, `conflated`, `not_applicable` | Whether format/mapping/graph/execution/output distinctions are preserved |
| learner action | `predict_execute_explain`, `execute_observe`, `read_or_watch`, `none` | Strongest learner activity |
| reproducibility | `locked_and_tested`, `specified`, `informal`, `none` | Environment and validation quality |
| accessibility | `multiple_modes`, `text_equivalent`, `unspecified`, `blocked` | Availability beyond a single visual/audio mode |
| license clarity | `explicit_reuse`, `explicit_restricted`, `unclear`, `not_applicable` | Reuse boundary |

The audit's primary outcome is the proportion of included resources rated `reconstructable` with `line_or_symbol` source references and `explicit` conceptual boundaries. Secondary outcomes are distributions across all dimensions and differences by stratum. No causal or population-wide claim is permitted.

## Reliability and adjudication

- Two coders independently code every included resource.
- Coders retain anchors and notes before seeing the other coder's labels.
- Exact agreement and Cohen's kappa are reported only for dimensions where the statistic is appropriate and the sample is sufficient.
- Every disagreement remains visible and receives an adjudication rationale.
- A single-coder batch may test tooling but cannot close `DOC-AUDIT-01` or support the documentation-gap claim.

## Verified, Interpretation, Historical, Open Question

### Verified

- The repository already labels the documentation-gap statement as a hypothesis.
- The research ledger contains official llama.cpp/GGML sources and a first-pass warning that broad searches were noisy.
- The target audience and source-level learning boundaries are frozen in the orchestrator state.

### Interpretation

- Stratified, query-retaining sampling is more defensible than selecting exemplary tutorials or only official documentation.
- Treating missing source depth as an outcome avoids excluding evidence that could falsify the gap hypothesis.

### Historical

- Earlier project work identified useful primary educational patterns such as CS336 executable lectures and MLSysBook labs, but these do not establish a llama.cpp documentation gap.

### Open Question

- Whether the sampled resource ecosystem actually lacks revision-pinned source-path explanations.
- Whether differences between official and community strata are large enough to matter educationally.
- Whether non-English resources materially change the result; the first protocol records unsupported languages as an explicit limitation.

## Acceptance criteria

`DOC-AUDIT-01` may close only when:

1. a frozen protocol record validates;
2. every query/result decision is retained;
3. every included item has two independent coding records;
4. disagreements are adjudicated without deleting original labels;
5. limitations and missing strata are explicit;
6. the final conclusion is one of `supported`, `revised`, `rejected`, or `inconclusive`;
7. no manuscript novelty claim exceeds the audited frame.

## Rejected alternatives

- counting only resources already known to the project;
- auditing only official documentation;
- treating search-engine snippets as resource content;
- scoring visual polish as source-level understanding;
- inferring educational effectiveness from documentation features;
- strengthening the gap claim before independent coding and adjudication.
