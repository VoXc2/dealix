"""Feature flags registry."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]


def test_feature_flags_yaml() -> None:
    data = yaml.safe_load((REPO / "dealix/transformation/feature_flags.yaml").read_text())
    assert len(data.get("flags") or []) >= 1
