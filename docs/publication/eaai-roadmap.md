# EAAI publication roadmap

_Last updated: 2026-07-18 06:02 Africa/Cairo_

This roadmap turns repository milestones into evidence gates for an EAAI experience report. It does not authorize manuscript drafting.

## Phase A — Foundation, July 17-23, 2026

### A1. Coordination and contracts

Audience, educational problem, three lesson contracts, research questions, evidence kinds, fixture policy, privacy constraints and the three-tier architecture are frozen. The documentation-gap claim remains a hypothesis until the systematic audit is executed.

**Status:** substantially evidenced; canonical-stack reconciliation and the documentation audit remain.

### A2. Deterministic evidence foundations

Synthetic GGUF fixtures, Lab 0 reports, trace/source schemas, local-progress schema, media provenance and deterministic figure generation have validators and retained CI evidence. Ordinary CI performs no paid generation or unauthorized model download.

**Status:** evidenced at component level.

### A3. Smallest vertical slice

A browser GGUF slice, authored/source-derived trace viewer, deterministic technical figure and model-free Lab 0 runners exist with explicit evidence boundaries and accessibility fallbacks.

**Status:** evidenced at component level; not yet one canonical integrated artifact.

## Phase B — Vertical slices, July 24-31, 2026

### B1. Lab 0 end to end

- Ubuntu 24.04 local-native row passed: run `29622240261`, artifact `8422651113`, time to ready 326,905 ms.
- Ubuntu 24.04 devcontainer row passed: run `29626470197`, artifact `8424069914`, time to ready 280,753 ms.
- Both rows use `uv sync --locked`, a pinned llama.cpp revision, CMake/Ninja, `GGML_NATIVE=OFF`, bounded `llama-cli` compilation and model-free executable launch.

**Status:** two reproducibility rows evidenced. These are not inference or learner-benefit results. Offline/degraded behavior and additional platforms remain unevidenced.

### B2. Browser GGUF Anatomy lab

The bounded parser/visualizer, Predict-Discover-Explain checkpoints, golden agreement and static fallback exist. Progress portability and corruption recovery remain prerequisites for end-to-end closure.

**Status:** component evidenced; integration incomplete.

### B3. Executable lecture and media dry run

The authored/source-derived viewer and deterministic figure are retained. Native or faithful capture, static baseline comparison, media lifecycle dry run and independent technical review remain open.

**Status:** prototype evidenced; research claims not yet supported.

### B4. Canonical end-to-end demo

One reconciled branch must combine Lab 0, GGUF lab, viewer, deterministic figure, progress export/import and validation without weakening evidence labels or privacy boundaries.

**Status:** blocked by `STACK-01` human canonical-progress decision.

## Phase C — Evidence development, August-September 2026

- Extract and independently code the longitudinal repository dataset.
- Freeze benchmark tasks and run fair workflow baselines.
- Obtain independent llama.cpp/GGML correctness review.
- Pilot expert or learner evaluation only after approval and ethics determination.
- Record negative results, failed generations, human labor, infrastructure maintenance and cost proxies.

## Phase D — Venue and manuscript readiness

- Verify current official EAAI call, area, deadlines, author kit, length and anonymity rules.
- Freeze claims-evidence table and limitations.
- Resolve fatal and major reviewer concerns.
- Activate Paper Integrator only after the gate in `orchestrator-state.md` is met.

## Immediate dependency order

1. `STACK-01`: human canonical progress choice and combined integration branch.
2. `PROGRESS-02`: export/import, migration, corruption recovery and local storage tests.
3. `DATA-01`: retrospective extraction and independent coding.
4. `REVIEW-01`: independent technical review.
5. `VENUE-01`: current official EAAI verification.
6. `BASE-01`: fair workflow baseline.
7. `EVAL-01`: approved evaluation and ethics pathway.

## Generalization boundary

The artifact is llama.cpp/GGML-specific. The potentially generalizable method is source-pinned executable explanation, evidence-labelled traces, deterministic validators, local-first learner state and human-supervised repository agents. Generalization beyond this codebase remains a design hypothesis until replicated.

## Ethics and AI-use boundary

No participant recruitment, personal-data collection, silent telemetry or authenticated progress sync is authorized. Deterministic technical graphics are authoritative. Generated media remains optional, provenance-recorded, accessibility-reviewed, cached and human-approved. Manuscript AI-use disclosure must report agent roles, tool/model versions when known, human corrections, validation failures and retained evidence.
