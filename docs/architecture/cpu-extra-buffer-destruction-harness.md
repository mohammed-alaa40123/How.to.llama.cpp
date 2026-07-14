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
5. skip with an explicit reason when runtime admission fails.

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

## Reference fixture shape

Use a tiny deterministic matrix operation rather than a full model:

```text
A: small activation tensor in ordinary CPU memory
B: quantized or packed weight tensor in the optional buffer
C: output tensor in ordinary CPU memory
operation: one implementation-supported MUL_MAT
```

The dimensions should be the smallest alignment-compatible shape accepted by the implementation. Expected output can be computed before repacking with a scalar reference or compared against the ordinary CPU buffer path using the same source values.

## Required assertions

| Phase | Assertion | Failure caught |
|---|---|---|
| Admission | Exact optional buffer type and operation are supported | False-positive test that silently uses ordinary CPU fallback |
| Population | Packed/converted tensor upload succeeds | Broken callback or unsupported layout |
| Execution | Graph compute returns success | Dispatch or work-size failure |
| Correctness | Optional path matches a reference within format tolerance | Wrong packing or kernel selection |
| Backend destruction | CPU backend wrapper is freed before the optional buffer | The intended lifetime ordering is actually exercised |
| Final destruction | No invalid free, UAF, double free, or leak | Deleter dependence or allocator mismatch |
| Repetition | The fixture passes repeatedly in one process | Static initialization or stale-state bug |

## Sanitizer matrix

### AddressSanitizer

Run the backend-free-before-buffer-free fixture with leak detection enabled where the platform supports it. Treat a use-after-free in a callback table, `tensor->extra`, buffer context, or allocator state as a direct failure of the independence claim.

### LeakSanitizer

Require all fixture-owned contexts, tensors, graphs, buffers, and backend wrappers to be released. Process-static type metadata may need a documented suppression only when it is intentionally process-lifetime and not fixture-owned.

### ThreadSanitizer

Add concurrent first-use lookup for KleidiAI and repeated buffer-type lookup for all implementations. TSan belongs in a separate test target because it is materially slower and can conflict with ASan.

## Implementation ladder

1. **CPU repack:** portable baseline; one supported `MUL_MAT`; backend free before buffer free; ASan/LSan.
2. **KleidiAI:** same fixture with runtime feature admission, packed-slot coverage, and concurrent first use.
3. **AMX:** add tile-permission admission, allocator-pair validation, and repeated initialization on each supported OS.
4. **SpacemiT IME:** add worker creation, TCM acquisition, clear-affinity, threadpool destruction, and process-pool shutdown checks on supported hardware.

## Negative tests

The harness should also call unsupported readback/copy paths through the public buffer interface and require an explicit unsupported result or guarded failure. A null callback must never be invoked blindly.

## Interpretation

This harness is intentionally smaller than an inference test. A full model can hide lifetime bugs behind process-wide objects, fallback placement, or unrelated buffers. A tiny graph makes the allocation owner, execution boundary, and destruction order reviewable.

The test proves only the audited fixture and selected implementation. It does not prove process-wide shutdown for SpacemiT TCM/pool state, AMX permission state, or future optional-buffer implementations.

## Historical

The fixture requirements are pinned to the optional CPU buffer interfaces and admission rules at revision `e3546c7948e3af463d0b401e6421d5a4c2faf565`. Tensor formats, callback tables, feature gates, and test utilities may change upstream.

## Open question

- Which existing upstream test helper gives the smallest stable way to construct a quantized `MUL_MAT` graph without duplicating test infrastructure?
- Should the first implementation live beside backend tests or as a dedicated optional-buffer lifetime executable?
- How should intentionally process-static metadata be distinguished from true leaks in LSan output?
- Can a single parameterized fixture cover repack and KleidiAI without concealing implementation-specific admission and packing?
- What explicit shutdown API, if any, is needed before SpacemiT process-pool resources can be tested without relying on process exit?
