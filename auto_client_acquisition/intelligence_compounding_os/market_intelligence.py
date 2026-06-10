"""Market intelligence — recurring pains and offer signals (taxonomy only)."""

from __future__ import annotations

from dataclasses import dataclass

MARKET_SIGNAL_SOURCES: tuple[str, ...] = (
    "sales_call",
    "inbound_form",
    "partner_referral",
    "benchmark_download",
    "workshop",
)


@dataclass(frozen=True, slots=True)
class MarketSignalRecord:
    signal_id: str
    source: str
    sector: str
    pain: str
    buyer: str
    recommended_offer: str
    confidence: str


def market_signal_record_valid(rec: MarketSignalRecord) -> bool:
    return all(
        (
            rec.signal_id.strip(),
            rec.source in MARKET_SIGNAL_SOURCES,
            rec.sector.strip(),
            rec.pain.strip(),
            rec.buyer.strip(),
            rec.recommended_offer.strip(),
            rec.confidence.strip(),
        ),
    )


def market_pattern_actionable_repeats(count: int) -> bool:
    """Pain / objection repeated ≥3 → offer page / response (operating rule)."""
    return count >= 3
