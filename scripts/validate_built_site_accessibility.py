#!/usr/bin/env python3
"""High-confidence structural accessibility checks for the built MkDocs site.

This is intentionally not a WCAG conformance claim. It catches regressions that can
be established reliably from generated HTML without a browser or CSS engine.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path


@dataclass
class PageFacts:
    html_lang: str | None = None
    main_count: int = 0
    h1_count: int = 0
    missing_img_alt: list[str] = field(default_factory=list)
    untitled_iframes: list[str] = field(default_factory=list)
    unnamed_buttons: int = 0


class AccessibilityParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.facts = PageFacts()
        self._button_stack: list[dict[str, object]] = []

    @staticmethod
    def _attrs(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {key: value or "" for key, value in attrs}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = self._attrs(attrs)
        if tag == "html":
            self.facts.html_lang = values.get("lang", "").strip() or None
        elif tag == "main":
            self.facts.main_count += 1
        elif tag == "h1":
            self.facts.h1_count += 1
        elif tag == "img":
            if "alt" not in values:
                self.facts.missing_img_alt.append(values.get("src", "<unknown>"))
        elif tag == "iframe":
            if not values.get("title", "").strip():
                self.facts.untitled_iframes.append(values.get("src", "<unknown>"))
        elif tag == "button":
            labelled = bool(values.get("aria-label", "").strip() or values.get("title", "").strip())
            self._button_stack.append({"labelled": labelled, "text": []})

    def handle_data(self, data: str) -> None:
        if self._button_stack:
            self._button_stack[-1]["text"].append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "button" and self._button_stack:
            button = self._button_stack.pop()
            text = "".join(button["text"]).strip()
            if not button["labelled"] and not text:
                self.facts.unnamed_buttons += 1


def inspect_page(path: Path) -> list[str]:
    parser = AccessibilityParser()
    parser.feed(path.read_text(encoding="utf-8"))
    facts = parser.facts
    errors: list[str] = []

    if not facts.html_lang:
        errors.append("missing non-empty html[lang]")
    if facts.main_count != 1:
        errors.append(f"expected exactly one <main>, found {facts.main_count}")
    if facts.h1_count != 1:
        errors.append(f"expected exactly one <h1>, found {facts.h1_count}")
    for src in facts.missing_img_alt:
        errors.append(f"image lacks alt attribute: {src}")
    for src in facts.untitled_iframes:
        errors.append(f"iframe lacks non-empty title: {src}")
    if facts.unnamed_buttons:
        errors.append(f"found {facts.unnamed_buttons} button(s) without text, aria-label, or title")
    return errors


def validate_site(site_dir: Path) -> list[str]:
    if not site_dir.is_dir():
        return [f"site directory does not exist: {site_dir}"]

    html_files = sorted(site_dir.rglob("*.html"))
    if not html_files:
        return [f"no HTML files found under: {site_dir}"]

    failures: list[str] = []
    for path in html_files:
        # Standalone interactive assets are validated separately and may not use
        # the MkDocs page shell. This validator targets generated documentation pages.
        if "assets/interactive" in path.as_posix():
            continue
        for error in inspect_page(path):
            failures.append(f"{path.relative_to(site_dir)}: {error}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("site_dir", nargs="?", default="site", type=Path)
    args = parser.parse_args()

    failures = validate_site(args.site_dir)
    if failures:
        print("Built-site accessibility validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Built-site accessibility validation passed: {args.site_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
