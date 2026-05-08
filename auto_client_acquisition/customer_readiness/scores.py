"""
Compute Customer Comfort Score and Expansion Readiness (0–100).

Inputs are intentionally plain dicts so routers can pass DB/portal aggregates later.
"""

from __future__ import annotations

from typing import Any


def compute_comfort_and_expansion(
    *,
    has_status_timeline: bool = False,
    has_next_action: bool = False,
    pending_approvals: int = 0,
    open_support_tickets: int = 0,
    proof_events_count: int = 0,
    max_proof_level: int = 0,
    payment_ok: bool = False,
    delivery_sessions_active: int = 0,
    avg_response_hours: float | None = None,
) -> dict[str, Any]:
    """Return comfort_score, expansion_readiness, and breakdown."""
    comfort = 50.0
    if has_status_timeline:
        comfort += 12.0
    if has_next_action:
        comfort += 13.0
    comfort -= min(20.0, pending_approvals * 5.0)
    comfort -= min(15.0, open_support_tickets * 3.0)
    if proof_events_count > 0:
        comfort += 10.0
    if avg_response_hours is not None and avg_response_hours <= 24:
        comfort += 10.0
    elif avg_response_hours is not None and avg_response_hours > 72:
        comfort -= 10.0
    comfort = max(0.0, min(100.0, comfort))

    expansion = 25.0
    expansion += min(25.0, proof_events_count * 5.0)
    expansion += min(20.0, max_proof_level * 4.0)
    if payment_ok:
        expansion += 15.0
    expansion += min(15.0, delivery_sessions_active * 5.0)
    expansion = max(0.0, min(100.0, expansion))

    return {
        "customer_comfort_score": round(comfort, 1),
        "expansion_readiness_score": round(expansion, 1),
        "breakdown": {
            "has_status_timeline": has_status_timeline,
            "has_next_action": has_next_action,
            "pending_approvals": pending_approvals,
            "open_support_tickets": open_support_tickets,
            "proof_events_count": proof_events_count,
            "max_proof_level": max_proof_level,
            "payment_ok": payment_ok,
            "delivery_sessions_active": delivery_sessions_active,
        },
        "notes_ar": (
            "الدرجات تقديرية إلى أن تُربط ببيانات البوابة والدليل الفعلية."
        ),
        "notes_en": "Scores are heuristic until wired to portal + proof ledger aggregates.",
    }


def from_passport_meta(passport_dict: dict[str, Any]) -> dict[str, Any]:
    """Bootstrap readiness from a fresh Decision Passport (minimal signals)."""
    tier = (passport_dict.get("icp_tier") or "D").upper()
    priority = passport_dict.get("priority_bucket") or "P3_LOW_PRIORITY"
    proof_events = 0
    max_lv = 0
    if tier in {"A", "B"} and priority != "BLOCKED":
        proof_events = 0
        max_lv = 0
    return compute_comfort_and_expansion(
        has_status_timeline=False,
        has_next_action=True,
        pending_approvals=1 if priority in {"P0_NOW", "P1_THIS_WEEK"} else 0,
        proof_events_count=proof_events,
        max_proof_level=max_lv,
        payment_ok=False,
        delivery_sessions_active=0,
    )


def compute_pricing_power_score(
    *,
    max_proof_level: int = 0,
    demand_signal_count: int = 0,
    gross_margin_hint: float = 0.35,
    delivery_repeatability: float = 0.5,
    case_study_public_count: int = 0,
    customer_urgency: float = 0.5,
) -> dict[str, Any]:
    """
    Heuristic 0–100 «pricing power» — raises upside ceiling when proof + repeatability exist.

    gross_margin_hint, delivery_repeatability, customer_urgency are 0..1.
    """
    score = 20.0
    score += min(25.0, max_proof_level * 5.0)
    score += min(15.0, demand_signal_count * 3.0)
    score += max(0.0, min(15.0, gross_margin_hint * 40.0))
    score += max(0.0, min(15.0, delivery_repeatability * 25.0))
    score += min(15.0, case_study_public_count * 7.5)
    score += max(0.0, min(10.0, customer_urgency * 15.0))
    score = max(0.0, min(100.0, score))
    return {
        "pricing_power_score": round(score, 1),
        "inputs": {
            "max_proof_level": max_proof_level,
            "demand_signal_count": demand_signal_count,
            "gross_margin_hint": gross_margin_hint,
            "delivery_repeatability": delivery_repeatability,
            "case_study_public_count": case_study_public_count,
            "customer_urgency": customer_urgency,
        },
        "notes_ar": "لا تستخدم وحدة لرفع السعر بدون Proof وبيانات هامش فعلية.",
        "notes_en": "Do not use standalone — combine with proof events + real margin data.",
    }
