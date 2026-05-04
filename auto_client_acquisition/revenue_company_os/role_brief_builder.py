"""
Role Brief Builder — single entry point that composes the daily brief
for any role by delegating to the role-specific OS module.

Roles supported (matches WhatsApp + Command Center routes):
    ceo
    sales_manager
    growth_manager
    revops
    customer_success
    agency_partner
    finance
    compliance

Each brief returns a uniform shape:
    {role, brief_type, date, summary, top_decisions, blocked_today_ar, ...}

All sub-modules are PURE — the router fetches DB rows and passes them in.
"""

from __future__ import annotations

from typing import Any


SUPPORTED_ROLES: tuple[str, ...] = (
    "ceo", "sales_manager", "growth_manager", "revops",
    "customer_success", "agency_partner", "finance", "compliance",
    "meeting_intelligence",
)


def build(role: str, *, data: dict[str, Any]) -> dict[str, Any]:
    """Dispatch to the right OS module.

    `data` carries the rows the role needs (deals/sessions/events/...).
    Each role uses a subset.
    """
    role = role.lower()
    if role == "sales_manager":
        from auto_client_acquisition.revenue_company_os.sales_manager_os import build_brief
        return build_brief(
            data.get("deals") or [],
            data.get("sessions") or [],
            data.get("objection_events") or [],
        )
    if role == "growth_manager":
        from auto_client_acquisition.revenue_company_os.growth_manager_os import build_brief
        return build_brief(data.get("yesterday_events") or [])
    if role == "ceo":
        from auto_client_acquisition.revenue_company_os.ceo_command_os import build_brief
        return build_brief(
            sales_summary=data.get("sales_summary") or {},
            growth_summary=data.get("growth_summary") or {},
            proof_summary=data.get("proof_summary") or {},
            partner_summary=data.get("partner_summary") or {},
        )
    if role == "revops":
        from auto_client_acquisition.revenue_company_os.revops_os import build_brief
        return build_brief(data.get("funnel_event_counts") or {})
    if role == "customer_success":
        from auto_client_acquisition.customer_ops.customer_success_os import build_brief
        return build_brief(
            customers=data.get("customers") or [],
            tickets=data.get("tickets") or [],
            sessions=data.get("sessions") or [],
        )
    if role == "agency_partner":
        from auto_client_acquisition.partner_os.agency_partner_os import build_brief
        return build_brief(
            partner=data.get("partner"),
            customers=data.get("customers") or [],
            sessions=data.get("sessions") or [],
            expected_commission_sar=float(data.get("expected_commission_sar") or 0.0),
        )
    if role == "finance":
        from auto_client_acquisition.customer_ops.finance_os import build_brief
        return build_brief(
            sessions=data.get("sessions") or [],
            payments=data.get("payments") or [],
            expected_partner_commission_sar=float(data.get("expected_partner_commission_sar") or 0.0),
        )
    if role == "compliance":
        from auto_client_acquisition.customer_ops.compliance_os import build_brief
        return build_brief(
            proof_events=data.get("proof_events") or [],
            settings=data.get("settings"),
        )
    if role == "meeting_intelligence":
        from auto_client_acquisition.revenue_company_os.call_meeting_intelligence_os import build_brief
        return build_brief(
            data.get("meetings") or [],
            data.get("proof_events") or [],
        )
    raise ValueError(f"unknown_role: {role}")
