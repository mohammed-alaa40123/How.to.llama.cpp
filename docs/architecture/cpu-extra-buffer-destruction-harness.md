# CPU optional extra-buffer destruction harness

This page turns the comparison matrix into an implementation-ready regression harness for the pinned llama.cpp revision [`e3546c7948e3af463d0b401e6421d5a4c2faf565`](https://github.com/ggml-org/llama.cpp/commit/e3546c7948e3af463d0b401e6421d5a4c2faf565).

The bounded goal is to prove one ownership statement:

> After a supported synchronous CPU operation completes, an admitted optional CPU buffer remains safely destructible after the ordinary CPU backend wrapper has been freed.

The harness covers CPU repack first because it is the most portable path. AMX, KleidiAI, and SpacemiT IME reuse the same ordering contract behind compile-time and runtime admission gates.

## Five-minute plan

```text
create CPU backend
→ locate one admitted optional buffer type
→ allocate a small supported tensor
→ populate deterministic data
→ build and execute one supported graph
→ verify the expected output while the backend is alive
→ free the CPU backend wrapper
→ free graph/tensor metadata and the optional buffer
→ repeat under ASan and LSan
```

The important ordering is deliberate: the backend wrapper is destroyed before the optional buffer.

## Verified

### The first portable target is CPU repack

The pinned repack implementation borrows ordinary CPU allocation/free machinery, stores process-static dispatch traits in `tensor->extra`, and executes synchronously through the CPU graph path. It therefore requires no accelerator queue, event, device synchronization primitive, or hardware-specific cleanup to exercise the target destruction order.

### The test must use an actually admitted path

An optional buffer type being compiled does not prove that a particular tensor layout and operation are supported. The harness must:

1. enumerate the CPU device's extra buffer types;
2. select the exact implementation under test;
3. create a tensor type and shape accepted by that implementation;
4. call the same support predicate used by normal backend placement;
5. fail or skip with an explicit reason when runtime admission is unavailable.

A skipped hardware-gated test is not a pass for the ownership claim.

### Completion and destruction are separate assertions

CPU graph execution is synchronous for these audited paths, so a successful graph-compute return is the completion boundary. The test still needs a separate backend-free-before-buffer-free phase to validate deleter independence.

```text
compute returned
    │
    ├── assertion A: output is correct
    │
    └── free CPU backend wrapper
             │
             └── assertion B: later tensor/buffer destruction has no UAF or invalid free
```

### Tensor metadata must outlive graph execution

The test must retain the GGML context, tensors, graph, and backing buffer through execution. After the backend wrapper is freed, release tensor/graph metadata and the optional buffer in the same order used by the selected ownership fixture. The harness should make each owner explicit rather than relying on process exit.

## Executable CPU_REPACK evidence

The first exact-revision implementation passed in GitHub Actions workflow run `29481384561` on July 16, 2026.

| Evidence | Result |
|---|---|
| Pinned llama.cpp revision | `e3546c7948e3af463d0b401e6421d5a4c2faf565` |
| Runner | Ubuntu 24.04 hosted runner with AVX2 |
| Weight path | `q4_0_8x8` CPU_REPACK |
| Shape | Q4_0 `[32, 8]` × F32 `[32, 1]` → F32 `[8, 1]` |
| Repetitions | 20 separate processes |
| Numerical result | NMSE `3.82787e-16` on every run |
| Threshold | `1e-7` |
| ASan/LSan | No reported error or leak |
| Skips | None |
| Retained artifact | `cpu-repack-lifetime-sanitizer-e3546c7`, artifact `8368782428` |
| Artifact digest | `sha256:ef4f0a36e27f7811b106e0a870c278724f1e620aed991807b7f2c3e443d1efaf` |

Each process printed:

```text
repack: repack tensor leaf_0 with q4_0_8x8
PASS: CPU_REPACK path executed; NMSE=3.82787e-16
```

This is executable evidence that the exact optional path ran. The fixture checks exact buffer-type identity, non-null repack traits, and operation admission before compute, so ordinary CPU fallback cannot silently satisfy the test.

The tested destruction sequence was:

```text
compute and compare
→ free tested CPU backend wrapper
→ destroy tested graph/context metadata
→ free retained CPU_REPACK buffer
```

The passing sanitizer result supports this bounded conclusion: the retained CPU_REPACK buffer and its tensor traits do not depend on the lifetime of the ordinary CPU backend wrapper for this admitted synchronous `MUL_MAT` case.

## Reference fixture shape

Use a tiny deterministic matrix operation rather than a full model:

```text
A: F32 activation [32, 1] in ordinary CPU memory
B: Q4_0 weight [32, 8] in the CPU_REPACK buffer
C: F32 output [8, 1] in ordinary CPU memory
operation: one admitted MUL_MAT
```

The reference and tested graphs receive the same deterministic activation and the exact same Q4_0 byte vector. This isolates backend representation and execution differences from quantization-input differences.

## Required assertions

| Phase | Assertion | Failure caught |
|---|---|---|
| Admission | Exact optional buffer type and operation are supported | False-positive test that silently uses ordinary CPU fallback |
| Population | Packed/converted tensor upload succeeds | Broken callback or unsupported layout |
| Execution | Graph compute returns success | Dispatch or work-size failure |
| Correctness | Optional path matches ordinary CPU within `1e-7` NMSE | Wrong packing or kernel selection |
| Backend destruction | CPU backend wrapper is freed before the optional buffer | The intended lifetime ordering is actually exercised |
| Final destruction | No invalid free, UAF, double free, or fixture-owned leak | Deleter dependence or allocator mismatch |
| Repetition | Twenty independent processes pass with no skip | Initialization, teardown, or process-lifetime regression |

## Sanitizer matrix

### AddressSanitizer

Run the backend-free-before-buffer-free fixture with leak detection enabled where the platform supports it. Treat a use-after-free in a callback table, `tensor->extra`, buffer context, or allocator state as a direct failure of the independence claim.

### LeakSanitizer

Require all fixture-owned contexts, tensors, graphs, buffers, and backend wrappers to be released. Process-static type metadata may need a documented suppression only when it is intentionally process-lifetime and not fixture-owned. The first CPU_REPACK run required no suppression.

### ThreadSanitizer

Add concurrent first-use lookup for KleidiAI and repeated buffer-type lookup for all implementations. TSan belongs in a separate test target because it is materially slower and can conflict with ASan.

## Implementation ladder

1. **CPU repack:** passing AVX2 baseline; Q4_0 `[32, 8]` `MUL_MAT`; backend free before buffer free; twenty ASan/LSan processes.
2. **KleidiAI:** same fixture with runtime feature admission, packed-slot coverage, and concurrent first use.
3. **AMX:** add tile-permission admission, allocator-pair validation, and repeated initialization on each supported OS.
4. **SpacemiT IME:** add worker creation, TCM acquisition, clear-affinity, threadpool destruction, and process-pool shutdown checks on supported hardware.
5. **ARM repack:** add an admitted NEON+dotprod case using the same exact-path and destruction-order requirements.

## Negative tests

The harness should also call unsupported readback/copy paths through the public buffer interface and require an explicit unsupported result or guarded failure. A null callback must never be invoked blindly.

## Interpretation

This harness is intentionally smaller than an inference test. A full model can hide lifetime bugs behind process-wide objects, fallback placement, or unrelated buffers. A tiny graph makes the allocation owner, execution boundary, and destruction order reviewable.

The passing CPU_REPACK result proves only the audited fixture and selected implementation. It does not prove all repack shapes, concurrent use, process-wide shutdown for SpacemiT TCM/pool state, AMX permission state, or future optional-buffer implementations.

## Historical

The fixture requirements and executable result are pinned to the optional CPU buffer interfaces and admission rules at revision `e3546c7948e3af463d0b401e6421d5a4c2faf565`. Tensor formats, callback tables, feature gates, and test utilities may change upstream.

## Open question

- Should the generated CPU_REPACK fixture be proposed upstream as a permanent regression test?
- Can the same executable safely add repeated iterations inside one process without obscuring ownership boundaries?
- Can a parameterized fixture cover repack and KleidiAI without concealing implementation-specific admission and packing?
- What explicit shutdown API, if any, is needed before SpacemiT process-pool resources can be tested without relying on process exit?
