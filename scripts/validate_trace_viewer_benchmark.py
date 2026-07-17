#!/usr/bin/env python3
"""Validate the frozen information-equivalent trace-viewer benchmark."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BENCHMARK = ROOT / "executable_lectures/benchmarks/gguf-load-static-vs-viewer-v0.json"
SHA40 = re.compile(r"^[0-9a-f]{40}$")


class BenchmarkValidationError(ValueError):
    """Raised when the benchmark violates a semantic invariant."""


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise BenchmarkValidationError("benchmark root must be an object")
    return value


def validate_benchmark(path: Path = DEFAULT_BENCHMARK, root: Path = ROOT) -> None:
    data = _load(path)
    required = {
        "schema_version", "benchmark_id", "source_revision", "trace_fixture",
        "conditions", "tasks", "scoring", "timing", "accessibility",
    }
    missing = sorted(required - data.keys())
    if missing:
        raise BenchmarkValidationError(f"missing required fields: {', '.join(missing)}")
    if data["schema_version"] != "0.1.0":
        raise BenchmarkValidationError("unsupported benchmark schema_version")
    if not SHA40.fullmatch(str(data["source_revision"])):
        raise BenchmarkValidationError("source_revision must be an immutable 40-character SHA")

    trace_path = root / str(data["trace_fixture"])
    if not trace_path.is_file():
        raise BenchmarkValidationError("trace_fixture does not exist")
    trace = _load(trace_path)
    trace_revision = trace.get("source", {}).get("revision")
    if trace_revision != data["source_revision"]:
        raise BenchmarkValidationError("benchmark and trace source revisions differ")

    steps = trace.get("steps", [])
    if not isinstance(steps, list) or not steps:
        raise BenchmarkValidationError("trace has no steps")
    available_evidence = {f"step:{step.get('step_id')}" for step in steps}
    for step in steps:
        for figure in step.get("figures", []):
            available_evidence.add(f"figure:{figure.get('figure_id')}")

    conditions = data["conditions"]
    if not isinstance(conditions, list) or len(conditions) != 2:
        raise BenchmarkValidationError("exactly two benchmark conditions are required")
    by_id = {condition.get("condition_id"): condition for condition in conditions}
    expected_ids = {"static-source-text", "interactive-viewer"}
    if set(by_id) != expected_ids:
        raise BenchmarkValidationError("conditions must be static-source-text and interactive-viewer")

    static = by_id["static-source-text"]
    viewer = by_id["interactive-viewer"]
    if static.get("evidence_ids") != viewer.get("evidence_ids"):
        raise BenchmarkValidationError("conditions must expose identical ordered evidence_ids")
    if static.get("question_ids") != viewer.get("question_ids"):
        raise BenchmarkValidationError("conditions must expose identical ordered question_ids")
    unknown = set(static.get("evidence_ids", [])) - available_evidence
    if unknown:
        raise BenchmarkValidationError(f"unknown evidence_ids: {sorted(unknown)}")

    forbidden_static = {
        "previous-next-navigation", "home-end-navigation",
        "coordinated-source-highlighting", "deterministic-layout-visualization",
    }
    if forbidden_static.intersection(static.get("allowed_interface_features", [])):
        raise BenchmarkValidationError("static condition includes an interactive-only feature")
    required_viewer = {
        "previous-next-navigation", "coordinated-source-highlighting",
        "deterministic-layout-visualization", "static-text-alternative",
    }
    if not required_viewer.issubset(viewer.get("allowed_interface_features", [])):
        raise BenchmarkValidationError("viewer condition omits required bounded features")

    tasks = data["tasks"]
    if not isinstance(tasks, list) or not (3 <= len(tasks) <= 12):
        raise BenchmarkValidationError("tasks must contain 3 to 12 items")
    task_ids = [task.get("question_id") for task in tasks]
    if len(task_ids) != len(set(task_ids)):
        raise BenchmarkValidationError("question_ids must be unique")
    if task_ids != static.get("question_ids"):
        raise BenchmarkValidationError("condition question order must match task order")
    if not any(task.get("task_type") == "transfer" for task in tasks):
        raise BenchmarkValidationError("at least one held-out transfer task is required")
    for task in tasks:
        if not task.get("answer_key"):
            raise BenchmarkValidationError(f"{task.get('question_id')} has no answer key")
        if set(task.get("evidence_ids", [])) - available_evidence:
            raise BenchmarkValidationError(f"{task.get('question_id')} references unknown evidence")
        if not isinstance(task.get("points"), int) or not 1 <= task["points"] <= 10:
            raise BenchmarkValidationError(f"{task.get('question_id')} has invalid points")

    scoring = data["scoring"]
    if scoring.get("method") != "frozen-exact-key" or scoring.get("missing_response_points") != 0:
        raise BenchmarkValidationError("scoring must use the frozen key and score missing responses as zero")
    timing = data["timing"]
    if timing.get("clock") != "monotonic":
        raise BenchmarkValidationError("timing must use a monotonic clock")
    if timing.get("timeout_handling") != "retain-responses-and-report-timeout-separately":
        raise BenchmarkValidationError("timeout handling must preserve responses and report timeout separately")
    if not 60 <= int(timing.get("limit_seconds", 0)) <= 1800:
        raise BenchmarkValidationError("time limit must be between 60 and 1800 seconds")

    accessibility = data["accessibility"]
    for field in ("keyboard", "static_fallback", "reduced_motion", "screen_reader_text"):
        if accessibility.get(field) is not True:
            raise BenchmarkValidationError(f"accessibility.{field} must be true")


def main(argv: list[str]) -> int:
    target = Path(argv[1]).resolve() if len(argv) > 1 else DEFAULT_BENCHMARK
    try:
        validate_benchmark(target)
    except (OSError, json.JSONDecodeError, BenchmarkValidationError) as exc:
        print(f"benchmark validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"benchmark validation passed: {target.relative_to(ROOT) if target.is_relative_to(ROOT) else target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
