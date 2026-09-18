#!/usr/bin/env python3
"""Lightweight, dependency-free GEP repository scanner.

Checks deterministic structure and assets only: documentation locations, brief
candidates, logo/favicon/OG candidates with image dimensions, the required GEP tree,
bootstrap placeholders still in place, and topics that the brief or product docs
mention without a matching folder or file ("referenced but missing").

It does not decide business requirements, payment correctness, SEO semantics, or
accessibility compliance. Its output is evidence for the skill, not a verdict.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import struct
from pathlib import Path
from typing import Optional, Tuple

REQUIRED_DOCS = [
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
    "docs/ui/README.md",
    "docs/assets",
    "docs/assets/README.md",
]

# Topics a brief or product doc may mention, with the GEP location expected to exist
# when they do. Word boundaries keep "api" from matching "rapid". The agent still has to
# confirm each hit against the brief: "no payments in v1" contains the word too.
SIGNALS = [
    {
        "signal": "ui-design",
        "pattern": r"\b(ui|ux|screens?|wireframes?|mockups?|prototype|figma|adobe xd|design system)\b",
        "check": "ui",
        "expected": "docs/ui/README.md (design source, screen inventory); screens.md, flows.md, screenshots/ as content exists",
    },
    {
        "signal": "logo-brand",
        "pattern": r"\b(logo|brand|branding)\b",
        "check": "logo",
        "expected": "docs/assets/logo-default.svg until the final logo, with a row in docs/assets/README.md",
    },
    {
        "signal": "favicon-icon",
        "pattern": r"\b(favicon|app icon|launcher icon)\b",
        "check": "favicon",
        "expected": "docs/assets/favicon-default.svg until the final favicon set",
    },
    {
        "signal": "og-social",
        "pattern": r"\b(og[: -]?image|open ?graph|social (?:preview|card|image)|share (?:card|preview)|link preview|preview card)\b",
        "check": "og",
        "expected": "docs/assets/og-default.png at exactly 1200x630 until the final og.png",
    },
    {
        "signal": "api",
        "pattern": r"\b(api|rest|graphql|endpoints?|webhooks?|openapi|swagger)\b",
        "check": "api",
        "expected": "an API section in docs/01-architecture.md or a feature doc; docs/api/ only for spec files",
    },
    {
        "signal": "payments",
        "pattern": r"\b(payments?|subscriptions?|billing|checkout|stripe|revenuecat|moonpay|in-app purchases?)\b",
        "check": "payments",
        "expected": "a provider ADR in docs/04-decisions.md and a billing/payment feature doc under docs/features/",
    },
]


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


def read_text(path: Path, limit: int = 512_000) -> str:
    """Read a text file for signal scanning; oversized or unreadable files count as empty."""
    try:
        if not path.is_file() or path.stat().st_size > limit:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def signal_sources(root: Path, briefs: list[str]) -> list[Path]:
    """Product-facing documents only. Release checklists and agent rules mention every
    topic by design, so scanning them would flag everything."""
    paths = [root / b for b in briefs]
    paths += [root / "README.md", root / "docs" / "00-product-brief.md", root / "docs" / "01-architecture.md"]
    paths += sorted((root / "docs" / "features").glob("*.md"))
    paths += sorted((root / "docs" / "ui").glob("*.md"))
    out: list[Path] = []
    for p in paths:
        if p.is_file() and p.suffix.lower() in {".md", ".txt"} and p not in out:
            out.append(p)
    return out


def heading_mentions(paths: list[Path], pattern: str) -> bool:
    """True when any Markdown heading in the given files matches the pattern."""
    rx = re.compile(pattern, re.IGNORECASE)
    for p in paths:
        for line in read_text(p).splitlines():
            if line.lstrip().startswith("#") and rx.search(line):
                return True
    return False


def location_present(root: Path, check: str, logos: list[str], favicons: list[str], ogs: list[str]) -> bool:
    if check == "ui":
        return bool(glob_existing(root, ["docs/ui/*", "docs/ui/**/*", "ui/*", "design/*"]))
    if check == "logo":
        return bool(logos)
    if check == "favicon":
        return bool(favicons)
    if check == "og":
        return bool(ogs)
    if check == "api":
        if glob_existing(root, ["docs/api/*", "docs/api/**/*", "docs/features/*api*", "openapi.*", "swagger.*", "docs/openapi.*"]):
            return True
        docs = [root / "docs" / "01-architecture.md"] + sorted((root / "docs" / "features").glob("*.md"))
        return heading_mentions(docs, r"\bapi\b|service contract|endpoints?")
    if check == "payments":
        if glob_existing(root, ["docs/features/*pay*", "docs/features/*bill*", "docs/features/*subscri*", "docs/features/*monetiz*", "docs/features/*checkout*"]):
            return True
        decisions = read_text(root / "docs" / "04-decisions.md").lower()
        return bool(re.search(r"\b(stripe|revenuecat|moonpay|payment provider|payment gateway)\b", decisions))
    return False


def detect_signals(root: Path, briefs: list[str], logos: list[str], favicons: list[str], ogs: list[str]):
    text = "\n".join(read_text(p) for p in signal_sources(root, briefs)).lower()
    topics = []
    missing = []
    for s in SIGNALS:
        hits = sorted({m.group(0) for m in re.finditer(s["pattern"], text)})
        if not hits:
            continue
        present = location_present(root, s["check"], logos, favicons, ogs)
        topics.append({
            "signal": s["signal"],
            "matched_terms": hits[:8],
            "present": present,
            "expected": s["expected"],
        })
        if not present:
            missing.append(s["signal"])
    return topics, missing


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

    required_status = {p: (root / p).exists() for p in REQUIRED_DOCS}
    gep_initialized = (root / "docs" / "docs-manifest.md").exists()
    placeholders = glob_existing(root, ["docs/assets/*-default.*"])
    topics, referenced_missing = detect_signals(root, briefs, logos, favicons, ogs)

    result = {
        "root": str(root),
        "gep_initialized": gep_initialized,
        "docs_locations": docs,
        "ui_locations": ui,
        "brief_candidates": briefs,
        "logo_candidates": logos,
        "favicon_candidates": favicons,
        "og_candidates": og_details,
        "placeholder_assets": placeholders,
        "required_gep_structure": required_status,
        "referenced_topics": topics,
        "referenced_but_missing": referenced_missing,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"GEP scan: {root}")
        print(f"GEP initialized: {'yes' if gep_initialized else 'no'} (docs/docs-manifest.md)")
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
        print(f"Placeholder assets: {', '.join(placeholders) if placeholders else 'none'}")
        print("GEP structure:")
        for p, ok in required_status.items():
            print(f"  {'PASS' if ok else 'MISS'} {p}")
        if topics:
            print("Referenced topics (advisory; confirm against the brief):")
            for t in topics:
                state = "present" if t["present"] else "MISSING"
                print(f"  {state:8} {t['signal']}: matched {', '.join(t['matched_terms'])}")
                if not t["present"]:
                    print(f"           expected: {t['expected']}")
        else:
            print("Referenced topics: none detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
