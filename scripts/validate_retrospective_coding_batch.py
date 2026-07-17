#!/usr/bin/env python3
"""Validate DATA-01B retrospective coding batches without external dependencies."""
from __future__ import annotations
import json, re, sys
from datetime import datetime
from pathlib import Path
from typing import Any

SHA40 = re.compile(r"^[0-9a-f]{40}$")
RUN_ID = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{4}Z-[a-z0-9-]{3,64}$")
SAFE_PREFIXES = ("logs/research/", "progress/examples/")
ALLOWED_MISSING = {"tool_calls","human_minutes","api_cost","failed_attempts","ci_run","output_decisions","blocker_detail"}

class ValidationError(ValueError): pass

def require(condition: bool, message: str) -> None:
    if not condition: raise ValidationError(message)

def parse_dt(value: Any, label: str) -> datetime:
    require(isinstance(value, str), f"{label} must be an ISO-8601 string")
    try: return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc: raise ValidationError(f"{label} must be valid ISO-8601") from exc

def safe_path(value: Any) -> bool:
    if not isinstance(value, str) or not value.startswith(SAFE_PREFIXES): return False
    return not value.startswith("/") and ".." not in Path(value).parts and "\\" not in value

def validate(data: dict[str, Any]) -> None:
    require(data.get("schema_version") == "1.0.0", "schema_version must be 1.0.0")
    require(data.get("protocol_version") == "data01b-v0.1", "protocol_version must be data01b-v0.1")
    require(bool(SHA40.fullmatch(str(data.get("source_revision", "")))), "source_revision must be immutable")
    frame = data.get("sampling_frame", {})
    start, end = parse_dt(frame.get("start_utc"), "start_utc"), parse_dt(frame.get("end_utc"), "end_utc")
    require(start < end, "sampling frame start must precede end")
    rule = frame.get("selection_rule")
    require(rule in {"all_eligible_runs", "systematic_every_nth"}, "invalid selection_rule")
    require(isinstance(frame.get("excluded_run_ids"), list), "excluded_run_ids must be a list")
    if rule == "systematic_every_nth": require(isinstance(frame.get("interval_n"), int) and frame["interval_n"] >= 2, "systematic sampling requires interval_n")
    records = data.get("records")
    require(isinstance(records, list) and 1 <= len(records) <= 500, "records must contain 1-500 rows")
    ids, paths = set(), set()
    for row in records:
        require(isinstance(row, dict), "records must be objects")
        rid = str(row.get("run_id", ""))
        require(bool(RUN_ID.fullmatch(rid)), "invalid run_id")
        require(rid not in ids, "run_id values must be unique")
        ids.add(rid)
        path = row.get("evidence_path")
        require(safe_path(path), "evidence_path must be safe and repository-relative")
        require(path not in paths, "evidence_path values must be unique")
        paths.add(path)
        require(row.get("assignment_outcome") in {"completed","partial","blocked_reassigned","blocked_stopped"}, "invalid assignment_outcome")
        require(row.get("selection_path") in {"highest_priority_ready","blocked_then_dependency_safe","human_override","historical_reconstruction"}, "invalid selection_path")
        require(row.get("human_intervention") in {"none_recorded","approval","correction","merge_resolution","environment_access","ethics_or_privacy_decision","not_reconstructable"}, "invalid human_intervention")
        require(row.get("validation_outcome") in {"passed_first_attempt","failed_then_fixed","failed_unresolved","not_run","not_reconstructable"}, "invalid validation_outcome")
        completeness = row.get("evidence_completeness")
        require(completeness in {"complete_for_protocol","partial","not_reconstructable"}, "invalid evidence_completeness")
        missing = row.get("missing_fields", [])
        require(isinstance(missing, list) and len(missing) == len(set(missing)) and set(missing) <= ALLOWED_MISSING, "invalid or duplicate missing_fields")
        if completeness == "complete_for_protocol": require(not missing, "complete rows cannot declare missing fields")
        else: require(bool(missing), "partial or unreconstructable rows require missing_fields")
        if row["assignment_outcome"].startswith("blocked"):
            require("blocker_detail" not in missing, "blocked rows require blocker detail")
        status = row.get("coding_status")
        require(status in {"single_coded","double_coded_agree","double_coded_disagree","adjudicated"}, "invalid coding_status")
        disagreements = row.get("disagreement_fields", [])
        if status == "double_coded_disagree": require(bool(disagreements), "disagreement status requires disagreement_fields")
        if status == "adjudicated": require(len(str(row.get("adjudication_note", ""))) >= 20, "adjudicated rows require an adjudication note")
        if status in {"single_coded","double_coded_agree"}: require(not disagreements, "agreeing/single-coded rows cannot retain disagreement_fields")
    excluded = frame["excluded_run_ids"]
    require(len(excluded) == len(set(excluded)), "excluded_run_ids must be unique")
    require(not (ids & set(excluded)), "coded records cannot also be excluded")

def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_retrospective_coding_batch.py <batch.json>", file=sys.stderr); return 2
    try:
        data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        require(isinstance(data, dict), "root must be an object")
        validate(data)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"invalid retrospective coding batch: {exc}", file=sys.stderr); return 1
    print("retrospective coding batch is valid"); return 0

if __name__ == "__main__": raise SystemExit(main(sys.argv))
