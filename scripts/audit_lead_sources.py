"""Audit lead sources — produce a report from sources.registry.json.

Usage:
    python3 scripts/audit_lead_sources.py
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTRY = REPO_ROOT / "business" / "_data" / "sources.registry.json"
OUT_DIR = REPO_ROOT / "reports" / "sources"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    if not REGISTRY.exists():
        print(f"missing: {REGISTRY}")
        return 1
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    today = dt.date.today().isoformat()
    sources = data.get("sources", [])

    lines: list[str] = []
    lines.append(f"# Source Audit — {today}")
    lines.append("")
    lines.append(f"Total sources registered: {len(sources)}")
    lines.append("")
    by_risk: dict[str, int] = {}
    by_review: dict[str, int] = {}
    for s in sources:
        by_risk[s["risk_level"]] = by_risk.get(s["risk_level"], 0) + 1
        key = "review" if s["terms_review_required"] else "no-review"
        by_review[key] = by_review.get(key, 0) + 1
    lines.append("## By risk")
    for k, v in by_risk.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## By review status")
    for k, v in by_review.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Per-source summary")
    for s in sources:
        lines.append(f"### {s['source_name']}")
        lines.append(f"- type: {s['source_type']}")
        lines.append(f"- risk: {s['risk_level']}")
        lines.append(f"- review: {'required' if s['terms_review_required'] else 'not required'}")
        lines.append(f"- allowed: {s['allowed_use']}")
        if s.get("notes"):
            lines.append(f"- notes: {s['notes']}")
        lines.append("")

    out = OUT_DIR / f"source-audit-{today}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
