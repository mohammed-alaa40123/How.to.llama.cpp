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

    def test_extract_symbols_handles_same_line_cpp_attributes(self) -> None:
        source = """\
[[nodiscard]] struct attributed_before_keyword {
};

struct [[gnu::packed]] attributed_after_keyword {
};

[[deprecated("use replacement")]] enum class [[nodiscard]] attributed_enum {
    value,
};
"""
        self.assertEqual(
            index_upstream.extract_symbols(source),
            [
                {"name": "attributed_before_keyword", "kind": "type", "line": 1},
                {"name": "attributed_after_keyword", "kind": "type", "line": 4},
                {"name": "attributed_enum", "kind": "type", "line": 7},
            ],
        )

    def test_extract_symbols_handles_same_line_function_attributes(self) -> None:
        source = """\
[[nodiscard]] static int attributed_function(int value) {
    return value;
}

[[gnu::always_inline]] int namespace_name::attributed_method() const noexcept {
    return 0;
}
"""
        self.assertEqual(
            index_upstream.extract_symbols(source),
            [
                {"name": "attributed_function", "kind": "function", "line": 1},
                {"name": "namespace_name::attributed_method", "kind": "function", "line": 5},
            ],
        )

    def test_extract_symbols_handles_same_line_trailing_return_definitions(self) -> None:
        source = """\
auto trailing_function(int value) -> int {
    return value;
}

[[nodiscard]] auto namespace_name::trailing_method() const noexcept -> long long {
    return 0;
}
"""
        self.assertEqual(
            index_upstream.extract_symbols(source),
            [
                {"name": "trailing_function", "kind": "function", "line": 1},
                {"name": "namespace_name::trailing_method", "kind": "function", "line": 5},
            ],
        )

    def test_extract_symbols_handles_requires_without_consuming_template_line(self) -> None:
        source = """\
template <typename T>
int constrained_function(T value) requires Integral<T> {
    return value;
}

template <typename T>
[[nodiscard]] auto namespace_name::constrained_method(T value) const noexcept -> T requires Serializable<T> {
    return value;
}
"""
        self.assertEqual(
            index_upstream.extract_symbols(source),
            [
                {"name": "constrained_function", "kind": "function", "line": 2},
                {"name": "namespace_name::constrained_method", "kind": "function", "line": 7},
            ],
        )

    def test_extract_symbols_handles_bounded_operator_definitions(self) -> None:
        source = """\
bool tensor_view::operator==(const tensor_view & other) const noexcept {
    return data == other.data;
}

void tensor_view::operator()(int index) const {
}

int & tensor_view::operator[](int index) {
    return data[index];
}

resource::operator bool() const noexcept {
    return handle != nullptr;
}
"""
        self.assertEqual(
            index_upstream.extract_symbols(source),
            [
                {"name": "tensor_view::operator==", "kind": "function", "line": 1},
                {"name": "tensor_view::operator()", "kind": "function", "line": 5},
                {"name": "tensor_view::operator[]", "kind": "function", "line": 8},
                {"name": "resource::operator bool", "kind": "function", "line": 12},
            ],
        )

    def test_extract_symbols_handles_qualified_constructors_and_destructors(self) -> None:
        source = """\
backend_state::backend_state(int device) noexcept {
    initialize(device);
}

backend_state::~backend_state() noexcept {
    release();
}

[[deprecated("use factory")]] nested::resource::resource() requires Enabled<nested::resource> {
}
"""
        self.assertEqual(
            index_upstream.extract_symbols(source),
            [
                {"name": "backend_state::backend_state", "kind": "function", "line": 1},
                {"name": "backend_state::~backend_state", "kind": "function", "line": 5},
                {"name": "nested::resource::resource", "kind": "function", "line": 9},
            ],
        )

    def test_extract_symbols_handles_same_line_constructor_initializer_lists(self) -> None:
        source = """\
backend_state::backend_state(int device) noexcept : device(device), handle(nullptr) {
    initialize();
}

nested::resource::resource(int value) : value_(value) {
}
"""
        self.assertEqual(
            index_upstream.extract_symbols(source),
            [
                {"name": "backend_state::backend_state", "kind": "function", "line": 1},
                {"name": "nested::resource::resource", "kind": "function", "line": 5},
            ],
        )

    def test_extract_symbols_handles_same_line_delegating_constructors(self) -> None:
        source = """\
backend_state::backend_state(int device) : backend_state(device, nullptr) {
}

nested::resource::resource() noexcept : resource(default_value()) {
}
"""
        self.assertEqual(
            index_upstream.extract_symbols(source),
            [
                {"name": "backend_state::backend_state", "kind": "function", "line": 1},
                {"name": "nested::resource::resource", "kind": "function", "line": 4},
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
