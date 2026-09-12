"""Truth Type System — explicit provenance, prevents synthetic pollution, purpose-specific + domain-aware authority."""

from __future__ import annotations

from enum import StrEnum

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


class EvidenceDomain(StrEnum):
    RELATIONSHIP = "relationship"
    PROBLEM = "problem"
    DIAGNOSTIC = "diagnostic"
    COMMERCIAL = "commercial"
    INVOICE = "invoice"
    PAYMENT = "payment"
    ACCOUNTING = "accounting"
    DELIVERY = "delivery"
    CUSTOMER_ACCEPTANCE = "customer_acceptance"
    CUSTOMER_VALUE = "customer_value"
    RUNTIME = "runtime"
    SECURITY = "security"
    PUBLIC_CLAIM = "public_claim"
    SIGNAL = "signal"


PAYMENT_BUSINESS_STATES: frozenset[str] = frozenset(
    {"PAYMENT_EVIDENCE_RECEIVED", "PAYMENT_VERIFIED", "VERIFIED_PAYMENT"}
)
REVENUE_BUSINESS_STATES: frozenset[str] = frozenset({"REVENUE_RECOGNIZED"})
PIPELINE_BUSINESS_STATES: frozenset[str] = frozenset(
    {"QUALIFIED_PROBLEM", "DIAGNOSTIC", "DISCOVERY", "QUOTE_READY"}
)

# Purpose-level authority: which purposes a truth class may ever serve.
# payment/revenue require can_use_for_v2 with a matching domain + business state.
AUTHORITY_MATRIX: dict[TruthClass, set[str]] = {
    TruthClass.OBSERVED: {"signal", "prioritization"},
    TruthClass.VERIFIED: {"signal", "prioritization", "pipeline", "invoice", "payment", "revenue", "customer_proof", "public_claim"},
    TruthClass.CUSTOMER_CONFIRMED: {"signal", "prioritization", "pipeline", "invoice", "customer_proof", "public_claim"},
    TruthClass.SYSTEM_VERIFIED: {"signal", "prioritization", "pipeline", "invoice", "payment", "revenue", "customer_proof", "public_claim"},
    TruthClass.ESTIMATED: {"signal", "prioritization"},
    TruthClass.INFERRED: {"signal", "prioritization"},
    TruthClass.HYPOTHESIS: {"planning"},
    TruthClass.SYNTHETIC: set(),
    TruthClass.SIMULATED: set(),
    TruthClass.TEST_ONLY: set(),
    TruthClass.UNKNOWN: set(),
}

# Domain-level authority: purposes that need provenance, not just a truth class.
AUTHORITY_MATRIX_V2: dict[tuple[TruthClass, str], set[EvidenceDomain]] = {
    (TruthClass.VERIFIED, "payment"): {EvidenceDomain.PAYMENT},
    (TruthClass.VERIFIED, "revenue"): {EvidenceDomain.ACCOUNTING, EvidenceDomain.INVOICE},
    (TruthClass.VERIFIED, "pipeline"): {EvidenceDomain.PROBLEM, EvidenceDomain.DIAGNOSTIC, EvidenceDomain.RELATIONSHIP},
    (TruthClass.VERIFIED, "customer_proof"): {EvidenceDomain.CUSTOMER_ACCEPTANCE, EvidenceDomain.CUSTOMER_VALUE, EvidenceDomain.DELIVERY},
    (TruthClass.VERIFIED, "public_claim"): {EvidenceDomain.PUBLIC_CLAIM, EvidenceDomain.CUSTOMER_ACCEPTANCE, EvidenceDomain.CUSTOMER_VALUE},
    (TruthClass.CUSTOMER_CONFIRMED, "pipeline"): {EvidenceDomain.PROBLEM, EvidenceDomain.DIAGNOSTIC},
    (TruthClass.CUSTOMER_CONFIRMED, "customer_proof"): {EvidenceDomain.CUSTOMER_ACCEPTANCE, EvidenceDomain.CUSTOMER_VALUE, EvidenceDomain.DELIVERY},
    (TruthClass.CUSTOMER_CONFIRMED, "public_claim"): {EvidenceDomain.PUBLIC_CLAIM, EvidenceDomain.CUSTOMER_ACCEPTANCE, EvidenceDomain.CUSTOMER_VALUE},
    (TruthClass.SYSTEM_VERIFIED, "payment"): {EvidenceDomain.PAYMENT},
    (TruthClass.SYSTEM_VERIFIED, "revenue"): {EvidenceDomain.ACCOUNTING, EvidenceDomain.INVOICE},
    (TruthClass.SYSTEM_VERIFIED, "pipeline"): {EvidenceDomain.PROBLEM, EvidenceDomain.RUNTIME},
    (TruthClass.SYSTEM_VERIFIED, "customer_proof"): {EvidenceDomain.RUNTIME, EvidenceDomain.CUSTOMER_ACCEPTANCE},
    (TruthClass.SYSTEM_VERIFIED, "public_claim"): {EvidenceDomain.PUBLIC_CLAIM, EvidenceDomain.RUNTIME},
}


def can_use_for(truth_class: TruthClass, purpose: str) -> bool:
    """Purpose-only authority. payment/revenue fail closed without provenance."""
    if purpose in ("payment", "revenue"):
        return False
    return purpose in AUTHORITY_MATRIX.get(truth_class, set())


def can_use_for_v2(
    truth_class: TruthClass,
    purpose: str,
    evidence_domain: EvidenceDomain | None = None,
    business_state: str | None = None,
) -> bool:
    """Purpose + evidence domain + business state must all authorize."""
    if purpose not in AUTHORITY_MATRIX.get(truth_class, set()):
        return False
    allowed_domains = AUTHORITY_MATRIX_V2.get((truth_class, purpose))
    if allowed_domains is None:
        return True
    if evidence_domain not in allowed_domains:
        return False
    if purpose == "payment":
        return business_state in PAYMENT_BUSINESS_STATES
    if purpose == "revenue":
        return business_state in REVENUE_BUSINESS_STATES
    if purpose == "pipeline":
        return business_state in PIPELINE_BUSINESS_STATES
    return True


class EconomicTruth(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    value: float | str
    truth_class: TruthClass
    source: str = "unknown"
    observed_at: str = ""
    verified_at: str = ""
    confidence: float = 0.5
    evidence_ref: str = ""
    evidence_domain: EvidenceDomain | None = None
    business_state: str | None = None

    def is_real(self) -> bool:
        return can_use_for_v2(self.truth_class, "pipeline", self.evidence_domain, self.business_state)

    def is_synthetic(self) -> bool:
        return self.truth_class in (TruthClass.SYNTHETIC, TruthClass.SIMULATED, TruthClass.TEST_ONLY)


def ensure_real_value(truth: EconomicTruth) -> float:
    if not can_use_for_v2(truth.truth_class, "pipeline", truth.evidence_domain, truth.business_state):
        raise ValueError(
            f"Truth {truth.truth_class} domain {truth.evidence_domain} state {truth.business_state} "
            f"cannot be counted as real pipeline (synthetic/estimated/hypothesis/generic-verified-without-provenance blocked)"
        )
    if not isinstance(truth.value, (int, float)):
        raise ValueError(f"Invalid financial value {truth.value}")
    return float(truth.value)


def ensure_verified_payment(truth: EconomicTruth) -> float:
    if not can_use_for_v2(truth.truth_class, "payment", truth.evidence_domain, truth.business_state):
        raise ValueError(
            f"Truth {truth.truth_class} with domain {truth.evidence_domain} and state {truth.business_state} cannot be verified payment"
        )
    if not truth.verified_at or not truth.evidence_ref:
        raise ValueError("Verified payment requires verified_at and evidence_ref")
    if not isinstance(truth.value, (int, float)):
        raise ValueError(f"Invalid payment value {truth.value}")
    return float(truth.value)


def ensure_verified_revenue(truth: EconomicTruth) -> float:
    if not can_use_for_v2(truth.truth_class, "revenue", truth.evidence_domain, truth.business_state):
        raise ValueError(
            f"Truth {truth.truth_class} with domain {truth.evidence_domain} and state {truth.business_state} cannot be verified revenue"
        )
    if not truth.verified_at or not truth.evidence_ref:
        raise ValueError("Verified revenue requires verified_at and evidence_ref")
    if not isinstance(truth.value, (int, float)):
        raise ValueError(f"Invalid revenue value {truth.value}")
    return float(truth.value)


__all__ = [
    "TruthClass",
    "EvidenceDomain",
    "PAYMENT_BUSINESS_STATES",
    "REVENUE_BUSINESS_STATES",
    "PIPELINE_BUSINESS_STATES",
    "AUTHORITY_MATRIX",
    "AUTHORITY_MATRIX_V2",
    "can_use_for",
    "can_use_for_v2",
    "EconomicTruth",
    "ensure_real_value",
    "ensure_verified_payment",
    "ensure_verified_revenue",
]
