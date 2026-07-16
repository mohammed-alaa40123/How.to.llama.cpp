# EAAI validation plan

_Last updated: 2026-07-17 02:06 Africa/Cairo_

This document defines evidence protocols for the executable-learning roadmap. It records designs and validators, not claims of demonstrated learner benefit.

## Current bounded protocol: executable lecture trace integrity

### EAAI claim supported or falsified

**Candidate claim:** a repository-native, human-supervised agent workflow can produce source-pinned executable-lecture artifacts whose evidence boundaries, replay order, accessibility fallback, and provenance are machine-checkable.

This protocol supports the claim only if valid traces remain deterministic and malformed or overstated evidence is rejected. It would falsify or weaken the claim if traces can silently use mutable source references, skip or reorder steps, claim native capture from authored data, escape repository paths, omit static fallbacks, or grow without practical bounds.

### Artifact under test

- Schema: `schemas/executable-trace.schema.json`
- Semantic validator: `scripts/validate_executable_trace.py`
- Authored fixture: `executable_lectures/traces/gguf-load-authored-v0.json`
- Focused tests: `tests/test_validate_executable_trace.py`

The authored fixture is intentionally **not** native runtime evidence. It establishes the minimum trace/viewer contract before invasive instrumentation.

### Required invariants

1. `schema_version` is explicit and currently fixed at `0.1.0`.
2. Upstream source uses `owner/repository` and a full immutable 40-character commit SHA.
3. Trace-level capture kind is one of `native-captured`, `source-derived`, or `authored-example`.
4. Step sequences are unique, ordered, contiguous, and zero-based; this defines deterministic forward/back replay semantics.
5. Step IDs are unique.
6. Source and figure paths are repository-relative and reject traversal.
7. Every step supplies a source location, explanation ID, evidence kind, and meaningful static summary.
8. Runtime objects, tensor shapes, memory events, and figures carry their own evidence kind.
9. An authored trace cannot contain a native-captured step or nested artifact.
10. Figures require meaningful alt text.
11. Trace files are bounded to 2 MiB, 500 steps, and bounded nested collections.
12. Optional runtime collections may be absent; the viewer must treat absence as unavailable evidence rather than failure or zero.

### Test cases

| Case | Expected result | Educational/evidence risk addressed |
|---|---|---|
| Committed authored GGUF trace | Pass | Establish deterministic minimum fixture |
| Noncontiguous step sequence | Reject | Prevent ambiguous forward/back replay |
| Native-captured claim inside authored trace | Reject | Prevent evidence inflation |
| Mutable source revision such as `main` | Reject | Preserve source-link reproducibility |
| `../` source path | Reject | Prevent unsafe or unverifiable links |
| Missing static summary | Reject | Preserve nonvisual accessibility fallback |
| Trace larger than 2 MiB | Reject | Bound browser/review cost |

### Source-link verification boundary

The dependency-free validator proves immutable revision syntax and safe path identity offline. A later CI lane must resolve each `file` and `line` against the pinned upstream commit. Network source-link checking is deliberately separate so ordinary offline validation remains deterministic and does not mistake a network outage for malformed trace data.

### Replay acceptance criteria

A minimal viewer may pass only when:

- `next` from step `n` selects `n + 1` until the final step;
- `previous` from step `n` selects `n - 1` until the first step;
- boundaries do not wrap silently;
- reloading the same trace begins at the documented initial step;
- missing optional collections render as “not available,” not empty captured state;
- evidence-kind labels are visible in the interactive and static representations;
- keyboard operation and an ordered text transcript expose equivalent step order.

### Limitations

- The JSON Schema is a portable structural contract, while the Python validator currently enforces the critical semantic invariants without adding a JSON Schema runtime dependency.
- The sample line numbers are authored contract locations and require later source-link CI verification before publication.
- No native instrumentation, timing measurement, learner study, or code-tracing outcome is claimed.
- The schema does not yet define event timestamps because a deterministic authored trace should not imply runtime timing.
- Trace compression, streaming, schema migration, and multi-thread event ordering remain future work.

## Next validation dependency

After this trace increment is reviewed, the next dependency-safe validation artifact is the media manifest/provenance schema or local progress export/import schema, according to the orchestrator's next ranking.
