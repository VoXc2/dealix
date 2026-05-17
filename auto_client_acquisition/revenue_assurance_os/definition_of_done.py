"""Definition of Done — a machine is not "built" until its DoD passes.

Each machine has a checklist of acceptance criteria. ``dod_status`` reports
which criteria carry evidence and whether the machine is genuinely done.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

MACHINE_DOD: dict[str, tuple[str, ...]] = {
    "sales_autopilot": (
        "every_lead_enters_system",
        "every_lead_scored",
        "every_lead_has_stage",
        "every_lead_has_next_action",
        "qualified_a_generates_approval_task",
        "meeting_booked_generates_meeting_brief",
        "meeting_done_requires_notes",
        "scope_requires_approval_before_send",
        "invoice_requires_approved_scope",
        "revenue_requires_invoice_paid",
    ),
    "marketing_factory": (
        "every_content_has_cta",
        "every_cta_has_utm",
        "every_lead_magnet_creates_lead",
        "every_campaign_has_source",
        "weekly_post_measured_by_qualified_leads",
        "objections_become_content_assets",
    ),
    "support_autopilot": (
        "every_ticket_classified",
        "answers_sourced_from_knowledge_base",
        "high_risk_questions_escalate",
        "unknown_questions_create_knowledge_gap",
        "customer_answers_have_source_or_approval",
    ),
    "affiliate_machine": (
        "every_affiliate_has_application",
        "every_affiliate_has_referral_code",
        "affiliates_use_approved_messaging",
        "affiliates_use_disclosure",
        "no_commission_before_invoice_paid",
        "misleading_claims_create_compliance_flag",
    ),
}


@dataclass(frozen=True, slots=True)
class DodStatus:
    machine: str
    total: int
    satisfied_count: int
    missing: tuple[str, ...]
    done: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def dod_status(machine: str, satisfied: set[str] | frozenset[str]) -> DodStatus:
    """Report Definition-of-Done status for one machine."""
    if machine not in MACHINE_DOD:
        raise ValueError(f"unknown machine: {machine!r} (known: {sorted(MACHINE_DOD)})")
    criteria = MACHINE_DOD[machine]
    missing = tuple(c for c in criteria if c not in satisfied)
    return DodStatus(
        machine=machine,
        total=len(criteria),
        satisfied_count=len(criteria) - len(missing),
        missing=missing,
        done=not missing,
    )


__all__ = [
    "MACHINE_DOD",
    "DodStatus",
    "dod_status",
]
