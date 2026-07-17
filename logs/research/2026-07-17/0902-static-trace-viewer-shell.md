# Documentation Builder run — VIEW-01 static trace viewer shell

- **Starting commit:** `e2361200d80028c86205359979487a94b958f306`
- **Assigned milestone:** `VIEW-01`, unblocked after TRACE-02 passed Documentation CI run `29556540213`.
- **Learner outcome:** a learner can move through three pinned GGUF-loading teaching steps, predict the evidence category, and inspect source, objects, tensor shapes and memory events without mistaking the authored trace for native capture.

## Files and sources

- `scripts/build_trace_viewer_data.py`
- `docs/assets/data/gguf-load-authored-v0.viewer.json`
- `docs/assets/javascripts/trace-viewer.js`
- `docs/executable-lectures/trace-viewer.md`
- `tests/test_trace_viewer_shell.py`
- `mkdocs.yml`
- `docs/publication/evidence-backlog.md`
- `docs/reference/project-state.md`
- Source trace: `executable_lectures/traces/gguf-load-authored-v0.json`
- Primary technical source remains `ggml-org/llama.cpp` revision `e3546c7948e3af463d0b401e6421d5a4c2faf565` through the TRACE-02 source-anchor lock.

## Claims

### Verified

TRACE-02 passed commit-scoped Documentation CI. The new viewer payload is a deterministic projection of the validated trace. The shell includes Previous/Next buttons, Arrow/Home/End keyboard operation, clamped boundaries, live text status, evidence labels, pinned source links, and an ordered static transcript.

### Interpretation

A framework-free static viewer is the smallest useful executable-lecture slice because it exercises trace replay and evidence boundaries without introducing native instrumentation, package-manager churn, or a visual-novelty claim.

### Historical

The trace schema and authored sample existed before immutable source resolution. TRACE-02 corrected plausible-but-false source anchors before this viewer was allowed to render them.

### Open question

The viewer has not been compared against a static source-and-text baseline, evaluated with learners or experts, or independently reviewed for pedagogical anchor selection.

## Validators

- generated payload must exactly equal `build_payload(trace)` rendered with stable ordering;
- step sequences and evidence kinds must remain intact;
- every source URL must contain the immutable revision;
- the lesson page must declare all ten learning-contract fields;
- accessibility markers, transcript fallback and reduced-motion behavior are required;
- JavaScript must expose bounded Arrow/Home/End navigation and avoid `eval` or unescaped trace-field HTML assignment.

## Failures and limitations

The runtime environment could not clone GitHub for local execution because outbound DNS resolution was unavailable. Repository tests therefore remain subject to commit-scoped GitHub Actions. The viewer intentionally does not render figures or native source text in this increment; it links pinned source and exposes structured state. Missing optional trace arrays degrade to explanatory text.

## Human-review needs

- independent llama.cpp/GGML review of the three selected anchors;
- accessibility review with keyboard and screen-reader tooling after deployment;
- approval of a later evaluation pathway and static-source/text baseline.

## Evidence produced

One bounded static executable-lecture prototype, deterministic data builder, generated payload, focused tests, site integration, explicit claim boundary and durable run record.

- **Ending commit:** recorded by the final PR head.
- **Next dependency:** obtain passing final-head Documentation CI; only then mark VIEW-01 evidenced.
