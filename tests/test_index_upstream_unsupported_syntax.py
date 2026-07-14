from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "index_upstream.py"
SPEC = importlib.util.spec_from_file_location("index_upstream", SCRIPT)
assert SPEC and SPEC.loader
index_upstream = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(index_upstream)


class UnsupportedSyntaxCounterTests(unittest.TestCase):
    def test_counts_braced_and_multiline_constructor_initializers(self) -> None:
        source = """\
backend_state::backend_state(int device) : options_{device, true} {
}

backend_state::backend_state(int device)
    : device(device) {
}

backend_state::backend_state(int device) : device(device) {
}
"""
        self.assertEqual(
            index_upstream.count_unsupported_syntax(source),
            {
                "braced_constructor_initializers": 1,
                "multiline_constructor_initializers": 1,
            },
        )

    def test_supported_parenthesized_initializer_is_not_counted(self) -> None:
        source = """\
backend_state::backend_state(int device) : device(device) {
}
"""
        self.assertEqual(
            index_upstream.count_unsupported_syntax(source),
            {
                "braced_constructor_initializers": 0,
                "multiline_constructor_initializers": 0,
            },
        )

    def test_unsupported_candidates_remain_absent_from_symbol_records(self) -> None:
        source = """\
backend_state::backend_state(int device) : options_{device, true} {
}

backend_state::backend_state(int device)
    : device(device) {
}
"""
        self.assertEqual(index_upstream.extract_symbols(source), [])


if __name__ == "__main__":
    unittest.main()
