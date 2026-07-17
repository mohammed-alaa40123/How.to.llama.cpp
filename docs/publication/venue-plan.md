# EAAI-27 venue plan

_Last verified: 2026-07-17_

This file records current official venue facts and repository actions. It is not manuscript prose. Reverify the official call before submission because venue instructions can change.

## Verified venue facts

Primary source: [EAAI-27 Call for Participation](https://aaai.org/conference/aaai/aaai-27/eaai-27-call/).

| Item | Verified EAAI-27 requirement |
|---|---|
| Venue | 17th Symposium on Educational Advances in Artificial Intelligence, co-located with AAAI-27 in Montréal |
| Symposium dates | February 21-23, 2027 |
| Abstract deadline | September 1, 2026, 11:59 PM UTC-12 |
| Paper deadline | September 8, 2026, 11:59 PM UTC-12 |
| Notification | November 17, 2026 |
| Camera ready | December 14, 2026 |
| Intended area | Main Track, Area 2: Experience Report and Innovative Practice |
| Length | Up to 7 pages plus up to 2 pages of references |
| Review | Double-blind; supplementary materials must also be anonymous |
| Presentation | In-person presentation is required if accepted |
| Submission system | EasyChair, as linked by the official call |
| Empirical guidance | SIGSOFT Empirical Standards are suggested but not mandatory |

The AAAI-27 main-track deadlines on July 21 and July 28, 2026 are not EAAI deadlines. The official AAAI-27 page explicitly states that track-specific deadlines may differ and links the EAAI-27 call.

## Scope and track fit

### Verified

EAAI-27 focuses on teaching and learning **about Artificial Intelligence**, including education and training of AI practitioners and users. It explicitly excludes work whose focus is using AI to support teaching of unrelated subjects.

### Interpretation for this project

How.to.llama.cpp fits only when its educational target is stated as AI-systems and inference education:

- how model artifacts are represented in GGUF;
- how an AI inference engine constructs and executes GGML graphs;
- how learners distinguish browser-derived, source-derived, authored, and native-captured evidence;
- how resource and runtime behavior affect AI-system understanding;
- how educational material for an evolving AI codebase is maintained under human supervision.

A generic “learn C++, debugging, or documentation with AI agents” framing is out of scope or substantially weaker.

## Area 2 evidence obligations

The official Area 2 language requires the context of use, data collected, and rich reflection on what did or did not work and why. The current repository therefore needs all of the following before manuscript integration:

1. **Context of use:** one frozen primary learner or expert population, prerequisites, setting, and exclusions.
2. **Actual use evidence:** an approved learner study, expert-usefulness evaluation, or other defensible deployment pathway; implementation contracts alone are insufficient.
3. **Collected data:** frozen measures, sampling frame, missing-data rules, and ethical/consent decision.
4. **Reflection:** retained failures, repairs, rejected outputs, human interventions, maintenance burden, and costs across a bounded run population.
5. **Technical soundness:** independent review of the GGUF fixture/parser, trace, explanations, deterministic figure, and benchmark answer key.
6. **Novelty against prior work:** systematic literature and documentation audit, not anecdotal gap claims.
7. **Broader value:** design lessons that transfer by mechanism rather than asserting that llama.cpp represents every AI system.

## Review-criteria mapping

| Official criterion | Required repository evidence |
|---|---|
| Relevance | Explicit AI-systems learning objectives and exclusions from generic programming education |
| Significance to intended audience | Frozen primary audience plus evidence that the selected misconceptions and tasks matter to that audience |
| Engagement with prior work | Verified literature map and systematic documentation audit |
| Novelty | Novelty matrix separating executable traces, evidence labels, reproducibility, progress, and supervised maintenance from existing tools |
| Technical soundness | Independent technical review and correction history |
| Clarity | Coherent three-experience progression and visible evidence boundaries |
| Evaluation of claims/results | Approved and completed evaluation using frozen outcomes and fair baselines |
| Ethics/inclusivity | Privacy-minimizing progress, accessibility review, AI-use disclosure, consent/ethics decision, and representation review for optional media |

## Double-blind and artifact plan

The repository is public and identifying. Before submission, create a separate versioned anonymized evidence snapshot. At minimum it must:

- remove author names, usernames, institution references, branch names, commit authorship, acknowledgements, and identifying URLs;
- preserve immutable content hashes and source revisions without exposing repository ownership;
- anonymize structured agent logs while retaining roles, decisions, failures, validators, and effort/cost fields;
- provide anonymous supplementary links only if permitted by the final instructions;
- keep every essential result and limitation in the seven-page paper because reviewers are not required to inspect supplements.

Do not rewrite the live repository history solely for anonymity. Produce an auditable anonymized release derived from a frozen evidence commit.

## Internal planning dates

These are project-management targets, not venue deadlines:

| Internal target | Condition |
|---|---|
| July 31, 2026 | Integrated vertical slice and evidence-gap report; no manuscript drafting unless the formal gate is satisfied |
| August 7, 2026 | Freeze evaluation pathway, independent-review plan, retrospective sampling frame, and anonymization design |
| August 17, 2026 | Evidence freeze candidate: integrated demo, measured reproducibility, technical review, and initial evaluated-use evidence |
| August 24, 2026 | Go/no-go review against Area 2 requirements and seven-page evidence budget |
| September 1, 2026 | Official abstract deadline |
| September 8, 2026 | Official paper deadline |

The internal dates may be revised by the orchestrator. They must never be represented as official EAAI dates.

## Human-action blockers

- Approve an evaluation pathway and complete any required ethics review before recruitment or personal-data collection.
- Nominate an independent llama.cpp/GGML technical reviewer.
- Decide who can satisfy the required in-person presentation and whether travel funding and visa timing are viable.
- Approve the anonymized artifact-release plan.
- Resolve and merge the stacked PR chain into an integrated evidence branch.

## Exact manuscript-start condition

Do not begin abstract, introduction, related-work, or results drafting until:

- the primary audience, learning progression, research questions, and claims are stable;
- the integrated Lab 0, Lab 1, trace viewer, deterministic figure, media contract, and progress path are reproducible;
- Ubuntu and devcontainer Lab 0 measurements exist;
- at least one fair baseline comparison or approved evaluated-use pathway is completed;
- independent technical correctness review is accepted;
- the retrospective agent dataset has a bounded sampling frame, coding rules, denominator, human effort, failures, and costs;
- major rejection risks are resolved or explicitly scoped out;
- the anonymization and in-person presentation plans are approved;
- the official EAAI-27 call is reverified.

## Rejected alternatives

- Do not use AAAI main-track July deadlines for EAAI planning.
- Do not claim Area 2 readiness from schemas, CI, or a deployed demo without use data and reflection.
- Do not move essential evidence exclusively into supplementary material.
- Do not position optional generative media attractiveness as an educational outcome.
- Do not submit as a Model AI Assignment without a separate track-fit decision and review of its special instructions.