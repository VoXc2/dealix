#!/usr/bin/env python3
"""Pilot 499 SAR close pack — markdown only, dry-run by default (no live charge)."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "docs" / "revenue" / "live"


def build_markdown() -> str:
    return "\n".join(
        [
            "# Dealix — 7-Day Growth Proof Sprint (499 SAR)",
            "",
            f"_Generated (UTC): {datetime.now(UTC).isoformat()}_",
            "",
            "## Included",
            "- Mini diagnostic refinement",
            "- 7-day growth proof plan (draft)",
            "- Up to 10 safe improvement ideas (no guaranteed lead volume)",
            "- Arabic/English message drafts (approval_required before send)",
            "- Follow-up checklist",
            "- Internal proof pack template",
            "",
            "## Not included",
            "- Guaranteed revenue or ROI",
            "- Cold WhatsApp or scraping",
            "- LinkedIn automation",
            "- Live Moyasar charge (manual invoice until explicitly approved)",
            "",
            "## Founder approval",
            "- [ ] Customer consent on record",
            "- [ ] Scope agreed in writing",
            "- [ ] Payment or written commitment captured outside repo",
            "",
        ]
    )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--write", action="store_true", help=f"write to {OUT_DIR}/pilot_499_close_pack.md")
    args = p.parse_args()
    md = build_markdown()
    if not args.write:
        print(md)
        return 0
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / "pilot_499_close_pack.md"
    path.write_text(md, encoding="utf-8")
    print(f"OK: wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
