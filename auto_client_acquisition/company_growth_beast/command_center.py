"""Single command center view for Growth Beast."""

from __future__ import annotations

from typing import Any


def build_command_center(
    profile: dict[str, Any] | None,
    targets: list[dict[str, Any]] | None,
    offer: dict[str, Any] | None,
    content: dict[str, Any] | None,
    warm: dict[str, Any] | None,
    experiment: dict[str, Any] | None,
    support: dict[str, Any] | None,
    proof: dict[str, Any] | None,
) -> dict[str, Any]:
    top_segments = [t.get("segment_name_ar") for t in (targets or [])[:3]]
    best_offer = ""
    if offer and isinstance(offer.get("offer"), dict):
        best_offer = str(offer["offer"].get("offer_name_ar") or "")

    angle = ""
    if content and isinstance(content.get("linkedin_post_draft_ar"), str):
        angle = content["linkedin_post_draft_ar"][:120]

    next_exp = ""
    if experiment and isinstance(experiment.get("experiment"), dict):
        next_exp = str(experiment["experiment"].get("hypothesis") or "")

    proof_ok = bool(proof and proof.get("proof_events_suggested"))

    actions: list[dict[str, str]] = [
        {"ar": "راجع وأكد الشريحة المستهدفة الأولى", "mode": "approval_first"},
        {"ar": "راجع مسودة العرض وحدود «ما لا نعد به»", "mode": "approval_first"},
        {"ar": "اختر مساراً دافئاً واحداً للأسبوع (بدون قنوات محظورة)", "mode": "approval_first"},
    ]

    return {
        "schema_version": 1,
        "experience_layer": "company_growth_beast",
        "top_3_segments": top_segments,
        "top_3_targets": top_segments,
        "best_offer": best_offer or "unknown",
        "best_content_angle": angle or "unknown",
        "best_safe_route": str((warm or {}).get("primary_route_ar") or "warm_intro_or_partner"),
        "next_experiment": next_exp or "unknown",
        "proof_available": "yes" if proof_ok else "no",
        "blocked_actions": [
            "auto_send",
            "live_charge",
            "cold_whatsapp",
            "linkedin_automation",
            "scraping",
            "fake_proof",
        ],
        "founder_approval_queue": [
            "مسودات المحتوى قبل أي نشر",
            "أي رسالة خارجية يدوية مع سجل موافقة",
            "أي proof علني أو شهادة عميل",
        ],
        "next_best_actions": actions,
        "language_primary": "ar",
    }
