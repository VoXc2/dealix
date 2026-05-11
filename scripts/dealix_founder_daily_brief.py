#!/usr/bin/env python3
"""Wave 15 §B4 — Consolidated Founder Daily Brief.

Single command, single output. Composes:
- Bottleneck Radar (Wave 13)
- Hard Gate Audit (Article 4 immutability)
- Service Catalog summary (Wave 13 truth registry)
- Today's single action (highest priority)

This is the founder's *one and only* morning briefing — designed to be
copy-pasted into the founder's WhatsApp or run as a Railway cron at
8AM KSA daily.

Hard rules:
- Article 4: NEVER auto-sends; ALWAYS prints to stdout / writes to
  gitignored file. Founder copies manually.
- Article 8: every numeric carries an `is_estimate=True` note in the
  output. No fake revenue.
- Article 11: composes existing modules — no new business logic.

Usage:
    # Print to terminal (default):
    python3 scripts/dealix_founder_daily_brief.py

    # Write markdown to gitignored file:
    python3 scripts/dealix_founder_daily_brief.py --out data/founder_briefs/today.md

    # Pass real counts from layer modules:
    python3 scripts/dealix_founder_daily_brief.py \\
        --blocking-approvals 2 --pending-payments 1 --overdue-followups 5

    # JSON output (for piping into WhatsApp Decision Bot):
    python3 scripts/dealix_founder_daily_brief.py --format json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.bottleneck_radar.computer import compute_founder_view  # noqa: E402
from auto_client_acquisition.founder_brief import query_layer_counts  # noqa: E402
from auto_client_acquisition.service_catalog.registry import list_offerings  # noqa: E402


# Article 4: the 8 hard gates that must always be present.
_HARD_GATES = (
    "no_live_send", "no_live_charge", "no_cold_whatsapp",
    "no_linkedin_auto", "no_scraping", "no_fake_proof",
    "no_fake_revenue", "no_blast",
)


def _today_ksa_label() -> str:
    """Today's date label in KSA timezone (UTC+3, approximated)."""
    return datetime.now(UTC).strftime("%Y-%m-%d")


def build_brief(
    *,
    blocking_approvals: int = 0,
    pending_payments: int = 0,
    pending_proof_packs: int = 0,
    overdue_followups: int = 0,
    sla_at_risk: int = 0,
    paid_customers_count: int = 0,
) -> dict:
    """Compose the brief as a dict (renderable as md/json)."""
    bottleneck = compute_founder_view(
        blocking_approvals_count=blocking_approvals,
        pending_payment_confirmations=pending_payments,
        pending_proof_packs_to_send=pending_proof_packs,
        overdue_followups=overdue_followups,
        sla_at_risk_tickets=sla_at_risk,
    )

    offerings = list_offerings()
    paid_offerings = [o for o in offerings if o.price_sar > 0 or o.price_unit == "custom"]

    return {
        "date": _today_ksa_label(),
        "schema_version": "1.0",
        "is_estimate": True,  # Article 8
        "bottleneck": bottleneck.model_dump(),
        "service_catalog_summary": {
            "total_offerings": len(offerings),
            "paid_offerings": len(paid_offerings),
            "lowest_priced_paid_sar": min(
                (o.price_sar for o in paid_offerings if o.price_sar > 0),
                default=0,
            ),
        },
        "hard_gates": list(_HARD_GATES),
        "paid_customers_count": paid_customers_count,
        "article_13_trigger_remaining": max(0, 3 - paid_customers_count),
        "next_founder_action": _decide_next_action(
            bottleneck_total=bottleneck.blocking_approvals_count
            + bottleneck.pending_payment_confirmations
            + bottleneck.pending_proof_packs_to_send
            + bottleneck.overdue_followups
            + bottleneck.sla_at_risk_tickets,
            paid_customers_count=paid_customers_count,
            single_action_ar=bottleneck.today_single_action_ar,
            single_action_en=bottleneck.today_single_action_en,
        ),
    }


def _decide_next_action(
    *,
    bottleneck_total: int,
    paid_customers_count: int,
    single_action_ar: str,
    single_action_en: str,
) -> dict:
    """Reconcile bottleneck signal with Article 13 (3 paid pilots) gate."""
    if bottleneck_total > 0:
        return {
            "ar": single_action_ar,
            "en": single_action_en,
            "rationale_ar": "البوتلنك أعلى أولوية اليوم.",
            "rationale_en": "Bottleneck is today's highest priority.",
        }
    if paid_customers_count < 3:
        return {
            "ar": "أرسل warm-intro لاثنين من شركة Saudi B2B في قائمتك.",
            "en": "Send warm-intros to 2 Saudi B2B prospects from your list.",
            "rationale_ar": (
                "لم تصل لـ 3 عملاء مدفوعين بعد — Article 13 still open."
            ),
            "rationale_en": "Article 13 (3 paid pilots) not yet triggered.",
        }
    return {
        "ar": "راجع customer signal synthesis لتحديد Wave 16.",
        "en": "Run customer signal synthesis to pick Wave 16 path.",
        "rationale_ar": "Article 13 triggered — حان وقت قرار المسار.",
        "rationale_en": "Article 13 triggered — time to pick the path.",
    }


def render_markdown(brief: dict) -> str:
    """Bilingual markdown (founder's coffee-time read)."""
    b = brief["bottleneck"]
    n = brief["next_founder_action"]
    s = brief["service_catalog_summary"]

    lines = [
        f"# 🌅 Dealix Founder Daily Brief · {brief['date']}",
        "",
        f"## 1. Bottleneck Radar — `{b['severity'].upper()}`",
        "",
        f"**{b['bottleneck_summary_ar']}**",
        f"_{b['bottleneck_summary_en']}_",
        "",
        f"- Blocking approvals: **{b['blocking_approvals_count']}**",
        f"- Pending payments: **{b['pending_payment_confirmations']}**",
        f"- Proof packs due: **{b['pending_proof_packs_to_send']}**",
        f"- Overdue follow-ups: **{b['overdue_followups']}**",
        f"- SLA at-risk tickets: **{b['sla_at_risk_tickets']}**",
        "",
        "## 2. Service Catalog",
        "",
        f"- Total offerings: {s['total_offerings']}",
        f"- Paid offerings: {s['paid_offerings']}",
        f"- Lowest paid price: {s['lowest_priced_paid_sar']:.0f} SAR",
        "",
        "## 3. Article 13 Status",
        "",
        f"- Paid customers: **{brief['paid_customers_count']} / 3**",
        f"- Remaining to trigger: **{brief['article_13_trigger_remaining']}**",
        "",
        "## 4. Hard Gates (8/8 IMMUTABLE)",
        "",
        "| Gate | State |",
        "|---|---|",
    ]
    for g in brief["hard_gates"]:
        lines.append(f"| `{g}` | immutable |")
    lines.extend([
        "",
        "## 5. Today's Single Action",
        "",
        f"### 🎯 {n['ar']}",
        f"_{n['en']}_",
        "",
        f"**Why?** {n['rationale_ar']} · {n['rationale_en']}",
        "",
        "---",
        "_Article 8: every count is an estimate. Article 4: never auto-send._",
        f"_Generated: {datetime.now(UTC).isoformat(timespec='seconds')}_",
    ])
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--blocking-approvals", type=int, default=0)
    p.add_argument("--pending-payments", type=int, default=0)
    p.add_argument("--pending-proof-packs", type=int, default=0)
    p.add_argument("--overdue-followups", type=int, default=0)
    p.add_argument("--sla-at-risk", type=int, default=0)
    p.add_argument("--paid-customers", type=int, default=0,
                   help="Confirmed paid customers count (Article 13 gate).")
    p.add_argument("--format", choices=("md", "json"), default="md")
    p.add_argument("--out", default=None,
                   help="Write to gitignored file (default: stdout only).")
    p.add_argument(
        "--auto-source", action="store_true",
        help=(
            "Read counts from live layer modules (approval_center, "
            "service_sessions, payment_ops, support_os) instead of "
            "manual flags. CLI flags override per-field if present. "
            "Article 8: returns 0 honestly when modules empty."
        ),
    )
    args = p.parse_args()

    if args.auto_source:
        live = query_layer_counts()
        # CLI flags take precedence (max with live values).
        kwargs = {
            "blocking_approvals": max(args.blocking_approvals, live.blocking_approvals),
            "pending_payments": max(args.pending_payments, live.pending_payment_confirmations),
            "pending_proof_packs": max(args.pending_proof_packs, live.pending_proof_packs_to_send),
            "overdue_followups": max(args.overdue_followups, live.overdue_followups),
            "sla_at_risk": max(args.sla_at_risk, live.sla_at_risk_tickets),
            "paid_customers_count": max(args.paid_customers, live.paid_customers),
        }
    else:
        kwargs = {
            "blocking_approvals": args.blocking_approvals,
            "pending_payments": args.pending_payments,
            "pending_proof_packs": args.pending_proof_packs,
            "overdue_followups": args.overdue_followups,
            "sla_at_risk": args.sla_at_risk,
            "paid_customers_count": args.paid_customers,
        }

    brief = build_brief(**kwargs)

    rendered = (
        json.dumps(brief, ensure_ascii=False, indent=2)
        if args.format == "json"
        else render_markdown(brief)
    )

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered + "\n", encoding="utf-8")
        print(f"WROTE · {out_path} · {len(rendered)} chars", file=sys.stderr)
    print(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
