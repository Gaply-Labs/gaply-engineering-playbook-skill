#!/usr/bin/env python3
"""Lightweight, dependency-free GEP repository scanner.

This script only checks deterministic structure/assets. It does not decide business
requirements, payment correctness, SEO semantics, or accessibility compliance.
"""
from __future__ import annotations

import argparse
import json
import os
import struct
from pathlib import Path
from typing import Optional, Tuple


def png_size(path: Path) -> Optional[Tuple[int, int]]:
    try:
        with path.open("rb") as f:
            sig = f.read(24)
        if len(sig) >= 24 and sig[:8] == b"\x89PNG\r\n\x1a\n" and sig[12:16] == b"IHDR":
            return struct.unpack(">II", sig[16:24])
    except OSError:
        pass
    return None


def jpeg_size(path: Path) -> Optional[Tuple[int, int]]:
    try:
        with path.open("rb") as f:
            if f.read(2) != b"\xff\xd8":
                return None
            while True:
                marker_start = f.read(1)
                if not marker_start:
                    return None
                if marker_start != b"\xff":
                    continue
                marker = f.read(1)
                while marker == b"\xff":
                    marker = f.read(1)
                if marker in (b"\xd8", b"\xd9"):
                    continue
                length_raw = f.read(2)
                if len(length_raw) != 2:
                    return None
                length = struct.unpack(">H", length_raw)[0]
                if marker and marker[0] in {
                    0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                    0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
                }:
                    data = f.read(5)
                    if len(data) != 5:
                        return None
                    height, width = struct.unpack(">HH", data[1:5])
                    return width, height
                f.seek(max(length - 2, 0), os.SEEK_CUR)
    except (OSError, struct.error):
        pass
    return None


def image_size(path: Path) -> Optional[Tuple[int, int]]:
    suffix = path.suffix.lower()
    if suffix == ".png":
        return png_size(path)
    if suffix in {".jpg", ".jpeg"}:
        return jpeg_size(path)
    return None


def existing(root: Path, candidates: list[str]) -> list[str]:
    out = []
    for c in candidates:
        p = root / c
        if p.exists():
            out.append(str(p.relative_to(root)))
    return out


def glob_existing(root: Path, patterns: list[str]) -> list[str]:
    found: set[str] = set()
    for pattern in patterns:
        for p in root.glob(pattern):
            if p.is_file():
                try:
                    found.add(str(p.relative_to(root)))
                except ValueError:
                    found.add(str(p))
    return sorted(found)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan a repository for GEP structure/assets")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    docs = existing(root, ["docs", "doc"])
    ui = existing(root, ["docs/ui", "ui", "design"])
    briefs = glob_existing(root, [
        "brief.md", "BRIEF.md", "product-brief.md", "docs/00-product-brief.md",
        "*brief*.md", "*brief*.txt", "*brief*.pdf", "*brief*.docx",
        "docs/*brief*.md", "docs/*requirement*.md", "docs/*prd*.md",
    ])
    logos = glob_existing(root, [
        "docs/assets/logo*", "public/logo*", "static/logo*", "assets/logo*",
        "**/brand/logo*",
    ])
    favicons = glob_existing(root, [
        "docs/assets/favicon*", "public/favicon*", "app/favicon*", "assets/favicon*",
    ])
    ogs = glob_existing(root, [
        "docs/assets/og*", "docs/assets/social*", "public/og*", "public/social*",
        "assets/og*", "assets/social*",
    ])

    og_details = []
    for rel in ogs:
        p = root / rel
        size = image_size(p)
        og_details.append({
            "path": rel,
            "dimensions": list(size) if size else None,
            "is_1200x630": bool(size == (1200, 630)),
        })

    required_docs = [
        "HANDOFF.md",
        "docs/README.md",
        "docs/docs-manifest.md",
        "docs/00-product-brief.md",
        "docs/01-architecture.md",
        "docs/02-ai-context.md",
        "docs/03-project-memory.md",
        "docs/04-decisions.md",
        "docs/05-open-questions.md",
        "docs/06-changelog.md",
        "docs/07-feature-status.md",
        "docs/08-tech-stack.md",
        "docs/09-release-readiness.md",
        "docs/features",
        "docs/ui",
        "docs/assets",
    ]
    required_status = {p: (root / p).exists() for p in required_docs}

    result = {
        "root": str(root),
        "docs_locations": docs,
        "ui_locations": ui,
        "brief_candidates": briefs,
        "logo_candidates": logos,
        "favicon_candidates": favicons,
        "og_candidates": og_details,
        "required_gep_structure": required_status,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"GEP scan: {root}")
        print(f"Docs: {', '.join(docs) if docs else 'MISSING'}")
        print(f"UI/design: {', '.join(ui) if ui else 'MISSING'}")
        print(f"Brief candidates: {', '.join(briefs) if briefs else 'MISSING'}")
        print(f"Logo candidates: {', '.join(logos) if logos else 'MISSING'}")
        print(f"Favicon candidates: {', '.join(favicons) if favicons else 'MISSING'}")
        if og_details:
            print("OG/social candidates:")
            for item in og_details:
                dim = "unknown" if item["dimensions"] is None else "x".join(map(str, item["dimensions"]))
                ok = "OK" if item["is_1200x630"] else "NOT-1200x630"
                print(f"  - {item['path']}: {dim} [{ok}]")
        else:
            print("OG/social candidates: MISSING")
        print("GEP structure:")
        for p, ok in required_status.items():
            print(f"  {'PASS' if ok else 'MISS'} {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
