# Runtime reproducibility literature slice

## Run scope

- **Starting commit:** `1c6a0e7e3868e56a34e31a5b6523969cba1ebd07`
- **Assigned dependency:** `DOC-AUDIT-01`
- **Blocker:** the predefined audit requires a nominated independent second coder; none is recorded.
- **Dependency-safe task:** verify operational semantics and evidence boundaries for browser, local-native and devcontainer/Codespaces tiers, directly supporting `LAB0-04` and the three-tier platform evaluation.
- **Learner outcome affected:** learners and reviewers should be able to distinguish configuration availability, actual executable success, persistence behavior and educational effectiveness.

## Primary and official sources checked

1. JupyterLite storage configuration: https://jupyterlite.readthedocs.io/en/stable/howto/configure/storage.html
2. JupyterLite kernel/filesystem access: https://jupyterlite.readthedocs.io/en/stable/howto/content/python.html
3. JupyterLite troubleshooting and WebAssembly limitations: https://jupyterlite.readthedocs.io/en/stable/troubleshooting.html
4. Development Container Specification repository: https://github.com/devcontainers/spec
5. GitHub Codespaces deep dive: https://docs.github.com/en/codespaces/about-codespaces/deep-dive
6. GitHub Codespaces product capabilities: https://github.com/features/codespaces
7. Binder reproducibility guidance: https://mybinder.readthedocs.io/en/latest/tutorials/reproducibility.html
8. Solarin, “It’s Not Just Timestamps: A Study on Docker Reproducibility,” arXiv:2602.17678 (2026): https://arxiv.org/abs/2602.17678

Sources were checked on 2026-07-18. No bibliographic detail beyond the primary source record was inferred.

## Claims

### Verified

- JupyterLite persistence and kernel/file synchronization depend on browser storage and deployment capabilities.
- WebAssembly kernel constraints prevent using ordinary browser execution as evidence of native llama.cpp behavior.
- Devcontainer and Codespaces configuration can define repeatable environments, but hosted lifecycle, persistence and machine resources remain separate operational factors.
- Codespaces preserves the `/workspaces` mount across rebuilds, while other container state may not survive rebuild.
- Empirical Docker evidence distinguishes successful/configured builds from byte-identical reproducibility.

### Interpretation

The repository should define five non-equivalent states: configured, buildable, operationally reproducible, bitwise reproducible and educationally effective. The two-week roadmap targets operational reproducibility.

### Historical

The project previously used “reproducibility” broadly in the three-tier comparison. This increment narrows the term without changing existing measured Lab 0 evidence.

### Open questions

- Whether the current devcontainer lane succeeds in a retained clean run.
- Whether the deployed browser lab has correct cross-origin headers or a reliable Service Worker path.
- Whether offline/degraded paths and progress export/import work after cache or storage loss.
- Whether these architecture choices improve learner outcomes.

## Files changed

- `docs/publication/literature-map.md`
- `docs/publication/handoffs/2026-07-18-0558-runtime-reproducibility-literature.md`
- this run record

## Validation

- All citations point to primary repositories, official documentation or a primary empirical study.
- No product price, quota or service guarantee was copied into a stable requirement.
- No model, API credential, paid service, participant data or manuscript prose was introduced.
- Commit-scoped Documentation CI remains authoritative.

## Human-review needs

- Nominate the independent `DOC-AUDIT-01` coder.
- Confirm that “operational reproducibility” is the intended term in the validation and reviewer packages.

## Evidence produced

A reviewable literature-map slice and handoff establishing a machine- and reviewer-checkable reproducibility claim taxonomy.

## Ending commit

To be filled by the final branch head and PR record.

## Next dependency

Return to `DOC-AUDIT-01` when an independent coder exists. Otherwise take the distinct source-code-comprehension and trace-visualization literature slice tied to the frozen baseline.
