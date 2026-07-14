from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "index_upstream.py"
SPEC = importlib.util.spec_from_file_location("index_upstream", SCRIPT)
assert SPEC and SPEC.loader
index_upstream = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(index_upstream)


class IndexUpstreamTests(unittest.TestCase):
    def test_extract_symbols_keeps_source_order_and_lines(self) -> None:
        source = """\
struct first_type {
    int value;
};

static void first_function() {
}

enum class second_type {
    value,
};

int namespace_name::second_function(int value) const {
    return value;
}
"""
        self.assertEqual(
            index_upstream.extract_symbols(source),
            [
                {"name": "first_type", "kind": "type", "line": 1},
                {"name": "first_function", "kind": "function", "line": 5},
                {"name": "second_type", "kind": "type", "line": 8},
                {"name": "namespace_name::second_function", "kind": "function", "line": 12},
            ],
        )

    def test_extract_symbols_handles_multiple_blank_lines_and_namespace_indentation(self) -> None:
        source = """\
namespace nested {


    struct indented_type {
        int value;
    };


        enum class more_indented_type {
            value,
        };
}
"""
        self.assertEqual(
            index_upstream.extract_symbols(source),
            [
                {"name": "indented_type", "kind": "type", "line": 4},
                {"name": "more_indented_type", "kind": "type", "line": 9},
            ],
        )

    def test_extract_symbols_retains_duplicate_names(self) -> None:
        source = """\
static void selected() {
}
#if FEATURE
static void selected() {
}
#endif
"""
        symbols = index_upstream.extract_symbols(source)
        self.assertEqual([item["line"] for item in symbols], [1, 4])
        self.assertEqual([item["name"] for item in symbols], ["selected", "selected"])

    def test_source_file_url_normalizes_base(self) -> None:
        self.assertEqual(
            index_upstream.source_file_url(
                "https://github.com/ggml-org/llama.cpp/blob/abc123/",
                "ggml/src/ggml-opencl/ggml-opencl.cpp",
            ),
            "https://github.com/ggml-org/llama.cpp/blob/abc123/ggml/src/ggml-opencl/ggml-opencl.cpp",
        )
        self.assertIsNone(index_upstream.source_file_url(None, "file.cpp"))

    def test_add_source_links_preserves_records_and_adds_line_fragments(self) -> None:
        symbols = [{"name": "selected", "kind": "function", "line": 17}]
        linked = index_upstream.add_source_links(symbols, "https://example.test/repo/blob/ref/file.cpp")
        self.assertEqual(
            linked,
            [{
                "name": "selected",
                "kind": "function",
                "line": 17,
                "source_url": "https://example.test/repo/blob/ref/file.cpp#L17",
            }],
        )
        self.assertNotIn("source_url", symbols[0])
        self.assertEqual(index_upstream.add_source_links(symbols, None), symbols)


if __name__ == "__main__":
    unittest.main()
