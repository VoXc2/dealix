"""Agent Observability — runs are recorded and PII is redacted on write."""

from __future__ import annotations

import pytest

from auto_client_acquisition.revenue_assurance_os.agent_observability import (
    list_runs,
    record_run,
)


@pytest.fixture(autouse=True)
def _isolated_log(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_AGENT_RUNS_PATH", str(tmp_path / "agent_runs.jsonl"))


def test_run_is_recorded_and_listed() -> None:
    record_run(agent_name="sales_autopilot", input_event="lead_captured")
    runs = list_runs()
    assert len(runs) == 1
    assert runs[0].agent_name == "sales_autopilot"
    assert runs[0].redacted is True


def test_raw_pii_is_redacted_on_write() -> None:
    record_run(
        agent_name="support_autopilot",
        input_event="customer wrote from buyer@example.com",
        output_summary="reply queued for 0501234567",
        input_refs=["contact buyer@example.com"],
    )
    run = list_runs()[0]
    assert "buyer@example.com" not in run.input_event
    assert "0501234567" not in run.output_summary
    assert "buyer@example.com" not in run.input_refs[0]


def test_empty_agent_name_rejected() -> None:
    with pytest.raises(ValueError):
        record_run(agent_name="  ", input_event="x")
