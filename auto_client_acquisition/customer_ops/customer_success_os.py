"""
Customer Success OS — onboarding + Proof cadence + SLA + renewal risk.

Pure brief builder. Reads CustomerRecord-like + SupportTicketRecord-like +
ServiceSessionRecord-like and produces the daily CS brief.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def health_score(
    *,
    proof_delivered: int = 0,
    response_rate: float = 0.0,
    onboarding_complete: bool = False,
    sla_breached: bool = False,
    upgrade_signal: bool = False,
) -> float:
    """Composite health score 0..1 used to prioritize CS attention."""
    return round(
        (1.0 if proof_delivered > 0 else 0.0) * 0.30
        + max(0.0, min(1.0, response_rate)) * 0.20
        + (1.0 if onboarding_complete else 0.0) * 0.20
        + (0.0 if sla_breached else 1.0) * 0.15
        + (1.0 if upgrade_signal else 0.0) * 0.15,
        3,
    )


def build_brief(
    *,
    customers,
    tickets,
    sessions,
) -> dict[str, Any]:
    customers = list(customers or [])
    tickets = list(tickets or [])
    sessions = list(sessions or [])

    proof_delayed = sum(
        1 for s in sessions
        if s.status in ("ready_to_deliver", "delivered") and not s.proof_pack_url
    )
    onboarding_pending = sum(1 for c in customers if c.onboarding_status == "kickoff_pending")
    p0_open = sum(1 for t in tickets if t.priority == "P0" and t.status == "open")
    p1_open = sum(1 for t in tickets if t.priority == "P1" and t.status == "open")
    high_risk = sum(1 for c in customers if c.churn_risk == "high")
    upgrade_ready = sum(
        1 for s in sessions if s.status == "upgrade_pending"
    )

    decisions: list[dict[str, Any]] = []
    if p0_open:
        decisions.append({
            "type": "support_p0",
            "title_ar": f"{p0_open} تذكرة P0 مفتوحة",
            "why_now_ar": "P0 = أمان / إرسال خاطئ / تعطل — SLA ساعة واحدة.",
            "recommended_action_ar": "افتح التذكرة الآن + صعّد لإنسان مباشرة.",
            "risk_level": "high",
            "proof_impact": ["sla_met", "tickets_resolved"],
            "action_mode": "approval_required",
            "buttons_ar": ["افتح التذكرة", "صعّد", "تخطي"],
        })
    if proof_delayed > 0:
        decisions.append({
            "type": "proof_delay",
            "title_ar": f"{proof_delayed} Proof Pack متأخر",
            "why_now_ar": "كل تأخير في Proof Pack يخفض ثقة العميل وعقد renewal.",
            "recommended_action_ar": "جهّز التحديث + احجز Quarterly Review قصير.",
            "risk_level": "medium",
            "proof_impact": ["proof_generated"],
            "action_mode": "approval_required",
            "buttons_ar": ["جهّز Update", "احجز QBR", "صعّد"],
        })
    if upgrade_ready > 0:
        decisions.append({
            "type": "upgrade_opportunity",
            "title_ar": f"{upgrade_ready} عميل جاهز للترقية",
            "why_now_ar": "Proof Pack تسلّم — اللحظة المثلى لعرض Executive Growth OS.",
            "recommended_action_ar": "أرسل deck الترقية + احجز اجتماع 20 دقيقة.",
            "risk_level": "low",
            "proof_impact": ["upgrade_meetings"],
            "action_mode": "approval_required",
            "buttons_ar": ["جهّز deck", "احجز اجتماع", "تخطي"],
        })

    decisions = decisions[:3]

    return {
        "role": "customer_success",
        "brief_type": "daily_cs",
        "date": _now().date().isoformat(),
        "summary": {
            "customers_total": len(customers),
            "high_churn_risk": high_risk,
            "onboarding_pending": onboarding_pending,
            "proof_delayed": proof_delayed,
            "p0_open": p0_open,
            "p1_open": p1_open,
            "upgrade_ready": upgrade_ready,
        },
        "top_decisions": decisions,
        "blocked_today_ar": [
            "لا outbound بدون proof",
            "لا renewal upsell بدون Proof Pack مسلّم",
        ],
    }
