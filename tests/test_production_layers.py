"""Production layer map unit tests."""

from __future__ import annotations

from dealix.commercial_ops.production_layers import (
    build_production_layers,
    layer_1_railway_p0,
)
from dealix.commercial_ops.railway_production import check_repo_railway_config


def test_repo_railway_config_ok() -> None:
    repo = check_repo_railway_config()
    assert repo["ok"], repo["issues"]


def test_layer_1_repo_without_env() -> None:
    layer = layer_1_railway_p0(check_env=False)
    assert layer["pct"] >= 50


def test_build_production_layers_shape() -> None:
    blob = build_production_layers(check_env=False)
    assert blob["verdict"] in ("PASS", "WARN", "FAIL")
    assert len(blob["layers"]) == 6
    assert blob["overall_pct"] >= 0
