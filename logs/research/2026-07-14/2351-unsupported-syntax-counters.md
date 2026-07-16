# Unsupported source-index syntax counters

- Run time: 2026-07-14 23:51 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: add bounded telemetry for constructor initializer forms intentionally skipped by the approximate source scanner

## Startup and inspection

Read the complete repository README first, followed by project state, research log, research ledger, and the latest detailed note. Inspected the current source-index implementation and constructor-initializer boundary tests before editing.

## Artifact

Updated `scripts/index_upstream.py` to emit per-file and aggregate candidate counts for:

1. same-line braced constructor initializers;
2. multiline constructor initializer lists.

Added `tests/test_index_upstream_unsupported_syntax.py` to verify positive counts, zero counts for supported parenthesized same-line initialization, and continued absence of unsupported candidates from `symbol_locations`.

The increment also repaired the constructor matcher exposed by the preceding CI run: it now requires horizontal same-line whitespace and an explicitly parenthesized initializer target before the function body brace.

## Verified

- Unsupported-syntax telemetry is separate from symbol extraction.
- Braced and multiline constructor initializer candidates remain excluded from generated symbol records, preventing partial or misleading pinned links.
- Every indexed file now carries an `unsupported_syntax` object.
- The root JSON summary now carries `unsupported_syntax_counts` totals.
- The generated Markdown summary reports both totals.
- The new counters are explicitly documented as bounded triage candidates, not complete C++ parser diagnostics.
- Documentation CI run `29363583865` passed both isolated suites but failed full discovery at the constructor-initializer boundary test.
- Reproduction showed that the old `SPECIAL_MEMBER_RE` used newline-capable `\s*` and accepted the opening brace of `options_{...}` as the function body.
- The repaired matcher accepts supported parenthesized member/delegating initialization while rejecting braced and multiline forms.

## Interpretation

The counters turn a known false-negative boundary into measurable backlog data. Tightening the matcher at the same time preserves the safer behavior: unsupported forms are counted for triage but never emitted as partial navigation links.

## Historical

The previous increment added negative tests proving braced and multiline constructor initializers were intentionally unsupported. Those tests exposed that the implementation did not actually enforce the documented boundary. This increment repairs that mismatch and adds observability for the omitted forms.

## Open questions

- How many candidates occur in the pinned llama.cpp tree once source regeneration is available?
- Do candidate counts justify a small stateful constructor scanner?
- Which additional unsupported forms should gain similarly bounded counters after evidence from the pinned tree?
- Complete pinned OpenCL teardown still requires searchable access to the end of `ggml-opencl.cpp` or a regenerated local inventory.

## Validation and CI

The focused regex reproduction now returns supported parenthesized constructors and rejects the braced and multiline examples. GitHub-hosted Documentation CI remains the authoritative full validation path because local cloning is blocked by DNS resolution. A commit-scoped run for the final repair head is pending.

## Next priority

Inspect the final Documentation CI run, then regenerate the pinned inventory and use the new telemetry to prioritize scanner work; continue the OpenCL teardown audit or implement the admitted CPU repack lifetime fixture if regeneration remains blocked.
