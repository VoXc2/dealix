"""Customer Company Portal — eight customer-safe fields only."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.company_growth_beast import (
    build_company_profile,
    build_growth_diagnostic,
)

router = APIRouter(prefix="/api/v1/customer-portal", tags=["customer-portal"])


def _session_deliverables(customer_handle: str) -> list[dict[str, Any]]:
    from api.routers import delivery_os as d_os

    handle = customer_handle.strip() or "Slot-A"
    matches: list[dict[str, Any]] = []
    for sess in d_os._SESSIONS.values():
        if sess.get("customer_handle") == handle:
            matches.append(
                {
                    "session_status": sess.get("status"),
                    "checklist": sess.get("checklist") or [],
                }
            )
    return matches


@router.get("/{customer_handle}")
async def customer_portal(customer_handle: str) -> dict[str, Any]:
    """Eight fields only — no internal engineering vocabulary."""
    profile = build_company_profile(
        company_handle=customer_handle,
        sector="b2b_services",
        consent_for_diagnostic=True,
    )
    diagnostic = build_growth_diagnostic(profile)
    plans = diagnostic.get("seven_day_plan") if isinstance(diagnostic, dict) else []
    deliverables = _session_deliverables(customer_handle)

    next_ar = (
        "راجع التشخيص والخطة ثم اعتمد الخطوة التالية يدوياً"
        if isinstance(diagnostic, dict) and not diagnostic.get("blocked")
        else "أكمل الموافقة على التشخيص للمتابعة"
    )
    next_en = (
        "Review diagnostic and plan; approve the next step manually"
        if isinstance(diagnostic, dict) and not diagnostic.get("blocked")
        else "Complete diagnostic consent to proceed"
    )

    return {
        "schema_version": 1,
        "experience_layer": "customer_portal",
        "start_diagnostic": "/api/v1/company-growth-beast/diagnostic",
        "seven_day_plan": plans if isinstance(plans, list) else [],
        "messages_and_followups": {
            "status_ar": "مسودات جاهزة للمراجعة قبل أي إرسال",
            "status_en": "Drafts ready for review before any send",
            "action_mode": "approval_required",
        },
        "support_tickets": [],
        "deliverables": deliverables,
        "proof_pack": {
            "status_ar": "لا حزمة إثبات مسجلة بعد",
            "status_en": "No proof pack logged yet",
            "ready": False,
        },
        "weekly_report": "/api/v1/company-growth-beast/weekly-report",
        "next_decision": {"ar": next_ar, "en": next_en},
    }
