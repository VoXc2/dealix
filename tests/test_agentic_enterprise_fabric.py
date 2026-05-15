"""Tests for the Agentic Enterprise AI Operating Fabric (12-layer index)."""

from __future__ import annotations

from pathlib import Path

from auto_client_acquisition.agentic_enterprise_os import (
    FABRIC_LAYERS,
    fabric_status,
    layer_by_key,
    layer_by_number,
    layer_to_dict,
    maturity_score,
    package_exists,
    resolve_layer_health,
)

_REPO = Path(__file__).resolve().parents[1]


def test_twelve_layers_numbered_one_to_twelve() -> None:
    assert len(FABRIC_LAYERS) == 12
    assert [ly.number for ly in FABRIC_LAYERS] == list(range(1, 13))


def test_layer_keys_are_unique() -> None:
    keys = [ly.key for ly in FABRIC_LAYERS]
    assert len(keys) == len(set(keys))


def test_every_layer_maps_to_at_least_one_package() -> None:
    for layer in FABRIC_LAYERS:
        assert layer.primary_packages, f"layer {layer.number} has no packages"
        assert layer.capabilities


def test_lookup_by_number_and_key() -> None:
    layer = layer_by_number(1)
    assert layer is not None
    assert layer.key == "agent_operating_system"
    assert layer_by_key("continuous_evolution").number == 12
    assert layer_by_number(99) is None
    assert layer_by_key("missing") is None


def test_mapped_packages_exist_on_disk() -> None:
    for layer in FABRIC_LAYERS:
        for pkg in layer.primary_packages:
            assert package_exists(pkg, _REPO), (
                f"layer {layer.number} maps to missing package {pkg}"
            )


def test_resolve_layer_health_is_operational() -> None:
    for layer in FABRIC_LAYERS:
        health = resolve_layer_health(layer, _REPO)
        assert health["coverage"] == 1.0
        assert health["status"] == "operational"
        assert health["packages_present"] == health["packages_total"]


def test_maturity_score_is_full() -> None:
    assert maturity_score(_REPO) == 1.0


def test_fabric_status_rollup() -> None:
    status = fabric_status(_REPO)
    assert status["layer_count"] == 12
    assert status["layers_operational"] == 12
    assert status["maturity_grade"] == "agentic_operating_company"
    assert status["human_over_the_loop"] is True
    assert status["governance_decision"] == "allow"
    assert len(status["layers"]) == 12


def test_layer_to_dict_is_serializable() -> None:
    d = layer_to_dict(FABRIC_LAYERS[0])
    assert d["number"] == 1
    assert isinstance(d["primary_packages"], list)
    assert isinstance(d["capabilities"], list)
