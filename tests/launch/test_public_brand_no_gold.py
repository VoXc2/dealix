"""Public brand guard: Dealix public surfaces use navy/cyan/neutrals — no gold.

Covers the canonical production frontend (apps/web, served as dealix.me /
www.dealix.me via Dockerfile.web).

- Gold HEX palette must be absent from public brand surfaces
  (CSS, TS/TSX, SVG). Semantic status colors use the separate amber system
  (amber/*#F59E0B), which this test intentionally does not touch.
- Backend API contract names (e.g. decision-passport golden-chain) are not
  brand surfaces and are excluded.
- Top explanation bar + second-logo geometry are asserted present.

PUBLIC_BRAND_GOLD_COUNT must stay 0.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "apps" / "web"
SCAN_ROOTS = [WEB / "app", WEB / "components", WEB / "lib", WEB / "public"]
SCAN_EXTS = {".css", ".ts", ".tsx", ".svg"}

GOLD_HEX = re.compile(r"#(?:D4AF37|FFD700|C9A227|B8860B|F5C518|f5d060)", re.IGNORECASE)
GOLD_RGBA = re.compile(r"212\s*,\s*175\s*,\s*55")
GOLD_NAME = re.compile(r"gold", re.IGNORECASE)
# The literal rule statement "no gold" documents the ban itself; it is not usage.
NO_GOLD_PHRASE = re.compile(r"no gold", re.IGNORECASE)

# Non-brand occurrences explicitly allowlisted with reason.
ALLOWLIST = {
    # Backend API contract (endpoint path), not a brand surface.
    (WEB / "lib" / "api.ts"): "decision-passport golden-chain API contract",
}


def _iter_brand_files():
    for root in SCAN_ROOTS:
        for path in sorted(root.rglob("*")):
            if path.is_file() and path.suffix in SCAN_EXTS:
                yield path


def test_no_gold_hex_in_public_brand():
    hits: list[str] = []
    for path in _iter_brand_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(text.splitlines(), 1):
            if GOLD_HEX.search(line) or GOLD_RGBA.search(line):
                hits.append(f"{path.relative_to(REPO)}:{i}:{line.strip()[:120]}")
    assert hits == [], (
        f"PUBLIC_BRAND_GOLD_COUNT={len(hits)} (expected 0):\n" + "\n".join(hits[:20])
    )


def test_no_gold_identifiers_in_public_brand():
    hits: list[str] = []
    for path in _iter_brand_files():
        if path in ALLOWLIST:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(text.splitlines(), 1):
            if GOLD_NAME.search(NO_GOLD_PHRASE.sub("", line)):
                hits.append(f"{path.relative_to(REPO)}:{i}:{line.strip()[:120]}")
    assert hits == [], (
        f"gold identifier count={len(hits)} (expected 0):\n" + "\n".join(hits[:20])
    )


def test_top_info_bar_present():
    bar = WEB / "components" / "TopInfoBar.tsx"
    assert bar.is_file(), "TopInfoBar component missing"
    text = bar.read_text(encoding="utf-8")
    assert "نظام تشغيل أعمال بالذكاء الاصطناعي للشركات في السعودية" in text
    assert "Saudi-first AI Business Operating System" in text
    assert "<marquee" not in text.lower(), "top bar must not use scrolling marquee"
    layout = (WEB / "app" / "layout.tsx").read_text(encoding="utf-8")
    assert "TopInfoBar" in layout, "root layout must render TopInfoBar on every page"


def test_second_logo_geometry_no_gold():
    logo = WEB / "public" / "dealix-logo.svg"
    assert logo.is_file(), "canonical logo missing"
    text = logo.read_text(encoding="utf-8")
    assert "M12 8h20c14 0 24 10.75 24 24S46 56 32 56H12V8Z" in text, "D-mark geometry changed"
    assert "ديليكس" in text and "Dealix" in text
    assert not GOLD_HEX.search(text), "logo contains gold hex"
    assert not GOLD_NAME.search(text), "logo references gold"
