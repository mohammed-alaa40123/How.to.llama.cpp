#!/usr/bin/env python3
"""Validate the frozen DOC-AUDIT-01 protocol without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED_STRATA = {
    "official_project_material",
    "primary_educational_repositories",
    "contributor_authored_explanations",
    "community_tutorials",
}
REQUIRED_DIMENSIONS = {
    "revision_clarity",
    "source_references",
    "execution_path_coverage",
    "runtime_evidence",
    "conceptual_boundaries",
    "learner_action",
    "reproducibility",
    "accessibility",
    "license_clarity",
}
REQUIRED_CONCLUSIONS = {"supported", "revised", "rejected", "inconclusive"}
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "0.1.0":
        errors.append("schema_version must be 0.1.0")
    if data.get("protocol_id") != "DOC-AUDIT-01":
        errors.append("protocol_id must be DOC-AUDIT-01")
    if not SHA40.fullmatch(str(data.get("repository_revision", ""))):
        errors.append("repository_revision must be an immutable 40-character SHA")
    if data.get("hypothesis_status") != "open_question":
        errors.append("the documentation gap must remain an open_question")

    queries = data.get("search_queries", [])
    if len(queries) < 5 or len(set(queries)) != len(queries):
        errors.append("at least five unique frozen search queries are required")
    if set(data.get("strata", [])) != REQUIRED_STRATA:
        errors.append("all four predefined strata are required exactly once")
    if set(data.get("rubric_dimensions", [])) != REQUIRED_DIMENSIONS:
        errors.append("all nine frozen rubric dimensions are required exactly once")

    sampling = data.get("sampling", {})
    expected_sampling = {
        "results_per_query": 20,
        "deduplicate": True,
        "retain_rank": True,
        "retain_exclusions": True,
        "freeze_before_coding": True,
    }
    if sampling != expected_sampling:
        errors.append("sampling settings must match the frozen top-20 retained-decision design")

    coding = data.get("coding", {})
    if coding.get("independent_coders", 0) < 2:
        errors.append("at least two independent coders are required")
    for key in ("retain_original_labels", "retain_anchors", "adjudication_required"):
        if coding.get(key) is not True:
            errors.append(f"coding.{key} must be true")
    if coding.get("single_coder_closes_task") is not False:
        errors.append("a single-coder batch cannot close DOC-AUDIT-01")

    if set(data.get("allowed_conclusions", [])) != REQUIRED_CONCLUSIONS:
        errors.append("all four bounded conclusions are required")
    limitations = data.get("limitations", [])
    if not limitations or any(len(str(item).strip()) < 10 for item in limitations):
        errors.append("at least one substantive limitation is required")
    return errors


def main(argv: list[str]) -> int:
    path = Path(argv[1] if len(argv) > 1 else "progress/examples/documentation-gap-audit-protocol-v0.json")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid: {exc}", file=sys.stderr)
        return 2
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"invalid: {error}", file=sys.stderr)
        return 1
    print(f"valid: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
