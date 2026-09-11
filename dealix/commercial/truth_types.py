"""Truth Type System — explicit provenance, prevents synthetic pollution, purpose-specific authority."""

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

# Authority matrix — purpose-specific, not one boolean
# Maps truth_class → allowed purposes
AUTHORITY_MATRIX: dict[TruthClass, set[str]] = {
    TruthClass.OBSERVED: {"signal","prioritization"},
    TruthClass.VERIFIED: {"signal","prioritization","pipeline","invoice","payment","revenue","customer_proof","public_claim"},
    TruthClass.CUSTOMER_CONFIRMED: {"signal","prioritization","pipeline","invoice","payment","revenue","customer_proof","public_claim"},
    TruthClass.SYSTEM_VERIFIED: {"signal","prioritization","pipeline","payment","revenue","customer_proof","public_claim"},
    TruthClass.ESTIMATED: {"signal","prioritization"},  # NEVER pipeline/revenue/payment/customer proof
    TruthClass.INFERRED: {"signal","prioritization"},
    TruthClass.HYPOTHESIS: {"planning"},
    TruthClass.SYNTHETIC: set(),
    TruthClass.SIMULATED: set(),
    TruthClass.TEST_ONLY: set(),
    TruthClass.UNKNOWN: set(),  # fail closed
}

def can_use_for(truth_class: TruthClass, purpose: str) -> bool:
    return purpose in AUTHORITY_MATRIX.get(truth_class, set())

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
        # Legacy: use can_use_for with strict purpose, not broad is_real
        return can_use_for(self.truth_class, "pipeline")

    def is_synthetic(self) -> bool:
        return self.truth_class in (TruthClass.SYNTHETIC, TruthClass.SIMULATED, TruthClass.TEST_ONLY, TruthClass.HYPOTHESIS, TruthClass.UNKNOWN, TruthClass.ESTIMATED, TruthClass.INFERRED)

def ensure_real_value(truth: EconomicTruth) -> float:
    # Strict: only VERIFIED/CUSTOMER_CONFIRMED/SYSTEM_VERIFIED can be pipeline/revenue
    if not can_use_for(truth.truth_class, "pipeline"):
        raise ValueError(f"Truth {truth.truth_class} value {truth.value} cannot be counted as real pipeline/revenue (synthetic/estimated/inferred/unknown blocked)")
    if not isinstance(truth.value, (int, float)):
        raise ValueError(f"Invalid financial value {truth.value}")
    return float(truth.value)

def ensure_verified_payment(truth: EconomicTruth) -> float:
    if not can_use_for(truth.truth_class, "payment"):
        raise ValueError(f"Truth {truth.truth_class} cannot be verified payment")
    if not truth.verified_at or not truth.evidence_ref:
        raise ValueError("Verified payment requires verified_at and evidence_ref")
    if not isinstance(truth.value, (int, float)):
        raise ValueError(f"Invalid payment value {truth.value}")
    return float(truth.value)

def ensure_verified_revenue(truth: EconomicTruth) -> float:
    if not can_use_for(truth.truth_class, "revenue"):
        raise ValueError(f"Truth {truth.truth_class} cannot be verified revenue")
    return ensure_verified_payment(truth)

__all__ = ["TruthClass", "EconomicTruth", "AUTHORITY_MATRIX", "can_use_for", "ensure_real_value", "ensure_verified_payment", "ensure_verified_revenue"]
