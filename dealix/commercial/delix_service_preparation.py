"""Dealix service preparation — research/draft packets, never synthetic relationships.

Compatibility note: the historical class/method names remain because internal callers
import them. Their semantics are Omega V3 CURRENT_ONLY: research may prepare a
sector/company hypothesis, but it cannot mint a relationship, consent, outreach task,
quote, payment, revenue, or a fixed agent roster.
"""
from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.agentic_holding.runtime import build_current_registry
from dealix.commercial.best_offers_catalog import BestOfferCatalog
from dealix.commercial.economic_cell import Sector
from dealix.commercial.sector_company_factory import SectorCompanyFactory
from dealix.commercial.universal_diagnostic_factory import DiagnosticDepth, UniversalDiagnosticFactory

UNKNOWN = "UNKNOWN"
RESEARCH_ONLY = "RESEARCH_ONLY"
DRAFT_ONLY = "DRAFT_ONLY"


class CompanyProfile(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    profile_id: str
    sector: Sector
    sector_name_ar: str
    sector_name_en: str
    why_dealix_general: str = (
        "Dealix Saudi AI Business Operating System — governed workflows, evidence, "
        "Agentic Holding execution and customer-specific outcomes; no fixed public agent count."
    )
    why_dealix_general_en: str = (
        "Dealix Saudi AI Business Operating System — governed workflows, evidence, "
        "Agentic Holding execution and customer-specific outcomes; no fixed public agent count."
    )
    what_dealix_serves_general: str = (
        "نخدم مشكلات تشغيلية واقتصادية قابلة للقياس بعد التحقق من سياق العميل وبياناته."
    )
    what_dealix_serves_sector: str = UNKNOWN
    on_demand: bool = True
    agents_with_him: list[str] = Field(default_factory=list)
    people_assigned: list[str] = Field(default_factory=list)
    authority_state: str = RESEARCH_ONLY
    relationship_state: str = UNKNOWN
    consent_state: str = UNKNOWN
    live_outbound_allowed: bool = False
    daily: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class DelixServicePreparation:
    """Prepare evidence-bounded diagnostic/offer drafts without manufacturing pipeline."""

    @staticmethod
    def _sector_agents(sector: Sector) -> list[str]:
        registry = build_current_registry()
        prefix = f"dealix.{sector.value}."
        preferred_roles = ("sector-diagnostic", "sector-sales", "sector-delivery", "sector-proof")
        candidates = [f"{prefix}{role}" for role in preferred_roles]
        return [agent_id for agent_id in candidates if agent_id in registry.agents]

    def prepare_for_person(
        self,
        person_id: str,
        sector: Sector,
        company_name: str,
        *,
        relationship_evidence_ref: str | None = None,
        consent_evidence_ref: str | None = None,
    ) -> dict[str, Any]:
        scf = SectorCompanyFactory()
        co = scf.build(sector)
        udf = UniversalDiagnosticFactory()
        problem = co.top_problems[0] if co.top_problems else "revenue_leakage"
        fams = udf.compose(sector.value, "sme", "ceo", problem, DiagnosticDepth.D1_RAPID)
        offer = BestOfferCatalog().top_offer(sector.value, "ceo", problem)

        relationship_state = "VERIFIED_INTERACTION" if relationship_evidence_ref else UNKNOWN
        consent_state = "VERIFIED_OPT_IN" if consent_evidence_ref else UNKNOWN
        live_outbound_allowed = bool(relationship_evidence_ref and consent_evidence_ref)
        subject_key = f"{sector.value}:{company_name}:{person_id}"
        profile = CompanyProfile(
            profile_id=f"profile_{sector.value}_{hashlib.sha256(subject_key.encode()).hexdigest()[:8]}",
            sector=sector,
            sector_name_ar=co.sector_name_ar,
            sector_name_en=co.sector_name_en,
            what_dealix_serves_sector=(
                f"فرضية قطاعية لـ {co.sector_name_ar}: {', '.join(co.top_problems[:2])}; "
                f"تحتاج Discovery قبل اعتماد أي نطاق أو عرض."
            ),
            agents_with_him=self._sector_agents(sector),
            authority_state=RESEARCH_ONLY if not relationship_evidence_ref else "INTERACTION_VERIFIED",
            relationship_state=relationship_state,
            consent_state=consent_state,
            live_outbound_allowed=live_outbound_allowed,
        )

        return {
            "company_reference": company_name,
            "person_reference": person_id,
            "sector": sector.value,
            "profile": profile.model_dump(),
            "diagnostic_families": [family.family_id for family in fams[:3]],
            "offer_hypothesis": offer.model_dump(),
            "commercial_status": RESEARCH_ONLY if not relationship_evidence_ref else DRAFT_ONLY,
            "communication": {
                "status": DRAFT_ONLY,
                "live_send_allowed": live_outbound_allowed,
                "message": (
                    f"مسودة داخلية فقط لـ {co.sector_name_ar}; لا تُرسل قبل إثبات العلاقة/الموافقة "
                    "وتأهيل المشكلة في Discovery."
                ),
            },
            "relationship_evidence_ref": relationship_evidence_ref,
            "consent_evidence_ref": consent_evidence_ref,
            "logical_agents": profile.agents_with_him,
            "execution": (
                "Market Signal → Evidence → Real Interaction → Qualified Problem → Free Diagnostic → "
                "Qualified Discovery → Customer-Specific Quote → Pilot Decision → Invoice → "
                "Verified Payment → Delivery → Customer-Validated Proof"
            ),
            "truth_firewall": {
                "research_is_relationship": False,
                "public_contact_is_consent": False,
                "draft_is_sent": False,
                "quote_is_revenue": False,
            },
        }

    def prepare_all_sectors_daily(self, people_per_sector: int = 1) -> list[dict[str, Any]]:
        """Legacy method name; creates research packets, never synthetic leads/outreach."""
        results: list[dict[str, Any]] = []
        copies = max(1, int(people_per_sector))
        for sector in Sector:
            for index in range(copies):
                results.append(
                    self.prepare_for_person(
                        f"UNVERIFIED_RESEARCH_SUBJECT_{index}",
                        sector,
                        "UNVERIFIED_RESEARCH_COMPANY",
                    )
                )
        return results

    def verify(self) -> dict[str, Any]:
        registry = build_current_registry()
        sectors = tuple(Sector)
        packets = self.prepare_all_sectors_daily(1)
        return {
            "total_research_packets": len(packets),
            "sectors": len(sectors),
            "logical_agents": len(registry.agents),
            "orphan_failures": registry.validate(),
            "synthetic_relationships_created": 0,
            "live_outbound_authority": False,
            "fixed_five_authority": False,
            "global_deepwip3_authority": False,
            "commercial_truth": "RESEARCH_ONLY_UNTIL_REAL_INTERACTION",
        }


__all__ = ["DelixServicePreparation", "CompanyProfile", "UNKNOWN", "RESEARCH_ONLY", "DRAFT_ONLY"]
