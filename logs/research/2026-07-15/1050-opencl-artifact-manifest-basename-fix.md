# OpenCL artifact manifest basename fix

- Run time: 2026-07-15 10:50 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: make the pinned OpenCL lifecycle/source artifact directly verifiable after extraction without rewriting checksum paths

## Verified

- The prior workflow generated checksum entries from repository-relative paths such as `build/reports/opencl-lifecycle-pinned-e3546c7.json`.
- GitHub Actions uploads the selected files into the artifact root, so those repository-relative paths do not exist after normal extraction.
- The workflow now changes directory to `build/reports` before running `sha256sum`, producing artifact-root basenames for both the JSON report and preserved source.
- The workflow immediately runs `sha256sum -c opencl-lifecycle-pinned-e3546c7.sha256` in the same directory before upload.
- A Python guard verifies that the manifest contains exactly two entries and that their names exactly match the two artifact-root filenames.
- The pinned revision check, minimum source-size check, non-empty lifecycle-call check, source preservation, and 30-day artifact upload remain unchanged.

## Interpretation

The manifest is now a portable evidence contract rather than a repository-layout-dependent record. A downloaded artifact can be extracted into one directory and verified with a single standard command:

```bash
sha256sum -c opencl-lifecycle-pinned-e3546c7.sha256
```

This improves reproducibility without changing the source evidence or lifecycle classification.

## Historical

The source-bearing artifact added cryptographic hashes, but its entries retained workflow-relative `build/reports/...` paths. The hashes were correct; only post-download usability was defective.

## Open questions

- Whether the workflow should also publish the pinned commit SHA and extractor version in a small machine-readable metadata file.
- Whether artifact verification should be documented in the public OpenCL page after the branch merges.

## Next priority

Classify OpenCL enqueue-then-release groups that depend on command-retained `cl_mem` references rather than explicit host waits, separating safe reference drops from host-storage or wrapper-lifetime hazards.
