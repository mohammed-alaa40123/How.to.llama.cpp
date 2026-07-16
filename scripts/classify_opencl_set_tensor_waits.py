#!/usr/bin/env python3
"""Classify unresolved simple OpenCL waits inside the pinned set_tensor path.

This is a bounded lexical aid. It consumes the lifecycle report produced by
extract_opencl_lifecycle_calls.py and the exact source used to produce it.
It classifies only unmatched simple-identifier waits that are not already
annotated as immediately followed by a same-queue blocking read.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

_FUNCTION_RE = re.compile(r"^\s*(?:static\s+)?(?:[\w:<>,*&]+\s+)+([\w:~]+)\s*\(")


def _next_statement(lines: list[str], wait_line: int, scope_end_line: int) -> tuple[int | None, str | None]:
    """Return the next non-comment source statement after a 1-based wait line."""
    for line_no in range(wait_line + 1, min(scope_end_line, len(lines)) + 1):
        text = lines[line_no - 1].strip()
        if not text or text.startswith("//") or text.startswith("#"):
            continue
        return line_no, text
    return None, None


def _enclosing_function(lines: list[str], line_no: int) -> str | None:
    for idx in range(line_no - 1, -1, -1):
        match = _FUNCTION_RE.match(lines[idx])
        if match:
            return match.group(1)
    return None


def classify_waits(source_text: str, report: dict[str, Any]) -> dict[str, Any]:
    lines = source_text.splitlines()
    records: list[dict[str, Any]] = []

    for record in report.get("simple_waited_events", []):
        if record.get("status") != "unmatched_in_scope":
            continue
        if record.get("followed_by_same_queue_blocking_read"):
            continue

        wait_line = int(record["wait_line"])
        scope_end_line = int(record["scope_end_line"])
        next_line, next_text = _next_statement(lines, wait_line, scope_end_line)

        if next_text and "clReleaseMemObject(data_device)" in next_text:
            classification = "temporary_upload_buffer_release"
        elif next_text == "}":
            classification = "nested_scope_exit"
        else:
            classification = "other"

        records.append(
            {
                "event": record.get("event"),
                "wait_line": wait_line,
                "scope_end_line": scope_end_line,
                "enclosing_function": _enclosing_function(lines, wait_line),
                "next_line": next_line,
                "next_statement": next_text,
                "classification": classification,
            }
        )

    counts = Counter(item["classification"] for item in records)
    return {
        "source": report.get("source"),
        "classified_wait_count": len(records),
        "counts": dict(sorted(counts.items())),
        "records": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("report", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    source_text = args.source.read_text(encoding="utf-8")
    report = json.loads(args.report.read_text(encoding="utf-8"))
    result = classify_waits(source_text, report)
    payload = json.dumps(result, indent=2, sort_keys=False) + "\n"

    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
