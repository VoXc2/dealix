"""
Finance OS — invoices ready / sent / paid + partner commission expected.

No live charge, no auto-pay. The brief lists invoices that NEED manual
operator action (since MOYASAR_ALLOW_LIVE_CHARGE is hard-False).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def build_brief(
    *,
    sessions,
    payments,
    expected_partner_commission_sar: float = 0.0,
) -> dict[str, Any]:
    sessions = list(sessions or [])
    payments = list(payments or [])

    invoices_ready = sum(
        1 for s in sessions
        if s.status == "ready_to_deliver" and s.service_id == "growth_starter"
    )
    paid_this_week = sum(
        1 for p in payments if p.status == "paid"
    )
    refunded = sum(1 for p in payments if p.status == "refunded")

    decisions: list[dict[str, Any]] = []
    if invoices_ready > 0:
        decisions.append({
            "type": "invoice_ready",
            "title_ar": f"{invoices_ready} فاتورة Pilot 499 جاهزة للإرسال (يدوياً)",
            "why_now_ar": "Live charge مغلق — Moyasar invoice manual فقط.",
            "recommended_action_ar": "افتح Moyasar dashboard + أنشئ invoice + أرسل الرابط بعد الموافقة.",
            "risk_level": "low",
            "proof_impact": ["payment_link_drafted", "invoice_requested"],
            "action_mode": "approval_required",
            "buttons_ar": ["افتح Moyasar", "ابعث الرابط", "تخطي"],
        })
    if expected_partner_commission_sar > 0:
        decisions.append({
            "type": "partner_commission",
            "title_ar": f"عمولة شريك متوقعة: {expected_partner_commission_sar:.2f} ر.س",
            "why_now_ar": "Subscriptions نشطة منسوبة لشريك — العمولة الشهرية تستحق.",
            "recommended_action_ar": "راجع scorecard الشريك + جهّز payout (manual transfer).",
            "risk_level": "low",
            "proof_impact": ["payout_drafted"],
            "action_mode": "approval_required",
            "buttons_ar": ["راجع Scorecard", "جهّز payout", "تخطي"],
        })

    decisions = decisions[:3]

    return {
        "role": "finance",
        "brief_type": "daily_finance",
        "date": _now().date().isoformat(),
        "summary": {
            "invoices_ready": invoices_ready,
            "paid_this_week": paid_this_week,
            "refunded": refunded,
            "expected_partner_commission_sar": float(expected_partner_commission_sar or 0.0),
        },
        "top_decisions": decisions,
        "blocked_today_ar": [
            "لا live charge — Moyasar manual فقط",
            "لا auto-renew بدون موافقة عميل",
            "لا تغيير سعر بدون policy approval",
        ],
    }
