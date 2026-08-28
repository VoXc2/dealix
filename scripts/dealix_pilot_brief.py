#!/usr/bin/env python3
"""Render a non-binding 30-day Revenue Command Pilot scope draft.

This compatibility command replaces the historical 499 SAR / 7-Day Revenue
Proof Sprint generator. It cannot select or authorize a price, payment term,
refund/remedy, customer outcome, external send, or contract commitment.

Precondition for real customer use:
- qualified discovery exists;
- a named-customer quote/proposal evidence reference exists or is being prepared;
- any commercial commitment is handled by the canonical approval/controlled
  execution path.

The artifact generated here is ``DRAFT_NOT_SENT`` and is suitable for internal
scope preparation only.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data/founder_briefs"


def build_brief(
    *,
    company: str,
    sector: str,
    quote_evidence_id: str,
    diagnostic_summary: str | None = None,
) -> dict:
    return {
        "schema": "dealix.revenue_command_pilot_scope_draft.v1",
        "truth_class": "DRAFT_NOT_SENT",
        "generated_at": datetime.now(UTC).isoformat(),
        "company": company,
        "sector": sector,
        "commercial_path": (
            "Free Mini Diagnostic -> Qualified Discovery -> Customer-Specific Quote -> "
            "Revenue Command Pilot — 30 days -> Proof Pack -> Stop/Expand/Redesign"
        ),
        "package": "Revenue Command Pilot — 30 days",
        "duration_days": 30,
        "quote_evidence_id": quote_evidence_id,
        "diagnostic_summary": diagnostic_summary or "UNKNOWN_NOT_EVIDENCE_BACKED",
        "scope_draft": [
            "Confirm one qualified revenue/operating problem and accountable owner",
            "Confirm lawful minimum-necessary data boundary and baseline",
            "Define acceptance criteria and weekly proof cadence",
            "Operate the agreed Revenue + Proof + Command workflow within the approved scope",
            "Record source-bound outcomes, blockers, decisions, and limitations",
            "Produce a final Proof Pack",
            "Hold final Stop / Expand / Redesign review",
        ],
        "required_before_commitment": [
            "qualified_discovery",
            "customer_specific_scope",
            "acceptance_criteria",
            "quote_or_commercial_terms_approved_by_applicable_authority",
            "external_action_gates_satisfied",
        ],
        "what_is_not_authorized_by_this_artifact": [
            "named_price_or_discount",
            "payment_or_invoice",
            "refund_or_remedy",
            "contract_or_legal_term",
            "tender_commitment",
            "guaranteed_revenue_roi_leads_or_conversion",
            "external_send_or_public_publish",
            "production_or_customer_system_mutation",
        ],
        "price_sar": None,
        "payment_terms": None,
        "refund_policy": None,
        "outcome_guarantee": None,
        "external_send_allowed": False,
        "execution_allowed": False,
        "approval_required_for_commitment": True,
        "source": "canonical_30_day_pilot_scope_compatibility_renderer",
    }


def render_markdown(brief: dict) -> str:
    lines = [
        f"# {brief['package']} — {brief['company']}",
        "",
        f"**Sector / القطاع:** {brief['sector']}",
        f"**Status / الحالة:** {brief['truth_class']}",
        f"**Quote evidence / مرجع العرض:** {brief['quote_evidence_id']}",
        "",
        "> This is an internal scope draft, not a price quote, invoice, contract, guarantee, or sent proposal.",
        "> هذه مسودة نطاق داخلية وليست تسعيرة أو فاتورة أو عقدًا أو ضمانًا أو عرضًا مرسلًا.",
        "",
        "## Current commercial path | المسار التجاري الحالي",
        brief["commercial_path"],
        "",
        "## Diagnostic / discovery summary | ملخص التشخيص والاستكشاف",
        brief["diagnostic_summary"],
        "",
        "## Draft scope | مسودة النطاق",
    ]
    for item in brief["scope_draft"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Required before commitment | المطلوب قبل الالتزام"])
    for item in brief["required_before_commitment"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Not authorized here | غير مصرح به هنا"])
    for item in brief["what_is_not_authorized_by_this_artifact"]:
        lines.append(f"- {item}")
    lines.extend([
        "",
        "**Price:** not set here — customer-specific quote authority required.",
        "**Payment/refund/contract/outcome commitments:** not authorized by this artifact.",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render 30-day Pilot scope draft (no price authority)")
    parser.add_argument("--company", required=True)
    parser.add_argument("--sector", required=True)
    parser.add_argument("--quote-evidence-id", required=True)
    parser.add_argument("--diagnostic-file", default=None)
    parser.add_argument(
        "--amount-sar",
        type=float,
        default=None,
        help="retired compatibility option; any supplied amount is rejected",
    )
    parser.add_argument("--out-md", default=None)
    parser.add_argument("--out-json", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.amount_sar is not None:
        print(
            "REFUSING=PRICE_NOT_AUTHORIZED_BY_PILOT_BRIEF; use approved customer-specific quote authority",
            file=sys.stderr,
        )
        return 2

    quote_ref = args.quote_evidence_id.strip()
    if not quote_ref:
        print("REFUSING=QUOTE_EVIDENCE_ID_REQUIRED", file=sys.stderr)
        return 2

    diagnostic_summary = None
    if args.diagnostic_file:
        try:
            data = json.loads(Path(args.diagnostic_file).read_text(encoding="utf-8"))
            diagnostic_summary = str(
                data.get("executive_summary_ar")
                or data.get("executive_summary_en")
                or data.get("summary")
                or ""
            )[:1000]
        except Exception as exc:
            print(f"WARNING=DIAGNOSTIC_FILE_UNREADABLE:{type(exc).__name__}", file=sys.stderr)

    brief = build_brief(
        company=args.company,
        sector=args.sector,
        quote_evidence_id=quote_ref,
        diagnostic_summary=diagnostic_summary,
    )
    markdown = render_markdown(brief)

    if args.dry_run:
        print(markdown)
        print(json.dumps(brief, ensure_ascii=False, indent=2))
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    slug = "_".join(args.company.strip().split())[:48] or "company"
    stamp = datetime.now(UTC).strftime("%Y-%m-%d")
    out_md = Path(args.out_md) if args.out_md else OUT_DIR / f"pilot_scope_{slug}_{stamp}.md"
    out_json = Path(args.out_json) if args.out_json else OUT_DIR / f"pilot_scope_{slug}_{stamp}.json"
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(markdown, encoding="utf-8")
    out_json.write_text(json.dumps(brief, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"WROTE={out_md}")
    print(f"RECEIPT={out_json}")
    print("STATUS=DRAFT_NOT_SENT")
    print("PRICE_AUTHORIZED=false")
    print("PAYMENT_AUTHORIZED=false")
    print("EXECUTION_ALLOWED=false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
