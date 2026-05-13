"""Revenue OS — lead scoring band tests (A / B / C / D).

اختبارات تقييم العملاء المحتملين في Revenue OS.

Guards `auto_client_acquisition/revenue_os/lead_scoring.py`: representative
records across the four bands plus a sanity check that rationale strings
travel with every feature.
"""
from __future__ import annotations

import pytest

pytest.importorskip("pydantic", reason="pydantic required for Revenue OS modules")


def test_high_trigger_high_vertical_record_lands_in_band_a():
    from auto_client_acquisition.revenue_os.lead_scoring import score_account

    record = {
        "vertical": "bfsi",
        "headcount": 500,
        "annual_revenue_sar": 500_000_000,
        "triggers": ["tender", "funding", "vision2030"],
        "data_quality_score": 92,
    }
    ls = score_account(record)
    assert ls.band == "A"
    assert ls.score >= 80


def test_mid_market_acceptable_data_lands_in_band_b():
    from auto_client_acquisition.revenue_os.lead_scoring import score_account

    record = {
        "vertical": "retail_ecomm",
        "headcount": 120,
        "annual_revenue_sar": 60_000_000,
        "triggers": ["hire"],
        "data_quality_score": 70,
    }
    ls = score_account(record)
    assert ls.band == "B"
    assert 60 <= ls.score < 80


def test_off_priority_sme_no_triggers_lands_in_band_c():
    from auto_client_acquisition.revenue_os.lead_scoring import score_account

    record = {
        "vertical": "manufacturing",
        "headcount": 30,
        "annual_revenue_sar": 10_000_000,
        "triggers": [],
        "data_quality_score": 65,
    }
    ls = score_account(record)
    assert ls.band == "C"
    assert 40 <= ls.score < 60


def test_empty_record_lands_in_band_d():
    """Negative path — an empty record should fall into the D band."""
    from auto_client_acquisition.revenue_os.lead_scoring import score_account

    ls = score_account({})
    assert ls.band == "D"
    assert ls.score < 40


def test_every_feature_has_bilingual_rationale():
    from auto_client_acquisition.revenue_os.lead_scoring import score_account

    ls = score_account({"vertical": "bfsi", "triggers": ["tender"]})
    assert ls.features, "expected at least one feature"
    for feat in ls.features:
        assert feat.rationale_ar
        assert feat.rationale_en


def test_score_serializes_via_to_dict():
    from auto_client_acquisition.revenue_os.lead_scoring import score_account

    ls = score_account({"vertical": "bfsi", "triggers": ["tender"]})
    payload = ls.to_dict()
    assert "score" in payload and "band" in payload
    assert payload["band"] in {"A", "B", "C", "D"}
    assert isinstance(payload["features"], list) and payload["features"]
