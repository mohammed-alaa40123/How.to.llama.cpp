# Lab 0 checker interface increment

- **Starting commit:** `d4050abafbe2c6f66939147b3f3240ae7faf832a`
- **Assigned milestone:** Week 1 Lab 0 machine-readable checker interface
- **Learner outcome:** distinguish environment, configuration, compilation, executable launch, model loading, and inference evidence
- **Ending branch:** `agent/eaai-two-week-execution-plan`

## Files added

- `docs/labs/lab0-checker-interface.md`
- `schemas/lab0-check-report.schema.json`
- `scripts/validate_lab0_report.py`
- `labs/lab0/examples/model-free-passing-report.json`
- `tests/test_validate_lab0_report.py`

## Claims

### Verified

The interface has six separate phase states and claim booleans. The dependency-free validator rejects impossible success chains, path disclosure in a redacted model basename, and any model-free report that claims model loading or inference.

### Interpretation

A machine-readable state boundary makes setup evidence auditable and turns the predicted misconception—"build or launch equals inference"—into a testable formative assessment.

### Open question

The exact bounded llama.cpp target, supported OS/container matrix, diagnostic-code taxonomy, and actual command runner remain for the next Lab 0 implementation increment.

## Validation evidence

Five focused unit tests were added for the valid model-free report and four semantic failure cases. The connector environment could not execute the tests locally, so final evidence depends on Documentation CI for the resulting branch head.

## Safety and privacy

The report schema stores revisions, platform labels, phase evidence, optional redacted basename, and optional checksum. It forbids full model paths by validator policy and contains no prompts, generated text, model bytes, telemetry, credentials, or personal identifiers.

## Next dependency

Add the machine-readable trace schema and authored sample trace contract, unless the orchestrator publishes a different dependency order.