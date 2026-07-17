#!/usr/bin/env python3
"""Validate the bounded first retrospective batch and required run archetypes."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from validate_agent_workflow_run import ValidationError, require, validate

REQUIRED_ARCHETYPES = {"successful_increment", "ci_repair", "blocked_reassignment"}


def classify(record: dict) -> set[str]:
    kinds: set[str] = set()
    failures = record["validation"]["failures"]
    decisions = {item["decision"] for item in record["outputs"]}
    if record["validation"]["ci_state"] == "passed" and not failures:
        kinds.add("successful_increment")
    if "revised" in decisions and any(item["resolution"] == "fixed" for item in failures):
        kinds.add("ci_repair")
    blocker = record["assignment"].get("blocker", "")
    if blocker and any(item["resolution"] == "blocked" for item in failures):
        kinds.add("blocked_reassignment")
    return kinds


def validate_batch(paths: list[Path]) -> None:
    require(len(paths) == 3, "first retrospective batch must contain exactly three records")
    run_ids: set[str] = set()
    archetypes: set[str] = set()
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        require(isinstance(data, dict), f"record root must be an object: {path}")
        validate(data)
        require(data["run_id"] not in run_ids, "batch run IDs must be unique")
        run_ids.add(data["run_id"])
        archetypes.update(classify(data))
    require(archetypes == REQUIRED_ARCHETYPES, f"batch archetypes must equal {sorted(REQUIRED_ARCHETYPES)}; found {sorted(archetypes)}")


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print("usage: validate_agent_workflow_batch.py <success.json> <repair.json> <blocked.json>", file=sys.stderr)
        return 2
    try:
        validate_batch([Path(value) for value in argv[1:]])
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"invalid agent workflow batch: {exc}", file=sys.stderr)
        return 1
    print("agent workflow batch is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
