#!/usr/bin/env python3
"""Execute the model-free Lab 0 path and emit a reviewable evidence record.

The same bounded runner is used for local-native and cloud-container matrix rows.
It records failed phases instead of hiding them, never loads or downloads model
weights, and excludes command output from the JSON record.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / os.environ.get("LAB0_OUTPUT", "artifacts/lab0-ubuntu-24.04-run.json")
LLAMA_DIR = ROOT / "llama.cpp"
BUILD_DIR = ROOT / "build" / "lab0"
LLAMA_REVISION = "e3546c7948e3af463d0b401e6421d5a4c2faf565"
ENVIRONMENT_ID = os.environ.get("LAB0_ENV_ID", "github-actions-ubuntu-24.04-x86_64")
EXECUTION_TIER = os.environ.get("LAB0_TIER", "local_native")
OS_ID = os.environ.get("LAB0_OS", "ubuntu-24.04")


def run(command: list[str], *, cwd: Path = ROOT) -> tuple[bool, str]:
    proc = subprocess.run(command, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode == 0, proc.stdout.strip()


def version(command: list[str]) -> dict[str, object]:
    executable = shutil.which(command[0])
    if executable is None:
        return {"command": " ".join(command), "version": "missing", "passed": False}
    ok, output = run(command)
    first_line = output.splitlines()[0] if output else "no-version-output"
    return {"command": " ".join(command), "version": first_line, "passed": ok}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    diagnostics: list[str] = []
    started_ms = time.monotonic_ns() // 1_000_000

    toolchain = {
        "uv": version(["uv", "--version"]),
        "python": version(["python3", "--version"]),
        "cmake": version(["cmake", "--version"]),
        "ninja": version(["ninja", "--version"]),
        "compiler": version(["c++", "--version"]),
    }
    missing_codes = {
        "uv": "UV_MISSING",
        "cmake": "CMAKE_MISSING",
        "ninja": "NINJA_MISSING",
        "compiler": "COMPILER_MISSING",
    }
    for name, code in missing_codes.items():
        if not toolchain[name]["passed"]:
            diagnostics.append(code)

    setup_success = False
    build_success = False
    launch_success = False

    if not diagnostics:
        setup_success, _ = run(["uv", "sync", "--locked"])
        if not setup_success:
            diagnostics.append("UV_LOCK_DRIFT")

    if setup_success:
        shutil.rmtree(LLAMA_DIR, ignore_errors=True)
        shutil.rmtree(BUILD_DIR, ignore_errors=True)
        clone_ok, _ = run([
            "git", "clone", "--filter=blob:none", "https://github.com/ggml-org/llama.cpp.git", str(LLAMA_DIR)
        ])
        checkout_ok = False
        if clone_ok:
            checkout_ok, _ = run(["git", "checkout", "--detach", LLAMA_REVISION], cwd=LLAMA_DIR)
        if not (clone_ok and checkout_ok):
            diagnostics.append("CONFIGURE_FAILED")
        else:
            configure_ok, _ = run([
                "cmake", "-S", "llama.cpp", "-B", "build/lab0", "-G", "Ninja", "-DGGML_NATIVE=OFF"
            ])
            if not configure_ok:
                diagnostics.append("CONFIGURE_FAILED")
            else:
                build_success, _ = run([
                    "cmake", "--build", "build/lab0", "--target", "llama-cli", "-j", "2"
                ])
                if not build_success:
                    diagnostics.append("COMPILE_FAILED")
                else:
                    executable = BUILD_DIR / "bin" / "llama-cli"
                    if not executable.is_file():
                        diagnostics.append("EXECUTABLE_MISSING")
                    else:
                        launch_success, _ = run([str(executable), "--help"])
                        if not launch_success:
                            diagnostics.append("EXECUTABLE_MISSING")

    ready_ms = time.monotonic_ns() // 1_000_000
    lock_path = ROOT / "uv.lock"
    course_sha = os.environ.get("LAB0_COURSE_SHA", os.environ.get("GITHUB_SHA", "0" * 40))
    arch = "x86_64" if platform.machine() in {"x86_64", "AMD64"} else "arm64"
    validated = setup_success and build_success and launch_success

    report = {
        "schema_version": "1.0.0",
        "environment": {
            "id": ENVIRONMENT_ID,
            "tier": EXECUTION_TIER,
            "os": OS_ID,
            "architecture": arch,
            "support_state": "validated" if validated else "degraded",
            "offline_mode": "not_tested",
        },
        "revisions": {
            "course": course_sha,
            "llama_cpp": LLAMA_REVISION,
            "uv_lock_sha256": sha256(lock_path),
        },
        "toolchain": toolchain,
        "commands": {
            "python_sync": "uv sync --locked",
            "configure": "cmake -S llama.cpp -B build/lab0 -G Ninja -DGGML_NATIVE=OFF",
            "compile": "cmake --build build/lab0 --target llama-cli -j 2",
            "launch": "build/lab0/bin/llama-cli --help",
        },
        "timings": {
            "started_monotonic_ms": started_ms,
            "ready_monotonic_ms": ready_ms,
            "time_to_ready_ms": ready_ms - started_ms,
        },
        "result": {
            "setup_success": setup_success,
            "build_success": build_success,
            "launch_success": launch_success,
            "model_kind": "none",
            "inference_state": "not_attempted",
            "diagnostics": sorted(set(diagnostics)),
        },
        "security": {
            "model_redistributed": False,
            "secrets_recorded": False,
            "personal_paths_recorded": False,
            "network_required_after_cache": False,
        },
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if validated else 1


if __name__ == "__main__":
    raise SystemExit(main())
