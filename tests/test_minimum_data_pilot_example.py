"""The shipped minimum-data onboarding example must stay valid and synthetic."""

from __future__ import annotations

import json
from pathlib import Path

from dealix.privacy.minimum_data import MinimumDataPilotDataset

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "templates" / "minimum_data_revenue_command_pilot.example.json"


def test_minimum_data_example_validates_without_import() -> None:
    payload = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    dataset = MinimumDataPilotDataset.model_validate(payload)
    assert dataset.profile_id == "revenue_command_minimum_data_v1"
    assert len(dataset.baseline_metrics) >= 1
    assert len(dataset.opportunities) >= 1


def test_minimum_data_example_is_clearly_non_customer_synthetic() -> None:
    raw = EXAMPLE.read_text(encoding="utf-8")
    for marker in ("example", "OPP-017", "OPP-023"):
        assert marker in raw
    for forbidden in (
        "@",
        "+966",
        "linkedin.com",
        "iban",
        "password",
        "api_key",
        "access_token",
        "refresh_token",
    ):
        assert forbidden not in raw.casefold(), forbidden
