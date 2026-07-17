#!/usr/bin/env python3
"""Validate immutable trace source anchors and deterministic navigation semantics."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from scripts.validate_executable_trace import validate_trace

LOCK_VERSION = "0.1.0"


def _anchor_key(location: dict[str, Any]) -> tuple[str, int, str] | None:
    file = location.get("file")
    line = location.get("line")
    function = location.get("function")
    if isinstance(file, str) and isinstance(line, int) and isinstance(function, str):
        return file, line, function
    return None


def validate_source_lock(trace: Any, lock: Any) -> list[str]:
    """Validate a trace against a checked-in lock derived from an immutable source blob."""
    errors = validate_trace(trace)
    if not isinstance(trace, dict) or not isinstance(lock, dict):
        return errors + ["trace and source lock must be objects"]

    if lock.get("lock_version") != LOCK_VERSION:
        errors.append(f"source lock version must be {LOCK_VERSION}")

    source = trace.get("source", {})
    for field in ("repository", "revision"):
        if source.get(field) != lock.get(field):
            errors.append(f"source lock {field} does not match trace")

    anchors: dict[tuple[str, int, str], dict[str, Any]] = {}
    files = lock.get("files")
    if not isinstance(files, list) or not files:
        return errors + ["source lock files must be a non-empty array"]

    for file_index, file_record in enumerate(files):
        if not isinstance(file_record, dict):
            errors.append(f"source lock files[{file_index}] must be an object")
            continue
        path = file_record.get("path")
        blob_sha = file_record.get("blob_sha")
        if not isinstance(path, str) or not path:
            errors.append(f"source lock files[{file_index}].path is invalid")
            continue
        if not isinstance(blob_sha, str) or len(blob_sha) != 40:
            errors.append(f"source lock files[{file_index}].blob_sha must be a 40-character SHA")
        for anchor_index, anchor in enumerate(file_record.get("anchors", [])):
            if not isinstance(anchor, dict):
                errors.append(f"source lock anchor {file_index}:{anchor_index} must be an object")
                continue
            key = _anchor_key({"file": path, **anchor})
            line_text = anchor.get("line_text")
            digest = anchor.get("line_sha256")
            if key is None or not isinstance(line_text, str) or not isinstance(digest, str):
                errors.append(f"source lock anchor {file_index}:{anchor_index} is incomplete")
                continue
            actual = hashlib.sha256(line_text.encode("utf-8")).hexdigest()
            if actual != digest:
                errors.append(f"source lock anchor hash mismatch: {path}:{anchor.get('line')}")
            if key in anchors:
                errors.append(f"duplicate source lock anchor: {path}:{anchor.get('line')}:{anchor.get('function')}")
            anchors[key] = anchor

    for step_index, step in enumerate(trace.get("steps", [])):
        if not isinstance(step, dict):
            continue
        locations = [("location", step.get("location"))]
        locations.extend((f"call_stack[{i}]", frame) for i, frame in enumerate(step.get("call_stack", [])))
        for label, location in locations:
            if not isinstance(location, dict):
                continue
            key = _anchor_key(location)
            if key not in anchors:
                file = location.get("file")
                line = location.get("line")
                function = location.get("function")
                errors.append(f"steps[{step_index}].{label} is not locked: {file}:{line}:{function}")

    return errors


def replay_step_index(current: int, command: str, step_count: int) -> int:
    """Return a deterministic, bounded index for keyboard/button navigation."""
    if step_count < 1:
        raise ValueError("step_count must be positive")
    if not 0 <= current < step_count:
        raise ValueError("current index is out of range")
    if command == "next":
        return min(current + 1, step_count - 1)
    if command == "previous":
        return max(current - 1, 0)
    if command == "first":
        return 0
    if command == "last":
        return step_count - 1
    raise ValueError(f"unknown replay command: {command}")


def static_replay(trace: dict[str, Any]) -> list[dict[str, Any]]:
    """Produce the ordered, non-animated fallback consumed by tests and future viewers."""
    return [
        {
            "sequence": step["sequence"],
            "step_id": step["step_id"],
            "source": f"{step['location']['file']}:{step['location']['line']}",
            "function": step["location"]["function"],
            "evidence_kind": step["evidence_kind"],
            "summary": step["static_summary"],
        }
        for step in trace["steps"]
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path)
    parser.add_argument("source_lock", type=Path)
    args = parser.parse_args()
    try:
        raw = args.trace.read_bytes()
        trace = json.loads(raw)
        lock = json.loads(args.source_lock.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors = validate_trace(trace, raw_size=len(raw)) + validate_source_lock(trace, lock)
    # validate_source_lock calls the structural validator for direct library use.
    errors = list(dict.fromkeys(errors))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Trace source/replay validation passed: {args.trace}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
