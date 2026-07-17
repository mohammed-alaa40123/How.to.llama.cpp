#!/usr/bin/env python3
"""Validate executable-trace source anchors and deterministic navigation semantics."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _manifest_index(manifest: dict[str, Any]) -> dict[tuple[str, str], list[dict[str, Any]]]:
    index: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for file_entry in manifest.get("files", []):
        if not isinstance(file_entry, dict):
            continue
        path = file_entry.get("path")
        for function in file_entry.get("functions", []):
            if isinstance(path, str) and isinstance(function, dict):
                name = function.get("name")
                if isinstance(name, str):
                    index.setdefault((path, name), []).append(function)
    return index


def _check_location(
    location: Any,
    *,
    prefix: str,
    source_index: dict[tuple[str, str], list[dict[str, Any]]],
    errors: list[str],
) -> None:
    if not isinstance(location, dict):
        errors.append(f"{prefix} must be an object")
        return
    path = location.get("file")
    function = location.get("function")
    line = location.get("line")
    ranges = source_index.get((path, function), [])
    if not ranges:
        errors.append(f"{prefix} has no pinned file/function anchor: {path}:{function}")
        return
    if not isinstance(line, int) or isinstance(line, bool):
        errors.append(f"{prefix}.line must be an integer")
        return
    if not any(item.get("start_line", 0) <= line <= item.get("end_line", -1) for item in ranges):
        errors.append(f"{prefix}.line {line} is outside the pinned function range")


def replay_index(step_count: int, index: int, action: str) -> int:
    """Pure, deterministic browser navigation transition with clamped boundaries."""
    if step_count < 1:
        raise ValueError("step_count must be positive")
    if not 0 <= index < step_count:
        raise ValueError("index is outside trace bounds")
    if action == "next":
        return min(index + 1, step_count - 1)
    if action == "previous":
        return max(index - 1, 0)
    raise ValueError(f"unsupported action: {action}")


def validate_source_links(trace: Any, manifest: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(trace, dict) or not isinstance(manifest, dict):
        return ["trace and source-anchor manifest must be objects"]

    source = trace.get("source", {})
    for key in ("repository", "revision"):
        if source.get(key) != manifest.get(key):
            errors.append(f"trace source.{key} does not match the pinned manifest")

    source_index = _manifest_index(manifest)
    steps = trace.get("steps")
    if not isinstance(steps, list) or not steps:
        return errors + ["trace steps must be a non-empty array"]

    for step_index, step in enumerate(steps):
        if not isinstance(step, dict):
            errors.append(f"steps[{step_index}] must be an object")
            continue
        _check_location(step.get("location"), prefix=f"steps[{step_index}].location", source_index=source_index, errors=errors)
        call_stack = step.get("call_stack", [])
        if not isinstance(call_stack, list):
            errors.append(f"steps[{step_index}].call_stack must be an array")
        else:
            for frame_index, frame in enumerate(call_stack):
                _check_location(frame, prefix=f"steps[{step_index}].call_stack[{frame_index}]", source_index=source_index, errors=errors)

    count = len(steps)
    for index in range(count):
        if replay_index(count, replay_index(count, index, "next"), "previous") != index and index < count - 1:
            errors.append(f"navigation round trip failed at step {index}")
        if replay_index(count, replay_index(count, index, "previous"), "next") != index and index > 0:
            errors.append(f"reverse navigation round trip failed at step {index}")
    if replay_index(count, 0, "previous") != 0:
        errors.append("previous must clamp at the first step")
    if replay_index(count, count - 1, "next") != count - 1:
        errors.append("next must clamp at the final step")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path)
    parser.add_argument("source_manifest", type=Path)
    args = parser.parse_args()
    try:
        trace = load_json(args.trace)
        manifest = load_json(args.source_manifest)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = validate_source_links(trace, manifest)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Trace source-link validation passed: {args.trace}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
