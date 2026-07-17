#!/usr/bin/env python3
"""Validate the deterministic MEDIA-02 accepted/revised/rejected lifecycle dry run."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from validate_media_manifest import validate_manifest

SHA40 = re.compile(r"^[0-9a-f]{40}$")
REQUIRED_STATES = {"accepted", "revised", "rejected"}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _repo_file(repo_root: Path, relative: Any) -> Path | None:
    if not isinstance(relative, str) or not relative or "\\" in relative:
        return None
    candidate = (repo_root / relative).resolve()
    root = repo_root.resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def validate_lifecycle(data: Any, *, repo_root: Path) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["lifecycle root must be an object"]

    if data.get("schema_version") != "0.1.0":
        errors.append("schema_version must be 0.1.0")
    if data.get("ordinary_ci_external_generation") is not False:
        errors.append("ordinary CI external generation must be false")

    revision = data.get("source_revision")
    if not isinstance(revision, str) or not SHA40.fullmatch(revision):
        errors.append("source_revision must be a full immutable commit SHA")
        revision = None

    manifests = data.get("manifests")
    if not isinstance(manifests, list) or len(manifests) != 3:
        return errors + ["manifests must contain exactly three lifecycle records"]

    statuses = [item.get("review_status") for item in manifests if isinstance(item, dict)]
    if set(statuses) != REQUIRED_STATES or len(statuses) != 3:
        errors.append("lifecycle must contain exactly one accepted, revised, and rejected record")

    ids: list[Any] = []
    output_paths: list[Any] = []
    for index, manifest in enumerate(manifests):
        if not isinstance(manifest, dict):
            errors.append(f"manifests[{index}] must be an object")
            continue

        for error in validate_manifest(manifest, expected_source_revision=revision):
            errors.append(f"manifests[{index}]: {error}")

        ids.append(manifest.get("asset_id"))
        output = manifest.get("output") if isinstance(manifest.get("output"), dict) else {}
        output_paths.append(output.get("path"))

        generation = manifest.get("generation") if isinstance(manifest.get("generation"), dict) else {}
        if generation.get("mode") != "deterministic":
            errors.append(f"manifests[{index}] must use deterministic generation")
        if generation.get("ordinary_ci_allowed") is not True:
            errors.append(f"manifests[{index}] must remain reproducible in ordinary CI")
        for key in ("model", "prompt_path", "prompt_sha256", "storyboard_path", "storyboard_sha256"):
            if generation.get(key) is not None:
                errors.append(f"manifests[{index}].generation.{key} must be null in the no-cost dry run")

        status = manifest.get("review_status")
        publication = manifest.get("publication") if isinstance(manifest.get("publication"), dict) else {}
        review = manifest.get("human_review") if isinstance(manifest.get("human_review"), dict) else {}
        notes = review.get("notes")
        if status == "accepted":
            if publication.get("publish") is not True or review.get("approved") is not True:
                errors.append("accepted record must be approved and published")
        elif status in {"revised", "rejected"}:
            if publication.get("publish") is not False or review.get("approved") is not False:
                errors.append(f"{status} record must remain unpublished and unapproved")
            if not isinstance(notes, str) or not notes.strip():
                errors.append(f"{status} record must preserve a review reason")

        source = manifest.get("source") if isinstance(manifest.get("source"), dict) else {}
        input_paths = source.get("input_paths", [])
        input_hashes = source.get("input_sha256", [])
        if isinstance(input_paths, list) and isinstance(input_hashes, list):
            for input_index, (relative, expected_hash) in enumerate(zip(input_paths, input_hashes)):
                path = _repo_file(repo_root, relative)
                if path is None or not path.is_file():
                    errors.append(f"manifests[{index}] input {input_index} is missing or unsafe")
                elif _sha256(path) != expected_hash:
                    errors.append(f"manifests[{index}] input {input_index} is stale")

        output_path = _repo_file(repo_root, output.get("path"))
        if output_path is None or not output_path.is_file():
            errors.append(f"manifests[{index}] output is missing or unsafe")
        else:
            raw = output_path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != output.get("sha256"):
                errors.append(f"manifests[{index}] output checksum is stale")
            if len(raw) != output.get("bytes"):
                errors.append(f"manifests[{index}] output byte count is stale")

    if len(ids) != len(set(ids)):
        errors.append("asset_id values must be unique")
    if len(output_paths) != len(set(output_paths)):
        errors.append("output paths must be unique")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lifecycle", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    try:
        data = json.loads(args.lifecycle.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = validate_lifecycle(data, repo_root=args.repo_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Media lifecycle validation passed: {args.lifecycle}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
