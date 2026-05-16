"""Fast lane vs governed lane policy."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]


def test_lane_policy_has_two_lanes() -> None:
    data = yaml.safe_load((REPO / "dealix/transformation/lane_policy.yaml").read_text(encoding="utf-8"))
    lanes = data.get("lanes") or {}
    assert "fast_lane" in lanes
    assert "governed_lane" in lanes
    assert lanes["governed_lane"]["requires_approval"] is True
