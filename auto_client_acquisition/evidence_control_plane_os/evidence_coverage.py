"""Evidence Coverage — typed snapshot + 4-tier classifier."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


COVERAGE_THRESHOLDS: dict[str, float] = {
    "fragile_below": 0.70,
    "internal_below": 0.85,
    "client_ready_below": 0.95,
}


class CoverageTier(str, Enum):
    FRAGILE = "fragile"                    # <70%
    INTERNAL_ONLY = "usable_internally"    # 70..84
    CLIENT_READY = "client_ready"          # 85..94
    ENTERPRISE_READY = "enterprise_ready"  # 95..100


@dataclass(frozen=True)
class EvidenceCoverageSnapshot:
    period: str
    source_passport_coverage: float
    ai_run_ledger_coverage: float
    policy_check_coverage: float
    human_review_coverage: float
    approval_linkage: float
    proof_linkage: float
    value_linkage: float
    risk_events: int
    open_evidence_gaps: int

    def __post_init__(self) -> None:
        for name in (
            "source_passport_coverage",
            "ai_run_ledger_coverage",
            "policy_check_coverage",
            "human_review_coverage",
            "approval_linkage",
            "proof_linkage",
            "value_linkage",
        ):
            v = getattr(self, name)
            if not 0.0 <= v <= 1.0:
                raise ValueError(f"{name}_out_of_range_0_1")

    def composite_coverage(self) -> float:
        return (
            self.source_passport_coverage
            + self.ai_run_ledger_coverage
            + self.policy_check_coverage
            + self.human_review_coverage
            + self.approval_linkage
            + self.proof_linkage
            + self.value_linkage
        ) / 7.0


def classify_evidence_coverage(coverage: float) -> CoverageTier:
    if coverage < COVERAGE_THRESHOLDS["fragile_below"]:
        return CoverageTier.FRAGILE
    if coverage < COVERAGE_THRESHOLDS["internal_below"]:
        return CoverageTier.INTERNAL_ONLY
    if coverage < COVERAGE_THRESHOLDS["client_ready_below"]:
        return CoverageTier.CLIENT_READY
    return CoverageTier.ENTERPRISE_READY
