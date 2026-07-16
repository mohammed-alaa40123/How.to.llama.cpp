#!/usr/bin/env python3
"""Dependency-free semantic validator for executable lecture traces."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any

MAX_TRACE_BYTES = 2 * 1024 * 1024
MAX_STEPS = 500
EVIDENCE_KINDS = {
    "native-captured",
    "source-derived",
    "authored-example",
    "interpretation",
    "open-question",
}
SOURCE_CAPTURE_KINDS = {
    "native-captured",
    "source-derived",
    "authored-example",
}
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,127}$")


def _require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def _safe_repo_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def validate_trace(data: Any, *, raw_size: int | None = None) -> list[str]:
    errors: list[str] = []
    if raw_size is not None:
        _require(raw_size <= MAX_TRACE_BYTES, f"trace exceeds {MAX_TRACE_BYTES} bytes", errors)
    if not isinstance(data, dict):
        return ["trace root must be an object"]

    _require(data.get("schema_version") == "0.1.0", "schema_version must be 0.1.0", errors)
    for key in ("trace_id", "lesson_id"):
        value = data.get(key)
        _require(isinstance(value, str) and bool(ID_RE.fullmatch(value)), f"{key} is invalid", errors)

    source = data.get("source")
    if not isinstance(source, dict):
        errors.append("source must be an object")
        source = {}
    repository = source.get("repository")
    _require(
        isinstance(repository, str)
        and repository.count("/") == 1
        and all(repository.split("/")),
        "source.repository must use owner/name",
        errors,
    )
    revision = source.get("revision")
    _require(isinstance(revision, str) and bool(SHA40.fullmatch(revision)), "source.revision must be a full 40-character lowercase commit SHA", errors)
    capture_kind = source.get("capture_kind")
    _require(capture_kind in SOURCE_CAPTURE_KINDS, "source.capture_kind is invalid", errors)
    fixture_sha = source.get("fixture_sha256")
    if fixture_sha is not None:
        _require(isinstance(fixture_sha, str) and bool(SHA256.fullmatch(fixture_sha)), "source.fixture_sha256 is invalid", errors)

    steps = data.get("steps")
    if not isinstance(steps, list):
        return errors + ["steps must be an array"]
    _require(1 <= len(steps) <= MAX_STEPS, f"steps must contain 1..{MAX_STEPS} items", errors)

    seen_step_ids: set[str] = set()
    sequences: list[int] = []
    for index, step in enumerate(steps):
        prefix = f"steps[{index}]"
        if not isinstance(step, dict):
            errors.append(f"{prefix} must be an object")
            continue

        sequence = step.get("sequence")
        _require(isinstance(sequence, int) and not isinstance(sequence, bool), f"{prefix}.sequence must be an integer", errors)
        if isinstance(sequence, int) and not isinstance(sequence, bool):
            sequences.append(sequence)

        step_id = step.get("step_id")
        _require(isinstance(step_id, str) and bool(ID_RE.fullmatch(step_id)), f"{prefix}.step_id is invalid", errors)
        if isinstance(step_id, str):
            _require(step_id not in seen_step_ids, f"duplicate step_id: {step_id}", errors)
            seen_step_ids.add(step_id)

        evidence_kind = step.get("evidence_kind")
        _require(evidence_kind in EVIDENCE_KINDS, f"{prefix}.evidence_kind is invalid", errors)

        location = step.get("location")
        if not isinstance(location, dict):
            errors.append(f"{prefix}.location must be an object")
        else:
            _require(_safe_repo_path(location.get("file")), f"{prefix}.location.file must be a safe repository-relative path", errors)
            line = location.get("line")
            _require(isinstance(line, int) and not isinstance(line, bool) and line >= 1, f"{prefix}.location.line must be >= 1", errors)
            end_line = location.get("end_line")
            if end_line is not None and isinstance(line, int):
                _require(isinstance(end_line, int) and end_line >= line, f"{prefix}.location.end_line must be >= line", errors)
            _require(isinstance(location.get("function"), str) and bool(location.get("function")), f"{prefix}.location.function is required", errors)

        _require(isinstance(step.get("explanation_id"), str) and bool(ID_RE.fullmatch(step.get("explanation_id", ""))), f"{prefix}.explanation_id is invalid", errors)
        static_summary = step.get("static_summary")
        _require(isinstance(static_summary, str) and len(static_summary.strip()) >= 20, f"{prefix}.static_summary must provide a meaningful static fallback", errors)

        for collection_name in ("runtime_objects", "tensor_shapes", "memory_events", "figures"):
            collection = step.get(collection_name, [])
            _require(isinstance(collection, list), f"{prefix}.{collection_name} must be an array when present", errors)
            if isinstance(collection, list):
                for item_index, item in enumerate(collection):
                    if not isinstance(item, dict):
                        errors.append(f"{prefix}.{collection_name}[{item_index}] must be an object")
                        continue
                    _require(item.get("evidence_kind") in EVIDENCE_KINDS, f"{prefix}.{collection_name}[{item_index}].evidence_kind is invalid", errors)
                    if evidence_kind == "authored-example" and item.get("evidence_kind") == "native-captured":
                        errors.append(f"{prefix}.{collection_name}[{item_index}] cannot claim native capture inside an authored-example step")

        figures = step.get("figures", [])
        if isinstance(figures, list):
            for figure_index, figure in enumerate(figures):
                if isinstance(figure, dict):
                    _require(_safe_repo_path(figure.get("path")), f"{prefix}.figures[{figure_index}].path must be repository-relative", errors)
                    alt_text = figure.get("alt_text")
                    _require(isinstance(alt_text, str) and len(alt_text.strip()) >= 20, f"{prefix}.figures[{figure_index}].alt_text is too short", errors)

    if len(sequences) == len(steps):
        _require(sequences == list(range(len(steps))), "step sequences must be contiguous, ordered, and zero-based", errors)

    if capture_kind == "authored-example":
        for index, step in enumerate(steps):
            if isinstance(step, dict) and step.get("evidence_kind") == "native-captured":
                errors.append(f"steps[{index}] cannot claim native capture when source.capture_kind is authored-example")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path)
    args = parser.parse_args()

    try:
        raw = args.trace.read_bytes()
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors = validate_trace(data, raw_size=len(raw))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Executable trace validation passed: {args.trace}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
