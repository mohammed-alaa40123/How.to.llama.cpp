# Run record — DATA-01 missing-value and coding policy

- **Starting commit:** `dc7a8c0bb032b3f371244fc314df93292b2ed81e`
- **Assigned milestone:** `DATA-01`, selected after `STACK-01` remained blocked and `PROGRESS-02` was found to already have overlapping implementations in PRs #23 and #24
- **Learner/publication outcome:** the longitudinal agent-workflow dataset now has an explicit rule against converting absent historical effort, cost or validation evidence into plausible-looking values
- **Files and sources inspected:** README; project state; research log and ledger; orchestrator state; evidence backlog; two-week plan; agent handoffs; latest LAB0-04 run record; PRs #21, #22, #23, #24 and #53; DATA-01 schema and first-batch examples
- **Artifact produced:** `docs/publication/retrospective-missing-value-policy.md`
- **Verified:** the first DATA-01 batch and schema exist; required numeric effort fields cannot currently represent unknown values; PROGRESS-02 already exists in two overlapping draft PRs
- **Interpretation:** excluding incomplete candidate records is safer than encoding unavailable measurements as zero before a reviewed schema migration
- **Historical:** early scheduled-run logs were not complete time-and-motion records
- **Open Question:** missingness prevalence, inter-rater agreement and workflow superiority remain unevaluated
- **Validators:** manual contract review against the existing `agent-workflow-run` schema and first-batch records; commit-scoped Documentation CI remains authoritative
- **Failures/blockers:** no local checkout or DNS path was available; `STACK-01` still requires a human canonical integration decision
- **Human review needs:** approve a future schema representation for unknown effort fields; independently double-code the predefined sample
- **Evidence produced:** a source hierarchy, prohibited imputations, coding distinctions, adjudication rules and acceptance checklist for the next extraction batch
- **Ending commit:** to be recorded by Git history for this branch
- **Next dependency:** use the policy to stage a broader DATA-01 extraction without adding records whose required effort fields are unavailable; do not duplicate PROGRESS-02 while the canonical progress choice is unresolved
