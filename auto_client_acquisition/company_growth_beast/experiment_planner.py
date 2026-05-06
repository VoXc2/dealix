"""Plan one weekly growth experiment (safe, measurable, stoppable)."""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.company_growth_beast.schemas import GrowthExperiment


def plan_growth_experiment(
    profile: dict[str, Any],
    targets: list[dict[str, Any]] | None,
    offer: dict[str, Any] | None,
) -> dict[str, Any]:
    seg = (targets or [{}])[0] if targets else {}
    seg_name = str(seg.get("segment_name_ar") or "الشريحة الأولى")
    offer_name = ""
    if offer and isinstance(offer.get("offer"), dict):
        offer_name = str(offer["offer"].get("offer_name_ar") or "")

    exp = GrowthExperiment(
        hypothesis=f"إذا ركزنا على {seg_name} فسيزيد طلب التشخيص (مقاس يدوي).",
        target_segment=seg_name,
        offer=offer_name or "عرض السبrint الأسبوعي",
        channel="inbound + warm_intro",
        safe_action="نشر مسودة واحدة بعد موافقة + رابط تشخيص يدوي",
        success_metric="عدد طلبات التشخيص المسجلة يدوياً",
        expected_learning="هل الشريحة تستجيب للزاوية الحالية؟",
        stop_condition="بعد 7 أيام أو صفر تفاعل مؤكد — إيقاف التجربة ومراجعة الرسالة",
        action_mode="draft_only",
    )
    return {"schema_version": 1, "experiment": exp.model_dump(), "action_mode": "draft_only"}
