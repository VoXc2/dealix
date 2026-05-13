"""Bad Revenue Filter — refuse revenue that destroys focus."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BadRevenueSignals:
    open_scope: bool = False
    weak_margin: bool = False
    high_risk: bool = False
    client_rejects_governance: bool = False
    requests_scraping: bool = False
    requests_guaranteed_sales: bool = False
    no_proof_path: bool = False
    no_retainer_path: bool = False
    no_productization_signal: bool = False


@dataclass(frozen=True)
class BadRevenueResult:
    is_bad_revenue: bool
    triggers: tuple[str, ...]


def bad_revenue_check(s: BadRevenueSignals) -> BadRevenueResult:
    triggers: list[str] = []
    for name in BadRevenueSignals.__dataclass_fields__:
        if getattr(s, name):
            triggers.append(name)
    # Doctrine: any single forbidden trigger flips the verdict.
    forbidden = {
        "requests_scraping",
        "requests_guaranteed_sales",
        "client_rejects_governance",
    }
    is_bad = bool(set(triggers) & forbidden) or len(triggers) >= 3
    return BadRevenueResult(is_bad_revenue=is_bad, triggers=tuple(triggers))
