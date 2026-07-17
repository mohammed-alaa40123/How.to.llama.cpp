# DATA-01 retrospective evidence contract

## Run identity

- **Starting commit:** `9d05719e25a25a1da644ec17237f2f3c5259afe1`
- **Assigned milestone:** highest-priority dependency-safe task after the real `LAB0-02` environment run was blocked
- **Learner/research outcome:** make scheduled-agent assignments, failures, corrections, validation, human supervision and effort analyzable without collecting learner identity or raw conversational content

## Dependency decision and blocker

`LAB0-02` contract CI run `29565651085` passed. The remaining highest-priority action was a real Ubuntu local-native or devcontainer row. The execution environment could not resolve `github.com`, so it could not clone the connected repository or pinned llama.cpp checkout. This is an environment blocker, not a protocol failure.

The next dependency-safe orchestrator assignment was `DATA-01`.

## Files added or changed

- `schemas/agent-workflow-run.schema.json`
- `scripts/validate_agent_workflow_run.py`
- `progress/examples/agent-workflow-run-v0.json`
- `tests/test_validate_agent_workflow_run.py`
- `docs/publication/retrospective-data-contract.md`
- `docs/publication/evidence-backlog.md`
- `docs/reference/project-state.md`
- this run record

## Evidence and validator behavior

The contract records:

- stable run ID and specialist role;
- orchestrator assignment, priority, dependency state, selection reason and blockers;
- immutable starting and ending commits and branch identities;
- repository-relative outputs marked accepted, revised or rejected;
- validators, failures, resolutions and commit-scoped CI state;
- human-review requirement, decisions and status;
- agent turns, tool calls, paid-generation count, external API cost and optional human minutes;
- claims labelled Verified, Interpretation, Historical or Open Question.

The semantic validator rejects mutable revisions, blocked work without a blocker, unsafe/duplicate output paths, unexplained revised or rejected outputs, passed CI without a run ID, paid generation without recorded cost, Verified claims without evidence, and privacy-sensitive fields such as identity, session/device identifiers, raw prompts/responses, secrets and API keys.

Eight focused tests cover the valid example and key malformed cases.

## EAAI claim supported or falsified

**Candidate claim:** repository-native scheduled-agent work can be transformed into an auditable longitudinal dataset that preserves assignments, corrections, validation, human boundaries and cost proxies.

**Falsification conditions:** historical runs cannot be represented without inventing missing values; records silently include identity or raw conversational data; accepted/revised/rejected outcomes cannot be reconstructed consistently; or the schema cannot support a fair baseline comparison.

## Truth labels

- **Verified:** the schema, validator, one example extraction, eight tests and evidence-boundary document are committed on the branch.
- **Interpretation:** normalized records may support analysis of correction rates, validator coverage and human-review burden.
- **Historical:** existing logs and PR handoffs contain similar information in prose with inconsistent structure.
- **Open Question:** final-head CI, historical coverage, extraction reliability, human-effort accuracy and workflow advantage remain unevidenced.

## Validation and limitations

- Local unit and MkDocs execution were blocked by the same unavailable checkout/network environment; commit-scoped GitHub Actions is authoritative.
- The example is a hand-authored extraction of the completed Lab 1 run, not a complete dataset.
- Tool-call and human-time fields must be reported as unavailable rather than guessed when historical evidence is missing.
- No participant data, learner identity, model, telemetry, credential, paid API call or manuscript prose was introduced.
- Independent review is still required before using the extracted dataset for a publication claim.

## Human-review needs

- Approve the retrospective coding rules before large-scale extraction.
- Decide how missing tool-call and human-time values should be represented in the future schema revision.
- Review the first multi-run extraction for consistency before `BASE-01` begins.

## Ending state

The final branch head and commit-scoped CI run are pending. `DATA-01` remains in progress until CI passes and a reviewed first batch of historical run records is extracted.

## Next dependency

If CI passes, extract a bounded first batch spanning at least one successful increment, one CI repair and one blocked/dependency-safe reassignment. Keep `LAB0-02` open until actual Ubuntu and devcontainer rows are retained.
