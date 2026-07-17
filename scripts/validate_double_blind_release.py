#!/usr/bin/env python3
"""Validate the bounded EAAI double-blind artifact release contract."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

SHA40 = re.compile(r"^[0-9a-f]{40}$")
FORBIDDEN_PUBLIC_TOKENS = (
    "mohammed-alaa40123",
    "github.com/",
    "@",
    "pull/",
    "issues/",
    "actions/runs/",
)
REQUIRED_CATEGORIES = {
    "identity", "repository", "provenance", "supplement",
    "licensing", "privacy", "accessibility", "cost",
}


def fail(message: str) -> None:
    raise ValueError(message)


def validate(data: dict[str, Any]) -> None:
    if data.get("schema_version") != "0.1.0":
        fail("schema_version must be 0.1.0")
    if data.get("venue") != "EAAI-27":
        fail("venue must be EAAI-27")
    revision = data.get("submission_revision", "")
    if not isinstance(revision, str) or not SHA40.fullmatch(revision):
        fail("submission_revision must be an immutable 40-character lowercase SHA")
    if data.get("release_mode") not in {"private_anonymized_supplement", "post_decision_public_release"}:
        fail("unsupported release_mode")

    artifact = data.get("public_artifact")
    if not isinstance(artifact, dict):
        fail("public_artifact must be an object")
    if artifact.get("source_anchor_policy") != "opaque_id_plus_sha256":
        fail("public source anchors must use opaque IDs plus SHA-256")
    for key in ("root", "included", "excluded"):
        if key not in artifact:
            fail(f"public_artifact.{key} is required")
    flattened = json.dumps(artifact, sort_keys=True).lower()
    for token in FORBIDDEN_PUBLIC_TOKENS:
        if token in flattened:
            fail(f"public artifact leaks forbidden identity or repository token: {token}")

    crosswalk = data.get("private_crosswalk")
    if not isinstance(crosswalk, dict):
        fail("private_crosswalk must be an object")
    if crosswalk.get("contains_identity_mapping") is not True:
        fail("private crosswalk must retain the identity mapping")
    if crosswalk.get("published_before_decision") is not False:
        fail("private crosswalk must not be published before decision")
    if not str(crosswalk.get("location", "")).startswith("private:"):
        fail("private crosswalk location must use a private: locator")

    checks = data.get("checks")
    if not isinstance(checks, list) or not checks:
        fail("checks must be a non-empty list")
    ids: set[str] = set()
    categories: set[str] = set()
    for check in checks:
        if not isinstance(check, dict):
            fail("each check must be an object")
        check_id = check.get("id")
        if not isinstance(check_id, str) or check_id in ids:
            fail("check IDs must be unique strings")
        ids.add(check_id)
        category = check.get("category")
        if category not in REQUIRED_CATEGORIES:
            fail(f"unknown check category: {category}")
        categories.add(category)
        status = check.get("status")
        if status not in {"pass", "blocked", "not_applicable"}:
            fail(f"invalid status for {check_id}")
        if not str(check.get("evidence", "")).strip():
            fail(f"check {check_id} requires evidence")
        if status == "blocked" and not str(check.get("blocker", "")).strip():
            fail(f"blocked check {check_id} requires blocker detail")
        if status != "blocked" and "blocker" in check:
            fail(f"non-blocked check {check_id} must not carry blocker detail")
    missing = REQUIRED_CATEGORIES - categories
    if missing:
        fail(f"missing required check categories: {sorted(missing)}")

    approvals = data.get("approvals")
    if not isinstance(approvals, dict):
        fail("approvals must be an object")
    required_approvals = {
        "author_anonymization_review", "technical_evidence_review",
        "licensing_review", "ethics_privacy_review",
    }
    if set(approvals) != required_approvals or not all(isinstance(v, bool) for v in approvals.values()):
        fail("approvals must contain exactly four boolean gates")

    blocked = any(check["status"] == "blocked" for check in checks)
    computed_ready = not blocked and all(approvals.values())
    if data.get("release_ready") is not computed_ready:
        fail("release_ready disagrees with blocked checks or approvals")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {argv[0]} PLAN.json", file=sys.stderr)
        return 2
    path = Path(argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            fail("top-level JSON value must be an object")
        validate(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"invalid double-blind release plan: {exc}", file=sys.stderr)
        return 1
    print(f"valid double-blind release plan: {path} (release_ready={data['release_ready']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
