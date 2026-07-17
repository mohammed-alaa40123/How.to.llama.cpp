"""Local-only learner progress import/export, migration, and recovery.

This module intentionally has no network or authenticated-sync surface.
"""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, MutableMapping

from scripts.validate_learner_progress import ProgressValidationError, validate_progress

CURRENT_SCHEMA_VERSION = "0.1.0"
LEGACY_SCHEMA_VERSION = "0.0.1"
STORAGE_KEY = "how-to-llama-cpp.progress.v0.1.0"
RECOVERY_KEY = "how-to-llama-cpp.progress.recovery.v0.1.0"
MAX_IMPORT_BYTES = 512 * 1024


class ProgressImportError(ValueError):
    """Raised when an import cannot be safely validated or migrated."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def migrate_progress(data: Any) -> dict[str, Any]:
    """Return a validated current-version copy of a supported progress export."""
    if not isinstance(data, dict):
        raise ProgressImportError("progress export must be a JSON object")

    migrated = copy.deepcopy(data)
    version = migrated.get("schema_version")
    if version == LEGACY_SCHEMA_VERSION:
        migrated["schema_version"] = CURRENT_SCHEMA_VERSION
        migrated.setdefault("storage_scope", "local-only")
        for lesson in migrated.get("lessons", []):
            lesson.setdefault("last_step_id", None)
    elif version != CURRENT_SCHEMA_VERSION:
        raise ProgressImportError(f"unsupported schema_version: {version!r}")

    try:
        validate_progress(migrated)
    except ProgressValidationError as exc:
        raise ProgressImportError(str(exc)) from exc
    return migrated


def import_progress_text(text: str) -> dict[str, Any]:
    encoded = text.encode("utf-8")
    if len(encoded) > MAX_IMPORT_BYTES:
        raise ProgressImportError(f"progress import exceeds {MAX_IMPORT_BYTES} bytes")
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ProgressImportError(f"invalid JSON: {exc.msg}") from exc
    return migrate_progress(parsed)


def export_progress(data: Any, *, exported_at: str | None = None) -> str:
    validated = migrate_progress(data)
    validated["exported_at"] = exported_at or _utc_now()
    try:
        validate_progress(validated)
    except ProgressValidationError as exc:
        raise ProgressImportError(str(exc)) from exc
    return json.dumps(validated, indent=2, sort_keys=True) + "\n"


@dataclass(frozen=True)
class LoadResult:
    progress: dict[str, Any] | None
    recovered: bool
    error: str | None


class LocalProgressStore:
    """Storage adapter compatible with a browser localStorage-shaped mapping."""

    def __init__(self, storage: MutableMapping[str, str]):
        self.storage = storage

    def save(self, progress: Any) -> None:
        payload = export_progress(progress)
        previous = self.storage.get(STORAGE_KEY)
        if previous is not None:
            self.storage[RECOVERY_KEY] = previous
        self.storage[STORAGE_KEY] = payload

    def load(self) -> LoadResult:
        primary = self.storage.get(STORAGE_KEY)
        if primary is None:
            return LoadResult(None, False, None)
        try:
            return LoadResult(import_progress_text(primary), False, None)
        except ProgressImportError as primary_error:
            recovery = self.storage.get(RECOVERY_KEY)
            if recovery is None:
                return LoadResult(None, False, str(primary_error))
            try:
                restored = import_progress_text(recovery)
            except ProgressImportError as recovery_error:
                return LoadResult(
                    None,
                    False,
                    f"primary invalid: {primary_error}; recovery invalid: {recovery_error}",
                )
            self.storage[STORAGE_KEY] = export_progress(restored)
            return LoadResult(restored, True, str(primary_error))

    def clear(self) -> None:
        self.storage.pop(STORAGE_KEY, None)
        self.storage.pop(RECOVERY_KEY, None)
