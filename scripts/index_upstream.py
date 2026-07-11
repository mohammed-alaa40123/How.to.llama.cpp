#!/usr/bin/env python3
"""Generate an approximate source inventory for a llama.cpp checkout.

This is intentionally a navigation index, not a compiler-grade call graph.
"""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

TEXT_SUFFIXES = {'.c','.cc','.cpp','.cxx','.h','.hh','.hpp','.m','.mm','.cu','.cuh','.metal','.comp','.vert','.frag','.py','.sh','.cmake','.md','.yml','.yaml','.json','.toml','.txt'}
SKIP = {'.git','build','site','__pycache__','.venv'}
INCLUDE_RE = re.compile(r'^\s*#\s*include\s*[<"]([^>"]+)[>"]', re.M)
FUNC_RE = re.compile(r'(?m)^[\t ]*(?:[A-Za-z_][\w:<>,~*&\s]+?)[\t ]+([A-Za-z_]\w*(?:::\w+)*)\s*\([^;{}]*\)\s*(?:const\s*)?(?:noexcept\s*)?\{')
CLASS_RE = re.compile(r'(?m)^\s*(?:class|struct|enum(?:\s+class)?)\s+([A-Za-z_]\w*)')

def language(p: Path) -> str:
    ext=p.suffix.lower()
    return {'.c':'C','.h':'C/C++ header','.cpp':'C++','.cc':'C++','.cxx':'C++','.hpp':'C++ header','.hh':'C++ header','.cu':'CUDA','.cuh':'CUDA header','.m':'Objective-C','.mm':'Objective-C++','.metal':'Metal','.py':'Python','.sh':'Shell','.md':'Markdown','.yml':'YAML','.yaml':'YAML'}.get(ext, ext.lstrip('.').upper() or 'text')

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('source', type=Path)
    ap.add_argument('--out', type=Path, default=Path('data/generated/source-index.json'))
    ap.add_argument('--markdown', type=Path, default=Path('docs/reference/generated-source-inventory.md'))
    args=ap.parse_args()
    src=args.source.resolve()
    records=[]
    for p in sorted(src.rglob('*')):
        if not p.is_file() or any(part in SKIP for part in p.parts): continue
        if p.suffix.lower() not in TEXT_SUFFIXES and p.name not in {'CMakeLists.txt','Makefile'}: continue
        try: raw=p.read_bytes(); text=raw.decode('utf-8')
        except (UnicodeDecodeError,OSError): continue
        rel=p.relative_to(src).as_posix()
        records.append({
          'path':rel,'language':language(p),'bytes':len(raw),'lines':text.count('\n')+1,
          'sha256':hashlib.sha256(raw).hexdigest(),
          'includes':sorted(set(INCLUDE_RE.findall(text))),
          'symbols':sorted(set(FUNC_RE.findall(text)) | set(CLASS_RE.findall(text)))[:500]
        })
    summary={'source_root':str(src),'file_count':len(records),'total_lines':sum(r['lines'] for r in records),'files':records,
      'limitations':['Regex symbols are approximate.','Conditional compilation is unresolved.','Virtual calls/function pointers/backend registration require human review.']}
    args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_text(json.dumps(summary,indent=2)+'\n')
    bylang={}
    for r in records: bylang.setdefault(r['language'],[0,0]); bylang[r['language']][0]+=1; bylang[r['language']][1]+=r['lines']
    rows='\n'.join(f"| {k} | {v[0]} | {v[1]:,} |" for k,v in sorted(bylang.items(), key=lambda kv:-kv[1][1]))
    md=f"""# Generated source inventory\n\nGenerated from `{src}`. This is a navigation index, not a compiler-grade call graph.\n\n- Files: **{len(records):,}**\n- Lines: **{summary['total_lines']:,}**\n\n| Language | Files | Lines |\n|---|---:|---:|\n{rows}\n\nThe full per-file index is stored in `data/generated/source-index.json`.\n"""
    args.markdown.parent.mkdir(parents=True,exist_ok=True); args.markdown.write_text(md)
    print(f"Indexed {len(records)} files / {summary['total_lines']} lines")
    return 0
if __name__=='__main__': raise SystemExit(main())
