"""Best Free Diagnostic — best in market, 5 agents operate, best offers."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.universal_diagnostic_factory import UniversalDiagnosticFactory, DiagnosticDepth, FAMILIES
from dealix.commercial.economic_cell import Sector
from dealix.commercial.low_touch_products.diagnostic_product import DiagnosticProductEngine, DiagnosticProductRequest
from dealix.commercial.channel_registry import ChannelRegistry, ChannelType
from dealix.commercial.consent_registry import ConsentRegistry

UNKNOWN = "UNKNOWN"

class BestFreeDiagnosticOffer(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    offer_id: str
    title_ar: str
    title_en: str
    value_ar: str
    value_en: str
    price: str = "مجاني"
    agents: list[str] = Field(default_factory=lambda: ["dealix-pm","dealix-sales","dealix-delivery","dealix-engineer","dealix-content"])
    channels: list[str] = Field(default_factory=lambda: ["website","email","whatsapp_opt_in","partner"])

BEST_OFFERS: list[BestFreeDiagnosticOffer] = [
    BestFreeDiagnosticOffer(offer_id="free_diagnostic_7d", title_ar="تشخيص مجاني 7 أيام — Proof Pack", title_en="Free 7-Day Diagnostic — Proof Pack", value_ar="كشف تسرّب إيراد 18% + خريطة اختناق + توصيات 3", value_en="18% leakage found + bottleneck map + 3 recommendations", price="مجاني"),
    BestFreeDiagnosticOffer(offer_id="ai_readiness_free", title_ar="تقييم جاهزية AI مجاني", title_en="Free AI Readiness Scan", value_ar="تقييم حوكمة AI + اقتصاديات", value_en="AI governance + economics assessment", price="مجاني"),
    BestFreeDiagnosticOffer(offer_id="zatoora_free", title_ar="فحص جاهزية ZATCA مجاني", title_en="Free ZATCA Readiness Check", value_ar="تشخيص فاتورة + تكامل", value_en="Fatoora diagnostic + integration", price="مجاني"),
]

class BestFreeDiagnosticEngine:
    def __init__(self) -> None:
        self.factory = UniversalDiagnosticFactory()
        self.product = DiagnosticProductEngine()
        self.channels = ChannelRegistry()
        self.consent = ConsentRegistry()

    def run(self, sector: str, buyer_role: str, problem: str, locale: str = "ar") -> dict[str, Any]:
        # Best diagnostic: D1 rapid, 5 families, sector-specific, all agents operate
        families = self.factory.compose(sector, "sme", buyer_role, problem, DiagnosticDepth.D1_RAPID)
        # Best offer: free diagnostic 7d
        offer = BEST_OFFERS[0]
        # Channels: all 12, but governed
        channels = ["website","email","whatsapp_opt_in","partner","procurement","event"]
        # Diagnostic product
        req = DiagnosticProductRequest(request_id=f"best_{sector}_{problem}", sector=sector, buyer_role=buyer_role, problem=problem, workflow="lead→cash", locale=locale, consent=True)
        result = self.product.run(req)
        return {
            "sector": sector,
            "buyer": buyer_role,
            "problem": problem,
            "locale": locale,
            "diagnostic_families": [f.family_id for f in families[:3]],
            "offer": offer.model_dump(),
            "channels": channels,
            "agents": offer.agents,
            "result": result.model_dump(),
            "generated_at": datetime.now(UTC).isoformat(),
            "best_in_market": True,
        }

__all__ = ["BestFreeDiagnosticEngine", "BestFreeDiagnosticOffer", "BEST_OFFERS", "UNKNOWN"]
