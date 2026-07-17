#!/usr/bin/env python3
"""Validate local-only learner progress exports without external dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

MAX_FILE_BYTES = 512 * 1024
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[a-z0-9.-]+)?$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,95}$")
FORBIDDEN_KEYS = {
    "name",
    "email",
    "username",
    "user_id",
    "ip",
    "ip_address",
    "prompt",
    "raw_prompt",
    "response",
    "raw_response",
    "code",
    "raw_code",
    "telemetry",
    "session_id",
    "device_id",
}


class ProgressValidationError(ValueError):
    """Raised when a progress export violates the local-only contract."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ProgressValidationError(message)


def _walk_forbidden(value: Any, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            _require(key not in FORBIDDEN_KEYS, f"{path}.{key}: forbidden privacy-sensitive field")
            _walk_forbidden(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_forbidden(child, f"{path}[{index}]")


def _validate_datetime(value: Any) -> None:
    _require(isinstance(value, str), "exported_at must be a string")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ProgressValidationError("exported_at must be ISO-8601 date-time") from exc
    _require(parsed.tzinfo is not None, "exported_at must include a timezone")


def validate_progress(data: Any) -> None:
    _require(isinstance(data, dict), "top-level progress export must be an object")
    _walk_forbidden(data)

    allowed_top = {
        "schema_version",
        "course_id",
        "course_version",
        "source_revision",
        "exported_at",
        "storage_scope",
        "lessons",
    }
    _require(set(data) == allowed_top, "top-level fields must exactly match the progress contract")
    _require(data["schema_version"] == "0.1.0", "unsupported schema_version")
    _require(data["course_id"] == "how-to-llama-cpp", "unexpected course_id")
    _require(isinstance(data["course_version"], str) and SEMVER_RE.fullmatch(data["course_version"]), "course_version must be semantic version")
    _require(isinstance(data["source_revision"], str) and SHA_RE.fullmatch(data["source_revision"]), "source_revision must be a full immutable SHA")
    _validate_datetime(data["exported_at"])
    _require(data["storage_scope"] == "local-only", "storage_scope must remain local-only")

    lessons = data["lessons"]
    _require(isinstance(lessons, list), "lessons must be an array")
    _require(len(lessons) <= 128, "lessons exceeds 128-item bound")
    lesson_ids: set[str] = set()

    for lesson_index, lesson in enumerate(lessons):
        prefix = f"lessons[{lesson_index}]"
        _require(isinstance(lesson, dict), f"{prefix} must be an object")
        allowed_lesson = {"lesson_id", "lesson_version", "status", "last_step_id", "checkpoints"}
        _require(set(lesson).issubset(allowed_lesson), f"{prefix} contains unknown fields")
        _require({"lesson_id", "lesson_version", "status", "checkpoints"}.issubset(lesson), f"{prefix} missing required fields")

        lesson_id = lesson["lesson_id"]
        _require(isinstance(lesson_id, str) and ID_RE.fullmatch(lesson_id), f"{prefix}.lesson_id is invalid")
        _require(lesson_id not in lesson_ids, f"duplicate lesson_id: {lesson_id}")
        lesson_ids.add(lesson_id)
        _require(isinstance(lesson["lesson_version"], str) and SEMVER_RE.fullmatch(lesson["lesson_version"]), f"{prefix}.lesson_version is invalid")
        _require(lesson["status"] in {"not-started", "in-progress", "completed"}, f"{prefix}.status is invalid")

        last_step = lesson.get("last_step_id")
        _require(last_step is None or (isinstance(last_step, str) and 1 <= len(last_step) <= 96), f"{prefix}.last_step_id is invalid")
        checkpoints = lesson["checkpoints"]
        _require(isinstance(checkpoints, list), f"{prefix}.checkpoints must be an array")
        _require(len(checkpoints) <= 256, f"{prefix}.checkpoints exceeds bound")

        checkpoint_ids: set[str] = set()
        passed_count = 0
        attempted_count = 0
        for checkpoint_index, checkpoint in enumerate(checkpoints):
            cp_prefix = f"{prefix}.checkpoints[{checkpoint_index}]"
            _require(isinstance(checkpoint, dict), f"{cp_prefix} must be an object")
            _require(set(checkpoint) == {"checkpoint_id", "state", "attempt_count"}, f"{cp_prefix} fields must exactly match contract")
            checkpoint_id = checkpoint["checkpoint_id"]
            _require(isinstance(checkpoint_id, str) and ID_RE.fullmatch(checkpoint_id), f"{cp_prefix}.checkpoint_id is invalid")
            _require(checkpoint_id not in checkpoint_ids, f"duplicate checkpoint_id in {lesson_id}: {checkpoint_id}")
            checkpoint_ids.add(checkpoint_id)
            state = checkpoint["state"]
            attempts = checkpoint["attempt_count"]
            _require(state in {"unanswered", "answered", "passed"}, f"{cp_prefix}.state is invalid")
            _require(isinstance(attempts, int) and not isinstance(attempts, bool) and 0 <= attempts <= 100, f"{cp_prefix}.attempt_count is invalid")
            _require(not (state == "unanswered" and attempts != 0), f"{cp_prefix}: unanswered requires zero attempts")
            _require(not (state in {"answered", "passed"} and attempts == 0), f"{cp_prefix}: answered/passed requires at least one attempt")
            attempted_count += int(attempts > 0)
            passed_count += int(state == "passed")

        status = lesson["status"]
        if status == "not-started":
            _require(attempted_count == 0 and last_step is None, f"{prefix}: not-started cannot contain attempts or last_step_id")
        elif status == "in-progress":
            _require(last_step is not None or attempted_count > 0, f"{prefix}: in-progress requires a step or attempted checkpoint")
        elif status == "completed":
            _require(len(checkpoints) > 0, f"{prefix}: completed requires at least one checkpoint")
            _require(passed_count == len(checkpoints), f"{prefix}: completed requires every checkpoint passed")


def validate_file(path: Path) -> None:
    size = path.stat().st_size
    _require(size <= MAX_FILE_BYTES, f"progress export exceeds {MAX_FILE_BYTES} bytes")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProgressValidationError(f"cannot read valid UTF-8 JSON: {exc}") from exc
    validate_progress(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("progress_file", type=Path)
    args = parser.parse_args()
    try:
        validate_file(args.progress_file)
    except (OSError, ProgressValidationError) as exc:
        print(f"learner progress validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"learner progress validation passed: {args.progress_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
