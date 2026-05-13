"""ROI Discipline — Estimated / Observed / Verified tiers."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ROILevel(str, Enum):
    ESTIMATED = "estimated"
    OBSERVED = "observed"
    VERIFIED = "verified"


@dataclass(frozen=True)
class ROIRecord:
    record_id: str
    level: ROILevel
    metric: str
    value: float
    assumption: str | None = None
    measurement_method: str | None = None
    client_confirmation_evidence: str | None = None

    def __post_init__(self) -> None:
        if self.level is ROILevel.VERIFIED and not self.client_confirmation_evidence:
            raise ValueError("verified_roi_requires_client_confirmation")
        if self.level is ROILevel.OBSERVED and not self.measurement_method:
            raise ValueError("observed_roi_requires_measurement_method")
        if self.level is ROILevel.ESTIMATED and not self.assumption:
            raise ValueError("estimated_roi_requires_assumption")

    def usable_as_public_case(self) -> bool:
        return self.level is ROILevel.VERIFIED

    def usable_in_sales(self) -> bool:
        return self.level in {ROILevel.OBSERVED, ROILevel.VERIFIED}
