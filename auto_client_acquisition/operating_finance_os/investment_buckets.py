"""Investment Buckets — 8 canonical buckets."""

from __future__ import annotations

from enum import Enum


class InvestmentBucket(str, Enum):
    REVENUE_CAPTURE = "revenue_capture"
    DELIVERY_EFFICIENCY = "delivery_efficiency"
    GOVERNANCE_AND_TRUST = "governance_and_trust"
    PROOF_AND_VALUE = "proof_and_value"
    PRODUCTIZATION = "productization"
    DISTRIBUTION = "distribution"
    TALENT_AND_ENABLEMENT = "talent_and_enablement"
    VENTURE_OPTIONALITY = "venture_optionality"


INVESTMENT_BUCKETS: tuple[InvestmentBucket, ...] = tuple(InvestmentBucket)
