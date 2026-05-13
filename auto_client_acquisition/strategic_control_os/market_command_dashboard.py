"""Market Command Dashboard — eight indicators of category formation.

See ``docs/strategic_control/MARKET_COMMAND_DASHBOARD.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MarketDashboardIndicator(str, Enum):
    CATEGORY_LANGUAGE_ADOPTION = "category_language_adoption"
    INBOUND_DIAGNOSTICS = "inbound_diagnostics"
    PROOF_PACK_REQUESTS = "proof_pack_requests"
    PARTNER_LEADS = "partner_leads"
    ENTERPRISE_TRUST_INQUIRIES = "enterprise_trust_inquiries"
    BENCHMARK_DOWNLOADS = "benchmark_downloads"
    ACADEMY_INTEREST = "academy_interest"
    COMPETITOR_COPY_SIGNALS = "competitor_copy_signals"


MARKET_DASHBOARD_INDICATORS: tuple[MarketDashboardIndicator, ...] = tuple(
    MarketDashboardIndicator
)


@dataclass(frozen=True)
class MarketCommandDashboardReading:
    quarter: str
    sustained: frozenset[MarketDashboardIndicator]

    def __post_init__(self) -> None:
        unknown = set(self.sustained) - set(MARKET_DASHBOARD_INDICATORS)
        if unknown:
            raise ValueError(
                "unknown_dashboard_indicators:"
                + ",".join(sorted(i.value for i in unknown))
            )


def sustained_indicator_count(reading: MarketCommandDashboardReading) -> int:
    return len(reading.sustained)
