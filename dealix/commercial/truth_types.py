"""Truth Type System — explicit provenance, prevents synthetic pollution."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict

class TruthClass(StrEnum):
    OBSERVED = "observed"
    VERIFIED = "verified"
    CUSTOMER_CONFIRMED = "customer_confirmed"
    SYSTEM_VERIFIED = "system_verified"
    ESTIMATED = "estimated"
    INFERRED = "inferred"
    HYPOTHESIS = "hypothesis"
    SYNTHETIC = "synthetic"
    SIMULATED = "simulated"
    TEST_ONLY = "test_only"
    UNKNOWN = "unknown"

class EconomicTruth(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    value: float | str
    truth_class: TruthClass
    source: str = "unknown"
    observed_at: str = ""
    verified_at: str = ""
    confidence: float = 0.5
    evidence_ref: str = ""

    def is_real(self) -> bool:
        return self.truth_class in (TruthClass.OBSERVED, TruthClass.VERIFIED, TruthClass.CUSTOMER_CONFIRMED, TruthClass.SYSTEM_VERIFIED)

    def is_synthetic(self) -> bool:
        return self.truth_class in (TruthClass.SYNTHETIC, TruthClass.SIMULATED, TruthClass.TEST_ONLY, TruthClass.HYPOTHESIS)

# Example usage for economic calculations
def ensure_real_value(truth: EconomicTruth) -> float:
    if truth.is_synthetic():
        raise ValueError(f"Synthetic value {truth.value} cannot be counted as real pipeline/revenue")
    if isinstance(truth.value, (int, float)):
        return float(truth.value)
    return 0.0

__all__ = ["TruthClass", "EconomicTruth", "ensure_real_value"]
