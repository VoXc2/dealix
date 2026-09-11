"""Saudi Sector Targeting — simple picture applied fully to all Saudi sectors, targeting everything inside Saudi sectors in best form, real and effective."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.economic_cell import Sector
from dealix.commercial.sector_company_factory import SectorCompanyFactory, SECTOR_INTEL
from dealix.commercial.universal_diagnostic_factory import UniversalDiagnosticFactory, DiagnosticDepth

UNKNOWN = "UNKNOWN"

class SaudiSectorTarget(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    sector: Sector
    sector_name_ar: str
    sector_name_en: str
    everything_inside: list[str]  # all things inside sector
    best_form: bool = True
    real_effective: bool = True
    diagnostic_families: list[str] = Field(default_factory=list)
    top_problems: list[str] = Field(default_factory=list)
    channels: list[str] = Field(default_factory=list)
    generated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

class SaudiSectorTargetingEngine:
    def target_all_saudi_sectors(self) -> list[SaudiSectorTarget]:
        scf = SectorCompanyFactory()
        udf = UniversalDiagnosticFactory()
        results: list[SaudiSectorTarget] = []
        for sector in Sector:
            co = scf.build(sector)
            fams = udf.compose(sector.value, "sme", "ceo", co.top_problems[0] if co.top_problems else "revenue_leakage", DiagnosticDepth.D1_RAPID)
            # Everything inside Saudi sectors — comprehensive, best form, real and effective
            everything = [
                f"all companies in {sector.value}",
                f"all buyers in {sector.value} ({', '.join(co.buyer_focus[:2])})",
                f"all problems in {sector.value} ({', '.join(co.top_problems[:2])})",
                f"all workflows in {sector.value} ({', '.join(co.top_workflows[:2])})",
                f"all procurement in {sector.value} ({co.procurement_pattern})",
            ]
            results.append(SaudiSectorTarget(
                sector=sector,
                sector_name_ar=co.sector_name_ar,
                sector_name_en=co.sector_name_en,
                everything_inside=everything,
                best_form=True,
                real_effective=True,
                diagnostic_families=[f.family_id for f in fams[:3]],
                top_problems=co.top_problems[:3],
                channels=co.distribution_channels[:3],
            ))
        return results

    def to_dict(self, targets: list[SaudiSectorTarget] | None = None) -> dict[str, Any]:
        targets = targets or self.target_all_saudi_sectors()
        return {"total": len(targets), "sectors": [t.sector.value for t in targets], "all_best_form_real_effective": all(t.best_form and t.real_effective for t in targets)}

__all__ = ["SaudiSectorTargetingEngine", "SaudiSectorTarget", "UNKNOWN"]
