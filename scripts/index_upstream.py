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
# Every return-type whitespace matcher is horizontal so the match cannot begin on
# a preceding template or blank line. This remains deliberately approximate and
# does not attempt to parse multiline attributes/returns, macros, or every legal
# declarator form.
FUNC_RE = re.compile(
    r'(?m)^[\t ]*(?:\[\[[^\]\n]+\]\][\t ]*)*'
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
    for kind, pattern in (("function", FUNC_RE), ("function", OPERATOR_RE), ("type", CLASS_RE)):
        for match in pattern.finditer(text):
            records.append({
                "name": match.group(1),
                "kind": kind,
                "line": line_number(text, match.start()),
            })
    return sorted(records, key=lambda item: (int(item["line"]), str(item["kind"]), str(item["name"])))


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
    src = args.source.resolve()
    records = []
    for p in sorted(src.rglob('*')):
        if not p.is_file() or any(part in SKIP for part in p.parts):
            continue
        if p.suffix.lower() not in TEXT_SUFFIXES and p.name not in {'CMakeLists.txt','Makefile'}:
            continue
        try:
            raw = p.read_bytes()
            text = raw.decode('utf-8')
        except (UnicodeDecodeError, OSError):
            continue
        rel = p.relative_to(src).as_posix()
        file_url = source_file_url(args.source_url_base, rel)
        symbol_records = add_source_links(extract_symbols(text), file_url)
        record = {
            'path': rel,
            'language': language(p),
            'bytes': len(raw),
            'lines': text.count('\n') + 1,
            'sha256': hashlib.sha256(raw).hexdigest(),
            'includes': sorted(set(INCLUDE_RE.findall(text))),
            # Preserve the original compact field for existing consumers.
            'symbols': sorted({str(item['name']) for item in symbol_records})[:500],
            # Untruncated, source-ordered navigation records.
            'symbol_locations': symbol_records,
        }
        if file_url:
            record['source_url'] = file_url
        records.append(record)
    summary = {
        'source_root': str(src),
        'source_url_base': args.source_url_base.rstrip('/') if args.source_url_base else None,
        'file_count': len(records),
        'total_lines': sum(r['lines'] for r in records),
        'files': records,
        'limitations': [
            'Regex symbols are approximate.',
            'Conditional compilation is unresolved.',
            'Overloads and repeated conditional declarations may share names.',
            'Virtual calls/function pointers/backend registration require human review.',
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2) + '\n')
    bylang = {}
    for r in records:
        bylang.setdefault(r['language'], [0, 0])
        bylang[r['language']][0] += 1
        bylang[r['language']][1] += r['lines']
    rows = '\n'.join(f"| {k} | {v[0]} | {v[1]:,} |" for k, v in sorted(bylang.items(), key=lambda kv: -kv[1][1]))
    source_note = f" Source links target `{summary['source_url_base']}`." if summary['source_url_base'] else ''
    md = f"""# Generated source inventory

Generated from `{src}`. This is a navigation index, not a compiler-grade call graph.{source_note}

- Files: **{len(records):,}**
- Lines: **{summary['total_lines']:,}**

| Language | Files | Lines |
|---|---:|---:|
{rows}

The full per-file index is stored in `data/generated/source-index.json`. Each file includes untruncated `symbol_locations` records with approximate declaration kind and 1-based source line. When `--source-url-base` is supplied, file records and symbols also include pinned GitHub URLs. The legacy compact `symbols` field remains for compatibility.
"""
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.write_text(md)
    print(f"Indexed {len(records)} files / {summary['total_lines']} lines")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
