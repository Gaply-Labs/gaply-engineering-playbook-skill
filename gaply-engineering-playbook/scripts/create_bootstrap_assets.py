#!/usr/bin/env python3
"""Create deterministic GEP bootstrap assets without third-party dependencies.

Creates clearly labeled placeholder assets only:
- docs/assets/logo-default.svg
- docs/assets/favicon-default.svg
- docs/assets/og-default.png (exactly 1200x630)

These files must be replaced by final brand assets before public release.
"""
from __future__ import annotations

import argparse
import binascii
import html
import struct
import zlib
from pathlib import Path


def initials(name: str) -> str:
    parts = [p for p in name.replace("-", " ").replace("_", " ").split() if p]
    if not parts:
        return "GP"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[1][0]).upper()


def write_svg(path: Path, project_name: str, size: int, favicon: bool = False) -> None:
    safe_name = html.escape(project_name)
    mark = html.escape(initials(project_name))
    label = "" if favicon else f'<text x="50%" y="82%" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" fill="#555">BOOTSTRAP - {safe_name}</text>'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}" role="img" aria-label="Bootstrap placeholder for {safe_name}">
  <rect width="{size}" height="{size}" rx="{max(8, size//8)}" fill="#f3f4f6"/>
  <rect x="{size*0.12:.1f}" y="{size*0.12:.1f}" width="{size*0.76:.1f}" height="{size*0.76:.1f}" rx="{max(6, size//10)}" fill="#111827"/>
  <text x="50%" y="54%" text-anchor="middle" dominant-baseline="middle" font-family="system-ui, sans-serif" font-weight="700" font-size="{size*0.34:.1f}" fill="#ffffff">{mark}</text>
  {label}
</svg>
'''
    path.write_text(svg, encoding="utf-8")


def png_chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)


def write_og_png(path: Path, width: int = 1200, height: int = 630) -> None:
    # Neutral bootstrap image with a simple dark central panel. No final branding.
    rows = []
    for y in range(height):
        row = bytearray([0])  # PNG filter type 0
        for x in range(width):
            panel = 120 <= x < width - 120 and 90 <= y < height - 90
            if panel:
                rgb = (31, 41, 55)
            else:
                # subtle neutral variation to avoid a completely flat placeholder
                v = 243 if ((x // 80 + y // 80) % 2 == 0) else 238
                rgb = (v, v, v)
            row.extend(rgb)
        rows.append(bytes(row))
    raw = b"".join(rows)
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = signature + png_chunk(b"IHDR", ihdr) + png_chunk(b"IDAT", zlib.compress(raw, 9)) + png_chunk(b"IEND", b"")
    path.write_bytes(png)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create GEP bootstrap placeholder assets")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--project-name", required=True, help="Confirmed project name")
    parser.add_argument("--force", action="store_true", help="Overwrite existing bootstrap assets")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    assets = root / "docs" / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    targets = {
        "logo": assets / "logo-default.svg",
        "favicon": assets / "favicon-default.svg",
        "og": assets / "og-default.png",
    }

    for p in targets.values():
        if p.exists() and not args.force:
            raise SystemExit(f"Refusing to overwrite existing asset: {p}. Use --force only if replacement is intended.")

    write_svg(targets["logo"], args.project_name, 512, favicon=False)
    write_svg(targets["favicon"], args.project_name, 128, favicon=True)
    write_og_png(targets["og"], 1200, 630)

    for name, path in targets.items():
        print(f"CREATED {name}: {path}")
    print("NOTE: These are bootstrap placeholders and must not be treated as final brand assets.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
