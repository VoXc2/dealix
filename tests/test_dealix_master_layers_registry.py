"""Smoke tests for dealix_master_layers registry."""

from __future__ import annotations

from pathlib import Path

from auto_client_acquisition.dealix_master_layers import (
    IMPLEMENTATION_HINTS,
    MASTER_LAYERS,
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
