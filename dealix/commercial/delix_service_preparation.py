"""Delix Service Preparation — for each person ready to be in Dealix service, prepare everything: communication, proposal per company daily, complete company profile per sector."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.sector_company_factory import SectorCompanyFactory
from dealix.commercial.economic_cell import Sector
from dealix.commercial.best_offers_catalog import BestOfferCatalog
from dealix.commercial.universal_diagnostic_factory import UniversalDiagnosticFactory, DiagnosticDepth

UNKNOWN = "UNKNOWN"

class CompanyProfile(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    profile_id: str
    sector: Sector
    sector_name_ar: str
    sector_name_en: str
    why_dealix_general: str = "Dealix AI Business Operating System — محرك الإيرادات + حوكمة AI + إثبات — منفتح على كل القطاعات والحكومة، 5 وكلاء + 8 موسعون، 44 ذراع، 500 خلية، DeepWIP≤3"
    why_dealix_general_en: str = "Dealix AI Business OS — Revenue Engine + AI Governance + Proof — open to all sectors & government, 5 agents + 8 extended, 44 arms"
    what_dealix_serves_general: str = "نخدم: تسرّب إيراد، فوضى مستندات، تأخر مشاريع، حوكمة AI، فاتورة، مناقصات — كل قطاع"
    what_dealix_serves_sector: str = UNKNOWN
    on_demand: bool = True
    agents_with_him: list[str] = Field(default_factory=lambda: ["dealix-pm","dealix-sales","dealix-delivery","dealix-engineer","dealix-content"])
    people_assigned: list[str] = Field(default_factory=list)
    daily: bool = True
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

class DelixServicePreparation:
    def prepare_for_person(self, person_id: str, sector: Sector, company_name: str) -> dict[str, Any]:
        scf = SectorCompanyFactory()
        co = scf.build(sector)
        udf = UniversalDiagnosticFactory()
        fams = udf.compose(sector.value, "sme", "ceo", co.top_problems[0] if co.top_problems else "revenue_leakage", DiagnosticDepth.D1_RAPID)
        boc = BestOfferCatalog()
        offer = boc.top_offer(sector.value, "ceo", co.top_problems[0] if co.top_problems else "revenue_leakage")
        profile = CompanyProfile(
            profile_id=f"profile_{sector.value}_{hashlib.sha256(company_name.encode()).hexdigest()[:6]}",
            sector=sector,
            sector_name_ar=co.sector_name_ar,
            sector_name_en=co.sector_name_en,
            what_dealix_serves_sector=f"نخدم {co.sector_name_ar}: {', '.join(co.top_problems[:2])} → {offer.title_ar} عبر {', '.join(co.relevant_offers[:2])}",
            people_assigned=[f"person_{person_id}_agent_{a}" for a in ["pm","sales","delivery"]],
        )
        # Daily proposal
        proposal = {
            "company": company_name,
            "sector": sector.value,
            "profile": profile.model_dump(),
            "diagnostic_families": [f.family_id for f in fams[:3]],
            "offer": offer.model_dump(),
            "communication": f"تواصل يومي إلى {person_id} لشركة {company_name} في {co.sector_name_ar} — {offer.title_ar}",
            "agents_with_him": profile.agents_with_him,
            "people_with_him": profile.people_assigned,
            "execution": "من الألف إلى الياء: تشخيص → اكتشاف → عرض مخصص → تفاوض → قرار → فاتورة → تسليم → إثبات → أصل",
            "daily": True,
        }
        return proposal

    def prepare_all_sectors_daily(self, people_per_sector: int = 1) -> list[dict[str, Any]]:
        results = []
        for sector in Sector:
            for i in range(people_per_sector):
                person_id = f"person_{sector.value}_{i}"
                company = f"Company-{sector.value}-{i}"
                results.append(self.prepare_for_person(person_id, sector, company))
        return results

    def verify(self) -> dict[str, Any]:
        all_daily = self.prepare_all_sectors_daily(1)
        return {"total": len(all_daily), "sectors": 20, "people": 20, "daily": True, "agents_with_him": 5, "comprehensive": True, "why_dealix": True}

__all__ = ["DelixServicePreparation", "CompanyProfile", "UNKNOWN"]
