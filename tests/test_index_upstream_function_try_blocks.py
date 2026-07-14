from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "index_upstream.py"
SPEC = importlib.util.spec_from_file_location("index_upstream", SCRIPT)
assert SPEC and SPEC.loader
index_upstream = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(index_upstream)


class ConstructorFunctionTryBlockCounterTests(unittest.TestCase):
    def test_counts_same_line_and_next_line_constructor_try_blocks(self) -> None:
        source = """\
backend_state::backend_state(int device) try : device(device) {
} catch (...) {
}

nested::resource::resource() noexcept
try {
} catch (...) {
}
"""
        self.assertEqual(
            index_upstream.count_unsupported_syntax(source),
            {
                "braced_constructor_initializers": 0,
                "multiline_constructor_initializers": 0,
                "constructor_function_try_blocks": 2,
            },
        )

    def test_ordinary_function_try_block_is_not_counted(self) -> None:
        source = """\
int parse_value(int input) try {
    return input;
} catch (...) {
    return 0;
}
"""
        self.assertEqual(
            index_upstream.count_unsupported_syntax(source),
            {
                "braced_constructor_initializers": 0,
                "multiline_constructor_initializers": 0,
                "constructor_function_try_blocks": 0,
            },
        )

    def test_constructor_try_blocks_remain_absent_from_symbol_records(self) -> None:
        source = """\
backend_state::backend_state(int device)
try : device(device) {
} catch (...) {
}
"""
        self.assertEqual(index_upstream.extract_symbols(source), [])


if __name__ == "__main__":
    unittest.main()
