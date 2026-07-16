# Upstream CPU_REPACK lifetime fixture proposal

_Last reviewed: 2026-07-16 12:50 Africa/Cairo_

## Scope

This proposal turns the project's passing, revision-pinned CPU_REPACK sanitizer fixture into a narrow candidate for `ggml-org/llama.cpp` upstream review.

Evidence baseline:

- pinned tested revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`;
- passing workflow run: `29481384561`;
- twenty separate AVX2-confirmed ASan/LSan processes;
- tested operation: Q4_0 `[32, 8]` × F32 `[32, 1]` → F32 `[8, 1]`;
- stable NMSE: `3.82787e-16`;
- retained artifact: `8368782428`;
- artifact digest: `sha256:ef4f0a36e27f7811b106e0a870c278724f1e620aed991807b7f2c3e443d1efaf`.

Current-upstream compatibility was reviewed at exact commit `8ee54c8b32a1b0cf13c03fc5723142bc62c775f6`.

## Verified

### Current test registration remains compatible

Current `tests/CMakeLists.txt` still provides `llama_build_and_test(source)` and registers `test-backend-ops.cpp` through that helper. Tests that access backends directly are grouped under `if (NOT GGML_BACKEND_DL)`.

The candidate can therefore remain a dedicated executable:

```cmake
if (NOT GGML_BACKEND_DL)
    llama_build_and_test(test-cpu-extra-buffer-lifetime.cpp LABEL "backend-lifetime")
    target_include_directories(test-cpu-extra-buffer-lifetime PRIVATE ${PROJECT_SOURCE_DIR}/ggml/src)
endif()
```

The `GGML_BACKEND_DL` guard is important because the fixture calls internal CPU backend APIs directly.

### The internal CPU_REPACK entry point still exists

At current upstream commit `8ee54c8`, `ggml/src/ggml-cpu/repack.h` still declares:

```cpp
ggml_backend_buffer_type_t ggml_backend_cpu_repack_buffer_type(void);
```

The header explicitly labels itself internal. A standalone backend test is therefore more suitable than adding this lifetime-specific ownership sequence to public API tests.

### The test must preserve exact path proof

A numerically correct result alone does not prove CPU_REPACK executed. The upstream candidate must retain all three guards:

```cpp
weight->buffer->buft == ggml_backend_cpu_repack_buffer_type()
weight->extra != nullptr
ggml_backend_supports_op(cpu_backend, mul_mat)
```

It must also preserve the observed path marker or an equivalent implementation-level assertion when maintainers prefer less diagnostic output.

### The teardown order is the regression target

The distinctive sequence is:

```text
compute and compare
  → ggml_backend_free(tested_backend)
  → destroy tested graph allocator/context metadata
  → ggml_backend_buffer_free(repack_buffer)
```

This is intentionally different from ordinary examples. The test exists to prove that completed CPU_REPACK buffer destruction does not depend on a live ordinary CPU backend wrapper.

## Interpretation

The fixture is suitable for upstream review, but the upstream patch should be narrower than the project workflow:

1. add the dedicated C++ regression target;
2. allow a clean runtime skip when AVX2 or the exact repack implementation is unavailable;
3. keep the repository's separate sanitizer workflow responsible for requiring AVX2 and twenty non-skipped runs;
4. avoid adding the project-specific patch generator, retained-artifact machinery, or twenty-process loop to llama.cpp itself.

A universal upstream CI job cannot assume every architecture exposes AVX2. Treating a hardware-gated skip as success is acceptable for the ordinary cross-platform test suite, but at least one authoritative x86 sanitizer lane should require admission so the test cannot silently stop exercising CPU_REPACK.

The first patch should not generalize the fixture into a framework for every extra buffer. KleidiAI, AMX, SpacemiT, and ARM repack have different hardware gates, storage layouts, and teardown questions; they should be added incrementally after one maintainable pattern lands.

## Historical

The project first audited CPU optional-buffer ownership from source, selected the minimal admitted AVX2 case, resolved mixed-buffer graph allocation, generated the dedicated fixture, and then ran it twenty times under ASan/LSan. The first successful evidence run closed the source-to-runtime chain before this upstream-suitability decision was made.

## Open questions

- Whether maintainers prefer the test under `tests/` or closer to GGML CPU backend tests.
- Which upstream CI lane can guarantee AVX2 and sanitizer execution rather than accepting a skip.
- Whether the path proof should rely on `tensor->extra`, an internal trait identity, or a test-only observable hook.
- Whether current upstream still produces the same `q4_0_8x8` admission and numerical result when the candidate is compiled at `8ee54c8`.
- Whether repeated in-process execution should be added before upstream submission or kept as a follow-up.

## Proposed upstream patch shape

Files:

```text
tests/test-cpu-extra-buffer-lifetime.cpp
tests/CMakeLists.txt
```

Proposed title:

```text
tests: cover CPU_REPACK buffer lifetime after CPU backend teardown
```

Proposed body:

```text
Add a focused CPU_REPACK lifetime regression for an admitted Q4_0 MUL_MAT.

The test allocates the quantized weight from the internal CPU_REPACK buffer type, proves that repack traits and operation admission are active, compares the result with ordinary CPU using identical quantized bytes, then frees the tested CPU backend wrapper before destroying the retained repack buffer.

This covers an ownership boundary that ordinary backend-op correctness tests do not exercise. The test skips on runners without the required CPU feature; sanitizer CI should include at least one AVX2 lane where admission is mandatory.

The initial validated case is Q4_0 [32, 8] × F32 [32, 1], with NMSE <= 1e-7.
```

## Decision

**Stage the narrow two-file fixture for upstream review.** Do not submit the generator or project-specific evidence workflow upstream. Before opening the upstream pull request, regenerate and compile the fixture against the then-current llama.cpp head and record whether the minimal case is still admitted without API changes.