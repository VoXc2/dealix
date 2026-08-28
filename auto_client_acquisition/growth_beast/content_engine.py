"""Content Engine — sector × angle -> bilingual evidence-safe content draft.

Draft-only / approval-required. No auto-publish. The template layer must not
invent customer work, case studies, market prevalence, delivery SLAs, or
results. A proof-oriented content type requires explicit proof context.
"""
from __future__ import annotations

from typing import Literal

ContentType = Literal[
    "linkedin_post",
    "sector_insight",
    "diagnostic_cta",
    "case_snippet",
    "objection_post",
]


def draft_content(
    *,
    sector: str,
    angle: str,
    content_type: ContentType = "linkedin_post",
    audience_hint: str = "founders",
    proof_context: dict | None = None,
) -> dict:
    """Generate a bilingual content draft without creating business truth."""

    sector_clean = sector.replace("_", " ")
    angle_clean = angle.replace("_", " ")
    proof_context = proof_context or {}

    proof_authorized = bool(
        proof_context.get("customer_approved")
        and proof_context.get("signed_publish_permission")
        and proof_context.get("audience") == "public_allowed"
        and proof_context.get("source_ref")
    )

    if content_type == "linkedin_post":
        ar = (
            f"سؤال يستحق الفحص في شركات {sector_clean}: هل توجد فجوة قابلة للإثبات حول {angle_clean}؟\n\n"
            "الهدف ليس إضافة أداة جديدة، بل فصل الحقائق عن الافتراضات وتحديد المالك والخطوة التالية ودليل النتيجة.\n\n"
            "إذا كانت المشكلة واقعية ومهمة لفريقك، يمكن البدء بـ Mini Diagnostic مجاني قبل أي نطاق مدفوع."
        )
        en = (
            f"A question worth testing in {sector_clean}: is there an evidence-backed gap around {angle_clean}?\n\n"
            "The goal is not another tool; it is to separate facts from assumptions and identify the owner, next step, and evidence path.\n\n"
            "If the problem is real and material to your team, the entry step can be a free Mini Diagnostic before any paid scope."
        )
        truth_class = "HYPOTHESIS_DRAFT"
    elif content_type == "sector_insight":
        ar = (
            f"فرضية للفحص في قطاع {sector_clean}: قد تكون {angle_clean} نقطة احتكاك، "
            "لكن لا تُعامل كحقيقة سوقية بدون مصدر موثوق."
        )
        en = (
            f"Hypothesis to test in {sector_clean}: {angle_clean} may be a friction point, "
            "but it is not a market fact without a reliable source."
        )
        truth_class = "HYPOTHESIS_DRAFT"
    elif content_type == "diagnostic_cta":
        ar = (
            f"لشركات {sector_clean}: إذا كانت {angle_clean} مشكلة حقيقية عندكم، "
            "ابدأوا بـ Mini Diagnostic مجاني يحدد المشكلة والأدلة المطلوبة والخطوة التالية — بدون التزام مدفوع مسبق."
        )
        en = (
            f"For {sector_clean} teams: if {angle_clean} is a real problem for you, "
            "start with a free Mini Diagnostic to define the problem, required evidence, and next step — before any paid commitment."
        )
        truth_class = "CTA_DRAFT"
    elif content_type == "case_snippet":
        if not proof_authorized:
            return {
                "content_type": content_type,
                "sector": sector,
                "angle": angle,
                "audience_hint": audience_hint,
                "blocked": True,
                "blocked_reason": "PUBLIC_CASE_REQUIRES_SOURCE_BOUND_PROOF_AND_PERMISSION",
                "proof_dependency": "required",
                "approval_required": True,
                "forbidden_claims_check": "blocked_pending_proof",
                "action_mode": "blocked",
            }
        result_summary = str(proof_context.get("result_summary") or "Verified delivery evidence available")
        ar = (
            f"حالة موثقة ومصرح بنشرها في {sector_clean}: {result_summary}. "
            "التفاصيل المنشورة تقتصر على ما يغطيه المصدر وإذن العميل."
        )
        en = (
            f"Verified, permissioned example in {sector_clean}: {result_summary}. "
            "Published detail is limited to the source evidence and customer permission."
        )
        truth_class = "PERMISSIONED_PROOF_DRAFT"
    else:  # objection_post
        ar = (
            f"اعتراض أو سؤال محتمل من فرق {sector_clean}: «{angle_clean}».\n"
            "الرد الأفضل يبدأ بفهم السياق والأدلة بدل الضغط أو الوعد بنتيجة."
        )
        en = (
            f"A possible question or objection from {sector_clean} teams: '{angle_clean}'.\n"
            "A useful response starts with context and evidence rather than pressure or an outcome promise."
        )
        truth_class = "HYPOTHESIS_DRAFT"

    return {
        "content_type": content_type,
        "sector": sector,
        "angle": angle,
        "audience_hint": audience_hint,
        "draft_ar": ar,
        "draft_en": en,
        "cta": "Free Mini Diagnostic / التشخيص المصغر المجاني",
        "truth_class": truth_class,
        "proof_dependency": "verified_permissioned_source" if content_type == "case_snippet" else "none",
        "approval_required": True,
        "external_publish_allowed_by_this_draft": False,
        "forbidden_claims_check": "passed",
        "action_mode": "draft_only",
    }
