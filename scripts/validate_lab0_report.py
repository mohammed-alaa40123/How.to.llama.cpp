#!/usr/bin/env python3
"""Validate Lab 0 checker reports without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

STATES = {"not_attempted", "passed", "failed", "blocked", "not_applicable"}
PHASES = ("environment", "configure", "compile", "executable_launch", "model_load", "inference")
CLAIMS = {
    "environment_ready": "environment",
    "native_configured": "configure",
    "native_compiled": "compile",
    "executable_launched": "executable_launch",
    "model_loaded": "model_load",
    "inference_succeeded": "inference",
}
SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def validate_report(report: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {"schema_version", "generated_at", "revisions", "platform", "model_input", "phases", "claims"}
    missing = sorted(required - report.keys())
    if missing:
        errors.append(f"missing top-level fields: {', '.join(missing)}")
        return errors

    if report["schema_version"] != "1.0.0":
        errors.append("schema_version must be 1.0.0")

    revisions = report.get("revisions", {})
    for name in ("course", "llama_cpp"):
        if not SHA_RE.fullmatch(str(revisions.get(name, ""))):
            errors.append(f"revisions.{name} must be a 7-40 character lowercase hex revision")

    model = report.get("model_input", {})
    kind = model.get("kind")
    if kind not in {"none", "learner_provided"}:
        errors.append("model_input.kind must be none or learner_provided")
    if "sha256" in model and not SHA256_RE.fullmatch(str(model["sha256"])):
        errors.append("model_input.sha256 must be 64 lowercase hex characters")
    basename = model.get("redacted_basename")
    if basename and ("/" in basename or "\\" in basename):
        errors.append("model_input.redacted_basename must not contain a path")

    phases = report.get("phases", {})
    for phase in PHASES:
        value = phases.get(phase)
        if not isinstance(value, dict):
            errors.append(f"phases.{phase} must be an object")
            continue
        if value.get("state") not in STATES:
            errors.append(f"phases.{phase}.state is invalid")
        if "duration_ms" in value and (not isinstance(value["duration_ms"], int) or value["duration_ms"] < 0):
            errors.append(f"phases.{phase}.duration_ms must be a non-negative integer")

    def state(name: str) -> str | None:
        value = phases.get(name)
        return value.get("state") if isinstance(value, dict) else None

    if state("compile") == "passed" and state("configure") != "passed":
        errors.append("compile=passed requires configure=passed")
    if state("executable_launch") == "passed" and state("compile") != "passed":
        errors.append("executable_launch=passed requires compile=passed")
    if state("model_load") == "passed":
        if state("executable_launch") != "passed":
            errors.append("model_load=passed requires executable_launch=passed")
        if kind != "learner_provided":
            errors.append("model_load=passed requires model_input.kind=learner_provided")
    if state("inference") == "passed" and state("model_load") != "passed":
        errors.append("inference=passed requires model_load=passed")
    if kind == "none":
        for phase in ("model_load", "inference"):
            if state(phase) not in {"not_attempted", "not_applicable"}:
                errors.append(f"model_input.kind=none requires {phase}=not_attempted or not_applicable")

    claims = report.get("claims", {})
    for claim, phase in CLAIMS.items():
        value = claims.get(claim)
        if not isinstance(value, bool):
            errors.append(f"claims.{claim} must be boolean")
        elif value != (state(phase) == "passed"):
            errors.append(f"claims.{claim} must equal whether {phase}=passed")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid report: {exc}", file=sys.stderr)
        return 2
    if not isinstance(report, dict):
        print("invalid report: top level must be an object", file=sys.stderr)
        return 2
    errors = validate_report(report)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Lab 0 report validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
