"""Normalize and validate company profile for Growth Beast."""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.company_growth_beast.schemas import CompanyGrowthProfile
from auto_client_acquisition.company_growth_beast.safety_policy import assess_text_safety, sector_requires_escalation


def upsert_company_profile(payload: dict[str, Any]) -> dict[str, Any]:
    profile = CompanyGrowthProfile.model_validate(payload)
    combined = " ".join(
        [
            profile.offer,
            profile.constraints,
            profile.support_questions,
        ]
    )
    safety = assess_text_safety(combined)
    escalation = sector_requires_escalation(profile.sector)
    if not safety["safe"]:
        mode = "blocked"
    elif not profile.consent_for_diagnostic:
        mode = "approval_required"
    else:
        mode = "draft_only"

    return {
        "schema_version": 1,
        "profile": profile.model_dump(),
        "risk_flags": {
            "sensitive_sector_escalation": escalation,
            "consent_for_diagnostic": profile.consent_for_diagnostic,
        },
        "safety": safety,
        "action_mode": mode,
        "note_ar": "لا تخزين دائم للبيانات في هذه الطبقة التجريبية؛ استخدم جلسة session_id للمتابعة.",
    }
