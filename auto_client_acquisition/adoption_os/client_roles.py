"""Client-side roles for adoption — clarity on who sees, approves, and is measured."""

from __future__ import annotations

CLIENT_ADOPTION_ROLES: tuple[str, ...] = (
    "executive_sponsor",
    "workflow_owner",
    "operator",
    "governance_reviewer",
    "dealix_success_owner",
)

ENABLEMENT_KIT_ITEMS: tuple[str, ...] = (
    "one_page_overview",
    "role_guide",
    "workflow_guide",
    "approval_guide",
    "what_dealix_will_not_do",
    "proof_pack_sample",
    "monthly_cadence_template",
    "governance_faq",
    "arabic_executive_summary_template",
    "escalation_path",
)


def enablement_kit_coverage_score(items_delivered: frozenset[str]) -> int:
    if not ENABLEMENT_KIT_ITEMS:
        return 0
    n = sum(1 for i in ENABLEMENT_KIT_ITEMS if i in items_delivered)
    return (n * 100) // len(ENABLEMENT_KIT_ITEMS)
