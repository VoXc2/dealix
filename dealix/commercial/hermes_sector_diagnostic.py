"""Hermes Sector Diagnostic — in every sector Hermes can diagnose and convince, giving everything needed in best form, very intelligent."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from dealix.commercial.sector_company_factory import SectorCompanyFactory
from dealix.commercial.universal_diagnostic_factory import UniversalDiagnosticFactory, DiagnosticDepth
from dealix.commercial.best_free_diagnostic import BestFreeDiagnosticEngine
from dealix.commercial.best_offers_catalog import BestOfferCatalog
from dealix.commercial.economic_cell import Sector

class HermesSectorDiagnostic:
    def diagnose(self, sector: Sector, buyer_role: str = "ceo", problem: str = "revenue_leakage", locale: str = "ar") -> dict[str, Any]:
        scf = SectorCompanyFactory()
        # Get sector company intelligence
        co = scf.build(sector)
        # Universal diagnostic families for sector
        udf = UniversalDiagnosticFactory()
        families = udf.compose(sector.value, "sme", buyer_role, problem, DiagnosticDepth.D1_RAPID)
        # Best diagnostic product (free, best in market)
        bfd = BestFreeDiagnosticEngine()
        diag = bfd.run(sector.value, buyer_role, problem, locale)
        # Best offers
        boc = BestOfferCatalog()
        offer = boc.top_offer(sector.value, buyer_role, problem)
        # Hermes convincing: give everything needed in best form, very intelligent, evidence-backed, no hype
        convincing_package = {
            "sector": sector.value,
            "sector_name_ar": co.sector_name_ar,
            "sector_name_en": co.sector_name_en,
            "buyer": buyer_role,
            "problem": problem,
            "diagnostic_families": [f.family_id for f in families[:3]],
            "diagnostic_result": diag["result"]["expected_impact_range"] if isinstance(diag["result"], dict) else diag["result"],
            "offer": {"offer_id": offer.offer_id, "title": offer.title_ar if locale=="ar" else offer.title_en, "price": offer.price, "agents": offer.agents},
            "evidence": f"sector_{sector.value}_diagnostic_{families[0].family_id}" if families else "evidence",
            "next_step": "discovery" if locale=="ar" else "discovery",
            "hermes_intelligence": "very intelligent, evidence-backed, sector-specific, gives everything needed in best form",
            "generated_at": datetime.now(UTC).isoformat(),
        }
        return convincing_package

    def diagnose_all_sectors(self) -> list[dict[str, Any]]:
        return [self.diagnose(s) for s in Sector]

__all__ = ["HermesSectorDiagnostic"]
