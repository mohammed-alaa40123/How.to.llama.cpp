#!/usr/bin/env python3
"""Dependency-free semantic validator for educational media manifests."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any

MAX_MANIFEST_BYTES = 256 * 1024
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,127}$")
FORBIDDEN_KEYS = {
    "api_key",
    "access_token",
    "secret",
    "authorization",
    "cookie",
    "email",
    "user_id",
    "device_id",
}


def _require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def _safe_repo_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def _find_forbidden_keys(value: Any, prefix: str = "root") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).lower()
            if normalized in FORBIDDEN_KEYS or normalized.endswith("_secret"):
                errors.append(f"{prefix}.{key} is forbidden in a manifest")
            errors.extend(_find_forbidden_keys(child, f"{prefix}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(_find_forbidden_keys(child, f"{prefix}[{index}]"))
    return errors


def validate_manifest(
    data: Any,
    *,
    raw_size: int | None = None,
    expected_source_revision: str | None = None,
) -> list[str]:
    errors: list[str] = []
    if raw_size is not None:
        _require(raw_size <= MAX_MANIFEST_BYTES, f"manifest exceeds {MAX_MANIFEST_BYTES} bytes", errors)
    if not isinstance(data, dict):
        return ["manifest root must be an object"]

    errors.extend(_find_forbidden_keys(data))
    _require(data.get("schema_version") == "0.1.0", "schema_version must be 0.1.0", errors)
    asset_id = data.get("asset_id")
    _require(isinstance(asset_id, str) and bool(ID_RE.fullmatch(asset_id)), "asset_id is invalid", errors)

    asset_kind = data.get("asset_kind")
    _require(asset_kind in {"diagram", "illustration", "audio", "video"}, "asset_kind is invalid", errors)
    authority = data.get("authority")
    _require(authority in {"authoritative-technical", "supplemental"}, "authority is invalid", errors)
    review_status = data.get("review_status")
    _require(review_status in {"pending", "accepted", "revised", "rejected"}, "review_status is invalid", errors)

    publication = data.get("publication")
    if not isinstance(publication, dict):
        errors.append("publication must be an object")
        publication = {}
    publish = publication.get("publish")
    _require(isinstance(publish, bool), "publication.publish must be a boolean", errors)
    if review_status == "rejected":
        _require(publish is False, "rejected assets cannot be published", errors)

    source = data.get("source")
    if not isinstance(source, dict):
        errors.append("source must be an object")
        source = {}
    _require(source.get("repository") == "mohammed-alaa40123/How.to.llama.cpp", "source.repository is invalid", errors)
    revision = source.get("revision")
    _require(isinstance(revision, str) and bool(SHA40.fullmatch(revision)), "source.revision must be a full 40-character lowercase commit SHA", errors)
    if expected_source_revision is not None:
        _require(revision == expected_source_revision, "manifest is stale for the expected source revision", errors)
    input_paths = source.get("input_paths")
    _require(isinstance(input_paths, list) and 1 <= len(input_paths) <= 32, "source.input_paths must contain 1..32 items", errors)
    if isinstance(input_paths, list):
        for index, path in enumerate(input_paths):
            _require(_safe_repo_path(path), f"source.input_paths[{index}] must be a safe repository-relative path", errors)
    input_hashes = source.get("input_sha256")
    _require(isinstance(input_hashes, list) and len(input_hashes) == len(input_paths or []), "source.input_sha256 must match input_paths length", errors)
    if isinstance(input_hashes, list):
        for index, digest in enumerate(input_hashes):
            _require(isinstance(digest, str) and bool(SHA256.fullmatch(digest)), f"source.input_sha256[{index}] is invalid", errors)

    generation = data.get("generation")
    if not isinstance(generation, dict):
        errors.append("generation must be an object")
        generation = {}
    mode = generation.get("mode")
    _require(mode in {"deterministic", "human-authored", "generative-api"}, "generation.mode is invalid", errors)
    for key in ("generator", "generator_version"):
        _require(isinstance(generation.get(key), str) and bool(generation.get(key).strip()), f"generation.{key} is required", errors)
    for key in ("manual_trigger", "cached", "ordinary_ci_allowed"):
        _require(isinstance(generation.get(key), bool), f"generation.{key} must be a boolean", errors)

    if mode == "generative-api":
        _require(authority == "supplemental", "generative-api assets cannot be authoritative technical evidence", errors)
        _require(generation.get("manual_trigger") is True, "generative-api assets must be manually triggered", errors)
        _require(generation.get("cached") is True, "generative-api assets must be cached", errors)
        _require(generation.get("ordinary_ci_allowed") is False, "ordinary CI cannot invoke a generative API", errors)
        _require(isinstance(generation.get("model"), str) and bool(generation.get("model").strip()), "generative-api assets require a model identifier", errors)
        for path_key, hash_key in (("prompt_path", "prompt_sha256"), ("storyboard_path", "storyboard_sha256")):
            _require(_safe_repo_path(generation.get(path_key)), f"generation.{path_key} must be a safe repository-relative path", errors)
            digest = generation.get(hash_key)
            _require(isinstance(digest, str) and bool(SHA256.fullmatch(digest)), f"generation.{hash_key} is invalid", errors)
    else:
        _require(generation.get("ordinary_ci_allowed") is True, "deterministic or human-authored generation must be reproducible in ordinary CI", errors)

    if authority == "authoritative-technical":
        _require(mode == "deterministic", "authoritative technical assets must use deterministic generation", errors)
        _require(asset_kind == "diagram", "authoritative technical assets must be diagrams", errors)

    output = data.get("output")
    if not isinstance(output, dict):
        errors.append("output must be an object")
        output = {}
    _require(_safe_repo_path(output.get("path")), "output.path must be a safe repository-relative path", errors)
    digest = output.get("sha256")
    _require(isinstance(digest, str) and bool(SHA256.fullmatch(digest)), "output.sha256 is invalid", errors)
    output_bytes = output.get("bytes")
    _require(isinstance(output_bytes, int) and not isinstance(output_bytes, bool) and 1 <= output_bytes <= 512 * 1024 * 1024, "output.bytes is invalid", errors)

    accessibility = data.get("accessibility")
    if not isinstance(accessibility, dict):
        errors.append("accessibility must be an object")
        accessibility = {}
    alt_text = accessibility.get("alt_text")
    _require(isinstance(alt_text, str) and len(alt_text.strip()) >= 20, "accessibility.alt_text must provide a meaningful fallback", errors)
    for key in ("caption_path", "transcript_path", "static_fallback_path"):
        value = accessibility.get(key)
        if value is not None:
            _require(_safe_repo_path(value), f"accessibility.{key} must be a safe repository-relative path", errors)
    _require(isinstance(accessibility.get("reduced_motion_safe"), bool), "accessibility.reduced_motion_safe must be a boolean", errors)
    if asset_kind in {"audio", "video"}:
        _require(_safe_repo_path(accessibility.get("transcript_path")), f"{asset_kind} assets require a transcript", errors)
    if asset_kind == "video":
        _require(_safe_repo_path(accessibility.get("caption_path")), "video assets require captions", errors)
        _require(_safe_repo_path(accessibility.get("static_fallback_path")), "video assets require a static fallback", errors)

    licensing = data.get("licensing")
    if not isinstance(licensing, dict):
        errors.append("licensing must be an object")
        licensing = {}
    _require(isinstance(licensing.get("asset_license"), str) and bool(licensing.get("asset_license").strip()), "licensing.asset_license is required", errors)
    notes = licensing.get("input_license_notes")
    _require(isinstance(notes, str) and len(notes.strip()) >= 10, "licensing.input_license_notes is required", errors)
    _require(isinstance(licensing.get("redistribution_allowed"), bool), "licensing.redistribution_allowed must be a boolean", errors)
    if publish is True:
        _require(licensing.get("redistribution_allowed") is True, "published assets must permit redistribution", errors)

    review = data.get("human_review")
    if not isinstance(review, dict):
        errors.append("human_review must be an object")
        review = {}
    for key in ("required", "approved"):
        _require(isinstance(review.get(key), bool), f"human_review.{key} must be a boolean", errors)
    if review_status == "accepted" or publish is True or mode == "generative-api":
        _require(review.get("required") is True, "accepted, published, or generated assets require human review", errors)
    if review_status == "accepted" or publish is True:
        _require(review.get("approved") is True, "accepted or published assets require human approval", errors)
        _require(isinstance(review.get("reviewer_role"), str) and bool(review.get("reviewer_role").strip()), "approved assets require reviewer_role", errors)
        _require(isinstance(review.get("reviewed_at"), str) and bool(review.get("reviewed_at").strip()), "approved assets require reviewed_at", errors)

    technical_claims = data.get("technical_claims", [])
    _require(isinstance(technical_claims, list) and len(technical_claims) <= 64, "technical_claims must be an array of at most 64 items", errors)
    if authority == "authoritative-technical":
        _require(bool(technical_claims), "authoritative technical assets must declare technical claims", errors)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--expected-source-revision")
    args = parser.parse_args()

    try:
        raw = args.manifest.read_bytes()
        data = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors = validate_manifest(
        data,
        raw_size=len(raw),
        expected_source_revision=args.expected_source_revision,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Media manifest validation passed: {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
