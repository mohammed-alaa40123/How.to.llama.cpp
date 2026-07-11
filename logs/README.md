# Logs

This directory stores durable project logs that should remain available across research sessions.

## Layout

- `logs/research/YYYY-MM-DD/HHMM-topic.md` — detailed per-run notes.
- `logs/runtime/` — local profiler, benchmark, memory, page-fault, and backend traces. This directory is ignored by default because raw traces can be large.

## What belongs in the canonical research log

Concise verified findings, design decisions, unresolved questions, and the next task belong in `docs/reference/research-log.md` so they appear on the documentation site.

Use this directory for supporting detail that would overwhelm the canonical log. Important conclusions from a detailed log must still be summarized in the canonical research log and project state.

## Naming

Use UTC timestamps unless an experiment requires device-local time:

```text
logs/research/2026-07-12/2215-context-scheduler-trace.md
```

Each note should identify the source revision, files inspected, evidence type, artifacts changed, validation performed, and remaining questions.
