"""Weekly growth report composed from session artifacts."""

from __future__ import annotations

from typing import Any


def build_weekly_growth_report(
    profile: dict[str, Any] | None,
    targets: list[dict[str, Any]] | None,
    offer: dict[str, Any] | None,
    experiment: dict[str, Any] | None,
    support: dict[str, Any] | None,
    proof: dict[str, Any] | None,
) -> dict[str, Any]:
    best_seg = str((targets or [{}])[0].get("segment_name_ar", "")) if targets else "غير محدد"
    best_offer = ""
    if offer and isinstance(offer.get("offer"), dict):
        best_offer = str(offer["offer"].get("offer_name_ar") or "")

    exp_hyp = ""
    if experiment and isinstance(experiment.get("experiment"), dict):
        exp_hyp = str(experiment["experiment"].get("hypothesis") or "")

    support_lines: list[str] = []
    if support and support.get("themes"):
        support_lines = [f"موضوع دعم: {t}" for t in support["themes"][:5]]

    proof_count = 0
    if proof and isinstance(proof.get("proof_events_suggested"), list):
        proof_count = len(proof["proof_events_suggested"])

    return {
        "schema_version": 1,
        "weekly_growth_report": {
            "best_segment": best_seg,
            "best_offer": best_offer or "غير محدد بعد",
            "best_message_angle": "وضوح القيمة بدون وعود رقمية",
            "what_worked": [exp_hyp] if exp_hyp else ["بيانات غير كافية — راجع التجارب الأسبوع القادم"],
            "what_failed": [] if exp_hyp else ["لم تُسجّل تجارب بعد"],
            "proof_events": [f"proof_events_suggested_count={proof_count}"],
            "support_insights": support_lines or ["لا توجد تذاكر مجمّعة هذا الأسبوع"],
            "next_experiment": "كرر بزاوية رسالة مختلفة بعد مراجعة المسودات",
            "top_3_decisions": [
                "اعتماد الشريحة الأولى أو تغييرها",
                "اعتماد العرض المقترح أو تعديل حدود الوعد",
                "اعتماد مسار دافئ واحد فقط للأسبوع القادم",
            ],
            "blocked_actions": [
                "cold_whatsapp",
                "linkedin_automation",
                "web_scraping",
                "live_send_without_approval",
                "moyasar_live_charge",
            ],
        },
        "action_mode": "draft_only",
        "language_primary": "ar",
    }
