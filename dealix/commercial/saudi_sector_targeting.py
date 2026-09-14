"""Saudi sector intelligence coverage — hypotheses and diagnostics, not targeting authority."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.economic_cell import Sector
from dealix.commercial.sector_company_factory import SectorCompanyFactory
from dealix.commercial.universal_diagnostic_factory import DiagnosticDepth, UniversalDiagnosticFactory

UNKNOWN = "UNKNOWN"
RESEARCH_ONLY = "RESEARCH_ONLY"


class SaudiSectorTarget(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    sector: Sector
    sector_name_ar: str
    sector_name_en: str
    everything_inside: list[str]
    best_form: bool = False
    real_effective: bool = False
    diagnostic_families: list[str] = Field(default_factory=list)
    top_problems: list[str] = Field(default_factory=list)
    channels: list[str] = Field(default_factory=list)
    evidence_state: str = RESEARCH_ONLY
    relationship_authority: bool = False
    consent_authority: bool = False
    outbound_authority: bool = False
    generated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class SaudiSectorTargetingEngine:
    """Maintain full-sector intelligence coverage without manufacturing leads or buyers."""

    def target_all_saudi_sectors(self) -> list[SaudiSectorTarget]:
        scf = SectorCompanyFactory()
        udf = UniversalDiagnosticFactory()
        results: list[SaudiSectorTarget] = []
        for sector in Sector:
            co = scf.build(sector)
            problem = co.top_problems[0] if co.top_problems else "revenue_leakage"
            families = udf.compose(
                sector.value,
                "sme",
                "ceo",
                problem,
                DiagnosticDepth.D1_RAPID,
            )
            coverage = [
                f"sector_company:{sector.value}",
                f"buyer_hypotheses:{','.join(co.buyer_focus[:2])}",
                f"problem_hypotheses:{','.join(co.top_problems[:2])}",
                f"workflow_hypotheses:{','.join(co.top_workflows[:2])}",
                f"procurement_pattern_hypothesis:{co.procurement_pattern}",
            ]
            results.append(
                SaudiSectorTarget(
                    sector=sector,
                    sector_name_ar=co.sector_name_ar,
                    sector_name_en=co.sector_name_en,
                    everything_inside=coverage,
                    best_form=False,
                    real_effective=False,
                    diagnostic_families=[family.family_id for family in families[:3]],
                    top_problems=co.top_problems[:3],
                    channels=[f"research:{channel}" for channel in co.distribution_channels[:3]],
                    evidence_state=RESEARCH_ONLY,
                    relationship_authority=False,
                    consent_authority=False,
                    outbound_authority=False,
                )
            )
        return results

    def to_dict(self, targets: list[SaudiSectorTarget] | None = None) -> dict[str, Any]:
        targets = targets or self.target_all_saudi_sectors()
        return {
            "total": len(targets),
            "sectors": [target.sector.value for target in targets],
            "coverage_state": RESEARCH_ONLY,
            "relationships_created": 0,
            "consent_created": 0,
            "outbound_authority": False,
            "all_best_form_real_effective": False,
            "truth_firewall": {
                "research_is_relationship": False,
                "signal_is_qualified_problem": False,
                "public_contact_is_consent": False,
            },
        }


__all__ = ["SaudiSectorTargetingEngine", "SaudiSectorTarget", "UNKNOWN", "RESEARCH_ONLY"]
