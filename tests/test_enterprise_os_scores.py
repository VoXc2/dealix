"""Tests for enterprise_os (capital asset score, venture gate, façades)."""

from __future__ import annotations

from auto_client_acquisition.enterprise_os import (
    CapitalAssetBand,
    CapitalAssetScoreInputs,
    CapabilityScores,
    VentureGateInputs,
    capital_asset_band,
    compute_capital_asset_score,
    compute_dci,
    compute_dealix_capability_score,
    meets_venture_gate,
)


def test_capital_asset_score_playbook_example() -> None:
    i = CapitalAssetScoreInputs(90, 90, 85, 88, 85, 88)
    s = compute_capital_asset_score(i)
    assert s >= 80
    assert capital_asset_band(s) == CapitalAssetBand.STRATEGIC


def test_capital_asset_archive_band() -> None:
    i = CapitalAssetScoreInputs(20, 20, 20, 20, 20, 20)
    s = compute_capital_asset_score(i)
    assert s < 40
    assert capital_asset_band(s) == CapitalAssetBand.ARCHIVE


def test_venture_gate_pass_and_fail() -> None:
    ok = VentureGateInputs(
        paid_clients=5,
        retainers=2,
        delivery_repeatable=True,
        product_module_used=True,
        playbook_maturity=80,
        owner_exists=True,
        gross_margin_healthy=True,
        proof_library_exists=True,
    )
    assert meets_venture_gate(ok)
    bad = ok._replace(paid_clients=4)
    assert not meets_venture_gate(bad)


def test_capability_facade_matches_intelligence() -> None:
    c = CapabilityScores(50, 50, 50, 50, 50, 50, 50)
    assert compute_dealix_capability_score(c) == compute_dci(c) == 50.0
