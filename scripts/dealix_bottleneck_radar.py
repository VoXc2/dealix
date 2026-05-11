#!/usr/bin/env python3
"""Wave 15 §B3 — Bottleneck Radar standalone CLI.

Surfaces the Wave 13 Bottleneck Radar from the terminal — the single
question the founder asks every morning: *"what's blocking revenue
today?"*.

Inputs are passed as flags (caller is responsible for sourcing the
counts from approval_center / payment_ops / service_sessions /
support_os). This keeps the CLI deterministic + sandbox-safe — no
network calls, no DB queries.

Output: bilingual JSON OR markdown table OR single-line summary.
Caller can pipe into WhatsApp Decision Bot, founder daily brief, or
just read it in the terminal.

Article 8 enforced: every count is `is_estimate=True` per the schema.

Usage:
    # Founder portfolio view (all customers aggregated):
    python3 scripts/dealix_bottleneck_radar.py \\
        --blocking-approvals 3 \\
        --pending-payments 1 \\
        --pending-proof-packs 2 \\
        --overdue-followups 5 \\
        --sla-at-risk 1

    # Per-customer view (filters tenant):
    python3 scripts/dealix_bottleneck_radar.py \\
        --customer-handle acme-real-estate \\
        --blocking-approvals 2

    # JSON output for piping:
    python3 scripts/dealix_bottleneck_radar.py --format json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.bottleneck_radar.computer import (  # noqa: E402
    compute_bottleneck,
    compute_founder_view,
)


def _format_md(b) -> str:
    """Markdown table — readable in terminal + GitHub + WhatsApp paste."""
    lines = [
        f"# Bottleneck Radar — {b.severity.upper()}",
        "",
        f"**{b.bottleneck_summary_ar}**",
        f"*{b.bottleneck_summary_en}*",
        "",
        "| Bucket | Count |",
        "|---|---:|",
        f"| Blocking approvals | {b.blocking_approvals_count} |",
        f"| Pending payment confirmations | {b.pending_payment_confirmations} |",
        f"| Pending proof packs | {b.pending_proof_packs_to_send} |",
        f"| Overdue follow-ups | {b.overdue_followups} |",
        f"| SLA at-risk tickets | {b.sla_at_risk_tickets} |",
        "",
        "## Today's single action",
        "",
        f"- 🇸🇦 {b.today_single_action_ar}",
        f"- 🇬🇧 {b.today_single_action_en}",
        "",
        "_Article 8: every count is_estimate=True_",
    ]
    return "\n".join(lines)


def _format_one_line(b) -> str:
    """Single line summary (for WhatsApp paste / 1-line cron logs)."""
    return f"[{b.severity}] {b.bottleneck_summary_ar} · ACT: {b.today_single_action_ar}"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--customer-handle", default=None,
                   help="Per-customer view (None = founder portfolio).")
    p.add_argument("--blocking-approvals", type=int, default=0)
    p.add_argument("--pending-payments", type=int, default=0)
    p.add_argument("--pending-proof-packs", type=int, default=0)
    p.add_argument("--overdue-followups", type=int, default=0)
    p.add_argument("--sla-at-risk", type=int, default=0)
    p.add_argument("--format", choices=("md", "json", "one-line"), default="md")
    args = p.parse_args()

    if args.customer_handle:
        bottleneck = compute_bottleneck(
            customer_handle=args.customer_handle,
            blocking_approvals_count=args.blocking_approvals,
            pending_payment_confirmations=args.pending_payments,
            pending_proof_packs_to_send=args.pending_proof_packs,
            overdue_followups=args.overdue_followups,
            sla_at_risk_tickets=args.sla_at_risk,
        )
    else:
        bottleneck = compute_founder_view(
            blocking_approvals_count=args.blocking_approvals,
            pending_payment_confirmations=args.pending_payments,
            pending_proof_packs_to_send=args.pending_proof_packs,
            overdue_followups=args.overdue_followups,
            sla_at_risk_tickets=args.sla_at_risk,
        )

    if args.format == "json":
        print(json.dumps(bottleneck.model_dump(), ensure_ascii=False, indent=2))
    elif args.format == "one-line":
        print(_format_one_line(bottleneck))
    else:
        print(_format_md(bottleneck))

    return 0


if __name__ == "__main__":
    sys.exit(main())
