#!/usr/bin/env python3
"""Generate an approximate source inventory for a llama.cpp checkout.

This is intentionally a navigation index, not a compiler-grade call graph.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

TEXT_SUFFIXES = {'.c','.cc','.cpp','.cxx','.h','.hh','.hpp','.m','.mm','.cu','.cuh','.metal','.comp','.vert','.frag','.py','.sh','.cmake','.md','.yml','.yaml','.json','.toml','.txt'}
SKIP = {'.git','build','site','__pycache__','.venv'}
INCLUDE_RE = re.compile(r'^\s*#\s*include\s*[<"]([^>"]+)[>"]', re.M)
# C++ attributes may precede a function declaration on the same physical line.
# Bounded trailing-return and requires clauses are accepted after qualifiers.
# Operator lines are reserved for OPERATOR_RE so ordinary extraction cannot emit
# partial duplicate names such as `operator` or a conversion target such as bool.
# Constructor function-try initializer lines beginning with `try :` are also
# reserved for unsupported-syntax telemetry so they cannot become fake functions.
# Every return-type whitespace matcher is horizontal so the match cannot begin on
# a preceding template or blank line. This remains deliberately approximate and
# does not attempt to parse multiline attributes/returns, macros, or every legal
# declarator form.
FUNC_RE = re.compile(
    r'(?m)^[\t ]*(?:\[\[[^\]\n]+\]\][\t ]*)*'
    r'(?!try[\t ]*:)(?![^\n;{}]*\boperator\b)'
    r'(?:[A-Za-z_][\w:<>,~*&\t ]+?)[\t ]+'
    r'([A-Za-z_]\w*(?:::\w+)*)\s*\([^;{}]*\)\s*'
    r'(?:const[\t ]*)?(?:noexcept[\t ]*)?'
    r'(?:->[\t ]*[^;{}\n]+?[\t ]*)?'
    r'(?:requires[\t ]+[^;{}\n]+?[\t ]*)?\{'
)
# Operators need a dedicated bounded pattern because conversion operators do not
# have a return type before the name. The optional horizontal-only prefix admits
# ordinary symbolic/call/subscript operators while still allowing conversions.
OPERATOR_RE = re.compile(
    r'(?m)^[\t ]*(?:\[\[[^\]\n]+\]\][\t ]*)*'
    r'(?:(?:[A-Za-z_][\w:<>,~*&\t ]+?)[\t ]+)?'
    r'((?:[A-Za-z_]\w*::)*operator[\t ]*'
    r'(?:\(\)|\[\]|(?:new|delete)(?:[\t ]*\[\])?|'
    r'[=!<>+\-*/%&|^~]+|[A-Za-z_]\w*(?:::\w+)*))'
    r'\s*\([^;{}]*\)\s*'
    r'(?:const[\t ]*)?(?:noexcept[\t ]*)?'
    r'(?:->[\t ]*[^;{}\n]+?[\t ]*)?'
    r'(?:requires[\t ]+[^;{}\n]+?[\t ]*)?\{'
)
# Qualified constructor and destructor definitions have no return type. The
# backreference requires the function name to equal the immediately preceding
# class name, preventing ordinary qualified methods from becoming duplicates.
# Only a bounded same-line parenthesized initializer list is accepted. Horizontal
# whitespace and explicit parenthesized initializer syntax prevent the opening
# brace of a braced initializer from being mistaken for the function body.
SPECIAL_MEMBER_RE = re.compile(
    r'(?m)^[\t ]*(?:\[\[[^\]\n]+\]\][\t ]*)*'
    r'((?:[A-Za-z_]\w*::)*([A-Za-z_]\w*)::~?\2)'
    r'[\t ]*\([^;{}\n]*\)[\t ]*'
    r'(?:noexcept[\t ]*)?'
    r'(?:requires[\t ]+[^;{}\n]+?[\t ]*)?'
    r'(?::[\t ]*[A-Za-z_]\w*(?:::\w+)*[\t ]*\([^;{}\n]*\)[\t ]*)?\{'
)
# Unsupported-syntax telemetry is intentionally separate from symbol extraction.
# These candidate counters identify constructor forms that the bounded scanner
# skips, without emitting partial or misleading symbol records.
BRACED_CONSTRUCTOR_INITIALIZER_RE = re.compile(
    r'(?m)^[\t ]*(?:\[\[[^\]\n]+\]\][\t ]*)*'
    r'((?:[A-Za-z_]\w*::)*([A-Za-z_]\w*)::\2)'
    r'[\t ]*\([^;{}\n]*\)[\t ]*'
    r'(?:noexcept[\t ]*)?'
    r'(?:requires[\t ]+[^;{}\n]+?[\t ]*)?'
    r':[\t ]*[^;\n]*\b[A-Za-z_]\w*[\t ]*\{[^}\n]*\}[^;\n]*\{'
)
MULTILINE_CONSTRUCTOR_INITIALIZER_RE = re.compile(
    r'(?m)^[\t ]*(?:\[\[[^\]\n]+\]\][\t ]*)*'
    r'((?:[A-Za-z_]\w*::)*([A-Za-z_]\w*)::\2)'
    r'[\t ]*\([^;{}\n]*\)[\t ]*'
    r'(?:noexcept[\t ]*)?'
    r'(?:requires[\t ]+[^;{}\n]+?[\t ]*)?'
    r'\n[\t ]*:'
)
# Count qualified constructor function-try-blocks without indexing them. The
# bounded form accepts optional same-line attributes/qualifiers and either a
# same-line or next-line `try`, but it stops before parsing initializer or catch
# bodies. Ordinary function try-blocks are excluded by the constructor backreference.
CONSTRUCTOR_FUNCTION_TRY_BLOCK_RE = re.compile(
    r'(?m)^[\t ]*(?:\[\[[^\]\n]+\]\][\t ]*)*'
    r'((?:[A-Za-z_]\w*::)*([A-Za-z_]\w*)::\2)'
    r'[\t ]*\([^;{}\n]*\)[\t ]*'
    r'(?:noexcept[\t ]*)?'
    r'(?:requires[\t ]+[^;{}\n]+?[\t ]*)?'
    r'(?:\n[\t ]*)?try(?:[\t ]*:|[\t ]*\{)'
)
# C++ attributes may precede a type declaration on the same physical line.
# Keep every whitespace matcher horizontal so source locations cannot drift to a
# preceding blank line. This remains deliberately approximate: macros and
# multiline attributes still require human review.
CLASS_RE = re.compile(
    r'(?m)^[\t ]*(?:\[\[[^\]\n]+\]\][\t ]*)*'
    r'(?:class|struct|enum(?:[\t ]+class)?)[\t ]+'
    r'(?:\[\[[^\]\n]+\]\][\t ]*)*([A-Za-z_]\w*)'
)


def language(p: Path) -> str:
    ext = p.suffix.lower()
    return {'.c':'C','.h':'C/C++ header','.cpp':'C++','.cc':'C++','.cxx':'C++','.hpp':'C++ header','.hh':'C++ header','.cu':'CUDA','.cuh':'CUDA header','.m':'Objective-C','.mm':'Objective-C++','.metal':'Metal','.py':'Python','.sh':'Shell','.md':'Markdown','.yml':'YAML','.yaml':'YAML'}.get(ext, ext.lstrip('.').upper() or 'text')


def line_number(text: str, offset: int) -> int:
    """Return the 1-based source line containing offset."""
    return text.count('\n', 0, offset) + 1


def extract_symbols(text: str) -> list[dict[str, object]]:
    """Return approximate declarations with source locations.

    Duplicate names are retained because overloads and repeated declarations in
    conditional branches are useful navigation targets. Results are source-ordered.
    """
    records: list[dict[str, object]] = []
    for kind, pattern in (
        ("function", FUNC_RE),
        ("function", OPERATOR_RE),
        ("function", SPECIAL_MEMBER_RE),
        ("type", CLASS_RE),
    ):
        for match in pattern.finditer(text):
            records.append({
                "name": match.group(1),
                "kind": kind,
                "line": line_number(text, match.start()),
            })
    return sorted(records, key=lambda item: (int(item["line"]), str(item["kind"]), str(item["name"])))


def count_unsupported_syntax(text: str) -> dict[str, int]:
    """Count bounded candidates intentionally skipped by symbol extraction.

    The counts are triage telemetry, not a claim to parse every C++ form. Keeping
    them separate ensures unsupported syntax never becomes a partial symbol link.
    """
    return {
        "braced_constructor_initializers": len(BRACED_CONSTRUCTOR_INITIALIZER_RE.findall(text)),
        "multiline_constructor_initializers": len(MULTILINE_CONSTRUCTOR_INITIALIZER_RE.findall(text)),
        "constructor_function_try_blocks": len(CONSTRUCTOR_FUNCTION_TRY_BLOCK_RE.findall(text)),
    }


def source_file_url(base: str | None, relative_path: str) -> str | None:
    """Return a normalized source-file URL when a repository/ref base is supplied."""
    if not base:
        return None
    return f"{base.rstrip('/')}/{relative_path}"


def add_source_links(symbols: list[dict[str, object]], file_url: str | None) -> list[dict[str, object]]:
    """Copy symbol records and add stable line-fragment URLs when possible."""
    if not file_url:
        return [dict(item) for item in symbols]
    return [dict(item, source_url=f"{file_url}#L{int(item['line'])}") for item in symbols]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('source', type=Path)
    ap.add_argument('--out', type=Path, default=Path('data/generated/source-index.json'))
    ap.add_argument('--markdown', type=Path, default=Path('docs/reference/generated-source-inventory.md'))
    ap.add_argument(
        '--source-url-base',
        help='Optional pinned blob URL prefix, for example https://github.com/ggml-org/llama.cpp/blob/<commit>',
    )
    args = ap.parse_args()
    files = []
    for p in sorted(args.source.rglob('*')):
        if not p.is_file() or p.suffix.lower() not in TEXT_SUFFIXES or any(part in SKIP for part in p.parts):
            continue
        try:
            data = p.read_bytes()
            text = data.decode('utf-8', errors='replace')
        except OSError:
            continue
        rel = str(p.relative_to(args.source))
        symbols = extract_symbols(text)
        file_url = source_file_url(args.source_url_base, rel)
        files.append({
            'path': rel,
            'language': language(p),
            'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(),
            'includes': INCLUDE_RE.findall(text)[:100],
            'symbols': [str(item['name']) for item in symbols[:200]],
            'symbol_locations': add_source_links(symbols, file_url),
            'source_url': file_url,
            'unsupported_syntax': count_unsupported_syntax(text),
        })
    aggregate_unsupported = {
        key: sum(int(item['unsupported_syntax'][key]) for item in files)
        for key in (
            'braced_constructor_initializers',
            'multiline_constructor_initializers',
            'constructor_function_try_blocks',
        )
    }
    summary = {
        'source': str(args.source),
        'source_url_base': args.source_url_base,
        'file_count': len(files),
        'unsupported_syntax_counts': aggregate_unsupported,
        'files': files,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2), encoding='utf-8')
    lines = ['# Generated upstream source inventory', '', f"Files indexed: **{len(files)}**", '']
    if args.source_url_base:
        lines.extend([f"Pinned source base: `{args.source_url_base}`", ''])
    lines.extend([
        'Unsupported syntax candidates (telemetry only):',
        '',
        f"- Braced constructor initializers: **{aggregate_unsupported['braced_constructor_initializers']}**",
        f"- Multiline constructor initializers: **{aggregate_unsupported['multiline_constructor_initializers']}**",
        f"- Constructor function-try-blocks: **{aggregate_unsupported['constructor_function_try_blocks']}**",
        '',
        '| Path | Language | Bytes | Includes | Symbols | Unsupported syntax |',
        '|---|---:|---:|---:|---:|---:|',
    ])
    for item in files:
        path_text = f"[`{item['path']}`]({item['source_url']})" if item['source_url'] else f"`{item['path']}`"
        unsupported = sum(int(value) for value in item['unsupported_syntax'].values())
        lines.append(f"| {path_text} | {item['language']} | {item['bytes']} | {len(item['includes'])} | {len(item['symbol_locations'])} | {unsupported} |")
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'indexed {len(files)} files')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
