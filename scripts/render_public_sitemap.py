#!/usr/bin/env python3
"""Render landing/sitemap.xml listing public verification endpoints +
public doctrine source files. Byte-stable for the CI drift gate.

Usage:
    python scripts/render_public_sitemap.py
    DEALIX_PUBLIC_ORIGIN=https://dealix.sa python scripts/render_public_sitemap.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "landing" / "sitemap.xml"

# Origin is configurable so the file is stable in CI (no DNS lookup),
# but the founder can re-render with the real origin before deploy.
ORIGIN = os.environ.get("DEALIX_PUBLIC_ORIGIN", "https://dealix.example.com")


PUBLIC_API_PATHS = [
    "/api/v1/dealix-promise",
    "/api/v1/doctrine",
    "/api/v1/capital-assets/public",
    "/api/v1/compliance/status",
    "/api/v1/founder/launch-status/public",
    "/api/v1/public/health",
]

PUBLIC_PAGES = [
    "/",
    "/founder-command-center.html",
    "/architecture.html",
    "/assets/data/verifier-report.json",
    "/assets/badges/doctrine-status.svg",
    "/assets/badges/verifier-score.svg",
    "/assets/badges/ceo-complete.svg",
]


def _open_doctrine_urls() -> list[str]:
    out = []
    d = REPO_ROOT / "open-doctrine"
    if d.exists():
        for p in sorted(d.glob("*.md")):
            out.append(f"/open-doctrine/{p.name}")
    return out


def render(origin: str = ORIGIN) -> str:
    urls = []
    urls.extend(PUBLIC_PAGES)
    urls.extend(PUBLIC_API_PATHS)
    urls.extend(_open_doctrine_urls())

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{origin}{u}</loc>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render(), encoding="utf-8")
    print(f"wrote {OUTPUT_PATH.relative_to(REPO_ROOT)} (origin: {ORIGIN})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
