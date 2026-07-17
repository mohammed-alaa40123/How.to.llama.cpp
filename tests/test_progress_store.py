import copy
import json
import unittest

from progress.progress_store import (
    CURRENT_SCHEMA_VERSION,
    LEGACY_SCHEMA_VERSION,
    LocalProgressStore,
    ProgressImportError,
    RECOVERY_KEY,
    STORAGE_KEY,
    export_progress,
    import_progress_text,
)


BASE = {
    "schema_version": CURRENT_SCHEMA_VERSION,
    "course_id": "how-to-llama-cpp",
    "course_version": "0.1.0",
    "source_revision": "d" * 40,
    "exported_at": "2026-07-17T10:00:00Z",
    "storage_scope": "local-only",
    "lessons": [
        {
            "lesson_id": "lab1-gguf-anatomy",
            "lesson_version": "0.1.0",
            "status": "in-progress",
            "last_step_id": "predict-alignment",
            "checkpoints": [
                {
                    "checkpoint_id": "predict-alignment",
                    "state": "answered",
                    "attempt_count": 1,
                }
            ],
        }
    ],
}


class ProgressStoreTests(unittest.TestCase):
    def test_export_import_round_trip_is_semantically_stable(self):
        text = export_progress(BASE, exported_at="2026-07-17T10:00:00Z")
        self.assertEqual(import_progress_text(text), BASE)

    def test_legacy_export_migrates_without_identity_or_network_fields(self):
        legacy = copy.deepcopy(BASE)
        legacy["schema_version"] = LEGACY_SCHEMA_VERSION
        legacy.pop("storage_scope")
        legacy["lessons"][0].pop("last_step_id")
        migrated = import_progress_text(json.dumps(legacy))
        self.assertEqual(migrated["schema_version"], CURRENT_SCHEMA_VERSION)
        self.assertEqual(migrated["storage_scope"], "local-only")
        self.assertIsNone(migrated["lessons"][0]["last_step_id"])

    def test_unknown_future_version_is_rejected(self):
        future = copy.deepcopy(BASE)
        future["schema_version"] = "9.0.0"
        with self.assertRaisesRegex(ProgressImportError, "unsupported schema_version"):
            import_progress_text(json.dumps(future))

    def test_privacy_sensitive_field_is_rejected(self):
        unsafe = copy.deepcopy(BASE)
        unsafe["email"] = "learner@example.com"
        with self.assertRaisesRegex(ProgressImportError, "forbidden privacy-sensitive field"):
            import_progress_text(json.dumps(unsafe))

    def test_corrupt_primary_recovers_last_valid_snapshot(self):
        storage = {}
        store = LocalProgressStore(storage)
        store.save(BASE)
        previous_snapshot = import_progress_text(storage[STORAGE_KEY])
        updated = copy.deepcopy(BASE)
        updated["lessons"][0]["checkpoints"][0]["attempt_count"] = 2
        store.save(updated)
        self.assertIn(RECOVERY_KEY, storage)
        storage[STORAGE_KEY] = "{broken"
        result = store.load()
        self.assertTrue(result.recovered)
        self.assertEqual(result.progress, previous_snapshot)
        self.assertIsNotNone(result.error)

    def test_two_corrupt_snapshots_fail_closed(self):
        storage = {STORAGE_KEY: "{broken", RECOVERY_KEY: "[]"}
        result = LocalProgressStore(storage).load()
        self.assertIsNone(result.progress)
        self.assertFalse(result.recovered)
        self.assertIn("primary invalid", result.error)

    def test_save_creates_no_server_or_authenticated_sync_state(self):
        storage = {}
        LocalProgressStore(storage).save(BASE)
        self.assertEqual(set(storage), {STORAGE_KEY})
        payload = storage[STORAGE_KEY]
        self.assertNotIn("token", payload)
        self.assertNotIn("email", payload)
        self.assertNotIn("session_id", payload)

    def test_clear_removes_primary_and_recovery(self):
        storage = {STORAGE_KEY: "x", RECOVERY_KEY: "y", "unrelated": "z"}
        LocalProgressStore(storage).clear()
        self.assertEqual(storage, {"unrelated": "z"})


if __name__ == "__main__":
    unittest.main()
