"""ICP fit scorer — deterministic 0-100 score for Saudi B2B leads (W9.11).

Used by:
  - LaaS weekly batch (scripts/laas_weekly_batch.py) to rank top-N
  - Sales pre-outreach (qualifying leads before founder time spent)
  - Customer dashboards (sort lead lists)

Design:
  - Pure function, no external IO, no LLM calls
  - Deterministic: same inputs → same score
  - Composable: 6 signal categories, each contributing weighted points
  - Transparent: returns full breakdown for debugging + customer transparency

Score breakdown:
  Sector fit          (0-20 pts)  matches customer's target sector
  Size band fit       (0-20 pts)  matches customer's target size
  Region fit          (0-15 pts)  matches geographic target
  Tech stack match    (0-15 pts)  uses tech that integrates with customer's product
  Buying intent       (0-20 pts)  recent fundraise, hiring, expansion signals
  Data completeness   (0-10 pts)  has email + domain + LinkedIn

Reference: aligned with auto_client_acquisition/agents/icp_matcher.py
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# Signal weights — sum to 100
WEIGHTS = {
    "sector_fit":         20,
    "size_band_fit":      20,
    "region_fit":         15,
    "tech_stack_match":   15,
    "buying_intent":      20,
    "data_completeness":  10,
}


@dataclass
class ICPFilter:
    """Customer's ICP filter — what they consider a good lead."""

    target_sectors: list[str] = field(default_factory=list)
    target_regions: list[str] = field(default_factory=list)
    target_size_bands: list[str] = field(default_factory=list)
    preferred_tech: list[str] = field(default_factory=list)


@dataclass
class LeadSignals:
    """Observable signals about a lead. Each field optional."""

    sector: str | None = None
    region: str | None = None
    size_band: str | None = None
    detected_tech: list[str] = field(default_factory=list)
    recent_funding_round: bool = False
    recent_executive_hire: bool = False
    recent_expansion_announcement: bool = False
    has_email: bool = False
    has_domain: bool = False
    has_linkedin: bool = False


def _sector_fit(signals: LeadSignals, icp: ICPFilter) -> int:
    if not icp.target_sectors:
        return WEIGHTS["sector_fit"] // 2  # neutral if no preference
    if signals.sector and signals.sector in icp.target_sectors:
        return WEIGHTS["sector_fit"]
    return 0


def _size_band_fit(signals: LeadSignals, icp: ICPFilter) -> int:
    if not icp.target_size_bands:
        return WEIGHTS["size_band_fit"] // 2
    if signals.size_band and signals.size_band in icp.target_size_bands:
        return WEIGHTS["size_band_fit"]
    return 0


def _region_fit(signals: LeadSignals, icp: ICPFilter) -> int:
    if not icp.target_regions:
        return WEIGHTS["region_fit"] // 2
    if signals.region and signals.region in icp.target_regions:
        return WEIGHTS["region_fit"]
    return 0


def _tech_stack_match(signals: LeadSignals, icp: ICPFilter) -> int:
    if not icp.preferred_tech or not signals.detected_tech:
        return 0
    overlap = set(icp.preferred_tech) & set(signals.detected_tech)
    # Up to full weight if any preferred tech detected; scales with overlap count
    if not overlap:
        return 0
    return min(WEIGHTS["tech_stack_match"],
               (len(overlap) * WEIGHTS["tech_stack_match"]) // max(1, len(icp.preferred_tech)))


def _buying_intent(signals: LeadSignals) -> int:
    """Each intent signal contributes a third of the weight."""
    points = 0
    third = WEIGHTS["buying_intent"] // 3
    if signals.recent_funding_round:
        points += third
    if signals.recent_executive_hire:
        points += third
    if signals.recent_expansion_announcement:
        points += third
    # Round up to full weight when all three present
    if (signals.recent_funding_round and signals.recent_executive_hire
            and signals.recent_expansion_announcement):
        points = WEIGHTS["buying_intent"]
    return min(points, WEIGHTS["buying_intent"])


def _data_completeness(signals: LeadSignals) -> int:
    """Lead with email + domain + LinkedIn = full points."""
    fields_present = sum([
        signals.has_email,
        signals.has_domain,
        signals.has_linkedin,
    ])
    return (fields_present * WEIGHTS["data_completeness"]) // 3


def score_lead(signals: LeadSignals, icp: ICPFilter) -> dict[str, Any]:
    """Compute the 0-100 ICP fit score with full breakdown.

    Returns:
        dict with keys: score, band, breakdown (per-signal points)
    """
    breakdown = {
        "sector_fit":         _sector_fit(signals, icp),
        "size_band_fit":      _size_band_fit(signals, icp),
        "region_fit":         _region_fit(signals, icp),
        "tech_stack_match":   _tech_stack_match(signals, icp),
        "buying_intent":      _buying_intent(signals),
        "data_completeness":  _data_completeness(signals),
    }
    total = sum(breakdown.values())
    total = max(0, min(100, total))

    if total >= 75:
        band = "hot"
    elif total >= 50:
        band = "warm"
    elif total >= 25:
        band = "cool"
    else:
        band = "cold"

    return {
        "score": total,
        "band": band,
        "breakdown": breakdown,
        "weights": dict(WEIGHTS),
    }


def rank_leads(leads: list[tuple[LeadSignals, dict]],
               icp: ICPFilter, top_n: int = 50) -> list[dict[str, Any]]:
    """Rank a list of (signals, metadata) tuples by score, return top N.

    metadata is preserved alongside the score so the caller can re-identify
    the lead by name/domain/etc. The function itself never touches PII.
    """
    scored = []
    for signals, metadata in leads:
        result = score_lead(signals, icp)
        scored.append({**result, "metadata": metadata})
    scored.sort(key=lambda r: r["score"], reverse=True)
    return scored[:top_n]
