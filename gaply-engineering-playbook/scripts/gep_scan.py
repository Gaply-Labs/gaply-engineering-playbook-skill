#!/usr/bin/env python3
"""Lightweight, dependency-free GEP repository scanner.

Checks deterministic structure and assets only:

- documentation locations and brief candidates;
- brand assets (logo, banner, favicon, OG/social) found by name pattern rather than
  by one exact path, so a file the user named themselves is still detected;
- where each asset sits, which decides whether init may move it or must only
  reference it (see `placement` below);
- image dimensions for PNG and JPEG, so the 1200x630 OG rule can be checked;
- discovery files: robots.txt, sitemap.xml, llms.txt, web app manifest;
- the required GEP tree and any bootstrap placeholders still in place;
- topics the brief or product docs mention with no matching location.

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

# Directories that never hold project-authored assets worth reporting.
PRUNE_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "bower_components", "vendor",
    ".next", ".nuxt", ".svelte-kit", ".astro", ".output", ".turbo", ".cache",
    "dist", "build", "out", "target", "coverage", ".venv", "venv", "env",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".tox", ".gradle",
    ".idea", ".vscode", ".remember", "Pods", "DerivedData",
}

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".svg", ".webp", ".avif", ".gif"}
ICON_EXTS = {".ico", ".webmanifest"}

# An asset kind is recognised by the name of the file, the name of the folder that
# holds it, or both. Patterns run against the file stem in lower case, so a user's
# own "company-logo.png" or "hero-banner.jpg" is found without being told about it.
ASSET_KINDS = {
    "logo": {
        "stem": r"(^|[-_. ])(logo|logotype|logomark|wordmark|brandmark|brand)([-_. ]|$)",
        "dirs": {"logo", "logos", "brand", "branding"},
        "exts": IMAGE_EXTS,
        "purpose": "brand logo",
    },
    "banner": {
        "stem": r"(^|[-_. ])(banner|hero|cover|header-image|headerimage|masthead)([-_. ]|$)",
        "dirs": {"banner", "banners"},
        "exts": IMAGE_EXTS,
        "purpose": "marketing or repository banner",
    },
    "favicon": {
        "stem": r"(^|[-_. ])(favicon|apple-touch-icon|apple-icon|android-chrome|mstile|safari-pinned-tab|site\.webmanifest|web-app-manifest)([-_. ]|$)",
        "dirs": {"favicon", "favicons", "icons", "app-icon", "appicon"},
        "exts": IMAGE_EXTS | ICON_EXTS,
        "purpose": "favicon or app icon set",
    },
    "og": {
        "stem": r"(^|[-_. ])(og|ogimage|opengraph|open-graph|social|share|twitter-card|twittercard|preview|card)([-_. ]|$)",
        "dirs": {"og", "social", "opengraph"},
        "exts": IMAGE_EXTS,
        "purpose": "Open Graph / social preview image, must be exactly 1200x630",
    },
}

# Where an asset may live, and what init is allowed to do about it.
#   assets  = already in docs/assets/, nothing to do
#   docs    = elsewhere under docs/, init moves it into docs/assets/
#   app     = served or bundled by the application, init only references it
#   other   = anywhere else, init only references it
APP_ASSET_ROOTS = ("public", "static", "assets", "src", "app", "www", "resources", "web")

DISCOVERY_FILES = {
    "robots.txt": r"^robots\.txt$",
    "sitemap.xml": r"^sitemap.*\.xml$",
    "llms.txt": r"^llms(-full)?\.txt$",
    "web_manifest": r"^(site\.webmanifest|manifest\.webmanifest|manifest\.json)$",
}
# Only these roots are searched for discovery files; deeper nesting is not how they
# are served, and scanning everywhere would report fixtures and examples.
DISCOVERY_ROOTS = ["", "public", "static", "app", "src/app", "www", "dist", "docs"]

# Topics a brief or product doc may mention, with the GEP location expected to exist
# when they do. Word boundaries keep "api" from matching "rapid". The agent still has to
# confirm each hit against the brief: "no payments in v1" contains the word too.
SIGNALS = [
    {
        "signal": "ui-design",
        "pattern": r"\b(ui|ux|screens?|wireframes?|mockups?|prototype|figma|adobe xd|design system)\b",
        "check": "ui",
        "expected": "docs/ui/README.md (design source, screen inventory); masterdoc.html plus pages as the design package lands",
    },
    {
        "signal": "logo-brand",
        "pattern": r"\b(logo|brand|branding)\b",
        "check": "logo",
        "expected": "a logo in docs/assets/ (logo-default.svg until the final file), with a row in docs/assets/README.md",
    },
    {
        "signal": "banner",
        "pattern": r"\b(banner|hero image|cover image|masthead)\b",
        "check": "banner",
        "expected": "a banner in docs/assets/, with a row in docs/assets/README.md",
    },
    {
        "signal": "favicon-icon",
        "pattern": r"\b(favicon|app icon|launcher icon|touch icon)\b",
        "check": "favicon",
        "expected": "a favicon set in docs/assets/ (favicon-default.svg until the final set), generated with https://favicon.io/favicon-converter/",
    },
    {
        "signal": "og-social",
        "pattern": r"\b(og[: -]?image|open ?graph|social (?:preview|card|image)|share (?:card|preview)|link preview|preview card)\b",
        "check": "og",
        "expected": "docs/assets/og-default.png at exactly 1200x630 until the final og.png",
    },
    {
        "signal": "seo-discovery",
        "pattern": r"\b(seo|search engines?|indexable|indexing|crawl(?:er|ing)?|sitemap|robots\.txt|llms\.txt)\b",
        "check": "seo",
        "expected": "robots.txt and sitemap.xml in the served root; llms.txt when AI discovery matters",
    },
    {
        "signal": "pwa",
        "pattern": r"\b(pwa|progressive web app|installable|service worker|offline mode|add to home screen)\b",
        "check": "pwa",
        "expected": "a web app manifest (site.webmanifest or manifest.json) in the served root",
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


def walk_files(root: Path, max_depth: int = 6, limit: int = 20000):
    """Yield project files, skipping build output and dependency folders."""
    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = Path(dirpath).relative_to(root)
        depth = 0 if rel_dir == Path(".") else len(rel_dir.parts)
        dirnames[:] = [] if depth >= max_depth else sorted(
            d for d in dirnames if d not in PRUNE_DIRS and not d.startswith(".")
        )
        for name in sorted(filenames):
            count += 1
            if count > limit:
                return
            yield Path(dirpath) / name


def existing(root: Path, candidates: list[str]) -> list[str]:
    return [c for c in candidates if (root / c).exists()]


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


def placement_of(rel: Path) -> str:
    parts = rel.parts
    if len(parts) >= 2 and parts[0] == "docs" and parts[1] == "assets":
        return "assets"
    if parts and parts[0] == "docs":
        return "docs"
    if parts and parts[0] in APP_ASSET_ROOTS:
        return "app"
    return "other"


def classify_asset(rel: Path) -> Optional[str]:
    """Return the asset kind for a file, by folder name first and then by file name."""
    suffix = rel.suffix.lower()
    stem = rel.stem.lower()
    dirs = {p.lower() for p in rel.parts[:-1]}
    for kind, spec in ASSET_KINDS.items():
        if suffix in spec["exts"] and dirs & spec["dirs"]:
            return kind
    for kind, spec in ASSET_KINDS.items():
        if suffix in spec["exts"] and re.search(spec["stem"], stem):
            return kind
    if suffix == ".webmanifest":
        return "favicon"
    return None


def is_placeholder(rel: Path) -> bool:
    stem = rel.stem.lower()
    return bool(re.search(r"(^|[-_.])(default|placeholder|bootstrap|sample)([-_.]|$)", stem))


def collect_assets(root: Path, files: list[Path]):
    assets: dict[str, list[dict]] = {kind: [] for kind in ASSET_KINDS}
    for path in files:
        rel = path.relative_to(root)
        kind = classify_asset(rel)
        if not kind:
            continue
        size = image_size(path)
        entry = {
            "path": str(rel),
            "placement": placement_of(rel),
            "dimensions": list(size) if size else None,
            "is_placeholder": is_placeholder(rel),
        }
        if kind == "og":
            entry["is_1200x630"] = bool(size == (1200, 630))
        assets[kind].append(entry)
    for kind in assets:
        assets[kind].sort(key=lambda e: e["path"])
    return assets


def find_discovery(root: Path, files: list[Path]):
    found: dict[str, list[str]] = {name: [] for name in DISCOVERY_FILES}
    allowed = {Path(r) if r else Path(".") for r in DISCOVERY_ROOTS}
    for path in files:
        rel = path.relative_to(root)
        if rel.parent not in allowed:
            continue
        for name, pattern in DISCOVERY_FILES.items():
            if re.match(pattern, rel.name, re.IGNORECASE):
                found[name].append(str(rel))
    for name in found:
        found[name].sort()
    return found


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
    rx = re.compile(pattern, re.IGNORECASE)
    for p in paths:
        for line in read_text(p).splitlines():
            if line.lstrip().startswith("#") and rx.search(line):
                return True
    return False


def location_present(root: Path, check: str, assets: dict, discovery: dict) -> bool:
    if check in ASSET_KINDS:
        return bool(assets.get(check))
    if check == "ui":
        return bool(glob_existing(root, ["docs/ui/*", "docs/ui/**/*", "ui/*", "design/*"]))
    if check == "seo":
        return bool(discovery["robots.txt"] or discovery["sitemap.xml"] or discovery["llms.txt"])
    if check == "pwa":
        return bool(discovery["web_manifest"])
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


def detect_signals(root: Path, briefs: list[str], assets: dict, discovery: dict):
    text = "\n".join(read_text(p) for p in signal_sources(root, briefs)).lower()
    topics, missing = [], []
    for s in SIGNALS:
        hits = sorted({m.group(0) for m in re.finditer(s["pattern"], text)})
        if not hits:
            continue
        present = location_present(root, s["check"], assets, discovery)
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
    files = list(walk_files(root))

    docs = existing(root, ["docs", "doc"])
    ui = existing(root, ["docs/ui", "ui", "design"])
    briefs = glob_existing(root, [
        "brief.md", "BRIEF.md", "product-brief.md", "docs/00-product-brief.md",
        "*brief*.md", "*brief*.txt", "*brief*.pdf", "*brief*.docx",
        "docs/*brief*.md", "docs/*requirement*.md", "docs/*prd*.md",
    ])

    assets = collect_assets(root, files)
    discovery = find_discovery(root, files)
    misplaced = sorted(
        e["path"] for kind in assets for e in assets[kind] if e["placement"] == "docs"
    )
    placeholders = sorted(
        e["path"] for kind in assets for e in assets[kind] if e["is_placeholder"]
    )
    required_status = {p: (root / p).exists() for p in REQUIRED_DOCS}
    gep_initialized = (root / "docs" / "docs-manifest.md").exists()
    topics, referenced_missing = detect_signals(root, briefs, assets, discovery)

    result = {
        "root": str(root),
        "gep_initialized": gep_initialized,
        "docs_locations": docs,
        "ui_locations": ui,
        "brief_candidates": briefs,
        "assets": assets,
        "assets_misplaced": misplaced,
        "placeholder_assets": placeholders,
        "discovery_files": discovery,
        "required_gep_structure": required_status,
        "referenced_topics": topics,
        "referenced_but_missing": referenced_missing,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print(f"GEP scan: {root}")
    print(f"GEP initialized: {'yes' if gep_initialized else 'no'} (docs/docs-manifest.md)")
    print(f"Docs: {', '.join(docs) if docs else 'MISSING'}")
    print(f"UI/design: {', '.join(ui) if ui else 'MISSING'}")
    print(f"Brief candidates: {', '.join(briefs) if briefs else 'MISSING'}")
    print("Brand assets (by name pattern, not by one fixed path):")
    for kind in ASSET_KINDS:
        entries = assets[kind]
        if not entries:
            print(f"  {kind:8} MISSING")
            continue
        for e in entries:
            dim = "" if not e["dimensions"] else " " + "x".join(map(str, e["dimensions"]))
            flags = []
            if e["is_placeholder"]:
                flags.append("placeholder")
            if kind == "og":
                flags.append("1200x630" if e["is_1200x630"] else "NOT-1200x630")
            if e["placement"] == "docs":
                flags.append("move to docs/assets/")
            elif e["placement"] in ("app", "other"):
                flags.append(f"in {e['placement']}, reference only")
            suffix = f" [{', '.join(flags)}]" if flags else ""
            print(f"  {kind:8} {e['path']}{dim}{suffix}")
    if misplaced:
        print(f"Assets to move into docs/assets/: {', '.join(misplaced)}")
    print("Discovery files (searched in served roots only, not in docs/assets/):")
    for name, hits in discovery.items():
        print(f"  {name:14} {', '.join(hits) if hits else 'MISSING'}")
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
