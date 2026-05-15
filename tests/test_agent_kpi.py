"""Agent OS — goal / KPI schema (task 4)."""
from __future__ import annotations

import pytest

from auto_client_acquisition.agent_os import (
    AgentKPI,
    clear_for_test,
    kpi_attainment,
    new_kpi,
    validate_kpi,
)


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_AGENT_REGISTRY_PATH", str(tmp_path / "agents.jsonl"))
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "fr.jsonl"))
    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    clear_for_test()
    yield
    clear_for_test()


def test_new_kpi_rejects_blank_metric():
    with pytest.raises(ValueError):
        new_kpi(
            agent_id="a1",
            output_metric="",
            output_target=10,
            business_impact_metric="revenue_sar",
            business_impact_target=5000,
        )


def test_new_kpi_rejects_non_positive_target():
    with pytest.raises(ValueError):
        new_kpi(
            agent_id="a1",
            output_metric="accounts_ranked",
            output_target=0,
            business_impact_metric="revenue_sar",
            business_impact_target=5000,
        )


def test_output_metric_must_differ_from_impact_metric():
    with pytest.raises(ValueError):
        new_kpi(
            agent_id="a1",
            output_metric="revenue_sar",
            output_target=10,
            business_impact_metric="revenue_sar",
            business_impact_target=5000,
        )


def test_validate_kpi_flags_bad_window():
    kpi = AgentKPI(
        agent_id="a1",
        output_metric="accounts_ranked",
        output_target=10,
        business_impact_metric="revenue_sar",
        business_impact_target=5000,
        window_days=0,
    )
    result = validate_kpi(kpi)
    assert result.ok is False
    assert "non_positive_window" in result.issues


def test_kpi_attainment_ratio():
    kpi = new_kpi(
        agent_id="a1",
        output_metric="accounts_ranked",
        output_target=10,
        business_impact_metric="revenue_sar",
        business_impact_target=5000,
    )
    out = kpi_attainment(kpi, output_actual=5, business_impact_actual=2500)
    assert out["output_attainment"] == 0.5
    assert out["business_impact_attainment"] == 0.5


def test_valid_kpi_roundtrip_to_dict():
    kpi = new_kpi(
        agent_id="a1",
        output_metric="accounts_ranked",
        output_target=10,
        business_impact_metric="revenue_sar",
        business_impact_target=5000,
    )
    d = kpi.to_dict()
    assert d["agent_id"] == "a1"
    assert d["output_metric"] == "accounts_ranked"
    assert validate_kpi(kpi).ok is True
