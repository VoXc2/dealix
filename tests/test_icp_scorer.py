"""Tests for ICP fit scorer (W9.11)."""
from __future__ import annotations

import pytest

from auto_client_acquisition.icp_scorer import (
    ICPFilter,
    LeadSignals,
    rank_leads,
    score_lead,
)


def test_score_is_deterministic():
    """Same inputs → same score (regression guard)."""
    signals = LeadSignals(sector="saas", region="riyadh", size_band="50_250")
    icp = ICPFilter(target_sectors=["saas"], target_regions=["riyadh"],
                    target_size_bands=["50_250"])
    r1 = score_lead(signals, icp)
    r2 = score_lead(signals, icp)
    assert r1["score"] == r2["score"]
    assert r1["band"] == r2["band"]


def test_score_clamped_0_to_100():
    """No combination produces score outside [0, 100]."""
    # Maximum signals
    signals_max = LeadSignals(
        sector="saas", region="riyadh", size_band="50_250",
        detected_tech=["python", "react"],
        recent_funding_round=True,
        recent_executive_hire=True,
        recent_expansion_announcement=True,
        has_email=True, has_domain=True, has_linkedin=True,
    )
    icp = ICPFilter(target_sectors=["saas"], target_regions=["riyadh"],
                    target_size_bands=["50_250"],
                    preferred_tech=["python", "react"])
    result = score_lead(signals_max, icp)
    assert 0 <= result["score"] <= 100

    # Empty signals
    empty_signals = LeadSignals()
    empty_icp = ICPFilter()
    result_min = score_lead(empty_signals, empty_icp)
    assert 0 <= result_min["score"] <= 100


def test_perfect_lead_lands_hot():
    """A maximally-matching lead should land in 'hot' band."""
    signals = LeadSignals(
        sector="saas", region="riyadh", size_band="50_250",
        detected_tech=["salla", "foodics"],
        recent_funding_round=True,
        recent_executive_hire=True,
        recent_expansion_announcement=True,
        has_email=True, has_domain=True, has_linkedin=True,
    )
    icp = ICPFilter(target_sectors=["saas"], target_regions=["riyadh"],
                    target_size_bands=["50_250"],
                    preferred_tech=["salla", "foodics"])
    result = score_lead(signals, icp)
    assert result["band"] == "hot"
    assert result["score"] >= 75


def test_no_match_lands_cold_or_cool():
    """Lead matching nothing in ICP should land in cold/cool."""
    signals = LeadSignals(
        sector="education",
        region="qassim",
        size_band="1_50",
    )
    icp = ICPFilter(target_sectors=["fintech"], target_regions=["riyadh"])
    result = score_lead(signals, icp)
    # Some neutral points from empty-preference defaults, but should not be hot
    assert result["band"] in ("cold", "cool")


def test_breakdown_sums_to_score():
    """The reported score equals sum of per-signal points (transparency)."""
    signals = LeadSignals(
        sector="saas", region="riyadh", size_band="50_250",
        detected_tech=["python"],
        has_email=True,
    )
    icp = ICPFilter(target_sectors=["saas"], target_regions=["riyadh"],
                    target_size_bands=["50_250"],
                    preferred_tech=["python"])
    result = score_lead(signals, icp)
    assert result["score"] == sum(result["breakdown"].values())


def test_breakdown_includes_all_six_signals():
    signals = LeadSignals()
    icp = ICPFilter()
    result = score_lead(signals, icp)
    for key in ("sector_fit", "size_band_fit", "region_fit",
                "tech_stack_match", "buying_intent", "data_completeness"):
        assert key in result["breakdown"]


def test_weights_sum_to_100():
    """All weights must sum to 100 so score is a true percentage."""
    signals = LeadSignals()
    icp = ICPFilter()
    result = score_lead(signals, icp)
    assert sum(result["weights"].values()) == 100


def test_buying_intent_all_three_signals_full_points():
    signals = LeadSignals(
        recent_funding_round=True,
        recent_executive_hire=True,
        recent_expansion_announcement=True,
    )
    icp = ICPFilter()
    result = score_lead(signals, icp)
    assert result["breakdown"]["buying_intent"] == result["weights"]["buying_intent"]


def test_data_completeness_partial_credit():
    """Missing fields → partial credit, not zero."""
    signals_one = LeadSignals(has_email=True)
    signals_three = LeadSignals(has_email=True, has_domain=True, has_linkedin=True)
    icp = ICPFilter()
    r1 = score_lead(signals_one, icp)
    r3 = score_lead(signals_three, icp)
    assert r1["breakdown"]["data_completeness"] < r3["breakdown"]["data_completeness"]


def test_rank_leads_returns_top_n_sorted_descending():
    icp = ICPFilter(target_sectors=["saas"])
    leads = [
        (LeadSignals(sector="fintech"), {"name": "low"}),
        (LeadSignals(sector="saas", has_email=True, has_domain=True,
                     has_linkedin=True), {"name": "high"}),
        (LeadSignals(sector="saas"), {"name": "mid"}),
    ]
    ranked = rank_leads(leads, icp, top_n=2)
    assert len(ranked) == 2
    assert ranked[0]["score"] >= ranked[1]["score"]
    # Metadata preserved
    assert "metadata" in ranked[0]
    assert "name" in ranked[0]["metadata"]


def test_rank_leads_top_n_caps_results():
    icp = ICPFilter()
    leads = [(LeadSignals(), {"i": i}) for i in range(10)]
    ranked = rank_leads(leads, icp, top_n=3)
    assert len(ranked) == 3
