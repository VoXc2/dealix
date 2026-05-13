"""Dealix Operating Finance OS — capital allocation + bad-revenue filter."""

from __future__ import annotations

from auto_client_acquisition.operating_finance_os.bad_revenue_filter import (
    BadRevenueSignals,
    bad_revenue_check,
)
from auto_client_acquisition.operating_finance_os.capital_allocation_score import (
    CAPITAL_ALLOCATION_WEIGHTS,
    CapitalAllocationComponents,
    CapitalAllocationTier,
    classify_capital_allocation,
    compute_capital_allocation_score,
)
from auto_client_acquisition.operating_finance_os.investment_buckets import (
    INVESTMENT_BUCKETS,
    InvestmentBucket,
)

__all__ = [
    "BadRevenueSignals",
    "bad_revenue_check",
    "CAPITAL_ALLOCATION_WEIGHTS",
    "CapitalAllocationComponents",
    "CapitalAllocationTier",
    "classify_capital_allocation",
    "compute_capital_allocation_score",
    "INVESTMENT_BUCKETS",
    "InvestmentBucket",
]
