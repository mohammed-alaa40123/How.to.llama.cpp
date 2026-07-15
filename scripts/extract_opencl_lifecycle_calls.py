#!/usr/bin/env python3
"""Extract bounded OpenCL lifecycle calls with exact source lines.

This is a teardown-audit aid, not a C/C++ parser. It reports selected direct
OpenCL creation, retention, completion, and release calls after masking comments
and string/character literals while preserving source length and newline
positions. Optional bounded source context makes generated reports reviewable
without changing call matching. A separate simple-local waited-event diagnostic
pairs ``clWaitForEvents(1, &event)`` with a later ``clReleaseEvent(event)`` in
the same lexical brace scope; it is deliberately a heuristic, not ownership proof.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

OPENCL_LIFECYCLE_CALL_RE = re.compile(
    r"\b("
    r"clCreateContext|clCreateContextFromType|clRetainContext|"
    r"clCreateCommandQueue|clCreateCommandQueueWithProperties|clRetainCommandQueue|"
    r"clFinish|clFlush|clWaitForEvents|"
    r"clReleaseCommandQueue|clReleaseContext|clReleaseProgram|"
    r"clReleaseKernel|clReleaseEvent|clReleaseMemObject"
    r")\s*\("
)
SIMPLE_WAIT_EVENT_RE = re.compile(
    r"\bclWaitForEvents\s*\(\s*1\s*,\s*&\s*([A-Za-z_]\w*)\s*\)"
)


def mask_comments_and_literals(text: str) -> str:
    """Mask C/C++ comments and quoted literals without shifting source lines."""
    chars = list(text)
    i = 0
    state = "code"
    quote = ""

    while i < len(chars):
        ch = chars[i]
        nxt = chars[i + 1] if i + 1 < len(chars) else ""

        if state == "code":
            if ch == "/" and nxt == "/":
                chars[i] = chars[i + 1] = " "
                state = "line_comment"
                i += 2
                continue
            if ch == "/" and nxt == "*":
                chars[i] = chars[i + 1] = " "
                state = "block_comment"
                i += 2
                continue
            if ch in {'"', "'"}:
                quote = ch
                chars[i] = " "
                state = "literal"
                i += 1
                continue
        elif state == "line_comment":
            if ch == "\n":
                state = "code"
            else:
                chars[i] = " "
        elif state == "block_comment":
            if ch == "*" and nxt == "/":
                chars[i] = chars[i + 1] = " "
                state = "code"
                i += 2
                continue
            if ch != "\n":
                chars[i] = " "
        else:  # literal
            if ch == "\\":
                chars[i] = " "
                if i + 1 < len(chars):
                    if chars[i + 1] != "\n":
                        chars[i + 1] = " "
                    i += 2
                    continue
            if ch == quote:
                chars[i] = " "
                state = "code"
            elif ch != "\n":
                chars[i] = " "

        i += 1

    return "".join(chars)


def line_number(text: str, offset: int) -> int:
    """Return the 1-based source line containing offset."""
    return text.count("\n", 0, offset) + 1


def source_context(text: str, line: int, radius: int) -> dict[str, object]:
    """Return bounded original-source context around a 1-based line."""
    if radius < 0:
        raise ValueError("context radius must be non-negative")

    lines = text.splitlines()
    if not lines:
        return {"start_line": 1, "end_line": 1, "text": ""}

    start_line = max(1, line - radius)
    end_line = min(len(lines), line + radius)
    return {
        "start_line": start_line,
        "end_line": end_line,
        "text": "\n".join(lines[start_line - 1 : end_line]),
    }


def enclosing_scope_end(masked: str, offset: int) -> int:
    """Return the offset just before the current lexical brace scope ends."""
    depth = 0
    for ch in masked[:offset]:
        if ch == "{":
            depth += 1
        elif ch == "}" and depth:
            depth -= 1

    if depth == 0:
        return len(masked)

    current_depth = depth
    for index in range(offset, len(masked)):
        ch = masked[index]
        if ch == "{":
            current_depth += 1
        elif ch == "}":
            current_depth -= 1
            if current_depth < depth:
                return index
    return len(masked)


def analyze_simple_waited_events(text: str) -> list[dict[str, object]]:
    """Pair simple local event waits with releases before lexical scope exit.

    Only ``clWaitForEvents(1, &identifier)`` is recognized. The search is lexical,
    ignores comments and literals, and does not model aliases, macros, control-flow
    reachability, ownership transfer, or releases performed by helper functions.
    """
    masked = mask_comments_and_literals(text)
    diagnostics: list[dict[str, object]] = []
    for wait in SIMPLE_WAIT_EVENT_RE.finditer(masked):
        event = wait.group(1)
        scope_end = enclosing_scope_end(masked, wait.end())
        release_re = re.compile(rf"\bclReleaseEvent\s*\(\s*{re.escape(event)}\s*\)")
        release = release_re.search(masked, wait.end(), scope_end)
        record: dict[str, object] = {
            "event": event,
            "wait_line": line_number(masked, wait.start()),
            "scope_end_line": line_number(masked, scope_end),
            "status": "released_in_scope" if release else "unmatched_in_scope",
        }
        if release:
            record["release_line"] = line_number(masked, release.start())
        diagnostics.append(record)
    return diagnostics


def extract_opencl_lifecycle_calls(
    text: str, context_lines: int = 0
) -> list[dict[str, object]]:
    """Return source-ordered selected OpenCL lifecycle call sites."""
    if context_lines < 0:
        raise ValueError("context_lines must be non-negative")

    masked = mask_comments_and_literals(text)
    calls: list[dict[str, object]] = []
    for match in OPENCL_LIFECYCLE_CALL_RE.finditer(masked):
        line = line_number(masked, match.start())
        record: dict[str, object] = {"name": match.group(1), "line": line}
        if context_lines:
            record["context"] = source_context(text, line, context_lines)
        calls.append(record)
    return calls


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument(
        "--context-lines",
        type=int,
        default=0,
        help="include this many original-source lines before and after each call",
    )
    args = parser.parse_args()

    if args.context_lines < 0:
        parser.error("--context-lines must be non-negative")

    text = args.source.read_text(encoding="utf-8")
    calls = extract_opencl_lifecycle_calls(text, context_lines=args.context_lines)
    wait_diagnostics = analyze_simple_waited_events(text)
    summary = {
        "source": str(args.source),
        "context_lines": args.context_lines,
        "calls": calls,
        "counts": {
            name: sum(1 for call in calls if call["name"] == name)
            for name in sorted({str(call["name"]) for call in calls})
        },
        "simple_waited_events": wait_diagnostics,
        "simple_waited_event_counts": {
            status: sum(1 for item in wait_diagnostics if item["status"] == status)
            for status in ("released_in_scope", "unmatched_in_scope")
        },
    }
    rendered = json.dumps(summary, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
