#!/usr/bin/env python3
"""Annotate bounded OpenCL waited-event diagnostics with immediate follow-up hints.

This tool intentionally keeps event ownership and synchronization separate. It
recognizes only simple ``clWaitForEvents(1, &identifier)`` records already emitted
by ``extract_opencl_lifecycle_calls.py`` and asks whether the immediately following
statement is a same-queue blocking ``clEnqueueReadBuffer(..., CL_TRUE, ...)``.
It is a lexical review aid, not C++ control-flow or alias analysis.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
EXTRACTOR_PATH = SCRIPT_DIR / "extract_opencl_lifecycle_calls.py"
SPEC = importlib.util.spec_from_file_location("extract_opencl_lifecycle_calls", EXTRACTOR_PATH)
assert SPEC and SPEC.loader
extractor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(extractor)


def statement_end(masked: str, start: int) -> int:
    """Return the end offset of the next semicolon-terminated statement."""
    depth = 0
    for index in range(start, len(masked)):
        ch = masked[index]
        if ch == "(":
            depth += 1
        elif ch == ")" and depth:
            depth -= 1
        elif ch == ";" and depth == 0:
            return index + 1
    return len(masked)


def matching_paren(text: str, open_index: int) -> int | None:
    depth = 0
    for index in range(open_index, len(text)):
        if text[index] == "(":
            depth += 1
        elif text[index] == ")":
            depth -= 1
            if depth == 0:
                return index
    return None


def split_top_level_arguments(arguments: str) -> list[str]:
    parts: list[str] = []
    start = 0
    depth = 0
    for index, ch in enumerate(arguments):
        if ch in "([{<":
            depth += 1
        elif ch in ")]}>":
            depth = max(0, depth - 1)
        elif ch == "," and depth == 0:
            parts.append(arguments[start:index].strip())
            start = index + 1
    parts.append(arguments[start:].strip())
    return parts


def classify_wait_followups(source: str) -> list[dict[str, Any]]:
    """Classify immediate statements after simple local event waits."""
    masked = extractor.mask_comments_and_literals(source)
    records: list[dict[str, Any]] = []

    for wait in extractor.SIMPLE_WAIT_EVENT_RE.finditer(masked):
        semicolon = masked.find(";", wait.end())
        if semicolon < 0:
            next_start = wait.end()
        else:
            next_start = semicolon + 1
        next_start += len(masked[next_start:]) - len(masked[next_start:].lstrip())
        end = statement_end(masked, next_start)
        statement = masked[next_start:end]

        call = re.search(r"\bclEnqueueReadBuffer\s*\(", statement)
        same_queue_blocking_read = False
        read_line: int | None = None
        if call:
            open_index = statement.find("(", call.start())
            close_index = matching_paren(statement, open_index)
            if close_index is not None:
                args = split_top_level_arguments(statement[open_index + 1 : close_index])
                same_queue_blocking_read = (
                    len(args) >= 3 and args[0] == "queue" and args[2] == "CL_TRUE"
                )
                read_line = extractor.line_number(masked, next_start + call.start())

        record: dict[str, Any] = {
            "event": wait.group(1),
            "wait_line": extractor.line_number(masked, wait.start()),
            "followed_by_same_queue_blocking_read": same_queue_blocking_read,
        }
        if read_line is not None:
            record["read_line"] = read_line
        records.append(record)

    return records


def annotate_report(report: dict[str, Any], source: str) -> dict[str, Any]:
    """Add synchronization hints to an existing lifecycle report in place."""
    followups = {
        (item["event"], item["wait_line"]): item
        for item in classify_wait_followups(source)
    }
    matched = 0
    unmatched = 0
    for item in report.get("simple_waited_events", []):
        hint = followups.get((item.get("event"), item.get("wait_line")))
        is_match = bool(hint and hint["followed_by_same_queue_blocking_read"])
        item["followed_by_same_queue_blocking_read"] = is_match
        if hint and "read_line" in hint:
            item["next_read_line"] = hint["read_line"]
        if item.get("status") == "unmatched_in_scope":
            if is_match:
                matched += 1
            else:
                unmatched += 1
    report["simple_waited_event_followup_counts"] = {
        "unmatched_followed_by_same_queue_blocking_read": matched,
        "other_unmatched": unmatched,
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()

    source = args.source.read_text(encoding="utf-8")
    report = json.loads(args.report.read_text(encoding="utf-8"))
    annotate_report(report, source)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
