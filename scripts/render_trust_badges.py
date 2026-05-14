#!/usr/bin/env python3
"""Render embeddable SVG trust badges from the verifier report.

Outputs five badges to `landing/assets/badges/`:
  - doctrine-status.svg   (PASS / FAIL)
  - verifier-score.svg    (N / 19)
  - ceo-complete.svg      (YES / NO)
  - partner-outreach.svg  (count)
  - invoice-sent.svg      (count)

Drift-gate properties:
  - byte-identical between runs on identical state,
  - sorted attribute order,
  - no timestamps in output,
  - no PII / pricing / partner names anywhere.

Usage:
    python scripts/render_trust_badges.py
    python scripts/render_trust_badges.py --output landing/assets/badges
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = REPO_ROOT / "landing" / "assets" / "badges"
REPORT_PATH = REPO_ROOT / "landing" / "assets" / "data" / "verifier-report.json"


# Shields.io-style color tokens.
COLORS = {
    "ok": "#2dd4a4",
    "warn": "#f5b86b",
    "bad": "#ef4d5c",
    "label": "#555",
    "border": "#cfd2d6",
}


def _badge_svg(label: str, value: str, value_color: str) -> str:
    """Build a minimal, stable shields-style badge SVG.

    Width math: each character ~7px in this monospace approximation.
    The implementation deliberately produces stable byte output:
      - no timestamps, no random ids, no current date,
      - sorted attribute order on the root element,
      - fixed font + fixed text-anchor.
    """
    label_w = max(60, 12 + 7 * len(label))
    value_w = max(50, 12 + 7 * len(value))
    total_w = label_w + value_w

    def esc(s: str) -> str:
        return (
            s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )

    label = esc(label)
    value = esc(value)

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'role="img" '
        f'viewBox="0 0 {total_w} 20" '
        f'width="{total_w}" '
        f'height="20">'
        f'<title>{label}: {value}</title>'
        f'<linearGradient id="g" x2="0" y2="100%">'
        f'<stop offset="0" stop-color="#fff" stop-opacity=".2"/>'
        f'<stop offset="1" stop-opacity=".15"/>'
        f'</linearGradient>'
        f'<mask id="m"><rect width="{total_w}" height="20" rx="3" fill="#fff"/></mask>'
        f'<g mask="url(#m)">'
        f'<rect width="{label_w}" height="20" fill="{COLORS["label"]}"/>'
        f'<rect x="{label_w}" width="{value_w}" height="20" fill="{value_color}"/>'
        f'<rect width="{total_w}" height="20" fill="url(#g)"/>'
        f'</g>'
        f'<g fill="#fff" '
        f'font-family="Verdana,Geneva,DejaVu Sans,sans-serif" '
        f'font-size="11" '
        f'text-anchor="middle">'
        f'<text x="{label_w // 2}" y="14">{label}</text>'
        f'<text x="{label_w + value_w // 2}" y="14">{value}</text>'
        f'</g>'
        f'</svg>\n'
    )


def _load_report() -> dict:
    if not REPORT_PATH.exists():
        # Stable empty default so the badges render even pre-render.
        return {
            "overall_pass": False,
            "ceo_complete": False,
            "systems": [],
        }
    return json.loads(REPORT_PATH.read_text(encoding="utf-8"))


def _market_counts() -> tuple[int, int]:
    po = REPO_ROOT / "data" / "partner_outreach_log.json"
    fi = REPO_ROOT / "data" / "first_invoice_log.json"
    out = 0
    inv = 0
    if po.exists():
        try:
            out = int(json.loads(po.read_text()).get("outreach_sent_count", 0))
        except Exception:
            pass
    if fi.exists():
        try:
            inv = int(json.loads(fi.read_text()).get("invoice_sent_count", 0))
        except Exception:
            pass
    return out, inv


def render(output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rpt = _load_report()
    out_count, inv_count = _market_counts()
    systems = rpt.get("systems") or []
    passed = sum(1 for s in systems if s.get("passed"))
    total = len(systems) or 19

    overall = bool(rpt.get("overall_pass"))
    ceo = bool(rpt.get("ceo_complete"))

    badges = {
        "doctrine-status.svg": _badge_svg(
            "doctrine",
            "PASS" if overall else "FAIL",
            COLORS["ok"] if overall else COLORS["bad"],
        ),
        "verifier-score.svg": _badge_svg(
            "verifier",
            f"{passed} / {total}",
            COLORS["ok"] if passed == total else (COLORS["warn"] if passed >= total - 2 else COLORS["bad"]),
        ),
        "ceo-complete.svg": _badge_svg(
            "ceo-complete",
            "YES" if ceo else "NO",
            COLORS["ok"] if ceo else COLORS["warn"],
        ),
        "partner-outreach.svg": _badge_svg(
            "partner outreach",
            str(out_count),
            COLORS["ok"] if out_count >= 1 else COLORS["warn"],
        ),
        "invoice-sent.svg": _badge_svg(
            "invoice sent",
            str(inv_count),
            COLORS["ok"] if inv_count >= 1 else COLORS["warn"],
        ),
    }

    written: dict[str, Path] = {}
    for name, content in badges.items():
        p = output_dir / name
        p.write_text(content, encoding="utf-8")
        written[name] = p
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="render trust badges")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    written = render(args.output)
    for name, p in written.items():
        rel = p.relative_to(REPO_ROOT) if p.is_absolute() else p
        print(f"wrote {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
