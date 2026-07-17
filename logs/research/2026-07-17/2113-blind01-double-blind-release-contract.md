# BLIND-01 — double-blind release and anonymization contract

- **Starting commit:** `a4360913874766c95778d4f0194d2c79418d0136`
- **Assigned milestone:** `BLIND-01`, selected because `STACK-01`, measured Lab 0, independent review and evaluation are blocked by human or environment dependencies.
- **Learner outcome:** no learner-facing behavior changed; this protects review compliance while preserving source-linked evidence integrity.

## Files and sources

Added the double-blind plan, schema, semantic validator, non-ready example and focused tests. Used the repository-retained official EAAI-27 venue facts; no new external source or model was introduced.

## Claims

- **Verified:** the contract rejects mutable submission revisions, public repository/identity tokens, published crosswalks, silent blocker states and false readiness.
- **Interpretation:** an allowlisted clean export with an unpublished crosswalk is safer than exposing the live repository or rewriting away provenance.
- **Historical:** the live repository and PR/Actions history contain identity-bearing metadata.
- **Open Question:** final author-kit artifact-hosting details may require a later bounded revision.

## Validation

Local isolated checks: eight focused tests, example validation and Python compilation. Full Documentation CI on the branch head remains authoritative because the runtime could not resolve `github.com` for checkout.

## Failures and blockers

The local clone attempt failed with `Could not resolve host: github.com`. The plan remains `release_ready=false` because no anonymous bundle, identity scan, final license review, built-artifact accessibility result or human approvals exist.

## Human review needs

Review the anonymization policy, final allowlist, source crosswalk, license inventory, privacy boundary and generated anonymous bundle before any release.

## Evidence produced and next dependency

This run produces a machine-checkable release-readiness contract supporting EAAI double-blind compliance without claiming that an anonymous artifact exists. Next: return to `STACK-01` when the canonical progress/merge choice is approved; otherwise design `DOC-AUDIT-01` without broad implementation expansion.
