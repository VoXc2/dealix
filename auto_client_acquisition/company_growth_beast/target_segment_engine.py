"""Rank 2–3 target segments from profile text."""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.company_growth_beast.schemas import TargetSegment


def _score_from_text(hay: str, needle: str, base: int) -> int:
    if not needle.strip():
        return max(0, base - 25)
    return min(100, base + (15 if needle.lower() in hay.lower() else 0))


def rank_target_segments(profile: dict[str, Any]) -> list[dict[str, Any]]:
    sector = str(profile.get("sector") or "unknown")
    offer = str(profile.get("offer") or "")
    ideal = str(profile.get("ideal_customer") or "")
    hay = f"{sector} {offer} {ideal}".lower()
    hay_ar = f"{profile.get('sector') or ''} {offer} {ideal}"

    templates: list[TargetSegment] = [
        TargetSegment(
            segment_name_ar="وكالات تسويق صغيرة ومتوسطة",
            segment_name_en="SMB marketing agencies",
            pain="ضغط إثبات قيمة لعملائهم",
            buying_trigger="عقد جديد أو تجديد يحتاج reporting أوضح",
            fit_score=max(_score_from_text(hay, "agency", 72), 78 if "وكالة" in hay_ar or "وكالات" in hay_ar else 0),
            urgency_score=65,
            proof_potential_score=88,
            access_score=70,
            risk_score=25,
            recommended_route="warm_intro_or_partner",
            reason="سهل ربط التسليم بـ Proof Pack",
        ),
        TargetSegment(
            segment_name_ar="خدمات B2B",
            segment_name_en="B2B services firms",
            pain="متابعة طويلة واعتراضات متكررة",
            buying_trigger="توسع فريق مبيعات أو مشروع كبير",
            fit_score=_score_from_text(hay, "b2b", 78),
            urgency_score=60,
            proof_potential_score=72,
            access_score=65,
            risk_score=30,
            recommended_route="inbound_diagnostic_then_manual_followup",
            reason="مناسب لمسارات متابعة آمنة",
        ),
        TargetSegment(
            segment_name_ar="استشارات وتدريب",
            segment_name_en="Consulting and training",
            pain="توضيح العرض والتسجيل في البرامج",
            buying_trigger="موسم تسجيل أو حملة محتوى",
            fit_score=_score_from_text(hay, "consult", 68),
            urgency_score=55,
            proof_potential_score=80,
            access_score=60,
            risk_score=28,
            recommended_route="content_cta_and_webinar_draft",
            reason="محتوى يدعم الثقة قبل الإغلاق",
        ),
    ]
    ranked = sorted(templates, key=lambda s: (s.fit_score + s.proof_potential_score), reverse=True)
    return [s.model_dump() for s in ranked]
