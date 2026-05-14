#!/usr/bin/env python3
"""Render the Dealix Group annual report.

Composes:
  - data/business_units.json           (PR10)
  - landing/assets/data/verifier-report.json  (PR1)
  - data/capital_asset_index.json      (PR3)
  - data/partner_outreach_log.json     (Wave 19 / PR3)
  - data/first_invoice_log.json        (Wave 19 / PR3)
  - data/_state/market_feedback_summary.json  (PR9, if present)
  - open-doctrine/doctrine_versions.json  (PR7)

Output: byte-stable Markdown at
  landing/assets/downloads/dealix-group-annual-report-<year>.md

Determinism: no timestamps, no `datetime.now()`, no random IDs in the
rendered document. The "as_of" line uses the year argument only.

Usage:
    python scripts/render_annual_report.py
    python scripts/render_annual_report.py --year 2026
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import date as _date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "landing" / "assets" / "downloads"


def _load_json(rel: str, default: Any) -> Any:
    p = REPO_ROOT / rel
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def _bu_summary() -> str:
    data = _load_json("data/business_units.json", {"entries": []})
    entries = data.get("entries") or []
    if not entries:
        return "_No BUs registered._\n"
    lines = ["| Slug | Name | Status | Owner | Doctrine |", "|---|---|---|---|---|"]
    for e in sorted(entries, key=lambda x: x.get("slug", "")):
        lines.append(
            f"| `{e.get('slug', '')}` "
            f"| {e.get('name', '')} "
            f"| `{e.get('status', '')}` "
            f"| {e.get('owner', '')} "
            f"| `{e.get('doctrine_version', '')}` |"
        )
    return "\n".join(lines) + "\n"


def _verifier_state() -> str:
    rpt = _load_json(
        "landing/assets/data/verifier-report.json",
        {"overall_pass": False, "ceo_complete": False, "systems": []},
    )
    systems = rpt.get("systems") or []
    passed = sum(1 for s in systems if s.get("passed"))
    overall = "PASS" if rpt.get("overall_pass") else "FAIL"
    ceo = "YES" if rpt.get("ceo_complete") else "NO"
    lines = [
        f"- Overall: **{overall}**",
        f"- CEO-complete (top 8 ≥ 4/5): **{ceo}**",
        f"- Systems passed: **{passed} / {len(systems)}**",
        "",
        "| System | Score |",
        "|---|---:|",
    ]
    for s in sorted(systems, key=lambda x: x.get("name", "")):
        lines.append(f"| {s.get('name', '')} | {s.get('score', 0)} / 5 |")
    return "\n".join(lines) + "\n"


def _market_motion() -> str:
    po = _load_json("data/partner_outreach_log.json", {})
    fi = _load_json("data/first_invoice_log.json", {})
    mf = _load_json("data/_state/market_feedback_summary.json", {})
    lines = [
        f"- Partner outreach sent (cumulative): **{int(po.get('outreach_sent_count', 0))}**",
        f"- Invoices sent (cumulative):         **{int(fi.get('invoice_sent_count', 0))}**",
    ]
    if mf:
        lines.append(f"- Market feedback (last 30 days, by signal):")
        for k in sorted((mf.get("by_signal_type") or {}).keys()):
            lines.append(f"  - {k}: {mf['by_signal_type'][k]}")
    return "\n".join(lines) + "\n"


def _capital_assets() -> str:
    data = _load_json("data/capital_asset_index.json", {"entries": []})
    entries = data.get("entries") or []
    by_type: Counter[str] = Counter()
    for e in entries:
        by_type[str(e.get("asset_type") or "")] += 1
    lines = [f"- Total capital assets registered: **{len(entries)}**"]
    if by_type:
        lines.append("- By type:")
        for k in sorted(by_type):
            lines.append(f"  - `{k}`: {by_type[k]}")
    return "\n".join(lines) + "\n"


def _doctrine_history() -> str:
    data = _load_json("open-doctrine/doctrine_versions.json", {"versions": []})
    versions = data.get("versions") or []
    if not versions:
        return "_No published versions yet._\n"
    lines = ["| Version | Date | SHA | Summary |", "|---|---|---|---|"]
    for v in versions:
        lines.append(
            f"| `{v.get('version', '')}` "
            f"| {v.get('date', '')} "
            f"| `{(v.get('commit_sha') or '')[:10]}` "
            f"| {v.get('summary', '')} |"
        )
    return "\n".join(lines) + "\n"


def _capital_allocation_decisions() -> str:
    """Decision counts derived from BU statuses (status itself is the recorded decision)."""
    data = _load_json("data/business_units.json", {"entries": []})
    entries = data.get("entries") or []
    by_status: Counter[str] = Counter()
    for e in entries:
        by_status[str(e.get("status") or "")] += 1
    if not by_status:
        return "_No BUs yet — no allocation decisions to summarize._\n"
    lines = ["- BU status distribution:"]
    for s in sorted(by_status):
        lines.append(f"  - `{s}`: {by_status[s]}")
    return "\n".join(lines) + "\n"


def render(year: int) -> str:
    sections: list[str] = []
    sections.append(f"# Dealix Group — Annual Report `{year}`")
    sections.append("")
    sections.append(f"_Year: {year}. This report is auto-rendered from "
                    "machine-readable state. Re-generate with "
                    "`python scripts/render_annual_report.py`._")
    sections.append("")

    sections.append("## 1. Overview")
    sections.append("")
    sections.append("Dealix Group operates under four principles: **Cash now. "
                    "Proof always. Governance by default. Productize repetition.**")
    sections.append("")
    sections.append("## 2. Business Unit Summary")
    sections.append("")
    sections.append(_bu_summary())

    sections.append("## 3. Capital Allocation Actions")
    sections.append("")
    sections.append(_capital_allocation_decisions())

    sections.append("## 4. Verifier State")
    sections.append("")
    sections.append(_verifier_state())

    sections.append("## 5. Market Motion")
    sections.append("")
    sections.append(_market_motion())

    sections.append("## 6. Capital Assets")
    sections.append("")
    sections.append(_capital_assets())

    sections.append("## 7. Doctrine Discipline")
    sections.append("")
    sections.append("**Published doctrine versions:**")
    sections.append("")
    sections.append(_doctrine_history())

    sections.append("## 8. Risks (qualitative)")
    sections.append("")
    sections.append("_See `docs/holding/GROUP_RISK_REGISTER.md` "
                    "(rendered after PR15)._")
    sections.append("")

    sections.append("## 9. Next Year Theses")
    sections.append("")
    sections.append("_Forward-looking statements — see board memos in "
                    "`data/_state/bu_memos/` (added in PR14)._")
    sections.append("")

    sections.append("## 10. Certifications")
    sections.append("")
    sections.append("- Doctrine adoption: group-level adopted at `v1.0.0`.")
    sections.append("- Partner Kit: published at `landing/assets/downloads/dealix-partner-kit-v1.zip`.")
    sections.append("- Internal audit: see `docs/holding/INTERNAL_AUDIT.md` "
                    "(rendered after PR15).")
    sections.append("")
    sections.append("---")
    sections.append("_Produced by `scripts/render_annual_report.py`. "
                    "Byte-stable for the CI drift gate._")
    return "\n".join(sections) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="render dealix group annual report")
    parser.add_argument("--year", type=int, default=_date.today().year)
    args = parser.parse_args(argv)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"dealix-group-annual-report-{args.year}.md"
    out_path.write_text(render(args.year), encoding="utf-8")
    try:
        display = out_path.relative_to(REPO_ROOT)
    except ValueError:
        display = out_path
    print(f"wrote {display}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
