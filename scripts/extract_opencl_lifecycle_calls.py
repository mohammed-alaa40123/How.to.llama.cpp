#!/usr/bin/env python3
"""Extract bounded OpenCL lifecycle calls with exact source lines.

This is a teardown-audit aid, not a C/C++ parser. It reports selected OpenCL
completion and release calls while ignoring comments and string literals only
when they do not resemble direct function calls.
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


def line_number(text: str, offset: int) -> int:
    """Return the 1-based source line containing offset."""
    return text.count("\n", 0, offset) + 1


def extract_opencl_lifecycle_calls(text: str) -> list[dict[str, object]]:
    """Return source-ordered selected OpenCL lifecycle call sites."""
    return [
        {"name": match.group(1), "line": line_number(text, match.start())}
        for match in OPENCL_LIFECYCLE_CALL_RE.finditer(text)
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
