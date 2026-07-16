# OpenCL `set_tensor` wait-group CI contract

- Run time: 2026-07-15 21:52 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Pinned source: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: convert the reviewed 21/3 `set_tensor` wait grouping into a pinned workflow and artifact contract

## Verified

The previous increment added `scripts/classify_opencl_set_tensor_waits.py` and established this pinned result:

```text
24 unresolved non-blocking-read waits
  21 → immediately followed by clReleaseMemObject(data_device)
   3 → nested lexical scope exit
```

All 24 records are inside `ggml_backend_opencl_buffer_set_tensor()` and none is classified as `other`.

This increment integrates that classifier into `.github/workflows/opencl-lifecycle-report.yml`. The workflow now:

1. triggers when the classifier or its focused tests change;
2. runs the classifier against the exact pinned OpenCL source and annotated lifecycle report;
3. writes `opencl-set-tensor-wait-groups-e3546c7.json`;
4. asserts exactly 24 records;
5. asserts exactly 21 `temporary_upload_buffer_release` and 3 `nested_scope_exit` records;
6. asserts that every record belongs to `ggml_backend_opencl_buffer_set_tensor()`;
7. rejects any `other` classification; and
8. uploads the grouping JSON beside the source, lifecycle report, release-only patch, and post-patch report.

The living README TODO list, project state, and concise research log were updated. The research ledger was reviewed and left unchanged because this increment introduced no new external source.

## Interpretation

The 21/3 split is now a version-pinned evidence contract rather than a one-time local observation. Any upstream-source drift or classifier regression that changes the reviewed grouping fails visibly and requires human re-audit.

The contract intentionally freezes lexical facts, not synchronization semantics. In particular, the 21 waits preceding `clReleaseMemObject(data_device)` are not proven removable merely because OpenCL commands retain memory objects. Synchronous tensor-set output readiness remains a separate API-contract question.

## Historical

The preceding run completed the classifier and focused unit tests but could not safely update the long living context files or add the classifier to CI. This increment closes both durability gaps.

## Open questions

- What exact operations follow the three nested-scope waits?
- Does synchronous `ggml_backend_tensor_set()` require device-side conversion completion before return?
- Are the 21 temporary-input-release waits required, redundant, or contract-dependent after separating host-input reuse from output readiness?
- Should the generated 46-release ownership patch be submitted upstream before any synchronization cleanup?

## Validation

- Workflow YAML was updated with a dedicated `Classify remaining set_tensor waits` step and artifact upload.
- The workflow assertion checks record count, exact category counts, enclosing function, and absence of `other` records.
- Local cloning remains blocked by `Could not resolve host: github.com`; GitHub-hosted Actions are the authoritative execution environment.
- Final-head workflow and Pages status must be checked after all commits land.

## Next priority

Trace the three nested-scope waits and establish the observable synchronous tensor-set return contract. Then classify the 21 temporary-input-release waits as required, redundant, or contract-dependent while keeping event ownership repair separate from synchronization optimization.