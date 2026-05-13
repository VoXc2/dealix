"""Market Power — category-formation indicators and escalation rule.

See ``docs/endgame/MARKET_POWER.md``. Vanity metrics (follower counts,
impressions, likes) are intentionally not represented here.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MarketPowerIndicator(str, Enum):
    CATEGORY_LANGUAGE_ADOPTION = "category_language_adoption"
    INBOUND_DIAGNOSTIC_REQUESTS = "inbound_diagnostic_requests"
    PARTNER_REFERRALS = "partner_referrals"
    PROOF_PACK_REQUESTS = "proof_pack_requests"
    BENCHMARK_DOWNLOADS = "benchmark_downloads"
    ACADEMY_WAITLIST = "academy_waitlist"
    ENTERPRISE_TRUST_INQUIRIES = "enterprise_trust_inquiries"
    CONTENT_TO_CALL_CONVERSION = "content_to_call_conversion"
    COMPETITOR_COPY_SIGNALS = "competitor_copy_signals"


MARKET_POWER_INDICATORS: tuple[MarketPowerIndicator, ...] = tuple(MarketPowerIndicator)


@dataclass(frozen=True)
class MarketPowerReading:
    """A snapshot of which indicators are *sustained* in a given quarter.

    A reading captures only the boolean "sustained" judgment — the raw
    counts live in the metrics engine. This module encodes the decision
    rule, not the data store.
    """

    quarter: str  # e.g. "2026-Q2"
    sustained: frozenset[MarketPowerIndicator]


# Doctrine: escalate market spend only when at least three indicators
# have been sustained for two consecutive quarters.
MIN_SUSTAINED_INDICATORS: int = 3
MIN_SUSTAINED_QUARTERS: int = 2


def should_escalate_market_spend(readings: tuple[MarketPowerReading, ...]) -> bool:
    """Return True when escalation is justified by the doctrine.

    ``readings`` is the ordered tail of quarterly readings. Only the last
    ``MIN_SUSTAINED_QUARTERS`` are evaluated.
    """

    if len(readings) < MIN_SUSTAINED_QUARTERS:
        return False

    tail = readings[-MIN_SUSTAINED_QUARTERS:]
    common = set(tail[0].sustained)
    for reading in tail[1:]:
        common &= reading.sustained
    return len(common) >= MIN_SUSTAINED_INDICATORS
