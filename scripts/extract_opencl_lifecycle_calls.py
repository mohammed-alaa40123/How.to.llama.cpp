#!/usr/bin/env python3
"""Extract bounded OpenCL lifecycle calls with exact source lines.

This is a teardown-audit aid, not a C/C++ parser. It reports selected direct
OpenCL completion and release calls after masking comments and string/character
literals while preserving source length and newline positions.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

OPENCL_LIFECYCLE_CALL_RE = re.compile(
    r"\b("
    r"clFinish|clFlush|clWaitForEvents|"
    r"clReleaseCommandQueue|clReleaseContext|clReleaseProgram|"
    r"clReleaseKernel|clReleaseEvent|clReleaseMemObject"
    r")\s*\("
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


def extract_opencl_lifecycle_calls(text: str) -> list[dict[str, object]]:
    """Return source-ordered selected OpenCL lifecycle call sites."""
    masked = mask_comments_and_literals(text)
    return [
        {"name": match.group(1), "line": line_number(masked, match.start())}
        for match in OPENCL_LIFECYCLE_CALL_RE.finditer(masked)
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    text = args.source.read_text(encoding="utf-8")
    calls = extract_opencl_lifecycle_calls(text)
    summary = {
        "source": str(args.source),
        "calls": calls,
        "counts": {
            name: sum(1 for call in calls if call["name"] == name)
            for name in sorted({str(call["name"]) for call in calls})
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
