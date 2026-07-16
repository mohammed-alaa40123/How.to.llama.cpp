#!/usr/bin/env python3
"""Generate a behavior-preserving release-only fix for simple waited OpenCL events.

This tool consumes the lifecycle JSON produced by
``extract_opencl_lifecycle_calls.py`` and inserts ``clReleaseEvent(event)``
immediately after every ``unmatched_in_scope`` simple wait. It deliberately
preserves every wait and all surrounding synchronization.

The transformation is bounded to the exact wait line and event identifier in
the report. It refuses stale or ambiguous inputs rather than guessing.
"""

from __future__ import annotations

import argparse
import difflib
import json
from pathlib import Path


def apply_release_fix(source: str, report: dict) -> tuple[str, int]:
    lines = source.splitlines(keepends=True)
    unmatched = {
        int(record["wait_line"]): str(record["event"])
        for record in report.get("simple_waited_events", [])
        if record.get("status") == "unmatched_in_scope"
    }

    if not unmatched:
        raise ValueError("report contains no unmatched simple waited events")

    if len(unmatched) != sum(
        1
        for record in report.get("simple_waited_events", [])
        if record.get("status") == "unmatched_in_scope"
    ):
        raise ValueError("multiple unmatched records refer to the same wait line")

    output: list[str] = []
    for line_number, line in enumerate(lines, start=1):
        output.append(line)
        event = unmatched.get(line_number)
        if event is None:
            continue

        expected = f"clWaitForEvents(1, &{event})"
        if expected not in line:
            raise ValueError(
                f"wait line {line_number} does not contain expected call {expected!r}"
            )

        indent = line[: len(line) - len(line.lstrip())]
        newline = "\r\n" if line.endswith("\r\n") else "\n"
        output.append(f"{indent}CL_CHECK(clReleaseEvent({event}));{newline}")

    missing = sorted(set(unmatched) - set(range(1, len(lines) + 1)))
    if missing:
        raise ValueError(f"wait lines fall outside source: {missing}")

    return "".join(output), len(unmatched)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("report", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--patch-out", type=Path)
    parser.add_argument("--expected-fixes", type=int)
    args = parser.parse_args()

    source_text = args.source.read_text(encoding="utf-8")
    report = json.loads(args.report.read_text(encoding="utf-8"))
    patched_text, fix_count = apply_release_fix(source_text, report)

    if args.expected_fixes is not None and fix_count != args.expected_fixes:
        raise SystemExit(
            f"expected {args.expected_fixes} release insertions, generated {fix_count}"
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(patched_text, encoding="utf-8")

    if args.patch_out is not None:
        patch = "".join(
            difflib.unified_diff(
                source_text.splitlines(keepends=True),
                patched_text.splitlines(keepends=True),
                fromfile="a/ggml/src/ggml-opencl/ggml-opencl.cpp",
                tofile="b/ggml/src/ggml-opencl/ggml-opencl.cpp",
                n=3,
            )
        )
        if not patch:
            raise SystemExit("release fix unexpectedly produced an empty patch")
        args.patch_out.parent.mkdir(parents=True, exist_ok=True)
        args.patch_out.write_text(patch, encoding="utf-8")

    print(f"inserted {fix_count} clReleaseEvent calls")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
