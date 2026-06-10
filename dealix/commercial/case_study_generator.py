"""Case Study Generator — builds LinkedIn-ready case studies from proof packs.

Constitutional gate: NO_UNAPPROVED_TESTIMONIAL — customer_consent required.
Output: bilingual AR+EN 1-page case study.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class CaseStudyRequest(BaseModel):
    account_id: str = Field(..., min_length=1)
    company_name: str = Field(..., min_length=1)
    sector: str = "b2b_services"
    proof_pack_id: str = ""
    customer_consent: bool = False
    anonymize: bool = False
    challenge_ar: str = ""
    challenge_en: str = ""
    approach_ar: str = ""
    approach_en: str = ""
    result_ar: str = ""
    result_en: str = ""
    customer_quote_ar: str = ""
    customer_quote_en: str = ""


class CaseStudyDocument(BaseModel):
    study_id: str
    account_id: str
    display_name: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    markdown_ar_en: str
    linkedin_post_ar: str = ""
    linkedin_post_en: str = ""
    is_consent_verified: bool = False
    approval_status: str = "approval_required"
    governance_decision: str = "pending"  # pending | approved | rejected

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.model_dump_json())


class CaseStudyGenerator:
    """Generates case studies — requires customer consent to include any quote."""

    def generate(self, req: CaseStudyRequest) -> CaseStudyDocument:
        import hashlib

        assert not (
            req.customer_quote_ar and not req.customer_consent
        ), "NO_UNAPPROVED_TESTIMONIAL: customer_consent must be True to include a quote"

        study_id = hashlib.sha256(
            f"{req.account_id}{datetime.now(UTC).date()}".encode()
        ).hexdigest()[:16]

        display_name = (
            "شركة سعودية في " + req.sector
            if req.anonymize
            else req.company_name
        )

        md = self._render_markdown(req, display_name, study_id)
        linkedin_ar = self._linkedin_post_ar(req, display_name)
        linkedin_en = self._linkedin_post_en(req, display_name)

        return CaseStudyDocument(
            study_id=study_id,
            account_id=req.account_id,
            display_name=display_name,
            markdown_ar_en=md,
            linkedin_post_ar=linkedin_ar,
            linkedin_post_en=linkedin_en,
            is_consent_verified=req.customer_consent,
        )

    def _render_markdown(self, req: CaseStudyRequest, name: str, study_id: str) -> str:
        now = datetime.now(UTC).strftime("%Y-%m-%d")
        quote_section = ""
        if req.customer_consent and req.customer_quote_ar:
            quote_section = f"""
## شهادة العميل / Customer Testimonial

> "{req.customer_quote_ar}"

> *"{req.customer_quote_en}"*
"""
        return f"""# قصة نجاح — {name}
**Case Study — {name}**

المعرف: `{study_id}` | التاريخ: {now} | القطاع: {req.sector}
الحالة: **يتطلب موافقة المؤسس** | الموافقة: {"✅ معطاة" if req.customer_consent else "⏳ مطلوبة"}

---

## التحدي / Challenge

**{req.challenge_ar or "يُحدَّد عند الاكتمال."}**

*{req.challenge_en or "To be completed."}*

---

## المنهجية / Approach

**{req.approach_ar or "يُحدَّد عند الاكتمال."}**

*{req.approach_en or "To be completed."}*

---

## النتائج / Results

**{req.result_ar or "يُحدَّد عند الاكتمال."}**

*{req.result_en or "To be completed."}*

{quote_section}

---

> قصة النجاح هذه للمراجعة الداخلية فقط.
> موافقة العميل {"✅ تمت" if req.customer_consent else "⏳ مطلوبة قبل النشر"}.
>
> **القيمة التقديرية ليست قيمة مُتحقَّقة** — Estimated value is not Verified value.
"""

    def _linkedin_post_ar(self, req: CaseStudyRequest, name: str) -> str:
        return f"""🎯 قصة نجاح: {name}

التحدي: {req.challenge_ar or '[يُكمَل لاحقاً]'}

ما فعلناه في 7 أيام:
{req.approach_ar or '[يُكمَل لاحقاً]'}

النتيجة:
✅ {req.result_ar or '[يُكمَل لاحقاً]'}

هذا ما يعنيه Dealix: نتائج قابلة للقياس، موثقة، وقابلة للتحقق.

هل شركتك تستحق نفس النتائج؟
← تشخيص مجاني: [رابط]

#Dealix #B2BSaudi #RevenueOps #السعودية
"""

    def _linkedin_post_en(self, req: CaseStudyRequest, name: str) -> str:
        return f"""🎯 Success Story: {name}

Challenge: {req.challenge_en or '[to be completed]'}

What we did in 7 days:
{req.approach_en or '[to be completed]'}

Result:
✅ {req.result_en or '[to be completed]'}

This is what Dealix means: measurable results, documented, verifiable.

Does your company deserve the same results?
← Free diagnostic: [link]

#Dealix #B2BSaudi #RevenueOps
"""
