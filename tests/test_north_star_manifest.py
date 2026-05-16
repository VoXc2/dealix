"""North star manifest sync."""

from __future__ import annotations

from pathlib import Path

import yaml

from auto_client_acquisition.business.launch_metrics import north_star_metrics

REPO = Path(__file__).resolve().parents[1]


def test_manifest_canonical() -> None:
    data = yaml.safe_load(
        (REPO / "dealix/transformation/north_star_manifest.yaml").read_text(encoding="utf-8")
    )
    assert data.get("canonical") is True
    assert data.get("primary_metric_key") == "measured_customer_value_sar"


def test_launch_metrics_bridge() -> None:
    ns = north_star_metrics()
    assert ns["primary"] == "measured_customer_value_sar"
    assert "manifest" in ns
