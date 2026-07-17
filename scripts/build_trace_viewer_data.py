#!/usr/bin/env python3
"""Build the static trace-viewer payload from the validated authored trace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "executable_lectures/traces/gguf-load-authored-v0.json"
DEFAULT_OUTPUT = ROOT / "docs/assets/data/gguf-load-authored-v0.viewer.json"


def build_payload(trace: dict) -> dict:
    source = trace["source"]
    revision = source["revision"]
    repository = source["repository"]
    steps = []
    for step in trace["steps"]:
        location = step["location"]
        source_url = (
            f"https://github.com/{repository}/blob/{revision}/"
            f"{location['file']}#L{location['line']}"
        )
        steps.append(
            {
                "sequence": step["sequence"],
                "step_id": step["step_id"],
                "phase": step["phase"],
                "evidence_kind": step["evidence_kind"],
                "location": location,
                "source_url": source_url,
                "prediction_prompt": step.get("prediction_prompt", ""),
                "static_summary": step["static_summary"],
                "call_stack": step.get("call_stack", []),
                "runtime_objects": step.get("runtime_objects", []),
                "tensor_shapes": step.get("tensor_shapes", []),
                "memory_events": step.get("memory_events", []),
            }
        )

    return {
        "viewer_data_version": "0.1.0",
        "trace_id": trace["trace_id"],
        "lesson_id": trace["lesson_id"],
        "title": trace["title"],
        "source": source,
        "steps": steps,
    }


def render(payload: dict) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    payload = build_payload(json.loads(args.input.read_text(encoding="utf-8")))
    expected = render(payload)
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != expected:
            raise SystemExit(f"stale trace-viewer payload: {args.output}")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(expected, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
