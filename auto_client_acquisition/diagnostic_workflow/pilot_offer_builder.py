"""Bilingual quote-only Revenue Command Pilot scope builder."""
from __future__ import annotations

from auto_client_acquisition.diagnostic_workflow.schemas import (
    DiagnosticBundle,
    PilotOffer,
)

_DESCRIPTION_AR = (
    "Revenue Command Pilot بنطاق ومدة مخصصين للحالة ومراجعة المؤسس "
    "لكلّ خطوة. السعر والنطاق والمدة تحدد في quote موثق بعد جلسة الاكتشاف."
)
_DESCRIPTION_EN = (
    "A Revenue Command Pilot with customer-specific scope and duration and founder "
    "review at every step. Price, scope, and duration are set in a documented quote after discovery."
)
_TERMS_AR = (
    "لا فاتورة ولا رابط دفع قبل اعتماد quote ومسار الدفع. لا يوجد التزام "
    "بأرقام إيرادات أو ترتيب — نلتزم بالنطاق والـ Proof Pack فقط. "
    "نلتزم بنظام حماية البيانات الشخصية (PDPL)."
)
_TERMS_EN = (
    "No invoice or payment link before quote and payment-path approval. "
    "No revenue or ranking commitment — only the scoped work + Proof Pack. "
    "PDPL-aware end-to-end."
)


def build_pilot_offer(bundle: DiagnosticBundle) -> PilotOffer:
    """Compose the bilingual quote-only pilot scope for the bundle."""
    return PilotOffer(
        company=bundle.company,
        recommended_bundle=bundle.recommended_bundle,
        amount_sar=None,
        description_ar=_DESCRIPTION_AR,
        description_en=_DESCRIPTION_EN,
        terms_ar=_TERMS_AR,
        terms_en=_TERMS_EN,
        payment_url=None,
    )
