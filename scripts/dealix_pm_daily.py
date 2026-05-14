#!/usr/bin/env python3
"""Dealix PM Daily Brief — single command that summarizes the day.

What it prints:
  1. Leads waiting > 24h
  2. Friction summary (last 7d)
  3. Renewals due (next 7d)
  4. Pending approvals
  5. Recent proof events
  6. Capital assets registered this week
  7. Top 3 recommended next actions

Usage:
    python scripts/dealix_pm_daily.py
    python scripts/dealix_pm_daily.py --json
    python scripts/dealix_pm_daily.py --customer acme

NO external sends. Founder reads + acts.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _leads_waiting() -> dict:
    try:
        from auto_client_acquisition import lead_inbox
        records = lead_inbox.list_records(limit=200) if hasattr(lead_inbox, "list_records") else []
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        items: list[dict] = []
        for r in records:
            try:
                created = datetime.fromisoformat(getattr(r, "created_at", "") or "")
                if created.tzinfo is None:
                    created = created.replace(tzinfo=timezone.utc)
            except Exception:
                continue
            if created < cutoff:
                items.append({
                    "id": getattr(r, "id", ""),
                    "company": getattr(r, "company", ""),
                    "sector": getattr(r, "sector", ""),
                    "created_at": created.isoformat(),
                })
        return {"count": len(items), "items": items[:5]}
    except Exception:
        return {"count": 0, "items": []}


def _friction_last_7d(customer_id: str) -> dict:
    try:
        from auto_client_acquisition.friction_log.aggregator import aggregate
        return aggregate(customer_id=customer_id, window_days=7).to_dict()
    except Exception:
        return {"total": 0}


def _renewals_due() -> dict:
    try:
        from auto_client_acquisition.payment_ops.renewal_scheduler import list_due
        due = list_due()
        return {
            "count": len(due),
            "items": [
                {"customer_id": s.customer_id, "plan": s.plan, "amount_sar": s.amount_sar,
                 "cycle": s.cycle_count}
                for s in due[:10]
            ],
        }
    except Exception:
        return {"count": 0, "items": []}


def _recent_proof_events() -> dict:
    try:
        from auto_client_acquisition.proof_ledger.file_backend import get_default_ledger
        ledger = get_default_ledger()
        events = ledger.list_events(limit=10)
        return {
            "count": len(events),
            "items": [
                {"event_type": str(e.event_type), "customer_handle": e.customer_handle,
                 "created_at": e.created_at.isoformat()}
                for e in events[:5]
            ],
        }
    except Exception:
        return {"count": 0, "items": []}


def _capital_this_week() -> dict:
    try:
        from auto_client_acquisition.capital_os.capital_ledger import list_assets
        assets = list_assets(limit=100)
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
        return {"count": len(recent), "items": recent[:5]}
    except Exception:
        return {"count": 0, "items": []}


def _top_recommendations(brief: dict) -> list[str]:
    recs: list[str] = []
    if brief["leads_waiting_24h_plus"]["count"] > 0:
        recs.append(
            f"Reply to {brief['leads_waiting_24h_plus']['count']} lead(s) waiting > 24h."
        )
    if brief["renewals_due_next_7d"]["count"] > 0:
        recs.append(
            f"Confirm {brief['renewals_due_next_7d']['count']} retainer renewal(s) this week."
        )
    if brief["friction_last_7d"].get("total", 0) >= 5:
        recs.append(
            f"Friction is elevated ({brief['friction_last_7d']['total']} events) "
            "— review top 3 kinds for productization opportunities."
        )
    if brief["capital_assets_this_week"]["count"] == 0:
        recs.append(
            "No capital asset registered this week — every engagement must "
            "produce >= 1 reusable asset (capital_os.add_asset)."
        )
    if not recs:
        recs.append("Quiet day. Publish 1 LinkedIn post and reach out to 2 warm contacts.")
    return recs[:3]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--customer", default="dealix_internal")
    args = parser.parse_args()

    brief = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "leads_waiting_24h_plus": _leads_waiting(),
        "friction_last_7d": _friction_last_7d(args.customer),
        "renewals_due_next_7d": _renewals_due(),
        "recent_proof_events": _recent_proof_events(),
        "capital_assets_this_week": _capital_this_week(),
    }
    brief["top_recommendations"] = _top_recommendations(brief)

    # Wave 16: always emit data/daily_brief/YYYY-MM-DD.md alongside other
    # output forms. The founder reads this file on their phone every
    # morning — 4 atomic sections, mobile-readable.
    _emit_daily_brief_markdown(brief)

    if args.json:
        print(json.dumps(brief, ensure_ascii=False, indent=2))
        return 0

    # Human-readable
    print(f"━━ Dealix PM Daily — {brief['generated_at']} ━━\n")
    print(f"Leads waiting > 24h: {brief['leads_waiting_24h_plus']['count']}")
    for item in brief["leads_waiting_24h_plus"]["items"]:
        print(f"  • {item['company']} ({item['sector']}) — {item['created_at']}")
    print()
    print(f"Friction last 7d: {brief['friction_last_7d'].get('total', 0)} events")
    print(f"Renewals due next 7d: {brief['renewals_due_next_7d']['count']}")
    print(f"Recent proof events: {brief['recent_proof_events']['count']}")
    print(f"Capital assets this week: {brief['capital_assets_this_week']['count']}")
    print()
    print("Top 3 recommendations:")
    for i, r in enumerate(brief["top_recommendations"], start=1):
        print(f"  {i}. {r}")
    return 0


def _emit_daily_brief_markdown(brief: dict) -> None:
    """Wave 16: write data/daily_brief/YYYY-MM-DD.md the founder reads on
    their phone each morning. 4 atomic sections.
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = REPO_ROOT / "data" / "daily_brief"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{today}.md"

    lines: list[str] = []
    lines.append(f"# Dealix Daily Brief — {today}")
    lines.append("")
    lines.append(
        f"_Generated {brief['generated_at']}._ "
        f"Read on phone every morning. Follow the 4 sections in order."
    )
    lines.append("")

    # Section 1 — Today's 5 messages to send (from warm_list_drafts if exists)
    lines.append("## 1. Today's 5 messages · رسائل اليوم")
    lines.append("")
    drafts_path = REPO_ROOT / "data" / "outreach" / "warm_list_drafts.md"
    if drafts_path.exists():
        lines.append(
            f"- See `data/outreach/warm_list_drafts.md` — pick the next 5 contacts "
            f"flagged `accept` or `diagnostic_only`. Send via LinkedIn or WhatsApp. "
            f"Mark `Sent: [x]` per row."
        )
    else:
        lines.append(
            "- ⚠ `data/warm_list.csv` not filled yet. Fill it then run "
            "`python scripts/warm_list_outreach.py` to generate today's drafts."
        )
    lines.append("")

    # Section 2 — Leads needing reply within 24h
    leads_waiting = brief.get("leads_waiting_24h_plus", {})
    lines.append(f"## 2. Leads to reply · ردود مطلوبة ({leads_waiting.get('count', 0)})")
    lines.append("")
    items = leads_waiting.get("items") or []
    if items:
        for item in items[:5]:
            lines.append(
                f"- **{item.get('company', '?')}** ({item.get('sector', '?')}) — "
                f"{item.get('created_at', '?')[:10]} — reply via "
                f"`/founder-leads.html?key=<admin>`"
            )
    else:
        lines.append("- 0 leads waiting > 24h. Continue outbound cadence.")
    lines.append("")

    # Section 3 — Diagnostic to deliver
    lines.append("## 3. Diagnostic to deliver · تشخيص للتسليم")
    lines.append("")
    if items:
        first = items[0]
        lines.append(
            f"- Top priority: **{first.get('company', '?')}** — open "
            f"`/founder-leads.html?key=<admin>` → triage → approve diagnostic → "
            f"send via Gmail. Target: < 24h from intake."
        )
    else:
        lines.append("- No diagnostics in queue. Use the time for content + warm-list send.")
    lines.append("")

    # Section 4 — Capital review
    capital = brief.get("capital_assets_this_week", {})
    lines.append(f"## 4. Capital review · مراجعة الأصول ({capital.get('count', 0)} this week)")
    lines.append("")
    if capital.get("items"):
        for asset in capital["items"][:5]:
            lines.append(
                f"- `{asset.get('asset_type', '?')}` (owner: {asset.get('owner', '?')})"
            )
    else:
        lines.append(
            "- ⚠ 0 capital assets this week. EVERY engagement must produce ≥ 1 "
            "reusable asset (`capital_os.add_asset`)."
        )
    lines.append("")

    # Top recommendations footer
    recs = brief.get("top_recommendations") or []
    if recs:
        lines.append("## Top 3 recommendations · أهم 3 إجراءات")
        lines.append("")
        for i, rec in enumerate(recs, start=1):
            lines.append(f"{i}. {rec}")
        lines.append("")

    # Friction high-severity alert
    friction = brief.get("friction_last_7d", {})
    if friction.get("by_severity", {}).get("high", 0) > 0:
        lines.append(
            f"## ⚠ ALERT — {friction['by_severity']['high']} high-severity friction events (7d)"
        )
        lines.append("")
        lines.append(
            "- Review `friction-log/` and resolve before continuing outbound."
        )
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "_Estimated outcomes are not guaranteed outcomes / "
        "النتائج التقديرية ليست نتائج مضمونة._"
    )

    out_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
