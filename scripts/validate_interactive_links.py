#!/usr/bin/env python3
"""Validate local documentation routes and anchors embedded in interactive assets."""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INTERACTIVE = DOCS / "assets" / "interactive"
SITE_BASE = "https://docs.invalid/"

HTML_HREF_RE = re.compile(r"\bhref\s*=\s*(['\"])(.*?)\1", re.IGNORECASE | re.DOTALL)
JS_PAGE_RE = re.compile(r"\bpage\s*:\s*(['\"])(.*?)\1", re.DOTALL)
JS_ANCHOR_RE = re.compile(r"\banchor\s*:\s*(['\"])(#.*?)\1", re.DOTALL)
EXPLICIT_ID_RE = re.compile(r"\s*\{#([A-Za-z][\w:.-]*)\}\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
MARKDOWN_LINK_RE = re.compile(r"!?\[([^]]*)\]\([^)]*\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")
CODE_RE = re.compile(r"`([^`]*)`")


@dataclass(frozen=True)
class Reference:
    asset: Path
    raw: str
    origin: str


@dataclass(frozen=True)
class Problem:
    asset: Path
    reference: str
    message: str


def markdown_slug(text: str) -> str:
    """Approximate Python-Markdown/MkDocs heading IDs for project headings."""
    explicit = EXPLICIT_ID_RE.search(text)
    if explicit:
        return explicit.group(1)
    text = EXPLICIT_ID_RE.sub("", text)
    text = MARKDOWN_LINK_RE.sub(r"\1", text)

    # Preserve characters that are literal inside inline-code spans while
    # removing Markdown emphasis markers elsewhere. Python-Markdown renders
    # ``llama_model`` as <code>llama_model</code>, and its TOC slugger keeps
    # the underscore. Removing all underscores before slugification produced
    # the incorrect anchor ``llamamodel``.
    code_spans: list[str] = []

    def stash_code(match: re.Match[str]) -> str:
        token = f"ZZZCODETOKEN{len(code_spans)}ZZZ"
        code_spans.append(match.group(1))
        return token

    text = CODE_RE.sub(stash_code, text)
    text = HTML_TAG_RE.sub("", text)
    text = re.sub(r"[*_~]", "", text)
    for index, code in enumerate(code_spans):
        text = text.replace(f"ZZZCODETOKEN{index}ZZZ", code)

    text = text.strip().lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s\-]+", "-", text).strip("-")
    return text


def heading_ids(markdown: str) -> set[str]:
    ids: set[str] = set()
    counts: dict[str, int] = {}
    in_fence = False
    fence_marker = ""
    for line in markdown.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if not match:
            continue
        slug = markdown_slug(match.group(2))
        if not slug:
            continue
        duplicate_index = counts.get(slug, 0)
        counts[slug] = duplicate_index + 1
        ids.add(slug if duplicate_index == 0 else f"{slug}_{duplicate_index}")
    return ids


def extract_references(asset: Path) -> list[Reference]:
    text = asset.read_text(encoding="utf-8")
    refs = [Reference(asset, match.group(2).strip(), "href") for match in HTML_HREF_RE.finditer(text)]
    refs.extend(Reference(asset, match.group(2).strip(), "page") for match in JS_PAGE_RE.finditer(text))

    # The foundations explorer stores memory-atlas anchors separately and joins
    # them to this canonical route in its renderer.
    if asset.name == "llama-foundations-explorer.html":
        refs.extend(
            Reference(asset, f"foundations/memory-lifetimes/{match.group(2)}", "anchor")
            for match in JS_ANCHOR_RE.finditer(text)
        )
    return refs


def is_ignored(raw: str) -> bool:
    parsed = urlparse(raw)
    return (
        not raw
        or "${" in raw
        or "{{" in raw
        or raw.startswith(("mailto:", "tel:", "javascript:", "data:"))
        or parsed.scheme in {"http", "https"}
        or raw.startswith("//")
    )


def normalize_site_target(reference: Reference) -> tuple[str, str]:
    raw = reference.raw
    if reference.origin in {"page", "anchor"}:
        absolute = urljoin(SITE_BASE, raw.lstrip("/"))
    else:
        asset_route = reference.asset.relative_to(DOCS).as_posix()
        absolute = urljoin(urljoin(SITE_BASE, asset_route), raw)
    parsed = urlparse(absolute)
    return unquote(parsed.path).lstrip("/"), unquote(parsed.fragment)


def route_candidates(route: str) -> list[Path]:
    route = route.strip("/")
    if not route:
        return [DOCS / "index.md"]
    suffix = Path(route).suffix.lower()
    if suffix in {".html", ".htm"}:
        route = route[: -len(suffix)]
    if suffix and suffix not in {".html", ".htm"}:
        return [DOCS / route]
    return [DOCS / f"{route}.md", DOCS / route / "index.md"]


def resolve_markdown(route: str) -> Path | None:
    for candidate in route_candidates(route):
        if candidate.is_file():
            return candidate
    return None


def validate_reference(reference: Reference) -> Problem | None:
    if is_ignored(reference.raw):
        return None
    route, anchor = normalize_site_target(reference)
    target = resolve_markdown(route)
    if target is None:
        candidates = ", ".join(str(path.relative_to(ROOT)) for path in route_candidates(route))
        return Problem(reference.asset, reference.raw, f"route does not resolve; expected one of: {candidates}")
    if anchor:
        ids = heading_ids(target.read_text(encoding="utf-8"))
        if anchor not in ids:
            return Problem(
                reference.asset,
                reference.raw,
                f"anchor '#{anchor}' not found in {target.relative_to(ROOT)}",
            )
    return None


def validate_assets(assets: list[Path]) -> list[Problem]:
    problems: list[Problem] = []
    for asset in assets:
        if not asset.is_file():
            problems.append(Problem(asset, "", "interactive asset is missing"))
            continue
        for reference in extract_references(asset):
            problem = validate_reference(reference)
            if problem:
                problems.append(problem)
    return problems


def discover_assets() -> list[Path]:
    return sorted(INTERACTIVE.glob("*.html"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assets", nargs="*", type=Path, help="optional interactive HTML assets")
    args = parser.parse_args(argv)
    assets = [path if path.is_absolute() else ROOT / path for path in args.assets] or discover_assets()
    problems = validate_assets(assets)
    if problems:
        for problem in problems:
            try:
                asset = problem.asset.relative_to(ROOT)
            except ValueError:
                asset = problem.asset
            reference = f" reference={problem.reference!r}" if problem.reference else ""
            print(f"ERROR: {asset}:{reference} {problem.message}", file=sys.stderr)
        print(f"Interactive link validation failed with {len(problems)} error(s).", file=sys.stderr)
        return 1
    print(f"Interactive link validation passed for {len(assets)} asset(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
