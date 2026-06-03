#!/usr/bin/env python3
"""Print founder comprehensive plan status (anchors, cadence, gates, GTM, PDPL, weekly)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.founder_comprehensive_plan import (  # noqa: E402
    build_comprehensive_status,
)
from dealix.commercial_ops.founder_full_autopilot import (  # noqa: E402
    build_autopilot_snapshot,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

SECTIONS = ("anchors", "cadence", "phase", "gtm", "pdpl", "weekly", "backlog", "master", "all")


def _render_ar(blob: dict) -> str:
    lines = ["# Founder Comprehensive Plan Status", ""]
    cadence = blob.get("daily_cadence") or {}
    lines.append(f"- تاريخ: `{cadence.get('date')}`")
    lines.append(
        f"- أدلة اليوم: `{cadence.get('evidence_today_total')}` "
        f"({'OK' if cadence.get('evidence_logged_today') else 'MISSING'})"
    )

    phase = blob.get("phase_0_1_gate") or {}
    lines.append(f"- بوابة 0–1: `{phase.get('verdict')}`")
    if phase.get("blockers_ar"):
        for b in phase["blockers_ar"]:
            lines.append(f"  - {b}")

    gtm = blob.get("gtm_codification") or {}
    lines.append(
        f"- ترميز GTM: `{gtm.get('verdict')}` "
        f"({gtm.get('debriefs_with_notes')}/{gtm.get('target_deals')} debriefs)"
    )

    pdpl = blob.get("pdpl_compliance_pass") or {}
    lines.append(
        f"- PDPL pass: `{pdpl.get('verdict')}` ({pdpl.get('done')}/{pdpl.get('total')})"
    )

    weekly = blob.get("weekly_one_decision") or {}
    lines.append(f"- قرار أسبوعي: `{weekly.get('verdict')}` (أسبوع `{weekly.get('week_id')}`)")

    ap = build_autopilot_snapshot()
    av = ap.get("verdict") or {}
    lines.append(f"- Full autopilot: `{av.get('level')}` — {av.get('summary_ar')}")
    stage = ap.get("customer_stage") or {}
    lines.append(f"- شريحة عملاء: `{stage.get('band')}`")

    lines.append("")
    lines.append("FOUNDER_COMPREHENSIVE_PLAN_VERDICT=OK")
    return "\n".join(lines)


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--section",
        choices=SECTIONS,
        default="all",
        help="Print one section only",
    )
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    blob = build_comprehensive_status()
    key_map = {
        "anchors": "daily_anchors",
        "cadence": "daily_cadence",
        "phase": "phase_0_1_gate",
        "gtm": "gtm_codification",
        "pdpl": "pdpl_compliance_pass",
        "weekly": "weekly_one_decision",
        "backlog": "max_ops_backlog",
        "master": "master_execution_phase",
    }
    if args.section != "all":
        out = {args.section: blob.get(key_map[args.section])}
    else:
        out = blob

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        if args.section == "all":
            print(_render_ar(blob))
        else:
            print(json.dumps(out, ensure_ascii=False, indent=2))
            print("FOUNDER_COMPREHENSIVE_PLAN_VERDICT=OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
