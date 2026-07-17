import json
import shutil
import subprocess
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "progress" / "progress-store.mjs"
EXAMPLE = ROOT / "progress" / "examples" / "local-progress-v0.json"


class ProgressStoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if shutil.which("node") is None:
            raise unittest.SkipTest("node is required for browser-progress contract tests")

    def run_node(self, body: str) -> subprocess.CompletedProcess[str]:
        script = textwrap.dedent(f"""
            import assert from 'node:assert/strict';
            import * as progress from {json.dumps(MODULE.as_uri())};
            const example = {EXAMPLE.read_text(encoding='utf-8')};
            {body}
        """)
        return subprocess.run(
            ["node", "--input-type=module", "-e", script],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def assert_node_passes(self, body: str) -> None:
        result = self.run_node(body)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_round_trip_is_deterministic(self):
        self.assert_node_passes("""
            const raw = progress.exportProgress(example);
            const imported = progress.importProgress(raw, null).state;
            assert.deepEqual(imported, example);
            assert.equal(progress.exportProgress(imported), raw);
        """)

    def test_failed_import_preserves_existing_storage(self):
        self.assert_node_passes("""
            const data = new Map();
            const storage = {
              getItem: key => data.has(key) ? data.get(key) : null,
              setItem: (key, value) => data.set(key, value),
              removeItem: key => data.delete(key),
            };
            const adapter = progress.createLocalStorageAdapter(storage);
            const before = adapter.save(example);
            assert.throws(() => adapter.import('{broken json'));
            assert.equal(adapter.export(), before);
        """)

    def test_unsupported_version_has_no_implicit_migration(self):
        self.assert_node_passes("""
            const future = structuredClone(example);
            future.schema_version = '0.2.0';
            assert.throws(() => progress.importProgress(JSON.stringify(future), example), /no migration path/);
        """)

    def test_privacy_sensitive_fields_are_rejected(self):
        self.assert_node_passes("""
            const unsafe = structuredClone(example);
            unsafe.lessons[0].email = 'learner@example.com';
            assert.throws(() => progress.exportProgress(unsafe), /forbidden privacy-sensitive field/);
        """)

    def test_adapter_clear_and_empty_export(self):
        self.assert_node_passes("""
            const data = new Map();
            const storage = {
              getItem: key => data.has(key) ? data.get(key) : null,
              setItem: (key, value) => data.set(key, value),
              removeItem: key => data.delete(key),
            };
            const adapter = progress.createLocalStorageAdapter(storage);
            adapter.save(example);
            adapter.clear();
            assert.equal(adapter.load(), null);
            assert.throws(() => adapter.export(), /no local progress exists/);
        """)


if __name__ == "__main__":
    unittest.main()
