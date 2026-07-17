#!/usr/bin/env python3
"""Validate the bounded STACK-01 human decision record."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

EXPECTED_ORDER = [3, 4, 5, 6, 7, 9, 11, 13, 15, 16, 17, 18, 21, 22, 24, 25, 27, 28, 29]
EXPECTED_FOLLOWUPS = {
    "schema-migration-0.0.1-to-0.1.0",
    "last-known-valid-recovery",
}
EXPECTED_SUPERSEDED = {(14, 13), (23, 24)}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class ValidationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def validate(record: dict[str, Any]) -> None:
    require(record.get("schema_version") == "0.1.0", "schema_version must be 0.1.0")
    require(record.get("decision_id") == "STACK-01", "decision_id must be STACK-01")
    revision = record.get("repository_revision")
    require(isinstance(revision, str) and SHA_RE.fullmatch(revision) is not None,
            "repository_revision must be an immutable 40-character SHA")

    progress = record.get("progress_choice")
    require(isinstance(progress, dict), "progress_choice must be an object")
    require(progress.get("selected_pr") == 24, "PR #24 must be the selected progress implementation")
    require(progress.get("rejected_pr") == 23, "PR #23 must be recorded as the overlapping rejected implementation")
    rationale = progress.get("rationale")
    require(isinstance(rationale, str) and len(rationale.strip()) >= 40,
            "progress_choice rationale must explain the downstream-dependency decision")
    followups = progress.get("preserved_followups")
    require(isinstance(followups, list) and set(followups) == EXPECTED_FOLLOWUPS,
            "both PR #23 follow-up ideas must be preserved explicitly")

    order = record.get("merge_order")
    require(order == EXPECTED_ORDER, "merge_order must match the reviewed canonical spine exactly")

    superseded = record.get("superseded_work")
    require(isinstance(superseded, list), "superseded_work must be a list")
    pairs = {(item.get("pr"), item.get("replacement_pr")) for item in superseded if isinstance(item, dict)}
    require(EXPECTED_SUPERSEDED.issubset(pairs), "superseded_work must include #14→#13 and #23→#24")
    for item in superseded:
        require(isinstance(item, dict), "each superseded_work item must be an object")
        reason = item.get("reason")
        require(isinstance(reason, str) and len(reason.strip()) >= 20,
                "each superseded decision needs a reviewable reason")

    approval = record.get("human_approval")
    require(isinstance(approval, dict), "human_approval must be an object")
    approved = approval.get("approved")
    status = record.get("integration_status")
    require(status in {"pending-human-approval", "approved-not-integrated", "integrating", "validated"},
            "integration_status is invalid")

    if approved is True:
        require(isinstance(approval.get("reviewer"), str) and approval["reviewer"].strip(),
                "approved decisions require a named reviewer")
        require(isinstance(approval.get("approved_at"), str) and approval["approved_at"].strip(),
                "approved decisions require an approval timestamp")
        require(status != "pending-human-approval",
                "approved decisions cannot remain pending-human-approval")
    else:
        require(approved is False, "human_approval.approved must be boolean")
        require(approval.get("reviewer") is None and approval.get("approved_at") is None,
                "pending decisions must not invent a reviewer or approval timestamp")
        require(status == "pending-human-approval",
                "unapproved decisions must remain pending-human-approval")

    if status == "validated":
        require(approved is True, "validated integration requires human approval")
        require("combined CI" in approval.get("notes", ""),
                "validated status must cite combined CI in approval notes")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    try:
        record = json.loads(args.record.read_text(encoding="utf-8"))
        require(isinstance(record, dict), "top-level JSON value must be an object")
        validate(record)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"canonical integration decision invalid: {exc}", file=sys.stderr)
        return 1
    print(f"canonical integration decision valid: {args.record}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
