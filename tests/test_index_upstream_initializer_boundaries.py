from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "index_upstream.py"
SPEC = importlib.util.spec_from_file_location("index_upstream", SCRIPT)
assert SPEC and SPEC.loader
index_upstream = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(index_upstream)


class InitializerBoundaryTests(unittest.TestCase):
    def test_parenthesized_same_line_initializer_is_indexed(self) -> None:
        source = """\
backend_state::backend_state(int device) : device(device) {
}
"""
        self.assertEqual(
            index_upstream.extract_symbols(source),
            [{"name": "backend_state::backend_state", "kind": "function", "line": 1}],
        )

    def test_braced_initializer_is_not_partially_indexed(self) -> None:
        source = """\
backend_state::backend_state(int device) : options_{device, true} {
}
"""
        self.assertEqual(index_upstream.extract_symbols(source), [])

    def test_multiline_initializer_is_not_partially_indexed(self) -> None:
        source = """\
backend_state::backend_state(int device)
    : device(device) {
}
"""
        self.assertEqual(index_upstream.extract_symbols(source), [])


if __name__ == "__main__":
    unittest.main()
