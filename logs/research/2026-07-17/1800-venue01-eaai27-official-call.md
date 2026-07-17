# VENUE-01 — official EAAI-27 call verification

- **Run date:** 2026-07-17 18:00 Africa/Cairo
- **Role:** Literature and Venue Scout
- **Starting commit:** `4c72b8908c0d41941a7f61f2d041a2668a788af5`
- **Assigned dependency:** `VENUE-01`
- **Learner outcome affected:** publication framing and evaluation requirements for the executable-learning environment; no learner-facing behavior changed

## Question

Has the official EAAI-27 call been published, and what venue requirements materially change the evidence roadmap?

## Sources checked

1. Official EAAI-27 Call for Participation: https://aaai.org/conference/aaai/aaai-27/eaai-27-call/
2. Official AAAI-27 conference page: https://aaai.org/conference/aaai/aaai-27/
3. Official EAAI-26 call, used only as historical comparison: https://aaai.org/conference/aaai/aaai-26/eaai-26-call/

Checked on 2026-07-17. No bibliographic, API, cost or deadline detail was inferred from unofficial sources.

## Verified findings

- The EAAI-27 call is live.
- Abstracts are due September 1, 2026 at 11:59 PM UTC-12.
- Papers are due September 8, 2026 at 11:59 PM UTC-12.
- Notification is November 17, 2026; camera ready is December 14, 2026; the symposium is February 21-23, 2027 in Montréal.
- The likely fit is Main Track Area 2, Experience Report and Innovative Practice.
- Area 2 requires context of use, data collected, and rich reflection on what did or did not work and why.
- EAAI-27 focuses on education about AI; using AI to teach unrelated programming or systems topics is explicitly outside scope.
- Review criteria include audience significance, prior work, novelty, technical soundness, evaluation, and ethics/inclusivity.
- Empirical submissions are encouraged, but not required, to use SIGSOFT Empirical Standards.
- Submissions and supplements are double-blind; papers are up to seven pages plus two reference pages; reviewers need not inspect supplementary material.
- In-person presentation is required if accepted.
- AAAI main-track July deadlines are not EAAI deadlines.

## Interpretation

The project can fit EAAI only as AI-systems and inference education. The strongest Area 2 framing combines the executable environment with reflective evidence from its supervised repository-native maintenance process. The agent case study cannot replace evidence of actual educational use.

## Open question

Whether a bounded expert-usefulness evaluation, without a classroom deployment, supplies sufficient use context and data for a competitive Area 2 report remains unresolved. The call does not answer this; the evaluation pathway requires human approval and later adversarial review.

## Concrete requirement added

Create `BLIND-01`: a versioned double-blind evidence-release plan and anonymized snapshot. Essential results must fit in the seven-page paper because reviewers are not required to inspect supplementary artifacts.

## Rejected alternative

Do not treat the project as a Model AI Assignment merely because it includes labs, and do not use AAAI main-track deadlines. The current contribution is a broader learning environment and longitudinal experience report.

## Files changed

- `docs/publication/literature-map.md`
- `docs/publication/venue-plan.md`
- `docs/publication/eaai-fit.md`
- `docs/publication/evidence-backlog.md`
- this run log

## Validation and limitations

- Official URLs and exact dates were rechecked in this run.
- No manuscript prose, participant recruitment, personal data, model download, paid API call or learner-facing implementation was introduced.
- MkDocs and repository CI remain the authority for link and integration validation.
- The active orchestrator file still contains the now-stale statement that no official EAAI-27 call is available; the Orchestrator must refresh its single source of truth after this branch is integrated.

## Evidence produced

- A venue plan with deadlines, Area 2 obligations, review-criteria mapping, anonymization requirements, internal go/no-go dates and manuscript-start gates.
- An EAAI fit matrix separating defensible current evidence from venue-critical gaps.
- A literature-map venue slice based only on official AAAI sources.
- `VENUE-01` marked evidenced and `BLIND-01` added as a blocker.

## Human-review needs

- Approve the evaluation pathway.
- Nominate the independent technical reviewer.
- Approve an anonymized artifact strategy.
- Confirm an in-person presenter, travel funding and visa feasibility.

## Next dependency

Conduct a predefined systematic audit of official and community llama.cpp/GGML learning resources before upgrading the source-level documentation-gap hypothesis.