"""Generate the Dealix demo pack (concatenates the demo scripts + QA).

Usage:
    python3 scripts/generate_demo_pack.py --lang both
"""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "business" / "demo" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", choices=["ar", "en", "both"], default="both")
    args = parser.parse_args()

    today = dt.date.today().isoformat()
    lines: list[str] = []
    lines.append(f"# Dealix Demo Pack — {today}\n")
    if args.lang in ("ar", "both"):
        ar = (REPO_ROOT / "business" / "demo" / "DEALIX_DEMO_SCRIPT_AR.md").read_text(encoding="utf-8")
        lines.append(ar + "\n")
    if args.lang in ("en", "both"):
        en = (REPO_ROOT / "business" / "demo" / "DEALIX_DEMO_SCRIPT_EN.md").read_text(encoding="utf-8")
        lines.append(en + "\n")

    lines.append("\n## QA Objections\n")
    lines.append("- We already have a CRM → Dealix is the layer, not the CRM\n")
    lines.append("- We tried AI before, it felt generic → every output has source + review gate\n")
    lines.append("- Our team is small → first 14 days are intake + map, not platform switch\n")
    lines.append("- Can you guarantee ROI? → no, but we show workflow + cadence + proof\n")
    lines.append("- We need to talk to the team → I send a one-pager + 20-min agenda\n")

    lines.append("\n## Close\n")
    lines.append("- Never pressure\n")
    lines.append("- Always offer the 20-min diagnostic as the next step\n")
    lines.append("- Always send the proposal within 48h if requested\n")
    lines.append("- Always log notes in CRM after the call\n")

    out = EXPORT_DIR / f"dealix-demo-pack-{today}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
