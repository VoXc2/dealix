#!/usr/bin/env python3
"""Distribution Day — the founder's single morning command report.

Composes the day's revenue command from the distribution_os stores: pending
drafts to approve, due follow-ups, proposal drafts, proof packs, payment
handoffs awaiting approval, the renewal/upsell queue, and the metrics
snapshot. Read-only; writes to the untracked runtime reports plane by default.
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUNTIME_REPORTS_ROOT = Path("/opt/dealix/control/reports")
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from auto_client_acquisition.distribution_os import (
    draft_factory,
    followup,
    metrics,
    payment_handoff,
    proof_pack,
    proposal,
    prospect,
)
from auto_client_acquisition.distribution_os.draft_factory import DraftStatus
from auto_client_acquisition.distribution_os.prospect import ProspectStatus


def _default_report() -> Path:
    runtime_root = os.environ.get("DEALIX_RUNTIME_REPORTS_ROOT")
    base = Path(runtime_root).expanduser() if runtime_root else DEFAULT_RUNTIME_REPORTS_ROOT
    if runtime_root:
        resolved_root = ROOT.resolve()
        resolved_base = base.resolve()
        if resolved_base == resolved_root or resolved_root in resolved_base.parents:
            raise ValueError("DEALIX_RUNTIME_REPORTS_ROOT must stay outside the canonical repository")
    return base / "distribution" / "DISTRIBUTION_DAY.md"


def _section(title: str, rows: list[str]) -> list[str]:
    out = [f"## {title}"]
    out += rows if rows else ["- (لا شيء / none)"]
    out.append("")
    return out


def _render() -> str:
    today = datetime.now(UTC).date().isoformat()
    pending = draft_factory.list_drafts(status=DraftStatus.PENDING_APPROVAL.value)
    due = followup.due_followups()
    props = proposal.list_proposals(approval_status="pending_approval")
    packs = proof_pack.list_proof_packs()
    handoffs = payment_handoff.list_handoffs(status="pending_approval")
    qualified = prospect.list_prospects(status=ProspectStatus.QUALIFIED.value)
    kpis = metrics.daily_kpis()

    lines = [
        "# Distribution Day — أمر اليوم التجاري",
        "",
        f"التاريخ / Date: {today}",
        "",
        "> القاعدة: الذكاء يجهّز، المؤسس يوافق، النظام يتتبّع. لا إرسال خارجي تلقائي.",
        "",
    ]
    lines += _section(
        f"مسودات بانتظار الموافقة / Pending drafts ({len(pending)})",
        [f"- `{d.id}` [{d.draft_type}/{d.channel}] {d.subject}" for d in pending[:25]],
    )
    lines += _section(
        f"متابعات مستحقة / Due follow-ups ({len(due)})",
        [
            f"- `{f.prospect_id}` [{f.draft_type}/{f.channel}] due {f.due_date[:10]}"
            for f in due[:25]
        ],
    )
    lines += _section(
        f"مقترحات بانتظار الموافقة / Proposal drafts ({len(props)})",
        [
            f"- `{p.id}` product={p.product_id} {p.price_min_sar}-{p.price_max_sar} SAR"
            for p in props[:25]
        ],
    )
    lines += _section(
        f"حزم الإثبات / Proof packs ({len(packs)})",
        [f"- `{p.id}` customer={p.customer_id} L{p.evidence_level}" for p in packs[:25]],
    )
    lines += _section(
        f"تسليمات الدفع بانتظار الموافقة / Payment handoffs ({len(handoffs)})",
        [
            f"- `{h.id}` proposal={h.proposal_id} {h.amount_sar} SAR — {h.governance_status}"
            for h in handoffs[:25]
        ],
    )
    lines += _section(
        f"مؤهلون جاهزون / Qualified prospects ({len(qualified)})",
        [f"- `{p.id}` {p.company} [{p.sector}] → {p.offer_angle}" for p in qualified[:25]],
    )
    lines += ["## مؤشرات اليوم / Today's metrics"]
    lines += [f"- {k}: {v}" for k, v in kpis.items()]
    lines += [
        "",
        "## قرارك اليومي / Your daily decision",
        "- Approve / Reject / Needs-edit المسودات",
        "- Mark-copied بعد الإرسال اليدوي",
        "- تابع المؤهّلين، ولّد المقترحات وحزم الإثبات، جهّز تسليم الدفع",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print", action="store_true", dest="to_stdout")
    parser.add_argument("--out", type=Path, help="explicit report path; default is the untracked runtime reports plane")
    args = parser.parse_args()

    content = _render()
    if args.to_stdout:
        print(content)
        return 0
    report = args.out.expanduser() if args.out else _default_report()
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(content, encoding="utf-8")
    try:
        shown = report.relative_to(ROOT)
    except ValueError:
        shown = report
    print(f"Wrote {shown}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
