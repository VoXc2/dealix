"""ROI attribution — engagement investment vs. tiered value ledger."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.delivery_factory.transformation_program import (
    clear_for_test as clear_programs,
    start_program,
)
from auto_client_acquisition.value_os.roi_attribution import (
    attribute_roi,
    program_investment_sar,
)
from auto_client_acquisition.value_os.value_ledger import (
    add_event,
    clear_for_test as clear_value,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "value.jsonl"))
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "fr.jsonl"))
    monkeypatch.setenv(
        "DEALIX_TRANSFORMATION_RUNS_PATH", str(tmp_path / "txp.jsonl")
    )
    clear_value("roi_co")
    clear_programs()
    yield
    clear_value("roi_co")
    clear_programs()


def test_program_investment_is_setup_plus_retainer() -> None:
    # ai_os_growth: setup 120,000 + monthly 25,000
    inv = program_investment_sar("ai_operating_system", "ai_os_growth", months=12)
    assert inv == 120_000 + 25_000 * 12


def test_estimated_value_never_folded_into_realized() -> None:
    add_event(customer_id="roi_co", kind="x", amount=500_000, tier="estimated")
    add_event(
        customer_id="roi_co", kind="x", amount=80_000, tier="verified",
        source_ref="invoice#1",
    )
    summary = attribute_roi(customer_id="roi_co", investment_sar=100_000)
    assert summary.estimated_value_sar == 500_000
    assert summary.realized_value_sar == 80_000  # verified only — not the estimate
    assert summary.roi_ratio_realized == 0.8


def test_roi_with_observed_separate_from_realized() -> None:
    add_event(
        customer_id="roi_co", kind="x", amount=40_000, tier="observed",
        source_ref="log#1",
    )
    add_event(
        customer_id="roi_co", kind="x", amount=60_000, tier="verified",
        source_ref="invoice#2",
    )
    summary = attribute_roi(customer_id="roi_co", investment_sar=100_000)
    assert summary.realized_value_sar == 60_000
    assert summary.roi_ratio_realized == 0.6
    assert summary.roi_ratio_with_observed == 1.0  # (60k + 40k) / 100k
    assert summary.is_estimate is True


def test_roi_endpoint_on_a_program() -> None:
    program = start_program(
        customer_id="roi_co",
        offering_id="enterprise_transformation_sprint",
        tier_id="sprint_growth",
    )
    add_event(
        customer_id="roi_co", kind="time_saved", amount=30_000, tier="verified",
        source_ref="report#1",
    )
    resp = client.get(
        f"/api/v1/transformation/{program.program_run_id}/roi",
        params={"retainer_months": 6},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    # sprint_growth: setup 75,000 + 8,000 * 6 = 123,000
    assert body["investment_sar"] == 123_000
    assert body["realized_value_sar"] == 30_000
    assert body["disclaimer"]


def test_roi_endpoint_404_for_unknown_program() -> None:
    resp = client.get("/api/v1/transformation/TXP-nope/roi")
    assert resp.status_code == 404
