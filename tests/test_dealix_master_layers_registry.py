"""Smoke tests for dealix_master_layers registry."""

from __future__ import annotations

from pathlib import Path

from auto_client_acquisition.dealix_master_layers import (
    IMPLEMENTATION_HINTS,
    MASTER_LAYERS,
    OI_DOMINANCE_LAYERS,
    dominance_layer_by_id,
    dominance_layer_by_slug,
    layer_by_folder,
    readme_path,
)


def test_master_layers_count_and_order() -> None:
    assert len(MASTER_LAYERS) == 37
    assert MASTER_LAYERS[0].folder == "00_constitution"
    assert MASTER_LAYERS[-1].folder == "36_architecture"


def test_layer_by_folder() -> None:
    assert layer_by_folder("10_agents") is not None
    assert layer_by_folder("10_agents").primary_packages[0] == "agentic_operations_os"
    assert layer_by_folder("missing") is None


def test_readme_paths_exist() -> None:
    repo = Path(__file__).resolve().parents[1]
    for layer in MASTER_LAYERS:
        p = readme_path(repo, layer.folder)
        assert p.is_file(), f"missing {p}"


def test_implementation_hints_nonempty() -> None:
    assert "saudi_layer" in IMPLEMENTATION_HINTS


def test_organizational_intelligence_layer_catalog_shape() -> None:
    assert len(OI_DOMINANCE_LAYERS) == 10
    assert OI_DOMINANCE_LAYERS[0].layer_id == 1
    assert OI_DOMINANCE_LAYERS[-1].layer_id == 10


def test_organizational_intelligence_lookup_helpers() -> None:
    layer = dominance_layer_by_slug("digital_workforce_infrastructure")
    assert layer is not None
    assert layer.layer_id == 2
    assert layer.title == "Digital Workforce Infrastructure"
    assert dominance_layer_by_slug("missing-layer") is None
    assert dominance_layer_by_id(10) is not None
    assert dominance_layer_by_id(999) is None


def test_organizational_intelligence_mapped_paths_exist() -> None:
    repo = Path(__file__).resolve().parents[1]
    for layer in OI_DOMINANCE_LAYERS:
        assert layer.mapped_paths, f"missing mapped_paths for {layer.slug}"
        assert layer.target_paths, f"missing target_paths for {layer.slug}"
        for target in layer.target_paths:
            assert target.startswith("/"), f"target path must be absolute style: {target}"
        for mapped_path in layer.mapped_paths:
            resolved = repo / mapped_path
            assert resolved.exists(), f"mapped path does not exist: {mapped_path}"
