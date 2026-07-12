# Interactive graph-construction and MoE links

- Run time: 2026-07-12 19:50 Africa/Cairo
- Scope: connect the interactive GGUF/graph view and graph workflow entries to the canonical graph-construction and MoE chapter
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream graph/MoE reference: `6b4dc2116a92c5c8f2782bfe51fabe5ee66fb5ef`

## Artifact

Updated `docs/assets/interactive/llama-foundations-explorer.html` with direct canonical-documentation routes for:

- graph construction;
- graph expansion;
- MoE router logits, `selection_probs`, and `selected_experts`;
- the GGML computation-graph system layer;
- the Build or reuse graph workflow step.

The MoE card also records the cache-design interpretation that a per-layer expert LRU should use `(layer_id, expert_id)` keys and track expert weight ranges rather than whole graph nodes.

## Verified

- The Graph construction card links to section 2 of `docs/ggml/graph-construction-and-moe.md`.
- The Graph expansion card links to section 3.
- The new MoE router and selected experts card links to section 5.
- The GGML computation graph system layer and Build or reuse graph workflow step link to the canonical chapter root.
- All local routes use `target="_top"`, so navigation escapes the iframe.
- Existing GGUF, model-placement, Context, memory, synchronization, and file-map views remain present.

## Interpretation

- Keeping `logits`, `selection_probs`, and `selected_experts` visible as separate stages prevents cache-aware routing from being confused with final expert-weight modification.
- The graph is the source of selected expert IDs, but expert residency belongs to model/backend storage; therefore cache metadata should not be keyed by ephemeral graph-node identity.

## Historical

- This is the third canonical-documentation integration in the explorer, after `llama_context` and GGUF/model placement.

## Open questions

- Replace hard-coded routes and section anchors with generated, versioned page metadata.
- Add CI validation that interactive local links and anchors resolve against the built MkDocs site.
- Add exact generated line-level source links to the canonical graph chapter.
- Add post-compute selected-expert traces before prototyping routing or residency changes.

## Sources inspected

- Complete repository README, project state, research log, research ledger, and latest available detailed note.
- Current interactive foundations explorer.
- Canonical graph-construction and MoE chapter.
- No external source changed, so the research ledger is unchanged.

## Validation

- Connector-side update succeeded and the changed file was re-fetched; all five new canonical routes and the router/cache labels are present.
- The execution container still returns `Could not resolve host: github.com`, so a local checkout, script validation, and `mkdocs build --strict` could not run.
- Combined commit status for the final research-log commit returned an empty status list.
- The connector's commit-workflow endpoint returned `workflow_runs: []`; because it filters to pull-request-triggered runs, push-triggered Documentation CI and Pages deployment remain unverified.
- Site-specific web search returned no indexed result for the project. Direct opening of the Pages URLs was rejected by the browser safety gate because no prior search result exposed those exact URLs, so live HTTP status and rendered content remain unverified.

## Next priority

Create the canonical `llama_model` object page, covering architecture dispatch, tensor registration, layer arrays, buffer ownership, `build_graph()` delegation, sharing across contexts, and teardown.