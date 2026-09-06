#!/usr/bin/env python3
"""Generate the Company Brain launch pack from canonical commercial truth.

Local-only generator. It creates capability, pain, proposal, and negotiation notes
for founder review. It must not recreate retired fixed-price or seven-day offers.
"""
from __future__ import annotations

import json
from datetime import UTC, date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "reports" / "commercial"

CANONICAL_ENTRY_OFFER = "Free Mini Diagnostic"
CANONICAL_PAID_OFFER = "30-Day Revenue Command Pilot"
CANONICAL_PAID_PATH = (
    "Qualified Discovery -> Customer-Specific Quote -> 30-Day Revenue Command Pilot "
    "-> Verified Payment -> Delivery -> Customer-Validated Proof -> Stop / Expand / Redesign"
)

CAPABILITIES = [
    {
        "capability": "Company Brain OS",
        "buyer": "CEO / Founder / GM",
        "pain": "unclear daily priorities across revenue, operations, and risk",
        "diagnostic_angle": "find decision, ownership, and evidence gaps that block execution",
        "delivery_value": "daily executive decisions, risk radar, and governed execution context",
    },
    {
        "capability": "Revenue Command Room OS",
        "buyer": "Sales Director / Founder",
        "pain": "pipeline, follow-up, and next actions are not visible enough",
        "diagnostic_angle": "find revenue leakage, stalled opportunities, and missing next actions",
        "delivery_value": "priority opportunities, follow-up control, and evidence-backed deal movement",
    },
    {
        "capability": "Follow-up Recovery OS",
        "buyer": "Sales / Operations Manager",
        "pain": "inquiries and conversations are not converted into clear actions",
        "diagnostic_angle": "find relationship-state, response, and ownership gaps",
        "delivery_value": "governed reply queue, escalation rules, and lost-opportunity evidence",
    },
    {
        "capability": "Proposal Co-Pilot",
        "buyer": "Founder / Sales Manager",
        "pain": "scope and negotiation discipline break before value is proven",
        "diagnostic_angle": "find scope, objection, approval, and decision-process gaps",
        "delivery_value": "customer-specific proposal support, objection map, and governed trade-offs",
    },
    {
        "capability": "Client Delivery OS",
        "buyer": "Operations / Account Manager",
        "pain": "delivery quality depends on people rather than a repeatable evidence loop",
        "diagnostic_angle": "find intake, ownership, acceptance, and proof gaps",
        "delivery_value": "intake, scope card, acceptance criteria, delivery receipts, and Proof Pack",
    },
    {
        "capability": "AI Trust OS",
        "buyer": "CEO / Compliance / IT",
        "pain": "AI is used without clear authority, data, or approval boundaries",
        "diagnostic_angle": "find authority, data, identity, and audit gaps",
        "delivery_value": "policy, data rules, approval map, and evidence-backed audit trail",
    },
]

SECTOR_ANGLES = {
    "clinics": "map operational and commercial follow-up leakage without treating patient data as sales permission",
    "real_estate": "find lead leakage after first inquiry and preserve channel/consent evidence",
    "logistics": "track proposals, B2B accounts, delivery decisions, and proof",
    "training": "convert permissioned inquiries into governed next actions and registrations",
    "marketing_agencies": "standardize delivery, customer proof, and expansion decisions",
    "b2b_services": "turn proposals and follow-ups into an evidence-backed Revenue Command Room",
}


def build_markdown() -> str:
    today = date.today().isoformat()
    lines = [
        f"# Dealix Company Brain Launch Pack — {today}",
        "",
        "## Executive positioning",
        "",
        "Dealix is a Saudi-first AI Business Operating System. The commercial wedge is Revenue + Proof + Command; capabilities are not standalone public offers.",
        "",
        "## Canonical buying path",
        "",
        f"`{CANONICAL_ENTRY_OFFER} -> {CANONICAL_PAID_PATH}`",
        "",
        "- public_fixed_price: false",
        "- public_checkout: false",
        "- customer_specific_quote_only: true",
        "- live_send_allowed: false unless action-bound authority and channel eligibility are proven",
        "- live_charge_allowed: false unless action-bound payment authority and independent evidence are proven",
        "",
        "## Capability matrix",
        "",
        "| Capability | Buyer | Pain | Diagnostic angle | Delivery value |",
        "|---|---|---|---|---|",
    ]
    for item in CAPABILITIES:
        lines.append(
            f"| {item['capability']} | {item['buyer']} | {item['pain']} | {item['diagnostic_angle']} | {item['delivery_value']} |"
        )
    lines += [
        "",
        "## Sector persuasion angles",
        "",
        "| Sector | Angle |",
        "|---|---|",
    ]
    for sector, angle in SECTOR_ANGLES.items():
        lines.append(f"| {sector} | {angle} |")
    lines += [
        "",
        "## Dealix pitch formula",
        "",
        "1. Start from a source-bound signal or a real inbound/relationship context.",
        "2. Identify one visible business pain and ask one diagnostic question.",
        f"3. Offer the {CANONICAL_ENTRY_OFFER}; do not invent a paid sprint or public price.",
        "4. If the problem is qualified, run discovery and prepare a customer-specific quote.",
        f"5. Start the {CANONICAL_PAID_OFFER} only after accepted scope and verified payment/start evidence.",
        "6. Deliver against acceptance criteria and produce customer-validated proof.",
        "7. Decide Stop / Expand / Redesign from measured value; do not infer recurring authority.",
        "",
        "## Negotiation rule",
        "",
        "Protect evidence, acceptance criteria, and delivery scope before price. Any commercial concession must remain inside customer-specific quote authority; no global price floor or automatic discount is created by this pack.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "commercial_truth": {
            "entry_offer": CANONICAL_ENTRY_OFFER,
            "paid_offer": CANONICAL_PAID_OFFER,
            "paid_path": CANONICAL_PAID_PATH,
            "public_fixed_price": False,
            "public_checkout": False,
            "customer_specific_quote_only": True,
            "live_send_allowed": False,
            "live_charge_allowed": False,
        },
        "capabilities": CAPABILITIES,
        "sector_angles": SECTOR_ANGLES,
        "status": "ready_for_founder_review",
    }
    (OUT_DIR / "company_brain_launch_pack.md").write_text(build_markdown(), encoding="utf-8")
    (OUT_DIR / "company_brain_launch_pack.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("COMPANY_BRAIN_PACK_GENERATED=reports/commercial/company_brain_launch_pack.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
