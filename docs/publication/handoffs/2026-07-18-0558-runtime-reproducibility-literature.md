# Literature and Venue Scout handoff — runtime reproducibility boundaries

**Date:** 2026-07-18 05:58 Africa/Cairo  
**Starting commit:** `1c6a0e7e3868e56a34e31a5b6523969cba1ebd07`  
**Assignment:** `DOC-AUDIT-01` was the highest-priority Literature Scout dependency but remains blocked by the missing independent second coder. This run therefore took the next dependency-safe slice supporting active `LAB0-04`: distinguish environment configuration from measured browser/local/container reproducibility.

## Bounded increment

Expanded `docs/publication/literature-map.md` with official JupyterLite, Development Containers, GitHub Codespaces and Binder operational constraints, plus a primary empirical Docker reproducibility study.

## Verified findings

- Browser persistence depends on available storage drivers and can be cleared or unavailable.
- JupyterLite kernel/file access depends on deployment headers or Service Worker support; WebAssembly package/runtime limits prevent treating the browser tier as native llama.cpp evidence.
- A devcontainer specification describes a recreatable environment, but only an actual clean build and command run can establish operational reproducibility.
- Codespaces persists `/workspaces`, while state outside it can disappear on rebuild; post-create lifecycle work can overlap with learner interaction.
- A Dockerfile or successful image build does not establish bitwise reproducibility.

## Interpretation

The evidence package needs a hierarchy: `configured`, `buildable`, `operationally reproducible`, `bitwise reproducible`, and `educationally effective`. The July roadmap targets operational reproducibility of bounded learner paths, not byte-identical native binaries.

## Concrete design requirement

Every environment-matrix row must separately retain:

1. configuration and pinning evidence;
2. clean execution, timing, outcome and artifact evidence;
3. persistence, degraded/offline and static-fallback evidence.

## Rejected alternative

Do not call a tier reproducible merely because `.devcontainer/`, `uv.lock`, a JupyterLite static build or a container image exists.

## EAAI implication

Cross-tier asymmetry and retained failures can support reflective experience-report lessons about executable systems education. They cannot substitute for learner-benefit evidence.

## Limitations and human need

- No devcontainer, browser deployment or offline path was executed in this literature run.
- Service behavior and billing require revalidation before deployment or submission.
- `DOC-AUDIT-01` remains blocked until a human nominates an independent second coder and approves retained result capture.

## Next dependency

After the independent audit-coder blocker, review empirical source-code-comprehension and trace-visualization work to constrain the information-equivalent static-versus-viewer baseline and prevent visual-novelty claims.
