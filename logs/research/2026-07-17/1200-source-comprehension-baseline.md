# Literature Scout run — source-comprehension baseline

- **Starting commit:** `9d05719e25a25a1da644ec17237f2f3c5259afe1`
- **Assigned dependency:** Literature and Venue Scout — identify primary evidence for a fair static-source/text baseline and code-tracing outcome measures for the executable lecture viewer.
- **Learner outcome under evaluation:** reconstruct a bounded GGUF-loading path and correctly classify captured, source-derived, authored, interpretive, and open-question evidence.

## Evidence reviewed

Primary or systematic sources were reviewed for execution-trace visualization, code-comprehension experiment design, tracing strategies, confidence measures, and remote eye-tracking validity. Full citations are recorded in `docs/publication/literature-map.md` and `docs/reference/research-ledger.md`.

## Decision

Use an information-equivalent static source/text condition rather than raw source alone. Both conditions must expose the same source excerpts, call-stack/step table, runtime-object/tensor/memory text, evidence labels, transcript, tasks, source revision, and accessibility alternatives. The viewer condition adds only synchronized navigation, coordinated highlighting, and the deterministic visualization.

Primary outcomes are frozen item-level correctness and bounded completion time. Confidence calibration, perceived difficulty/cognitive load, navigation errors, and accessibility completion mode are secondary. Visual attractiveness, clicks, and animation use are not educational outcomes.

## Rejected alternatives

- raw upstream source as the control, because it confounds information availability and interaction;
- webcam eye tracking for the first remote evaluation, because primary evidence reports validity limitations and it adds privacy burden;
- transferring historical trace-visualization effect sizes to this system;
- claiming general code comprehension when the tasks measure bounded path reconstruction and evidence classification.

## EAAI claim supported or falsified

This literature slice supports a defensible protocol for testing whether synchronized source/state/explanation navigation improves bounded code tracing. It will falsify the educational-value claim if correctness/time do not improve, if confidence becomes less calibrated, or if the viewer harms accessibility compared with the static condition.

## Files

- `docs/publication/literature-map.md`
- `docs/publication/related-work.md`
- `docs/publication/novelty-matrix.md`
- `docs/publication/eaai-fit.md`
- `docs/publication/venue-plan.md`
- `docs/reference/research-ledger.md`
- `docs/publication/agent-handoffs.md`

## Limitations and human review

No participant data was collected and no study is authorized. Independent technical review, information-equivalence review, benchmark freezing, and evaluation/ethics approval remain required. The broader usage-documentation versus source-understanding gap remains a hypothesis pending systematic audit.

## Validation

Documentation-only changes use repository-relative paths and verified external citations. Final-head Documentation CI remains authoritative.

## Next dependency

Create a versioned static-versus-viewer benchmark fixture and scoring contract after the Validation Architect accepts this literature handoff. Continue `VENUE-01` official monitoring in later runs.