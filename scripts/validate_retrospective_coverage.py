#!/usr/bin/env python3
"""Validate DATA-01 missing-value and evidence-coverage declarations."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SHA40 = re.compile(r"^[0-9a-f]{40}$")
RUN_ID = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{4}Z-[a-z0-9-]{3,64}$")
STATUSES = {"observed", "not_reconstructable", "not_applicable"}
REQUIRED_FIELDS = {
    "assignment.selection_reason",
    "revisions.starting_commit",
    "revisions.ending_commit",
    "validation.ci_state",
    "validation.failures",
    "human_supervision.decisions",
    "effort.agent_turns",
    "effort.tool_calls",
    "effort.human_minutes",
    "effort.external_api_cost_usd",
    "outputs.decisions",
}


class ValidationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate(data: dict) -> None:
    require(data.get("schema_version") == "1.0.0", "schema_version must be 1.0.0")
    require(bool(SHA40.fullmatch(str(data.get("source_revision", "")))), "source_revision must be immutable")

    records = data.get("records")
    require(isinstance(records, list) and 1 <= len(records) <= 100, "records must contain 1-100 run IDs")
    require(len(records) == len(set(records)), "record IDs must be unique")
    require(all(RUN_ID.fullmatch(str(value)) for value in records), "record IDs must be stable timestamped IDs")

    dimensions = data.get("dimensions")
    require(isinstance(dimensions, list) and 1 <= len(dimensions) <= 50, "dimensions must contain 1-50 entries")
    fields: set[str] = set()
    for item in dimensions:
        require(isinstance(item, dict), "dimension entries must be objects")
        field = item.get("field")
        require(isinstance(field, str) and field, "dimension field is required")
        require(field not in fields, "dimension fields must be unique")
        fields.add(field)
        status = item.get("status")
        require(status in STATUSES, "invalid coverage status")
        reason = item.get("reason")
        require(isinstance(reason, str) and len(reason) >= 10, "every dimension requires an explicit reason")
        evidence_paths = item.get("evidence_paths")
        require(isinstance(evidence_paths, list) and len(evidence_paths) == len(set(evidence_paths)), "evidence_paths must be a unique list")
        if status == "observed":
            require(len(evidence_paths) > 0, f"observed field requires evidence: {field}")
        else:
            require(len(evidence_paths) == 0, f"non-observed field must not cite evidence: {field}")

    missing = REQUIRED_FIELDS - fields
    require(not missing, f"required coverage dimensions are missing: {sorted(missing)}")
    require(any(item["status"] == "not_reconstructable" for item in dimensions), "coverage record must expose at least one reconstruction limit")
    boundary = data.get("claim_boundary")
    require(isinstance(boundary, str) and len(boundary) >= 30, "claim_boundary must state the inference limit")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_retrospective_coverage.py <coverage.json>", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        require(isinstance(data, dict), "coverage root must be an object")
        validate(data)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"invalid retrospective coverage: {exc}", file=sys.stderr)
        return 1
    print("retrospective coverage is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
