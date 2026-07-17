# EAAI adversarial review — 2026-07-17 04:58 Africa/Cairo

## Starting point

- Base branch: `agent/fix-strict-mkdocs-handoff-links`
- Starting commit: `5bbc595b9e2d076ddbc8393514e2a9f26fab9fa8`
- Assigned milestone: Week 1 architecture and acceptance-criteria review

## Evidence inspected

- orchestrator state, evidence backlog, two-week execution plan and agent handoff ledger;
- trace, Lab 0, synthetic GGUF and progress contracts summarized by the current stack;
- Documentation CI run `29546570700`, which completed successfully on the base commit.

## Reviewer outcome

Recommendation remains **reject in current form**. No fatal architecture flaw was found, but seven major concerns remain: no educational outcome evidence; feature-collection risk; undefined multi-agent comparative contribution; unproven native/cloud reproducibility; untested trace-viewer learning value; absent independent technical review; and excessive two-week scope.

## Artifacts produced

- `docs/publication/reviewer-notes.md`
- `docs/publication/claims-evidence-table.md`
- `docs/publication/rejection-risks.md`
- `docs/publication/eaai-review-scorecard.md`

## Ranked next priorities

1. Approve an educational evaluation pathway and define misconception/code-tracing measures.
2. Nominate an independent llama.cpp/GGML reviewer.
3. Produce clean-environment Lab 0 reproducibility evidence and diagnostics.
4. Validate trace source links, keyboard replay and static fallback before viewer expansion.
5. Extract the longitudinal agent dataset and freeze fair baseline tasks.
6. Implement the media manifest validator; keep generated media optional.
7. Cut optional media and cloud polish before compromising the coherent Lab 0 + GGUF + trace vertical slice.

## Claims and limitations

- **Verified:** the base commit's Documentation CI run passed.
- **Interpretation:** the architecture is defensible but insufficient for an EAAI experience report without use/evaluation evidence.
- **Open question:** whether a trace viewer improves code tracing over static source plus text.
- No manuscript prose, participant data, model download or paid API call was introduced.
