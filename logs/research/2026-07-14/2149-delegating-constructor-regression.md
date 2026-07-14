# Delegating constructor regression

- Run time: 2026-07-14 21:49 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: convert the verified same-line delegating-constructor behavior into explicit source-index regression coverage

## Startup and inspection

Read the complete repository README first, followed by project state, research log, research ledger, and the latest detailed note. Inspected the current source-index implementation and complete unit-test module before editing.

## Artifact

Added `test_extract_symbols_handles_same_line_delegating_constructors` to `tests/test_index_upstream.py`.

The fixture covers two qualified delegating constructors:

```cpp
backend_state::backend_state(int device) : backend_state(device, nullptr) {
}

nested::resource::resource() noexcept : resource(default_value()) {
}
```

Expected records preserve exact physical definition lines:

```text
backend_state::backend_state   line 1
nested::resource::resource     line 4
```

## Verified

- The production scanner was not broadened; this increment adds only regression coverage for behavior already verified in the preceding audit.
- The fixture exercises an ordinary qualified constructor and a nested qualified constructor with `noexcept`.
- Both delegation targets use parenthesized arguments, matching the bounded same-line initializer-list contract.
- The test continues to require exact declaration lines rather than merely checking symbol presence.

## Interpretation

The source index can now treat same-line parenthesized constructor delegation as a tested compatibility promise. This is narrower than general constructor-initializer support: multiline delegation and brace-containing arguments remain outside the regex contract.

## Historical

Delegating-constructor support was introduced implicitly by the bounded initializer-list clause and documented in the preceding behavior audit. This run closes the missing-test gap.

## Open questions

- Multiline delegation, braced initializer arguments, function-try-blocks, and in-class definitions remain unsupported.
- Complete pinned OpenCL teardown still requires searchable access to the end of the translation unit or a regenerated local source inventory.

## Validation and CI

The focused test was committed to the active PR branch. GitHub-hosted Documentation CI is the authoritative validation path because a local checkout remains unavailable in this runtime.

## Next priority

Regenerate the pinned source inventory and finish the OpenCL teardown audit. If complete pinned-source access remains blocked, implement the admitted CPU repack backend-free-before-buffer-free fixture under ASan/LSan.
