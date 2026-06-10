"""Wave 13 Phase 8 — Customer Churn Risk Model.

Dedicated model (per plan §34.2 Phase 8 — currently churn_risk_pct
is embedded inside HealthScore; this elevates it to a standalone
component with 5 explicit input signals + per-bucket recommended action.

Article 8: every score `is_estimate=True`; deterministic (no LLM v1).
Article 11: ~120 LOC — does NOT replace HealthScore; complements it.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

ChurnRiskBucket = Literal["low", "medium", "high", "critical"]


@dataclass(slots=True)
class ChurnRiskAssessment:
    customer_id: str
    risk_score: float  # 0-100 (higher = more risk)
    bucket: ChurnRiskBucket
    signals_active: list[str]  # which of the 5 signals fired
    drivers: list[str]  # human-readable reasons (bilingual-safe)
    recommended_action_ar: str
    recommended_action_en: str
    is_estimate: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _bucket_for(score: float) -> ChurnRiskBucket:
    if score >= 75:
        return "critical"
    if score >= 50:
        return "high"
    if score >= 25:
        return "medium"
    return "low"


def _recommended_action(bucket: ChurnRiskBucket, signals: list[str]) -> tuple[str, str]:
    """Per-bucket recommended next action (bilingual)."""
    if bucket == "critical":
        return (
            "اتصل بالعميل خلال ٢٤ ساعة. عرض حلّ مخصّص.",
            "Call the customer within 24 hours. Offer custom resolution.",
        )
    if bucket == "high":
        return (
            "أرسل رسالة شخصية من المؤسس. خصّص اجتماعًا خلال أسبوع.",
            "Send personal founder message. Schedule a call within 1 week.",
        )
    if bucket == "medium":
        return (
            "راجع آخر تفاعلات العميل. اعرض موارد إضافية.",
            "Review recent interactions. Offer additional resources.",
        )
    # low
    return (
        "متابعة عادية ضمن الإيقاع الأسبوعي.",
        "Continue normal weekly cadence.",
    )


def compute_churn_risk(
    *,
    customer_id: str,
    engagement_drop_pct: float = 0.0,         # % drop in engagement vs baseline
    support_escalations_last_30d: int = 0,    # ticket escalations
    payment_late_count: int = 0,              # # of late payments in last 90d
    nps_below_7: bool = False,                # detractor or passive at 6
    decision_maker_left: bool = False,        # confirmed DM departed
) -> ChurnRiskAssessment:
    """Compute churn risk from 5 explicit signals.

    Each signal contributes points (capped). Score is 0-100.
    All signals deterministic; no LLM. Article 8: is_estimate=True always.
    """
    score = 0.0
    signals: list[str] = []
    drivers: list[str] = []

    # Signal 1: engagement_drop (max 25 pts)
    if engagement_drop_pct >= 50:
        score += 25
        signals.append("engagement_drop")
        drivers.append(f"Engagement dropped {engagement_drop_pct:.0f}% vs baseline")
    elif engagement_drop_pct >= 25:
        score += 15
        signals.append("engagement_drop")
        drivers.append(f"Engagement down {engagement_drop_pct:.0f}%")
    elif engagement_drop_pct >= 10:
        score += 8
        drivers.append(f"Engagement slightly down ({engagement_drop_pct:.0f}%)")

    # Signal 2: support_escalations (max 20 pts)
    if support_escalations_last_30d >= 3:
        score += 20
        signals.append("support_escalations")
        drivers.append(f"{support_escalations_last_30d} support escalations in 30 days")
    elif support_escalations_last_30d >= 1:
        score += 10
        signals.append("support_escalations")
        drivers.append(f"{support_escalations_last_30d} support escalation(s) in 30 days")

    # Signal 3: payment_late (max 20 pts)
    if payment_late_count >= 2:
        score += 20
        signals.append("payment_late")
        drivers.append(f"{payment_late_count} late payments in 90 days")
    elif payment_late_count == 1:
        score += 10
        signals.append("payment_late")
        drivers.append("1 late payment in 90 days")

    # Signal 4: nps_below_7 (15 pts)
    if nps_below_7:
        score += 15
        signals.append("nps_below_7")
        drivers.append("NPS score < 7 (detractor or passive)")

    # Signal 5: decision_maker_left (20 pts — relationship reset risk)
    if decision_maker_left:
        score += 20
        signals.append("decision_maker_left")
        drivers.append("Primary decision-maker no longer with company")

    score = min(100.0, score)
    bucket = _bucket_for(score)
    rec_ar, rec_en = _recommended_action(bucket, signals)

    return ChurnRiskAssessment(
        customer_id=customer_id,
        risk_score=score,
        bucket=bucket,
        signals_active=signals,
        drivers=drivers[:5],  # cap to 5 most relevant
        recommended_action_ar=rec_ar,
        recommended_action_en=rec_en,
        is_estimate=True,
    )
