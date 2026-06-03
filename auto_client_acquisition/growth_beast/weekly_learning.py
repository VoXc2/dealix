"""Weekly learning summary — suggest_only insights from real data."""
from __future__ import annotations


def weekly_summary(*, signals: dict, intros_sent: int = 0,
                   replies: int = 0, diagnostics: int = 0,
                   pilots_offered: int = 0, paid_pilots: int = 0,
                   proof_events: int = 0) -> dict:
    """Compose a weekly learning summary from real (or zero) data."""
    reply_rate = (replies / intros_sent) if intros_sent else 0
    diag_rate = (diagnostics / replies) if replies else 0
    paid_rate = (paid_pilots / pilots_offered) if pilots_offered else 0

    if intros_sent == 0:
        status = "no_data_yet"
        next_ar = "ما زلنا في الأسبوع الأول — أرسل warm intros أولاً"
        next_en = "Still week one — send warm intros first."
    elif reply_rate < 0.2:
        status = "low_reply_rate"
        next_ar = "معدّل الردّ منخفض — جرّب قطاع أو رسالة مختلفة"
        next_en = "Reply rate low — try different sector or message."
    elif paid_pilots >= 1:
        status = "first_revenue"
        next_ar = "أوّل دفع! وثّق Proof Pack ثم upsell"
        next_en = "First payment! Document Proof Pack then upsell."
    else:
        status = "scaling_validation"
        next_ar = "تابع الـ pipeline؛ ركّز على conversion للـ pilot"
        next_en = "Continue pipeline; focus on pilot conversion."

    return {
        "status": status,
        "intros_sent": intros_sent,
        "replies": replies,
        "diagnostics": diagnostics,
        "pilots_offered": pilots_offered,
        "paid_pilots": paid_pilots,
        "proof_events": proof_events,
        "reply_rate": round(reply_rate, 3),
        "diagnostic_rate": round(diag_rate, 3),
        "paid_rate": round(paid_rate, 3),
        "signals_total": signals.get("total", 0) if signals else 0,
        "next_action_ar": next_ar,
        "next_action_en": next_en,
        "action_mode": "suggest_only",
    }
