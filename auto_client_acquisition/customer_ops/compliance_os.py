"""
Compliance & Safety OS — daily safety brief.

Surfaces blocked actions + missing-consent flags + live-action gates so the
operator sees what Dealix REFUSED to do today (not just what it did).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def _now() -> datetime:
    return datetime.now(timezone.utc)


def build_brief(
    *,
    proof_events,
    settings,
) -> dict[str, Any]:
    """
    Args:
      proof_events: iterable of ProofEventRecord-like — we sum risk_blocked.
      settings: dealix Settings instance — we surface the live-action gates.
    """
    proof_events = list(proof_events or [])
    blocked = sum(1 for e in proof_events if e.unit_type == "risk_blocked")
    high_risk_blocked = sum(
        1 for e in proof_events if e.unit_type == "risk_blocked" and e.risk_level == "high"
    )

    gates = {
        "WHATSAPP_ALLOW_LIVE_SEND": bool(getattr(settings, "whatsapp_allow_live_send", False)),
        "WHATSAPP_ALLOW_INTERNAL_SEND": bool(getattr(settings, "whatsapp_allow_internal_send", False)),
        "WHATSAPP_ALLOW_CUSTOMER_SEND": bool(getattr(settings, "whatsapp_allow_customer_send", False)),
        "GMAIL_ALLOW_LIVE_SEND": bool(getattr(settings, "gmail_allow_live_send", False)),
        "MOYASAR_ALLOW_LIVE_CHARGE": bool(getattr(settings, "moyasar_allow_live_charge", False)),
        "LINKEDIN_ALLOW_AUTO_DM": bool(getattr(settings, "linkedin_allow_auto_dm", False)),
        "RESEND_ALLOW_LIVE_SEND": bool(getattr(settings, "resend_allow_live_send", False)),
        "CALLS_ALLOW_LIVE_DIAL": bool(getattr(settings, "calls_allow_live_dial", False)),
    }

    flipped_on = [k for k, v in gates.items() if v]

    decisions: list[dict[str, Any]] = []
    if high_risk_blocked > 0:
        decisions.append({
            "type": "compliance_alert",
            "title_ar": f"{high_risk_blocked} محاولة عالية المخاطرة تم منعها",
            "why_now_ar": "Risk-blocked events بمستوى high — تحتاج مراجعة policy لمعرفة المصدر.",
            "recommended_action_ar": "راجع log + اعرف المصدر + حدّث ICP/Suppression لو لزم.",
            "risk_level": "high",
            "proof_impact": ["compliance_review", "policy_updated"],
            "action_mode": "approval_required",
            "buttons_ar": ["افتح log", "حدّث policy", "تخطي"],
        })
    if flipped_on:
        decisions.append({
            "type": "gate_alert",
            "title_ar": f"{len(flipped_on)} live-action gate مُفعَّل",
            "why_now_ar": "بعض الـ gates لا تساوي False — تحقق أنه أُذِنَ به صراحةً.",
            "recommended_action_ar": "راجع " + ", ".join(flipped_on) + " وتأكد من الـ approval.",
            "risk_level": "high",
            "proof_impact": ["gate_audited"],
            "action_mode": "approval_required",
            "buttons_ar": ["افتح Gates", "أعد للـ False", "تخطي"],
        })

    decisions = decisions[:3]

    return {
        "role": "compliance",
        "brief_type": "daily_compliance",
        "date": _now().date().isoformat(),
        "summary": {
            "risks_blocked_total": blocked,
            "high_risk_blocked": high_risk_blocked,
            "live_gates_on_count": len(flipped_on),
        },
        "live_action_gates": gates,
        "top_decisions": decisions,
        "blocked_today_ar": [
            "approval-first في كل خطوة",
            "PDPL consent لكل سجل",
            "لا تغيير policy بدون موافقة المؤسس",
        ],
    }
