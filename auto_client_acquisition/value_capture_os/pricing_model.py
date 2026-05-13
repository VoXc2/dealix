"""Offer pricing model — factors that drive price for each offer category."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DiagnosticPricingFactors:
    company_size: str         # sme | mid_market | enterprise
    source_count: int
    workflow_count: int
    governance_level_required: str  # low | medium | high


@dataclass(frozen=True)
class SprintPricingFactors:
    account_count: int
    data_quality_score: int   # 0..100
    sector_count: int
    scoring_depth: str        # shallow | standard | deep
    draft_pack_type: str      # email | whatsapp_consented | multi_channel
    executive_report_level: str  # basic | standard | board


@dataclass(frozen=True)
class RetainerPricingFactors:
    workflow_count: int
    update_frequency: str     # weekly | bi_weekly | monthly
    report_count: int
    support_level: str        # standard | priority | enterprise
    governance_level: str
    review_cycles: int


def diagnostic_price_tier(f: DiagnosticPricingFactors) -> str:
    """Return a coarse pricing tier label.

    The actual price book lives outside this module; this is the
    capability-aware tier the price book consumes.
    """

    weight = 0
    if f.company_size == "enterprise":
        weight += 2
    elif f.company_size == "mid_market":
        weight += 1
    weight += min(2, f.source_count // 3)
    weight += min(2, f.workflow_count // 2)
    if f.governance_level_required == "high":
        weight += 2
    elif f.governance_level_required == "medium":
        weight += 1

    if weight >= 6:
        return "premium"
    if weight >= 3:
        return "standard"
    return "starter"
