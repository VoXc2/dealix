"""Tests for investment_os PMF and trust_os primitives."""

from __future__ import annotations

import pytest

from auto_client_acquisition.investment_os import (
    FUNDING_READINESS_ITEMS,
    OPERATING_COVENANTS,
    PMF_WEIGHTS,
    VALUATION_DRIVERS,
    PmfScoreInputs,
    compute_pmf_score,
    pmf_band,
)
from auto_client_acquisition.trust_os import (
    CONTROL_PLANE_COMPONENTS,
    ENTERPRISE_TRUST_SECTIONS,
    example_ai_run_record,
    example_client_upload_passport,
)


def test_pmf_weights_sum_to_100() -> None:
    assert sum(PMF_WEIGHTS.values()) == 100


def test_compute_pmf_all_zero() -> None:
    z = PmfScoreInputs(0, 0, 0, 0, 0, 0, 0, 0)
    assert compute_pmf_score(z) == 0.0


def test_compute_pmf_all_hundred() -> None:
    h = PmfScoreInputs(100, 100, 100, 100, 100, 100, 100, 100)
    assert compute_pmf_score(h) == 100.0


def test_pmf_band_thresholds() -> None:
    assert pmf_band(85) == "scale"
    assert pmf_band(84.99) == "build"
    assert pmf_band(70) == "build"
    assert pmf_band(69.99) == "pilot"
    assert pmf_band(55) == "pilot"
    assert pmf_band(54.99) == "hold_or_kill"


def test_operating_covenant_count() -> None:
    assert len(OPERATING_COVENANTS) == 10


def test_funding_and_valuation_lens() -> None:
    assert len(FUNDING_READINESS_ITEMS) == 10
    assert len(VALUATION_DRIVERS) == 10


def test_trust_pack_sections() -> None:
    assert "human_oversight" in ENTERPRISE_TRUST_SECTIONS


def test_control_plane_component_count() -> None:
    assert len(CONTROL_PLANE_COMPONENTS) == 10


def test_example_passport_roundtrip_keys() -> None:
    p = example_client_upload_passport()
    d = p.to_jsonable()
    assert d["source_id"] == "SRC-001"
    assert d["contains_pii"] is True


def test_example_ai_run_has_required_keys() -> None:
    r = example_ai_run_record()
    assert r["ai_run_id"] == "AIR-001"
    assert r["governance_status"] == "approved_with_review"


def test_pmf_out_of_range_raises() -> None:
    with pytest.raises(ValueError, match=r"must be 0\.\.100"):
        compute_pmf_score(
            PmfScoreInputs(101, 0, 0, 0, 0, 0, 0, 0),
        )


def test_pmf_band_invalid_score_raises() -> None:
    with pytest.raises(ValueError):
        pmf_band(-1)
