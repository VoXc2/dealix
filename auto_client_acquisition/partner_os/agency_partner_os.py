"""
Agency Partner OS — daily brief for agency partners.

Reuses partners router data + adds the agency-specific decision queue:
  - clients waiting for Diagnostic
  - co-branded Proof Packs ready
  - revenue-share earned this period
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def _now() -> datetime:
    return datetime.now(timezone.utc)


def build_brief(
    *,
    partner,
    customers,
    sessions,
    expected_commission_sar: float = 0.0,
) -> dict[str, Any]:
    customers = list(customers or [])
    sessions = list(sessions or [])

    diagnostics_ready = sum(
        1 for s in sessions
        if s.service_id == "free_diagnostic" and s.status in ("new", "waiting_inputs")
    )
    proof_ready = sum(
        1 for s in sessions if s.status == "ready_to_deliver"
    )
    needs_followup = sum(1 for c in customers if c.churn_risk in ("medium", "high"))
    active = sum(1 for c in customers if c.onboarding_status not in ("churned",))

    decisions: list[dict[str, Any]] = []

    if diagnostics_ready:
        decisions.append({
            "type": "agency_action",
            "title_ar": f"{diagnostics_ready} عميل جاهز لـ Diagnostic",
            "why_now_ar": "تشغيل Diagnostic يولّد Co-branded Proof Pack باسمكم خلال 24 ساعة.",
            "recommended_action_ar": "اعتمد بدء الـ Diagnostic + ابعث intake form للعميل.",
            "risk_level": "low",
            "proof_impact": ["client_diagnostics", "cobranded_proof_packs"],
            "action_mode": "approval_required",
            "buttons_ar": ["شغّل Diagnostic", "ابعث intake", "تخطي"],
        })

    if proof_ready:
        decisions.append({
            "type": "agency_action",
            "title_ar": f"{proof_ready} Co-branded Proof Pack جاهز",
            "why_now_ar": "Proof Pack جاهز — أنت من يرسله من بريدك حتى تظهر العلاقة بصورة الوكالة.",
            "recommended_action_ar": "راجع PDF + عدّل التعليق التنفيذي + أرسله.",
            "risk_level": "low",
            "proof_impact": ["proof_packs_sent", "client_health_visible"],
            "action_mode": "approval_required",
            "buttons_ar": ["راجع وأرسل", "عدّل أولاً", "تخطي"],
        })

    if needs_followup:
        decisions.append({
            "type": "agency_action",
            "title_ar": f"{needs_followup} عميل بحاجة متابعة",
            "why_now_ar": "Churn risk = medium/high — Proof + reach-out يحلّ معظم الحالات.",
            "recommended_action_ar": "افتح Customer Health + أرسل update + احجز اجتماع 15 دقيقة.",
            "risk_level": "medium",
            "proof_impact": ["customer_health_updated"],
            "action_mode": "approval_required",
            "buttons_ar": ["افتح Customer Health", "احجز اجتماع", "صعّد"],
        })

    decisions = decisions[:3]

    return {
        "role": "agency_partner",
        "brief_type": "daily_agency",
        "date": _now().date().isoformat(),
        "partner_id": getattr(partner, "id", None),
        "summary": {
            "active_clients": active,
            "diagnostics_ready": diagnostics_ready,
            "proof_packs_ready": proof_ready,
            "needs_followup": needs_followup,
            "expected_commission_sar": float(expected_commission_sar or 0.0),
        },
        "top_decisions": decisions,
        "blocked_today_ar": [
            "لا exclusivity بدون اتفاق مكتوب",
            "لا revenue share بدون referral متتبع",
            "لا white-label قبل 3 paid pilots ناجحة",
        ],
    }
