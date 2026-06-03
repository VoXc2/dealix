#!/usr/bin/env python3
"""Weekly CEO retro — CEO status + phase gate + GTM blitz + production layers."""

from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.ceo_master_plan import build_ceo_master_plan_snapshot  # noqa: E402
from dealix.commercial_ops.founder_comprehensive_plan import analyze_phase_0_1_gate  # noqa: E402
from dealix.commercial_ops.gtm_blitz_tracker import build_gtm_blitz_snapshot  # noqa: E402

OUT_DIR = ROOT / "data/founder_briefs"


def _week_label() -> str:
    return datetime.now(UTC).strftime("%Y-W%V")


def build_retro_markdown() -> str:
    week = _week_label()
    ceo = build_ceo_master_plan_snapshot()
    gate = analyze_phase_0_1_gate()
    gtm = build_gtm_blitz_snapshot()
    prod = (ceo.get("p0_production_trust") or {}).get("production") or {}
    decision = ((ceo.get("p0_ceo_decision") or {}).get("decision") or {})

    lines = [
        f"# CEO Weekly Retro — {week}",
        "",
        f"**Generated:** {datetime.now(UTC).isoformat()}",
        "",
        "## Overall",
        f"- CEO Master Plan: **{ceo.get('overall_verdict')}**",
        f"- Phase 0–1 gate: **{gate.get('verdict')}**",
        f"- GTM blitz: **{gtm.get('verdict')}** ({gtm.get('pct')}%)",
        f"- Production layers: **{prod.get('overall_pct', 'n/a')}%** ({prod.get('verdict', '—')})",
        "",
        "## One decision",
        f"- {decision.get('one_decision_ar') or '—'}",
        f"- Success by Friday: {decision.get('success_by_friday_ar') or '—'}",
        "",
        "## Workstreams",
    ]
    for key in (
        "p0_revenue_close",
        "p0_production_trust",
        "p0_ceo_decision",
        "p0_gtm_blitz",
        "p1_trust_pack",
        "p2_repeatability",
    ):
        ws = ceo.get(key) or {}
        lines.append(f"- {key}: {ws.get('verdict')}")

    blockers = gate.get("blockers_ar") or []
    if blockers:
        lines.extend(["", "## Blockers (Phase 0–1)", ""])
        lines.extend(f"- {b}" for b in blockers[:8])

    hint = (ceo.get("p2_repeatability") or {}).get("phase_2_hint_ar")
    if hint:
        lines.extend(["", "## Phase 2 hint", "", hint])

    lines.extend(
        [
            "",
            "## Next week",
            "- [ ] Update founder_weekly_one_decision.yaml (one decision only)",
            "- [ ] Log evidence + GTM conversations",
            "- [ ] Run founder_weekly_loop.ps1",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--stdout", action="store_true", help="Print to stdout only")
    args = p.parse_args()

    text = build_retro_markdown()
    week = _week_label()
    if args.stdout:
        print(text)
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"ceo_retro_{week}.md"
    out.write_text(text, encoding="utf-8")
    print(f"WROTE {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
