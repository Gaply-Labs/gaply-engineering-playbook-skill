#!/usr/bin/env python3
"""Move brand assets that sit loose under docs/ into docs/assets/.

The Gaply playbook keeps every brand asset in `docs/assets/`. Projects rarely start
that way: a logo lands in `docs/logo.png`, a favicon set arrives as `docs/favicon/`.
This script finds those files with the same name patterns `gep_scan.py` uses, so a
file the user named themselves is moved too, and relocates them while preserving any
set structure (`docs/favicon/` stays a folder inside `docs/assets/`).

It never touches assets the application serves (`public/`, `static/`, `src/`, `app/`
and similar). Those stay where the build expects them and are only referenced from
the inventory in `docs/assets/README.md`; moving them would break the site.

Nothing moves without `--apply`. Without it the script prints the plan and exits.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

# Importing a sibling module would leave a __pycache__ folder inside the installed
# skill directory, which then travels into the upload ZIP and into every project the
# skill is copied to. The skill directory is not ours to litter in.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

from gep_scan import classify_asset, placement_of, walk_files  # noqa: E402


def plan_moves(root: Path) -> list[tuple[Path, Path, str]]:
    """Return (source, destination, kind) for every asset loose under docs/."""
    moves = []
    for path in walk_files(root):
        rel = path.relative_to(root)
        kind = classify_asset(rel)
        if not kind or placement_of(rel) != "docs":
            continue
        # docs/logo.png        -> docs/assets/logo.png
        # docs/favicon/x.ico   -> docs/assets/favicon/x.ico
        inside_docs = Path(*rel.parts[1:])
        moves.append((path, root / "docs" / "assets" / inside_docs, kind))
    return sorted(moves, key=lambda m: str(m[0]))


def find_references(root: Path, names: set[str]) -> dict[str, list[str]]:
    """Markdown files that mention a moved file by name, so links can be corrected."""
    refs: dict[str, list[str]] = {}
    for path in walk_files(root):
        if path.suffix.lower() not in {".md", ".html"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        hits = sorted(n for n in names if n in text)
        if hits:
            refs[str(path.relative_to(root))] = hits
    return refs


def main() -> int:
    parser = argparse.ArgumentParser(description="Move loose brand assets into docs/assets/")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--apply", action="store_true", help="Perform the moves (default: plan only)")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    moves = plan_moves(root)

    if not moves:
        print("No loose brand assets under docs/. Nothing to move.")
        return 0

    conflicts = [(s, d) for s, d, _ in moves if d.exists()]
    for src, dst, kind in moves:
        rel_src = src.relative_to(root)
        rel_dst = dst.relative_to(root)
        mark = "SKIP (destination exists)" if dst.exists() else ("MOVE" if args.apply else "PLAN")
        print(f"{mark:26} {kind:8} {rel_src} -> {rel_dst}")

    if not args.apply:
        print("\nPlan only. Re-run with --apply to move these files.")
        return 0

    moved = 0
    for src, dst, _ in moves:
        if dst.exists():
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        moved += 1

    # Remove directories left empty by the move, such as an emptied docs/favicon/.
    for parent in sorted({s.parent for s, _, _ in moves}, key=lambda p: -len(p.parts)):
        if parent != root / "docs" and parent.is_dir() and not any(parent.iterdir()):
            parent.rmdir()
            print(f"Removed empty directory: {parent.relative_to(root)}")

    print(f"\nMoved {moved} file(s) into docs/assets/.")
    if conflicts:
        print(f"Skipped {len(conflicts)} file(s) because the destination already existed.")

    refs = find_references(root, {s.name for s, _, _ in moves})
    if refs:
        print("\nFiles mentioning a moved asset by name; check their links:")
        for path, names in sorted(refs.items()):
            print(f"  {path}: {', '.join(names)}")
    print("\nRecord every asset in docs/assets/README.md with its status and dimensions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
