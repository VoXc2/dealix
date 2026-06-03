"""
Build DecisionPassport from Phase-8 PipelineResult.
"""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.decision_passport.schema import DecisionPassport, ScoreBoard
from auto_client_acquisition.pipeline import PipelineResult


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def _data_quality(lead_dict: dict[str, Any]) -> float:
    score = 0.0
    if lead_dict.get("contact_email"):
        score += 0.35
    if lead_dict.get("contact_phone"):
        score += 0.25
    if lead_dict.get("message"):
        score += 0.25
    if lead_dict.get("sector"):
        score += 0.15
    return _clamp(score)


def _intent_from_extraction(extraction: dict[str, Any] | None) -> float:
    if not extraction:
        return 0.25
    pains = extraction.get("pain_points") or []
    urgency = float(extraction.get("urgency_score") or 0.0)
    pain_n = len(pains) if isinstance(pains, list) else 0
    pain_part = _clamp(0.2 + 0.15 * min(pain_n, 3))
    return _clamp(0.5 * pain_part + 0.5 * _clamp(urgency))


def _revenue_potential(fit: dict[str, Any] | None, budget: float | None) -> float:
    base = 0.35
    if fit:
        base = float(fit.get("overall_score") or 0.35)
    if budget and budget >= 50_000:
        base += 0.15
    elif budget and budget >= 20_000:
        base += 0.08
    return _clamp(base)


def _engagement(qual: dict[str, Any] | None, data_q: float) -> float:
    if not qual:
        return _clamp(0.25 + 0.5 * data_q)
    bant = float(qual.get("bant_score") or 0.0)
    return _clamp(0.3 * bant + 0.4 * data_q + 0.3 * min(1.0, len(qual.get("questions") or []) / 5))


def _warm_route(tier: str, source: str) -> float:
    t = tier.upper()
    if t == "A":
        return 0.95
    if t == "B":
        return 0.75
    if t == "C":
        return 0.55
    inbound = source.lower() in {"website", "inbound", "referral", "partner"}
    return 0.45 if inbound else 0.35


def _compliance_risk(source: str) -> float:
    s = source.lower()
    if s in {"purchased_list", "scraped", "unknown"}:
        return 0.85
    if s in {"website", "inbound", "referral", "partner"}:
        return 0.15
    return 0.35


def _deliverability_risk(lead_dict: dict[str, Any]) -> float:
    if lead_dict.get("contact_email"):
        return 0.25
    return 0.65


def _priority_bucket(tier: str, urgency: float, compliance: float) -> str:
    if compliance >= 0.7:
        return "BLOCKED"
    if tier == "A" and urgency >= 0.5:
        return "P0_NOW"
    if tier in {"A", "B"}:
        return "P1_THIS_WEEK"
    if tier == "C":
        return "P2_NURTURE"
    return "P3_LOW_PRIORITY"


def _why_now(
    fit: dict[str, Any] | None,
    extraction: dict[str, Any] | None,
    sector: str | None,
    region: str | None,
) -> tuple[str, str]:
    reasons = (fit or {}).get("reasons") or []
    reason_txt = "؛ ".join(str(r) for r in reasons[:3]) if reasons else "مطابقة قطاع وميزانية ضمن النطاق المستهدف"
    pain_txt = ""
    if extraction and extraction.get("key_phrases"):
        kp = extraction["key_phrases"]
        if isinstance(kp, list) and kp:
            pain_txt = " — نقاط ألم: " + "، ".join(str(x) for x in kp[:3])
    ar = f"قطاع {sector or 'غير محدد'} في {region or 'السعودية'}. {reason_txt}{pain_txt}"
    en = (
        f"Sector {sector or 'unknown'} in {region or 'GCC'}. "
        f"{'; '.join(str(r) for r in reasons[:3]) if reasons else 'ICP alignment within target range.'}"
        f"{(' Pain signals: ' + ', '.join(str(x) for x in (extraction or {}).get('key_phrases', [])[:3])) if extraction and extraction.get('key_phrases') else ''}"
    )
    return ar, en


def _recommended_action(tier: str, priority: str) -> tuple[str, str, str]:
    if priority == "BLOCKED":
        return (
            "compliance_review",
            "مراجعة امتثال ومصدر البيانات قبل أي تواصل",
            "Compliance review — validate source and consent before outreach",
        )
    if tier == "A":
        return (
            "prepare_mini_diagnostic",
            "تحضير تشخيص مصغّر وجدولة جلسة اكتشاف خلال 48 ساعة",
            "Prepare mini diagnostic and book discovery within 48h",
        )
    if tier == "B":
        return (
            "prepare_mini_diagnostic",
            "تأهيل قصير عبر بريد/قناة دافئة ثم تشخيص مصغّر",
            "Short qualification via warm channel then mini diagnostic",
        )
    if tier == "C":
        return (
            "nurture_sequence",
            "تسلسل قيمة (محتوى/لقاء) قبل طلب اجتماع",
            "Value-add nurture before asking for a meeting",
        )
    return (
        "long_term_nurture",
        "إبقاء في المراقبة أو إعادة تعريف ICP",
        "Monitor or refine ICP fit",
    )


def _proof_target(tier: str) -> tuple[str, str]:
    if tier in {"A", "B"}:
        return "demo_booked", "حجز عرض أو جلسة اكتشاف مع قرار"
    return "internal_proof_draft", "مسودة دليل داخلي (قائمة فرص مرتّبة + خطة متابعة)"


def build_from_pipeline_result(result: PipelineResult) -> DecisionPassport:
    """Construct a DecisionPassport from a full pipeline run."""
    lead = result.lead
    lead_d = lead.to_dict()
    fit_d = result.fit_score.to_dict() if result.fit_score else None
    ext_d = result.extraction.to_dict() if result.extraction else None
    qual_d = result.qualification.to_dict() if result.qualification else None

    tier = (fit_d or {}).get("tier") or "D"
    if hasattr(result.fit_score, "tier"):
        tier = result.fit_score.tier  # type: ignore[union-attr]

    urgency = float(lead.urgency_score or 0.0)
    budget = lead.budget if getattr(lead, "budget", None) is not None else lead_d.get("budget")

    scores = ScoreBoard(
        fit_score=float((fit_d or {}).get("overall_score") or 0.0),
        intent_score=_intent_from_extraction(ext_d),
        urgency_score=_clamp(urgency),
        revenue_potential_score=_revenue_potential(fit_d, float(budget) if budget is not None else None),
        data_quality_score=_data_quality(lead_d),
        warm_route_score=_warm_route(str(tier), lead.source.value if hasattr(lead.source, "value") else str(lead.source)),
        compliance_risk_score=_compliance_risk(lead.source.value if hasattr(lead.source, "value") else str(lead.source)),
        deliverability_risk_score=_deliverability_risk(lead_d),
        engagement_score=_engagement(qual_d, _data_quality(lead_d)),
    )

    priority = _priority_bucket(str(tier), urgency, scores.compliance_risk_score)
    why_ar, why_en = _why_now(fit_d, ext_d, lead.sector, lead.region)
    action_key, action_ar, action_en = _recommended_action(str(tier), priority)
    proof_key, proof_ar = _proof_target(str(tier))

    blocked = [
        "cold_whatsapp",
        "linkedin_automation",
        "scraping",
        "purchased_list_bulk",
    ]

    open_q = len([q for q in (qual_d or {}).get("questions", []) if not q.get("answered")])
    qual_status = (qual_d or {}).get("new_status") if qual_d else None

    return DecisionPassport(
        lead_id=lead.id,
        company=lead.company_name,
        contact_name=lead.contact_name,
        source=lead.source.value if hasattr(lead.source, "value") else str(lead.source),
        locale=lead.locale or "ar",
        why_now_ar=why_ar,
        why_now_en=why_en,
        icp_tier=str(tier),
        priority_bucket=priority,  # type: ignore[arg-type]
        scores=scores,
        best_channel="email_draft_approval_first",
        recommended_action=action_key,
        recommended_action_ar=action_ar,
        blocked_actions=blocked,
        proof_target=proof_key,
        proof_target_ar=proof_ar,
        next_step_ar=action_ar,
        next_step_en=action_en,
        bant_open_count=open_q,
        qualification_status=str(qual_status) if qual_status is not None else None,
        meta={
            "pipeline_warnings": result.warnings,
            "fit_tier": str(tier),
            "budget_hint": budget,
        },
    )
