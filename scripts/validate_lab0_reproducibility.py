#!/usr/bin/env python3
"""Validate Lab 0 reproducibility evidence without external dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
DIAGNOSTICS = {
    "UV_MISSING", "UV_LOCK_DRIFT", "PYTHON_UNSUPPORTED", "CMAKE_MISSING",
    "NINJA_MISSING", "COMPILER_MISSING", "CONFIGURE_FAILED", "COMPILE_FAILED",
    "EXECUTABLE_MISSING", "MODEL_PATH_MISSING", "MODEL_LOAD_FAILED",
    "INFERENCE_FAILED", "OFFLINE_DEPENDENCY_MISS", "UNSUPPORTED_PLATFORM",
}
TOOLS = ("uv", "python", "cmake", "ninja", "compiler")


class ValidationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate(data: dict[str, Any]) -> None:
    require(data.get("schema_version") == "1.0.0", "schema_version must be 1.0.0")

    env = data.get("environment", {})
    require(env.get("tier") in {"local_native", "cloud_container"}, "invalid execution tier")
    require(env.get("support_state") in {"planned", "validated", "degraded", "unsupported"}, "invalid support_state")
    require(env.get("offline_mode") in {"not_tested", "ready_from_cache", "blocked_without_cache"}, "invalid offline_mode")

    revisions = data.get("revisions", {})
    require(bool(SHA40.fullmatch(str(revisions.get("course", "")))), "course revision must be a full commit")
    require(bool(SHA40.fullmatch(str(revisions.get("llama_cpp", "")))), "llama_cpp revision must be a full commit")
    require(bool(SHA256.fullmatch(str(revisions.get("uv_lock_sha256", "")))), "uv lock hash must be SHA-256")

    toolchain = data.get("toolchain", {})
    for name in TOOLS:
        tool = toolchain.get(name)
        require(isinstance(tool, dict), f"missing toolchain.{name}")
        require(isinstance(tool.get("command"), str) and tool["command"], f"{name} command is required")
        require(isinstance(tool.get("version"), str) and tool["version"], f"{name} version is required")
        require(isinstance(tool.get("passed"), bool), f"{name} passed must be boolean")

    commands = data.get("commands", {})
    require(commands.get("python_sync") == "uv sync --locked", "Python environment must use uv sync --locked")
    require(str(commands.get("configure", "")).startswith("cmake "), "configure command must use cmake")
    require("-G Ninja" in str(commands.get("configure", "")), "configure command must select Ninja")
    require(str(commands.get("compile", "")).startswith("cmake --build "), "compile command must use cmake --build")
    require("--target" in str(commands.get("compile", "")), "compile command must name a bounded target")
    require(bool(commands.get("launch")), "launch command is required")

    timings = data.get("timings", {})
    start = timings.get("started_monotonic_ms")
    ready = timings.get("ready_monotonic_ms")
    ttr = timings.get("time_to_ready_ms")
    require(all(isinstance(v, int) and v >= 0 for v in (start, ready, ttr)), "ready timings must be non-negative integers")
    require(ready >= start, "ready timestamp precedes start")
    require(ttr == ready - start, "time_to_ready_ms must equal ready-start")

    result = data.get("result", {})
    for key in ("setup_success", "build_success", "launch_success"):
        require(isinstance(result.get(key), bool), f"result.{key} must be boolean")
    require(result.get("model_kind") in {"none", "learner_provided"}, "invalid model_kind")
    require(result.get("inference_state") in {"not_attempted", "passed", "failed", "blocked"}, "invalid inference_state")
    diagnostics = result.get("diagnostics")
    require(isinstance(diagnostics, list), "diagnostics must be a list")
    require(len(diagnostics) == len(set(diagnostics)), "diagnostics must be unique")
    require(set(diagnostics) <= DIAGNOSTICS, "unknown diagnostic code")

    all_tools = all(toolchain[name]["passed"] for name in TOOLS)
    if result["setup_success"]:
        require(all_tools, "setup_success requires every required tool check to pass")
        require(not diagnostics.intersection({"UV_MISSING", "UV_LOCK_DRIFT", "PYTHON_UNSUPPORTED", "CMAKE_MISSING", "NINJA_MISSING", "COMPILER_MISSING"}), "setup_success conflicts with setup diagnostic")
    if result["build_success"]:
        require(result["setup_success"], "build_success requires setup_success")
        require("CONFIGURE_FAILED" not in diagnostics and "COMPILE_FAILED" not in diagnostics, "build_success conflicts with build diagnostic")
    if result["launch_success"]:
        require(result["build_success"], "launch_success requires build_success")
        require("EXECUTABLE_MISSING" not in diagnostics, "launch_success conflicts with executable diagnostic")

    model_kind = result["model_kind"]
    inference_state = result["inference_state"]
    if model_kind == "none":
        require(inference_state == "not_attempted", "model-free runs cannot claim inference")
        require("optional_inference" not in commands, "model-free runs cannot include an inference command")
        require("time_to_first_token_ms" not in timings and "first_token_monotonic_ms" not in timings, "model-free runs cannot record first-token timing")
    if inference_state == "passed":
        require(model_kind == "learner_provided", "passed inference requires a learner-provided model")
        require(result["launch_success"], "passed inference requires launch_success")
        require("optional_inference" in commands, "passed inference requires an explicit command")
        first = timings.get("first_token_monotonic_ms")
        ttft = timings.get("time_to_first_token_ms")
        require(isinstance(first, int) and isinstance(ttft, int), "passed inference requires first-token timings")
        require(first >= start and ttft == first - start, "time_to_first_token_ms must equal first-token-start")

    security = data.get("security", {})
    require(security.get("model_redistributed") is False, "model redistribution is forbidden")
    require(security.get("secrets_recorded") is False, "secrets must not be recorded")
    require(security.get("personal_paths_recorded") is False, "personal paths must not be recorded")
    require(isinstance(security.get("network_required_after_cache"), bool), "network_required_after_cache must be boolean")
    if env.get("offline_mode") == "ready_from_cache":
        require(security["network_required_after_cache"] is False, "cached offline readiness cannot require network")
    if env.get("support_state") == "validated":
        require(result["setup_success"] and result["build_success"] and result["launch_success"], "validated environments require setup, build, and launch success")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_lab0_reproducibility.py <report.json>", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        require(isinstance(data, dict), "report root must be an object")
        validate(data)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"invalid Lab 0 reproducibility report: {exc}", file=sys.stderr)
        return 1
    print("Lab 0 reproducibility report is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
