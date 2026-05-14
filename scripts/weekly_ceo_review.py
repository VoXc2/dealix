#!/usr/bin/env python3
"""Weekly CEO Review — Wave 18.

Sunday morning composer. Aggregates the week's signals into a single
markdown the founder reads with their first coffee and uses to plan the
upcoming week:

  - Capital Assets registered (last 7 days)
  - Friction events by severity (last 7 days)
  - Renewals confirmed / skipped / due
  - Anchor partner pipeline state (queued / called / LOI / signed)
  - 90-day cadence position (Day-N / N-of-90 / current phase target)
  - Doctrine drift check (any test_no_*.py file missing?)
  - SAR committed in renewal pipeline (toward 100K Day-90 gate)
  - Top 3 strategic decisions for the upcoming week

Output: `data/weekly_ceo_review/YYYY-WW.md` (ISO week).

Idempotent — re-running overwrites the same file. NEVER sends external
messages. Pure composition over existing modules. Honors the 11
non-negotiables (especially #8 no_external_action_without_approval).

Usage:
    python scripts/weekly_ceo_review.py
    python scripts/weekly_ceo_review.py --json
    python scripts/weekly_ceo_review.py --week 2026-W20
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _iso_week(d: datetime | None = None) -> str:
    d = d or datetime.now(timezone.utc)
    iso_year, iso_week, _ = d.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"


def _capital_assets_7d() -> dict:
    try:
        from auto_client_acquisition.capital_os.capital_ledger import list_assets
        assets = list_assets(limit=200)
        cutoff = datetime.now(timezone.utc) - timedelta(days=7)
        recent = []
        for a in assets:
            try:
                created = datetime.fromisoformat(a.created_at)
                if created.tzinfo is None:
                    created = created.replace(tzinfo=timezone.utc)
            except Exception:
                continue
            if created >= cutoff:
                recent.append({"asset_type": a.asset_type, "owner": a.owner})
        return {"count": len(recent), "items": recent[:10]}
    except Exception:
        return {"count": 0, "items": []}


def _friction_7d() -> dict:
    try:
        from auto_client_acquisition.friction_log.aggregator import aggregate
        agg = aggregate(customer_id="dealix_internal", window_days=7)
        return agg.to_dict()
    except Exception:
        return {"total": 0, "by_severity": {}}


def _renewals_state() -> dict:
    try:
        from auto_client_acquisition.payment_ops.renewal_scheduler import list_due
        cutoff_7 = datetime.now(timezone.utc) + timedelta(days=7)
        cutoff_90 = datetime.now(timezone.utc) + timedelta(days=90)
        due_7 = list_due(on_date=cutoff_7)
        due_90 = list_due(on_date=cutoff_90)
        sar_7 = sum(int(getattr(r, "amount_sar", 0)) for r in due_7)
        sar_90 = sum(int(getattr(r, "amount_sar", 0)) for r in due_90)
        return {
            "due_next_7d_count": len(due_7),
            "due_next_7d_sar": sar_7,
            "due_next_90d_count": len(due_90),
            "due_next_90d_sar": sar_90,
        }
    except Exception:
        return {
            "due_next_7d_count": 0, "due_next_7d_sar": 0,
            "due_next_90d_count": 0, "due_next_90d_sar": 0,
        }


def _anchor_partner_state() -> dict:
    p = REPO_ROOT / "data" / "anchor_partner_pipeline.json"
    if not p.exists():
        return {"seeded": False, "partner_count": 0, "by_status": {}}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {"seeded": False, "partner_count": 0, "by_status": {}}
    partners = data.get("partners", [])
    by_status: dict[str, int] = {}
    for pn in partners:
        s = pn.get("status", "unknown")
        by_status[s] = by_status.get(s, 0) + 1
    return {
        "seeded": True,
        "partner_count": len(partners),
        "by_status": by_status,
    }


def _doctrine_drift_check() -> dict:
    """Verify every commitment's enforced_by path still exists on disk."""
    try:
        from auto_client_acquisition.governance_os.non_negotiables import (
            NON_NEGOTIABLES,
        )
    except Exception:
        return {"all_enforcers_exist": False, "missing": [], "error": "import failed"}
    missing: list[str] = []
    for n in NON_NEGOTIABLES:
        for rel in n.enforced_by:
            if not (REPO_ROOT / rel).exists():
                missing.append(f"{n.id}::{rel}")
    return {
        "commitments_count": len(NON_NEGOTIABLES),
        "missing": missing,
        "all_enforcers_exist": not missing,
    }


def _ninety_day_position() -> dict:
    """Best-effort: 90-day cadence is tracked in docs/ops/FOUNDER_90_DAY_CADENCE.md.
    We don't have a registered "campaign start date" yet; we estimate from
    the first commit on the active branch.
    """
    # Use file-system mtime of the cadence doc as a stable anchor.
    p = REPO_ROOT / "docs" / "ops" / "FOUNDER_90_DAY_CADENCE.md"
    if not p.exists():
        return {"day_of_90": 0, "phase": "pre-launch"}
    start = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).date()
    today = datetime.now(timezone.utc).date()
    day = (today - start).days + 1
    if day < 1:
        phase = "pre-launch"
    elif day <= 30:
        phase = "Days 1-30: Diagnostic engine"
    elif day <= 60:
        phase = "Days 31-60: Retainer scaling"
    elif day <= 90:
        phase = "Days 61-90: Flagship + partner activation"
    else:
        phase = "Day 90+: review gate"
    return {
        "day_of_90": day,
        "phase": phase,
        "anchor_doc": "docs/ops/FOUNDER_90_DAY_CADENCE.md",
    }


def _top_three_decisions(state: dict) -> list[str]:
    decisions: list[str] = []
    arr = state["renewals"]
    target_90 = 100_000
    if arr["due_next_90d_sar"] < target_90:
        gap = target_90 - arr["due_next_90d_sar"]
        decisions.append(
            f"Close enough deals next week to compress the {gap:,} SAR ARR gap to "
            f"Day-90 target. Priority: 1 Retainer (3-mo × 4,999) or 1 Flagship Sprint (25,000)."
        )
    ap = state["anchor_partners"]
    queued = ap.get("by_status", {}).get("queued_for_founder_call", 0)
    if queued > 0:
        decisions.append(
            f"Book {queued} anchor partner call(s) — pick one named company per archetype "
            "from `data/anchor_partner_pipeline.json` and send the bilingual draft."
        )
    cap = state["capital_assets"]
    if cap["count"] == 0:
        decisions.append(
            "Zero Capital Assets registered this week. Either we shipped no engagement "
            "(focus on closing one) or we shipped one without registering — fix via "
            "`capital_os.add_asset`. Non-negotiable #11."
        )
    fric = state["friction"]
    high = fric.get("by_severity", {}).get("high", 0)
    if high > 0:
        decisions.append(
            f"Resolve {high} high-severity friction event(s) before continuing outbound. "
            "Friction is the highest-leverage productization signal we have."
        )
    while len(decisions) < 3:
        decisions.append(
            "Read `docs/sales-kit/PRICING_REFRAME_2026Q2.md` objection-handling block "
            "and rehearse one objection out loud."
        )
    return decisions[:3]


def _emit_markdown(week: str, state: dict, decisions: list[str]) -> Path:
    out_dir = REPO_ROOT / "data" / "weekly_ceo_review"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{week}.md"

    cap = state["capital_assets"]
    fric = state["friction"]
    ren = state["renewals"]
    ap = state["anchor_partners"]
    doc = state["doctrine"]
    pos = state["cadence"]

    lines: list[str] = []
    lines.append(f"# Dealix Weekly CEO Review — {week}")
    lines.append("")
    lines.append(
        f"_Generated {datetime.now(timezone.utc).isoformat()}._ "
        "Read with Sunday coffee. Decide three things. Move."
    )
    lines.append("")

    # 1. 90-day position
    lines.append("## 1. Where we are in the 90-day plan · أين نحن في خطة الـ ٩٠ يومًا")
    lines.append("")
    lines.append(f"- **Day:** {pos['day_of_90']} of 90")
    lines.append(f"- **Phase:** {pos['phase']}")
    lines.append(f"- **Reference:** `{pos['anchor_doc']}`")
    lines.append("")

    # 2. Commercial pacing
    lines.append("## 2. Commercial pacing · إيقاع تجاري")
    lines.append("")
    lines.append(f"- **Renewals due next 7d:** {ren['due_next_7d_count']} retainer(s) — **{ren['due_next_7d_sar']:,} SAR**")
    lines.append(f"- **Renewals due next 90d:** {ren['due_next_90d_count']} retainer(s) — **{ren['due_next_90d_sar']:,} SAR committed**")
    target = 100_000
    pct = round((ren['due_next_90d_sar'] / target) * 100, 1) if target > 0 else 0.0
    lines.append(f"- **Day-90 target (100K SAR ARR committed):** {pct}% of target")
    lines.append("")

    # 3. Anchor partners
    lines.append("## 3. Anchor partner pipeline · خط الشركاء")
    lines.append("")
    if ap["seeded"]:
        lines.append(f"- **Seeded archetypes:** {ap['partner_count']}")
        for status, count in ap["by_status"].items():
            lines.append(f"  - `{status}`: {count}")
        lines.append("- **Action:** open `data/anchor_partner_pipeline.json` + book one named company per archetype.")
    else:
        lines.append("- ⚠ Anchor partner pipeline NOT seeded. Run `python scripts/seed_anchor_partner_pipeline.py`.")
    lines.append("")

    # 4. Capital + friction
    lines.append("## 4. Capital + friction (last 7d) · الأصول والاحتكاك")
    lines.append("")
    lines.append(f"- **Capital Assets registered:** {cap['count']}")
    if cap["items"]:
        for it in cap["items"][:5]:
            lines.append(f"  - `{it.get('asset_type', '?')}` (owner: `{it.get('owner', '?')}`)")
    else:
        lines.append("  - ⚠ Zero. Non-negotiable #11: every engagement must produce ≥ 1 reusable asset.")
    lines.append("")
    lines.append(f"- **Friction events:** {fric.get('total', 0)} total")
    by_sev = fric.get("by_severity", {})
    if by_sev:
        for sev in ("high", "medium", "low"):
            if by_sev.get(sev, 0) > 0:
                lines.append(f"  - `{sev}`: {by_sev[sev]}")
    lines.append("")

    # 5. Doctrine drift
    lines.append("## 5. Doctrine health · صحّة الالتزامات")
    lines.append("")
    if doc.get("all_enforcers_exist"):
        lines.append(f"- ✅ All {doc.get('commitments_count', 11)} non-negotiables have a live enforcer file on disk.")
    else:
        lines.append(f"- ⚠ Drift detected: {len(doc.get('missing', []))} enforcer file(s) missing:")
        for m in doc.get("missing", [])[:5]:
            lines.append(f"  - `{m}`")
    lines.append("")

    # 6. Top 3 decisions
    lines.append("## Top 3 decisions for next week · أهم 3 قرارات للأسبوع القادم")
    lines.append("")
    for i, d in enumerate(decisions, start=1):
        lines.append(f"{i}. {d}")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "_Estimated outcomes are not guaranteed outcomes / "
        "النتائج التقديرية ليست نتائج مضمونة._"
    )

    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--week", default=None, help="ISO week tag like 2026-W20 (default: current week)")
    args = parser.parse_args()

    week = args.week or _iso_week()

    state = {
        "week": week,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "capital_assets": _capital_assets_7d(),
        "friction": _friction_7d(),
        "renewals": _renewals_state(),
        "anchor_partners": _anchor_partner_state(),
        "doctrine": _doctrine_drift_check(),
        "cadence": _ninety_day_position(),
    }
    decisions = _top_three_decisions(state)
    state["top_three_decisions"] = decisions

    out_path = _emit_markdown(week, state, decisions)

    if args.json:
        print(json.dumps({**state, "output_path": str(out_path.relative_to(REPO_ROOT))},
                         ensure_ascii=False, indent=2))
        return 0

    print(f"━━ Dealix Weekly CEO Review — {week} ━━\n")
    print(f"Day {state['cadence']['day_of_90']} of 90 · {state['cadence']['phase']}")
    print(f"Renewals: {state['renewals']['due_next_90d_count']} due in 90d "
          f"({state['renewals']['due_next_90d_sar']:,} SAR committed)")
    print(f"Anchor partners: {state['anchor_partners'].get('partner_count', 0)} seeded")
    print(f"Capital assets this week: {state['capital_assets']['count']}")
    print(f"Friction events this week: {state['friction'].get('total', 0)}")
    print(f"Doctrine drift: {'none' if state['doctrine'].get('all_enforcers_exist') else 'YES — review'}")
    print()
    print("Top 3 decisions:")
    for i, d in enumerate(decisions, start=1):
        print(f"  {i}. {d}")
    print()
    print(f"✓ Wrote review to {out_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
