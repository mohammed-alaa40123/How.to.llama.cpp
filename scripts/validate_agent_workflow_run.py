#!/usr/bin/env python3
"""Validate retrospective scheduled-agent evidence without external dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

SHA40 = re.compile(r"^[0-9a-f]{40}$")
RUN_ID = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{4}Z-[a-z0-9-]{3,64}$")
ASSIGNMENT_ID = re.compile(r"^[A-Z0-9]+-[0-9]{2}$")
ROLES = {"orchestrator", "documentation_builder", "validation_architect", "literature_scout", "adversarial_reviewer", "human_reviewer"}
CLAIM_LABELS = {"Verified", "Interpretation", "Historical", "Open Question"}
OUTPUT_DECISIONS = {"accepted", "revised", "rejected"}
CI_STATES = {"not_run", "queued", "in_progress", "passed", "failed"}
SENSITIVE_KEYS = {"email", "name", "username", "user_id", "device_id", "session_id", "ip_address", "prompt", "response", "raw_content", "token", "secret", "api_key"}


class ValidationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def walk_sensitive(value: Any, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            require(key.lower() not in SENSITIVE_KEYS, f"privacy-sensitive field is forbidden: {path}.{key}")
            walk_sensitive(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            walk_sensitive(child, f"{path}[{index}]")


def validate(data: dict[str, Any]) -> None:
    require(data.get("schema_version") == "1.0.0", "schema_version must be 1.0.0")
    require(bool(RUN_ID.fullmatch(str(data.get("run_id", "")))), "run_id must be timestamped and stable")
    require(data.get("role") in ROLES, "invalid role")

    assignment = data.get("assignment", {})
    require(bool(ASSIGNMENT_ID.fullmatch(str(assignment.get("id", "")))), "invalid assignment id")
    require(assignment.get("priority") in {"P0", "P1", "P2", "P3"}, "invalid priority")
    require(assignment.get("dependency_state") in {"ready", "blocked", "in_progress"}, "invalid dependency_state")
    require(len(str(assignment.get("objective", ""))) >= 20, "assignment objective is too short")
    require(len(str(assignment.get("selected_reason", ""))) >= 20, "selected_reason is too short")
    if assignment.get("dependency_state") == "blocked":
        require(len(str(assignment.get("blocker", ""))) >= 10, "blocked assignments require a blocker")

    revisions = data.get("revisions", {})
    for key in ("starting_commit", "ending_commit"):
        require(bool(SHA40.fullmatch(str(revisions.get(key, "")))), f"{key} must be a full commit")
    require(revisions["starting_commit"] != revisions["ending_commit"], "ending commit must differ from starting commit")
    require(bool(revisions.get("base_branch")) and bool(revisions.get("working_branch")), "branch identities are required")

    outputs = data.get("outputs")
    require(isinstance(outputs, list) and 1 <= len(outputs) <= 50, "outputs must contain 1-50 records")
    paths: set[str] = set()
    decisions: set[str] = set()
    for output in outputs:
        require(isinstance(output, dict), "output entries must be objects")
        path = output.get("path")
        require(isinstance(path, str) and path and not path.startswith("/") and ".." not in Path(path).parts, "output path must be safe and repository-relative")
        require(path not in paths, "output paths must be unique")
        paths.add(path)
        require(output.get("decision") in OUTPUT_DECISIONS, "invalid output decision")
        decisions.add(output["decision"])
        if output["decision"] != "accepted":
            require(len(str(output.get("reason", ""))) >= 10, "revised/rejected outputs require a reason")

    validation = data.get("validation", {})
    validators = validation.get("validators")
    require(isinstance(validators, list) and len(validators) == len(set(validators)), "validators must be a unique list")
    failures = validation.get("failures")
    require(isinstance(failures, list) and len(failures) <= 30, "failures must be a bounded list")
    require(validation.get("ci_state") in CI_STATES, "invalid ci_state")
    if validation.get("ci_state") in {"queued", "in_progress", "passed", "failed"}:
        require(isinstance(validation.get("ci_run_id"), int) and validation["ci_run_id"] > 0, "CI state requires ci_run_id")
    if validation.get("ci_state") == "passed":
        require(len(validators) > 0, "passed CI requires recorded validators")
    for failure in failures:
        require(failure.get("resolution") in {"fixed", "deferred", "blocked", "not_reproducible"}, "invalid failure resolution")
        require(len(str(failure.get("summary", ""))) >= 10, "failure summary is required")

    supervision = data.get("human_supervision", {})
    require(isinstance(supervision.get("required"), bool), "human_supervision.required must be boolean")
    require(supervision.get("review_status") in {"not_required", "pending", "approved", "changes_requested", "rejected"}, "invalid review_status")
    require(isinstance(supervision.get("decisions"), list), "human decisions must be a list")
    if supervision["required"]:
        require(supervision["review_status"] != "not_required", "required human review cannot be marked not_required")

    effort = data.get("effort", {})
    require(isinstance(effort.get("agent_turns"), int) and effort["agent_turns"] >= 1, "agent_turns must be positive")
    require(isinstance(effort.get("tool_calls"), int) and effort["tool_calls"] >= 0, "tool_calls must be non-negative")
    require(isinstance(effort.get("external_api_cost_usd"), (int, float)) and effort["external_api_cost_usd"] >= 0, "external_api_cost_usd must be non-negative")
    require(isinstance(effort.get("paid_generation_calls"), int) and effort["paid_generation_calls"] >= 0, "paid_generation_calls must be non-negative")
    require(effort["paid_generation_calls"] == 0 or effort["external_api_cost_usd"] > 0, "paid generation calls require a positive recorded cost")

    claims = data.get("claims")
    require(isinstance(claims, list) and 1 <= len(claims) <= 20, "claims must contain 1-20 records")
    for claim in claims:
        require(claim.get("label") in CLAIM_LABELS, "invalid claim label")
        evidence_paths = claim.get("evidence_paths")
        require(isinstance(evidence_paths, list), "claim evidence_paths must be a list")
        if claim["label"] == "Verified":
            require(len(evidence_paths) > 0, "Verified claims require evidence paths")

    require("accepted" in decisions, "a completed run must retain at least one accepted output")
    walk_sensitive(data)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_agent_workflow_run.py <record.json>", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        require(isinstance(data, dict), "record root must be an object")
        validate(data)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"invalid agent workflow record: {exc}", file=sys.stderr)
        return 1
    print("agent workflow record is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
