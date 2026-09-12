"""Read-only website/SEO/content projection from canonical sector packs.

This is not a CMS or another truth store. It derives public-draft material from
``SectorCommercialFactory`` so the website remains Dealix, with one free
Diagnostic engine and no synthetic client proof. Publishing remains L5.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.economic_cell import Sector
from dealix.commercial.sector_commercial_factory import SectorCommercialFactory


class SectorLandingProjection(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    sector_id: str
    locale: str
    brand: str = "Dealix"
    page_kind: str = "DEALIX_SECTOR_APPLICATION"
    title: str
    context: str
    buyer_problems: list[str]
    capabilities: list[str]
    free_diagnostic_cta: str
    diagnostic_price: str = "FREE"
    how_dealix_works: list[str]
    trust_patterns: list[str]
    faq: list[dict[str, str]]
    seo_queries: list[str]
    content_themes: list[str]
    proof_claims: list[str] = Field(default_factory=list)
    publish_authority: bool = False


class WebsiteCommercialDerivation:
    def __init__(self) -> None:
        self.factory = SectorCommercialFactory()

    def sector_page(self, sector: Sector, locale: str = "ar") -> SectorLandingProjection:
        if locale not in {"ar", "en"}:
            raise ValueError("locale must be ar or en")
        pack = self.factory.build(sector)
        arabic = locale == "ar"
        title = (
            f"Dealix لقطاع {pack.arabic_name}"
            if arabic
            else f"Dealix for {pack.english_name}"
        )
        context = (
            "طبّق Dealix على مشاكلك التشغيلية والتجارية مع تشخيص مجاني مبني على الأدلة."
            if arabic
            else "Apply Dealix to your operating and commercial problems with a free evidence-governed diagnostic."
        )
        cta = (
            "ابدأ التشخيص المجاني — بلا بطاقة أو التزام"
            if arabic
            else "Start the free diagnostic — no card or commitment"
        )
        how = (
            ["إشارة/طلب حقيقي", "تشخيص مجاني", "اكتشاف مؤهل", "نطاق وقرار", "تنفيذ محكوم", "قبول وقيمة مثبتة"]
            if arabic
            else ["Real signal/request", "Free diagnostic", "Qualified discovery", "Scope/decision", "Governed delivery", "Acceptance/validated value"]
        )
        trust = (
            [
                "البحث لا يساوي علاقة",
                "النمط لا يساوي حقيقة عميل",
                "لا ROI بلا أساس",
                "لا إثبات عام بلا إذن العميل",
            ]
            if arabic
            else [
                "Research is not a relationship",
                "A pattern is not a customer fact",
                "No ROI without a basis",
                "No public proof without customer permission",
            ]
        )
        faq = [
            {
                "q": "هل التشخيص مجاني؟" if arabic else "Is the diagnostic free?",
                "a": "نعم، كل أعماق التشخيص مجانية." if arabic else "Yes. Every diagnostic depth is free.",
            },
            {
                "q": "هل النتائج مضمونة؟" if arabic else "Are results guaranteed?",
                "a": (
                    "لا. نفصل الملاحظة والتقدير والتوصية، ونثبت النتائج فقط بالأدلة."
                    if arabic
                    else "No. Observations, estimates and recommendations stay separate; results require evidence."
                ),
            },
            {
                "q": "متى يبدأ العمل المدفوع؟" if arabic else "When does paid work begin?",
                "a": (
                    "بعد التشخيص والاكتشاف المؤهل فقط، عبر نطاق عميل محدد وموافقة تجارية مستقلة."
                    if arabic
                    else "Only after diagnostic/qualified discovery, through customer-specific scope and separate commercial approval."
                ),
            },
        ]
        return SectorLandingProjection(
            sector_id=sector.value,
            locale=locale,
            title=title,
            context=context,
            buyer_problems=pack.top_pain_patterns[:5],
            capabilities=list(dict.fromkeys(pack.ai_opportunities + pack.automation_opportunities + pack.workflow_opportunities))[:8],
            free_diagnostic_cta=cta,
            how_dealix_works=how,
            trust_patterns=trust,
            faq=faq,
            seo_queries=pack.arabic_queries if arabic else pack.english_queries,
            content_themes=pack.content_themes,
        )

    def all_sector_pages(self) -> list[SectorLandingProjection]:
        return [
            self.sector_page(sector, locale)
            for sector in Sector
            for locale in ("ar", "en")
        ]

    def content_queue_projection(self) -> list[dict[str, Any]]:
        queue: list[dict[str, Any]] = []
        for sector in Sector:
            pack = self.factory.build(sector)
            for theme in pack.content_themes:
                queue.append(
                    {
                        "sector_id": sector.value,
                        "theme": theme,
                        "source_refs": [source.source_url for source in pack.official_sources],
                        "diagnostic_cta": "FREE",
                        "truth_status": "DRAFT_REQUIRES_SOURCE_VALIDATION",
                        "publish_authority": False,
                    }
                )
        return queue


__all__ = ["SectorLandingProjection", "WebsiteCommercialDerivation"]
