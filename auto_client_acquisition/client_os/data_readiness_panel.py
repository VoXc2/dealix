"""Client Data Readiness Panel — typed snapshot."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DataReadinessPanel:
    client_id: str
    sources_uploaded: int
    sources_with_passport: int
    data_quality_score: int        # 0..100
    duplicate_rate: float          # 0..1
    missing_fields_pct: float      # 0..1
    pii_flagged_sources: int
    allowed_use_documented: bool

    def readiness_tier(self) -> str:
        if self.data_quality_score >= 85:
            return "ready_for_ai_workflow"
        if self.data_quality_score >= 70:
            return "usable_with_cleanup"
        if self.data_quality_score >= 50:
            return "diagnostic_only"
        return "data_readiness_sprint_first"
