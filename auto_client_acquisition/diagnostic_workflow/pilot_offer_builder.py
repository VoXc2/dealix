"""Bilingual 499-SAR pilot offer builder.

Price is FIXED at 499 SAR via the schema's ``Literal[499]`` — the
builder takes no price parameter. Output text is intentionally bland
(no marketing claims, no forbidden vocabulary).
"""
from __future__ import annotations

from auto_client_acquisition.diagnostic_workflow.schemas import (
    DiagnosticBundle,
    PilotOffer,
)

_DESCRIPTION_AR = (
    "Pilot لمدّة 7 أيّام يشمل الباقة الموصى بها مع مراجعة المؤسس "
    "لكلّ خطوة. السعر التعريفي 499 ريال — لا يوجد خصم تلقائي."
)
_DESCRIPTION_EN = (
    "7-day pilot covering the recommended bundle with founder review "
    "at every step. Introductory price 499 SAR — no auto-charge."
)
_TERMS_AR = (
    "الدفع عبر Moyasar (وضع الاختبار) بإشراف المؤسس. لا يوجد التزام "
    "بأرقام إيرادات أو ترتيب — نلتزم بالعمل والـ Proof Pack فقط. "
    "نلتزم بنظام حماية البيانات الشخصية (PDPL)."
)
_TERMS_EN = (
    "Payment via Moyasar (test mode) under founder supervision. "
    "No revenue or ranking commitment — only the work + Proof Pack. "
    "PDPL-aware end-to-end."
)


def build_pilot_offer(bundle: DiagnosticBundle) -> PilotOffer:
    """Compose the bilingual 499-SAR pilot offer for the bundle."""
    return PilotOffer(
        company=bundle.company,
        recommended_bundle=bundle.recommended_bundle,
        amount_sar=499,
        description_ar=_DESCRIPTION_AR,
        description_en=_DESCRIPTION_EN,
        terms_ar=_TERMS_AR,
        terms_en=_TERMS_EN,
        payment_url=None,
    )
