"""Tests for dominance execution contracts and readiness snapshot."""

from __future__ import annotations

from auto_client_acquisition.dealix_master_layers import (
    CAPABILITY_CONTRACTS,
    DOMINANCE_GATES,
    OI_DOMINANCE_LAYERS,
    contracts_by_layer_slug,
    dominance_readiness_snapshot,
    missing_contract_layer_slugs,
)


def test_every_dominance_layer_has_contract() -> None:
    missing = missing_contract_layer_slugs()
    assert missing == ()


def test_contract_count_matches_layer_count() -> None:
    assert len(CAPABILITY_CONTRACTS) == len(OI_DOMINANCE_LAYERS) == 10


def test_grouping_preserves_all_contracts() -> None:
    grouped = contracts_by_layer_slug()
    total = sum(len(contracts) for contracts in grouped.values())
    assert total == len(CAPABILITY_CONTRACTS)
    assert "governed_autonomy_engine" in grouped


def test_gate_catalog_is_stable() -> None:
    assert [gate.gate_id for gate in DOMINANCE_GATES] == ["A", "B", "C", "D"]
    assert all(gate.priorities for gate in DOMINANCE_GATES)


def test_readiness_snapshot_shape() -> None:
    snapshot = dominance_readiness_snapshot()
    assert snapshot["layer_count"] == 10
    assert snapshot["contract_count"] == 10
    assert snapshot["missing_layer_contracts"] == []
    assert set(snapshot["status_counts"]) >= {"planned", "in_progress", "operational"}
