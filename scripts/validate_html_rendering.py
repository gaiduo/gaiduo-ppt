#!/usr/bin/env python3
"""Static guardrails for gaiduo-ppt Stage 4 HTML output.

This catches the most damaging failure mode: using Stage 3 full-slide images as
the visible deck and hiding real HTML text in a transparent semantic layer.
It is intentionally conservative; failures should trigger manual review or a
real browser screenshot QA pass.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

STAGE3_SLIDE_REF_RE = re.compile(
    r"""(?ix)
    (?:stage3_production/)?slides/slide_\d+\.(?:png|jpg|jpeg|webp)
    |assets/slides/slide_\d+\.(?:png|jpg|jpeg|webp)
    """
)

SUSPICIOUS_FULL_SLIDE_CLASS_RE = re.compile(
    r"""(?ix)
    class\s*=\s*["'][^"']*
    (?:slide-image|full-slide|page-image|semantic-layer)
    [^"']*["']
    """
)

LOW_OPACITY_RE = re.compile(r"(?i)opacity\s*:\s*(0(?:\.\d+)?|0?\.[0-7]\d*)\b")
LOW_TEXT_COLOR_RE = re.compile(r"(?i)\bcolor\s*:\s*rgba?\([^)]*,\s*(0(?:\.\d+)?|0?\.[0-7]\d*)\s*\)")
HIDDEN_TEXT_RE = re.compile(
    r"(?i)(display\s*:\s*none|visibility\s*:\s*hidden|font-size\s*:\s*0|left\s*:\s*-\d{3,}px|transform\s*:\s*translateX\(-\d{3,}px\))"
)
SUSPICIOUS_TEXT_LAYER_RE = re.compile(r"(?i)(semantic-layer|html-title|html-body|html-data|sr-only|visually-hidden)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("html_root", help="Path to generated HTML project root or index.html")
    parser.add_argument("--allow-full-slide-raster", action="store_true")
    return parser.parse_args()


def collect_files(target: Path) -> list[Path]:
    if target.is_file():
        root = target.parent
    else:
        root = target
    patterns = ["*.html", "*.css", "*.js", "*.mjs", "*.ts", "*.tsx", "*.jsx"]
    files: list[Path] = []
    for pattern in patterns:
        files.extend(root.rglob(pattern))
    return sorted(set(files))


def main() -> int:
    args = parse_args()
    target = Path(args.html_root)
    failures: list[str] = []

    if not target.exists():
        print("FAILED")
        print(f"- path not found: {target}")
        return 1

    files = collect_files(target)
    if not files:
        failures.append("no HTML/CSS/JS files found")

    for file_path in files:
        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:
            failures.append(f"{file_path}: cannot read file: {exc}")
            continue

        rel = str(file_path)
        if STAGE3_SLIDE_REF_RE.search(text) and not args.allow_full_slide_raster:
            failures.append(f"{rel}: references full-slide Stage 3/slide image as runtime asset")
        if SUSPICIOUS_FULL_SLIDE_CLASS_RE.search(text) and not args.allow_full_slide_raster:
            failures.append(f"{rel}: contains suspicious full-slide image or semantic-layer class")
        if SUSPICIOUS_TEXT_LAYER_RE.search(text) and LOW_OPACITY_RE.search(text):
            failures.append(f"{rel}: suspicious text layer contains opacity below 0.8")
        if SUSPICIOUS_TEXT_LAYER_RE.search(text) and LOW_TEXT_COLOR_RE.search(text):
            failures.append(f"{rel}: suspicious text layer contains text color alpha below 0.8")
        if SUSPICIOUS_TEXT_LAYER_RE.search(text) and HIDDEN_TEXT_RE.search(text):
            failures.append(f"{rel}: suspicious text layer contains CSS that may hide authoritative HTML text")

    if failures:
        print("FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
