"""Market power signal checklist (doctrine layer)."""

from __future__ import annotations

MARKET_POWER_SIGNALS: tuple[str, ...] = (
    "category_language_adoption",
    "inbound_diagnostic_requests",
    "partner_referrals",
    "proof_pack_requests",
    "benchmark_downloads",
    "academy_waitlist",
    "enterprise_trust_inquiries",
    "content_to_call_conversion",
    "competitor_copy_signals",
)


def market_power_activation_score(active_signals: frozenset[str]) -> int:
    if not MARKET_POWER_SIGNALS:
        return 0
    n = sum(1 for s in MARKET_POWER_SIGNALS if s in active_signals)
    return (n * 100) // len(MARKET_POWER_SIGNALS)
