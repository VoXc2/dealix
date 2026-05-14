"""Bad Revenue Council — channel + ethics signals on top of finance bad-revenue."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from auto_client_acquisition.operating_finance_os.bad_revenue_filter import (
    BadRevenueSignals,
    is_bad_revenue,
)


class BadRevenueCouncilOutcome(StrEnum):
    REJECT = "reject"
    REFRAME_DIAGNOSTIC = "reframe_as_diagnostic"
    REPRICE = "reprice"
    ADD_STRICT_SCOPE = "add_strict_scope"
    REFER_OUT = "refer_out"
    QUALIFIED_PROCEED = "qualified_proceed"


@dataclass(frozen=True, slots=True)
class BadRevenueCouncilSignals:
    """Council-specific red lines (plus operating-finance bad revenue)."""

    asks_scraping: bool
    asks_cold_whatsapp_automation: bool
    asks_linkedin_automation: bool
    wants_guaranteed_sales: bool
    data_source_unclear: bool
    scope_open_ended: bool
    margin_weak: bool
    no_proof_path: bool
    no_retainer_path: bool


def council_hard_red_lines(s: BadRevenueCouncilSignals) -> tuple[str, ...]:
    reasons: list[str] = []
    if s.asks_scraping:
        reasons.append("asks_scraping")
    if s.asks_cold_whatsapp_automation:
        reasons.append("asks_cold_whatsapp_automation")
    if s.asks_linkedin_automation:
        reasons.append("asks_linkedin_automation")
    if s.wants_guaranteed_sales:
        reasons.append("wants_guaranteed_sales")
    return tuple(reasons)


def council_recommend_outcome(
    council: BadRevenueCouncilSignals,
    finance: BadRevenueSignals,
) -> tuple[BadRevenueCouncilOutcome, tuple[str, ...]]:
    """Return recommended council outcome and reason slugs."""
    hard = council_hard_red_lines(council)
    if hard:
        return BadRevenueCouncilOutcome.REJECT, hard

    bad_fin, fin_reasons = is_bad_revenue(finance)
    if not bad_fin:
        return BadRevenueCouncilOutcome.QUALIFIED_PROCEED, ()

    reasons_set = set(fin_reasons)
    if council.data_source_unclear:
        return BadRevenueCouncilOutcome.REFRAME_DIAGNOSTIC, tuple(fin_reasons)
    if "open_scope" in reasons_set:
        return BadRevenueCouncilOutcome.ADD_STRICT_SCOPE, tuple(fin_reasons)
    if "weak_margin" in reasons_set:
        return BadRevenueCouncilOutcome.REPRICE, tuple(fin_reasons)
    if "governance_refused" in reasons_set or "high_risk" in reasons_set:
        return BadRevenueCouncilOutcome.REFER_OUT, tuple(fin_reasons)
    return BadRevenueCouncilOutcome.REFRAME_DIAGNOSTIC, tuple(fin_reasons)
