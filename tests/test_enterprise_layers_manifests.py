"""Schema + integrity tests for the 8 enterprise layer manifests."""

from __future__ import annotations

from pathlib import Path

import pytest

from dealix.layer_validation.loader import (
    load_all,
    load_manifest,
    validate_all,
    validate_schema,
)
from dealix.layer_validation.spec import ENTERPRISE_LAYERS, lower_layer_ids

REPO = Path(__file__).resolve().parents[1]
_LAYER_IDS = [spec.id for spec in ENTERPRISE_LAYERS]


def test_all_manifests_load_and_validate() -> None:
    assert validate_all() == []


def test_exactly_eight_layers() -> None:
    assert len(ENTERPRISE_LAYERS) == 8
    orders = sorted(spec.order for spec in ENTERPRISE_LAYERS)
    assert orders == list(range(1, 9))
    assert len(set(_LAYER_IDS)) == 8


@pytest.mark.parametrize("layer_id", _LAYER_IDS)
def test_manifest_schema_valid(layer_id: str) -> None:
    manifest = load_manifest(layer_id)
    assert validate_schema(layer_id, manifest) == []


@pytest.mark.parametrize("layer_id", _LAYER_IDS)
def test_depends_on_is_every_lower_layer(layer_id: str) -> None:
    manifest = load_manifest(layer_id)["layer"]
    assert set(manifest["depends_on"]) == set(lower_layer_ids(layer_id))


@pytest.mark.parametrize("layer_id", _LAYER_IDS)
def test_module_paths_are_real(layer_id: str) -> None:
    manifest = load_manifest(layer_id)["layer"]
    for module in manifest["modules"]:
        path = module["path"]
        assert (REPO / path).exists(), f"{layer_id}: module path missing: {path}"


@pytest.mark.parametrize("layer_id", _LAYER_IDS)
def test_required_test_paths_are_real(layer_id: str) -> None:
    manifest = load_manifest(layer_id)["layer"]
    for spec in manifest["required_tests"]:
        if any(ch in spec for ch in "*?["):
            assert list(REPO.glob(spec)), f"{layer_id}: glob matched nothing: {spec}"
        else:
            assert (REPO / spec).is_file(), f"{layer_id}: required test missing: {spec}"


def test_load_all_returns_eight_layers() -> None:
    assert sorted(load_all().keys()) == sorted(_LAYER_IDS)
