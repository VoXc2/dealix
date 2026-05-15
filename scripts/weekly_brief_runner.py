#!/usr/bin/env python3
"""Weekly brief runner — for every active retainer customer, generate a
brief that combines:

- value_os.summarize(customer_id, period_days=7)
- friction_log.aggregate(customer_id, window_days=7)
- adoption_os.compute(customer_id, ...) [if signals available]
- proof_ledger recent events (last 7 days)

Output: a markdown file under data/weekly_briefs/{customer_id}/{YYYY-WW}.md
plus a JSON sidecar for any downstream automation.

NO external sends. Founder reviews + approves manually.

Usage:
    python scripts/weekly_brief_runner.py --customers acme,beta
    python scripts/weekly_brief_runner.py --all-active

The "active" gate reads renewal_scheduler.list_by_customer + filters
by status=CONFIRMED in the last 60 days.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _active_customers() -> list[str]:
    """Customers with a confirmed renewal in the last 60 days."""
    try:
        from auto_client_acquisition.payment_ops.renewal_scheduler import (
            RenewalStatus,
            list_by_customer,
        )
    except ImportError:
        return []
    # Without a global list, we'd need a tenant index — for now read the
    # full ledger and dedupe by customer_id.
    from auto_client_acquisition.payment_ops.renewal_scheduler import _path  # type: ignore
    p = _path()
    if not p.exists():
        return []
    customers: set[str] = set()
    cutoff = datetime.now(timezone.utc) - timedelta(days=60)
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except Exception:
            continue
        if data.get("status") != RenewalStatus.CONFIRMED.value:
            continue
        last_paid = data.get("last_paid_at", "")
        if not last_paid:
            continue
        try:
            ts = datetime.fromisoformat(last_paid)
        except Exception:
            continue
        if ts >= cutoff and data.get("customer_id"):
            customers.add(data["customer_id"])
    return sorted(customers)


def _generate_brief_for(customer_id: str) -> dict:
    from auto_client_acquisition.friction_log.aggregator import aggregate as friction_agg
    from auto_client_acquisition.value_os.value_ledger import summarize as value_summary

    value = value_summary(customer_id=customer_id, period_days=7)
    friction = friction_agg(customer_id=customer_id, window_days=7)

    # Proof events
    try:
        from auto_client_acquisition.proof_ledger.file_backend import get_default_ledger
        ledger = get_default_ledger()
        events = ledger.list_events(customer_handle=customer_id, limit=20)
        recent_events = [
            {"id": e.id, "type": str(e.event_type), "created_at": e.created_at.isoformat()}
            for e in events
        ][:10]
    except Exception:
        recent_events = []

    return {
        "customer_id": customer_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "value_summary": value,
        "friction_summary": friction.to_dict(),
        "recent_proof_events": recent_events,
        "is_estimate": True,
        "governance_decision": "allow_with_review",
    }


def _render_markdown(brief: dict) -> str:
    cid = brief["customer_id"]
    value = brief["value_summary"]
    friction = brief["friction_summary"]
    lines = [
        f"# Weekly Brief — {cid}",
        f"_Generated: {brief['generated_at']}_",
        f"_Governance: {brief['governance_decision']} — review required before send_",
        "",
        "## Value (last 7 days)",
        f"- Total events: {value.get('total_events', 0)}",
        f"- Verified amount: {value.get('verified_amount', 0):.2f}",
        f"- Observed amount: {value.get('observed_amount', 0):.2f}",
        f"- Client-confirmed amount: {value.get('client_confirmed_amount', 0):.2f}",
        f"- Estimated amount: {value.get('estimated_amount', 0):.2f}",
        "",
        "## Friction (last 7 days)",
        f"- Total: {friction.get('total', 0)}",
        f"- Top 3 kinds: {friction.get('top_3_kinds', [])}",
        f"- Cost minutes: {friction.get('total_cost_minutes', 0)}",
        "",
        "## Recent Proof Events",
    ]
    for ev in brief["recent_proof_events"]:
        lines.append(f"- [{ev['type']}] {ev['id']} at {ev['created_at']}")
    if not brief["recent_proof_events"]:
        lines.append("- (none)")
    lines.append("")
    lines.append("---")
    lines.append("_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--customers", default="")
    parser.add_argument("--all-active", action="store_true")
    parser.add_argument("--out-dir", default="data/weekly_briefs")
    args = parser.parse_args()

    if args.all_active:
        customers = _active_customers()
    elif args.customers:
        customers = [c.strip() for c in args.customers.split(",") if c.strip()]
    else:
        print("No customers selected. Use --customers or --all-active.")
        return 1

    out_dir = REPO_ROOT / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    week = datetime.now(timezone.utc).strftime("%Y-W%V")
    summary = []
    for cid in customers:
        brief = _generate_brief_for(cid)
        cust_dir = out_dir / cid
        cust_dir.mkdir(parents=True, exist_ok=True)
        (cust_dir / f"{week}.json").write_text(
            json.dumps(brief, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (cust_dir / f"{week}.md").write_text(
            _render_markdown(brief), encoding="utf-8"
        )
        summary.append({"customer_id": cid, "value_events": brief["value_summary"].get("total_events", 0)})

    print(json.dumps({"week": week, "customers_processed": len(customers), "summary": summary}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
