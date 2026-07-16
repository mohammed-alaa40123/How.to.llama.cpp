# Constructor initializer boundary regression

- Run time: 2026-07-14 22:49 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: make the approximate source-index boundary explicit for parenthesized, braced, and multiline constructor initializer lists

## Startup and inspection

Read the complete repository README first, followed by project state, research log, research ledger, and the latest detailed note. Inspected the current source-index implementation and complete source-index test module before editing.

## Artifact

Added `tests/test_index_upstream_initializer_boundaries.py` with three focused cases:

1. a same-line parenthesized initializer list must be indexed at the constructor definition line;
2. a same-line braced initializer must not be partially indexed;
3. a multiline initializer list must not be partially indexed.

## Verified

- `SPECIAL_MEMBER_RE` deliberately excludes braces, semicolons, and newlines from its initializer-list clause.
- Parenthesized same-line initialization remains an accepted and tested capability.
- Braced and multiline forms are treated as unsupported rather than being emitted with a misleading partial symbol record.
- The production scanner was not broadened in this increment.
- The preceding branch head passed Documentation CI run `29359626167`.

## Interpretation

For an approximate navigation index, a false negative on unsupported syntax is safer than a false positive that links readers to a malformed or partially matched declaration. This regression therefore protects the scanner's documented precision boundary rather than expanding grammar coverage.

## Historical

The bounded initializer-list rule was introduced to capture common same-line constructor ownership setup while preserving exact physical source lines. The unsupported braced and multiline boundary was documented but not previously protected by negative tests.

## Open questions

- Whether the pinned llama.cpp tree contains enough braced or multiline constructor initializers to justify a small stateful scanner.
- Whether unsupported-syntax counters should be emitted during source inventory generation so human review can prioritize missed constructs.
- Complete pinned OpenCL teardown still requires searchable access to the end of `ggml-opencl.cpp` or a regenerated local source inventory.

## Validation and CI

The new tests were committed to the active PR branch. GitHub-hosted Documentation CI remains the authoritative full validation path because a local checkout is unavailable in this runtime.

## Next priority

Regenerate the pinned source inventory and finish the OpenCL teardown audit. If source recovery remains blocked, implement the admitted CPU repack backend-free-before-buffer-free fixture under ASan/LSan.
