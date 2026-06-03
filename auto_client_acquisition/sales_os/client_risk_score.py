"""Client risk score — flags unsafe asks or delivery traps (deterministic)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ClientRiskSignals:
    wants_scraping_or_spam: bool
    wants_guaranteed_sales: bool
    unclear_pain: bool
    no_owner: bool
    data_not_ready: bool
    budget_unknown: bool


def client_risk_score(signals: ClientRiskSignals) -> int:
    """Higher = riskier (0–100)."""
    pts = 0
    if signals.wants_scraping_or_spam:
        pts += 40
    if signals.wants_guaranteed_sales:
        pts += 25
    if signals.unclear_pain:
        pts += 10
    if signals.no_owner:
        pts += 10
    if signals.data_not_ready:
        pts += 10
    if signals.budget_unknown:
        pts += 5
    return min(100, pts)


__all__ = ["ClientRiskSignals", "client_risk_score"]
