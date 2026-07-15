# OpenCL simple waited-event regression

- Run time: 2026-07-15 16:51 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Pinned source: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: bounded lexical detection of simple local `clWaitForEvents(1, &event)` ownership

## Verified

`scripts/extract_opencl_lifecycle_calls.py` now emits a separate `simple_waited_events` inventory. For every lexically visible call matching:

```cpp
clWaitForEvents(1, &identifier)
```

it records the event identifier, exact wait line, enclosing lexical brace-scope end, and either:

- `released_in_scope`, with the exact subsequent `clReleaseEvent(identifier)` line; or
- `unmatched_in_scope`, when no such release appears before the current brace scope exits.

The diagnostic reuses the existing comment/string/character masking, so call-shaped text in comments and literals does not enter the inventory. Focused tests cover same-scope release, scope exit without release, a release outside a nested scope, and unsupported non-simple waits.

The pinned OpenCL workflow now treats the previously human-audited result as a regression contract:

```text
51 simple local waits
  5 released_in_scope
 46 unmatched_in_scope
```

A change to any of those counts fails the source-evidence workflow and forces a new human ownership review.

## Interpretation

This converts the 5/46 pairing result from a one-time research finding into a reproducible pinned-source guard. It is intentionally narrower than C++ ownership analysis: it does not model aliases, macros, helper-function release, control-flow reachability, event arrays, ownership transfer, or waits with counts other than literal `1`.

The diagnostic is suitable for guarding the known pinned pattern and for verifying a future release-only patch. After adding the missing releases upstream, the expected regression should move toward 51 released and zero unmatched; any remaining unmatched entries would require explicit classification.

## Historical

The previous run manually paired all 51 direct waits and established 5 released versus 46 unmatched. That result was documented but not enforced by generated evidence. This increment makes the same classification machine-readable and CI-checked without broadening the tool into a claimed C++ parser.

## Open questions

- Should a future upstream patch be validated by expecting zero `unmatched_in_scope` entries on the patched revision?
- Which of the 46 waits are redundant before a following same-queue blocking command?
- Should the report later include a bounded `next_blocking_command` hint, kept separate from ownership status?
- Are there event-array or helper-owned patterns outside this simple-local diagnostic that need a second explicit heuristic?

## Validation

Focused logic was exercised locally against synthetic same-scope, nested-scope, unmatched, comment/literal, and non-simple-wait cases. GitHub-hosted Documentation CI and the pinned OpenCL report workflow remain the authoritative full-repository validation paths because direct cloning is unavailable in this runtime.

## Next priority

Use the source-bearing report to classify the 46 unmatched waits as required versus redundant before same-queue blocking operations, then prepare a behavior-preserving release-only upstream patch and use this diagnostic as its regression guard.
