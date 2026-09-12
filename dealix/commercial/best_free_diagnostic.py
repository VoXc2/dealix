"""Best Free Diagnostic — evidence-governed free entry point across Dealix sectors."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.low_touch_products.diagnostic_product import (
    DiagnosticProductEngine,
    DiagnosticProductRequest,
)
from dealix.commercial.universal_diagnostic_factory import (
    DiagnosticDepth,
    UniversalDiagnosticFactory,
)

UNKNOWN = "UNKNOWN"


class BestFreeDiagnosticOffer(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    offer_id: str
    title_ar: str
    title_en: str
    value_ar: str
    value_en: str
    price: str = "مجاني"
    agents: list[str] = Field(
        default_factory=lambda: [
            "dealix-pm",
            "dealix-sales",
            "dealix-delivery",
            "dealix-engineer",
            "dealix-content",
        ]
    )
    channels: list[str] = Field(
        default_factory=lambda: [
            "website",
            "email_consent",
            "whatsapp_opt_in",
            "partner",
        ]
    )


BEST_OFFERS: list[BestFreeDiagnosticOffer] = [
    BestFreeDiagnosticOffer(
        offer_id="free_diagnostic_evidence_pack",
        title_ar="تشخيص مجاني — حزمة أدلة",
        title_en="Free Diagnostic — Evidence Pack",
        value_ar="خريطة اختناقات وفرص وتوصيات مبنية على الأدلة المتاحة دون ادعاء عائد غير مثبت",
        value_en="Evidence-based bottleneck/opportunity map and recommendations with no fabricated ROI",
    ),
    BestFreeDiagnosticOffer(
        offer_id="ai_readiness_free",
        title_ar="تقييم جاهزية الذكاء الاصطناعي مجاني",
        title_en="Free AI Readiness Scan",
        value_ar="جاهزية وحوكمة الذكاء الاصطناعي مع فجوات الأدلة والخطوات التالية",
        value_en="AI readiness/governance with evidence gaps and next actions",
    ),
    BestFreeDiagnosticOffer(
        offer_id="fatoora_free",
        title_ar="فحص جاهزية فاتورة مجاني",
        title_en="Free Fatoora Readiness Check",
        value_ar="فجوات الفوترة والتكامل والاختبار والتشغيل دون تقديم استشارة ضريبية أو قانونية",
        value_en="E-invoicing integration, testing and operating readiness gaps; not tax/legal advice",
    ),
    BestFreeDiagnosticOffer(
        offer_id="supplier_readiness_free",
        title_ar="فحص جاهزية المورد مجاني",
        title_en="Free Supplier Readiness Check",
        value_ar="فجوات المستندات والتأهيل والمناقصات وسير العمل دون ادعاء وصول مميز",
        value_en="Supplier qualification, documents, bid readiness and workflow gaps; no privileged-access claim",
    ),
]


class BestFreeDiagnosticEngine:
    def __init__(self) -> None:
        self.factory = UniversalDiagnosticFactory()
        self.product = DiagnosticProductEngine()

    def run(
        self,
        sector: str,
        buyer_role: str,
        problem: str,
        locale: str = "ar",
        *,
        consent: bool = False,
        depth: DiagnosticDepth = DiagnosticDepth.D1_RAPID,
    ) -> dict[str, Any]:
        families = self.factory.compose(
            sector,
            "sme",
            buyer_role,
            problem,
            depth,
        )
        offer = BEST_OFFERS[0]
        req = DiagnosticProductRequest(
            request_id=f"best_{sector}_{problem}",
            sector=sector,
            buyer_role=buyer_role,
            problem=problem,
            workflow=UNKNOWN,
            locale=locale,
            consent=consent,
            depth=depth,
        )
        result = self.product.run(req)
        return {
            "sector": sector,
            "buyer": buyer_role,
            "problem": problem,
            "locale": locale,
            "diagnostic_families": [f.family_id for f in families[:3]],
            "offer": offer.model_dump(),
            "channels": [
                "website",
                "email_consent",
                "whatsapp_opt_in",
                "partner",
                "procurement_research",
                "event",
            ],
            "agents": offer.agents,
            "result": result.model_dump(),
            "generated_at": datetime.now(UTC).isoformat(),
            "quality_claim": "NOT_ASSERTED_WITHOUT_EVIDENCE",
            "counts_as_relationship": False,
            "counts_as_pipeline": False,
        }


__all__ = [
    "BestFreeDiagnosticEngine",
    "BestFreeDiagnosticOffer",
    "BEST_OFFERS",
    "UNKNOWN",
]
