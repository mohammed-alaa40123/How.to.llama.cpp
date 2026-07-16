# First passing CPU_REPACK sanitizer evidence

- Run time: 2026-07-16 11:58 Africa/Cairo
- Documentation branch: `automation/backend-teardown-audit-method`
- Pinned llama.cpp revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Workflow run: `29481384561`
- Job: `asan-lsan` (`87565708592`)
- Artifact: `cpu-repack-lifetime-sanitizer-e3546c7` (`8368782428`)
- Artifact digest: `sha256:ef4f0a36e27f7811b106e0a870c278724f1e620aed991807b7f2c3e443d1efaf`

## Verified

The first exact-revision sanitizer run completed successfully on GitHub's Ubuntu 24.04 hosted runner with AVX2 exposed.

The workflow successfully:

1. verified AVX2 capability;
2. fetched and verified the pinned llama.cpp tree;
3. materialized the generated fixture and CMake target;
4. configured and compiled the dedicated target with AddressSanitizer and LeakSanitizer;
5. executed the fixture in twenty separate processes; and
6. uploaded retained CPU, generated-source, and sanitizer evidence.

Every execution printed both:

```text
repack: repack tensor leaf_0 with q4_0_8x8
PASS: CPU_REPACK path executed; NMSE=3.82787e-16
```

The pass marker appeared exactly twenty times. No run emitted `SKIP:`, AddressSanitizer diagnostics, LeakSanitizer diagnostics, or a non-zero exit.

The tested operation was the pinned minimal admitted case:

```text
Q4_0 weight [32, 8]
× F32 activation [32, 1]
→ F32 output [8, 1]
```

The fixture proved exact CPU_REPACK buffer identity, non-null repack traits, operation admission, successful synchronous compute, numerical agreement with ordinary CPU, and the intended destruction order in which the tested CPU backend wrapper is freed before the retained repack buffer.

## Interpretation

This is the first executable evidence for the bounded ownership claim:

> After this admitted synchronous CPU_REPACK `MUL_MAT` completes, its optional buffer can be destroyed safely after the ordinary CPU backend wrapper has already been freed.

The result is stronger than source reasoning alone because the exact path executed under ASan/LSan twenty times and numerical comparison was stable at `3.82787e-16`, far below the `1e-7` threshold.

The result remains intentionally bounded. It does not prove all CPU_REPACK shapes, concurrent use, other optional CPU buffer implementations, or process-global cleanup outside fixture ownership.

## Historical

Earlier increments selected the minimal AVX2 shape, resolved graph and per-tensor allocation topology, generated a complete two-graph fixture, and added the exact-revision sanitizer workflow. This run closes that sequence with a passing compiler and runtime artifact.

## Open question

- Add equivalent admitted lifetime fixtures for KleidiAI, AMX, SpacemiT, and ARM NEON+dotprod.
- Decide whether the CPU_REPACK fixture should be proposed upstream as a permanent regression target.
- Extend the fixture to repeated execution within one process to complement the current twenty-process teardown coverage.
- Verify the public Pages deployment after PR #1 merges.

## Validation

- Read the complete README, project state, research log, research ledger, and previous detailed note before editing.
- Inspected workflow job status, complete execution evidence around all twenty iterations, and retained artifact metadata.
- Research ledger unchanged because no external source was added or reclassified.

## Next priority

Promote the passing CPU_REPACK evidence into the canonical destruction-harness page, then design the first hardware-gated KleidiAI or ARM repack lifetime extension without weakening the exact path-proof and sanitizer requirements.
