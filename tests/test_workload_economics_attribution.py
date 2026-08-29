from __future__ import annotations

import pytest

from dealix.observability.economic_attribution import (
    UNKNOWN,
    WorkloadEconomicsAttribution,
    WorkloadMeasurement,
)


def test_measurement_attributes_time_cost_and_evidence() -> None:
    run = WorkloadMeasurement(
        run_id="run-1",
        workload_id="content-draft",
        agent_id="dealix-content",
        account_id="acct-1",
        started_at="2026-08-29T08:00:00+00:00",
        completed_at="2026-08-29T09:00:00+00:00",
        output_evidence_refs=["evidence-2", "evidence-1"],
        first_evidence_at="2026-08-29T08:15:00+00:00",
        founder_minutes=4.5,
        provider="deepseek",
        model="deepseek-chat",
        input_tokens=1000,
        output_tokens=500,
        cached_tokens=0,
        payment_proof_refs=["payment-1"],
    )

    record = WorkloadEconomicsAttribution().measure(run).to_dict()

    assert record["duration_ms"] == 3_600_000.0
    assert record["time_to_evidence_ms"] == 900_000.0
    assert record["output_evidence_refs"] == ["evidence-1", "evidence-2"]
    assert record["payment_proof_state"] == "REFERENCE_RECORDED_REQUIRES_CANONICAL_VERIFICATION"
    assert record["verified_revenue"] == UNKNOWN
    assert record["customer_value_state"] == UNKNOWN
    assert record["llm_cost_usd"] == 0.00028
    assert record["cost_basis"] == "MODEL_PRICE_TABLE"


def test_missing_attribution_stays_unknown() -> None:
    run = WorkloadMeasurement(
        run_id="run-1",
        workload_id="research",
        agent_id="market-intelligence",
        started_at="2026-08-29T08:00:00+00:00",
        completed_at="2026-08-29T08:01:00+00:00",
    )

    record = WorkloadEconomicsAttribution().measure(run).to_dict()

    assert record["time_to_evidence_ms"] == UNKNOWN
    assert record["llm_cost_usd"] == UNKNOWN
    assert record["evidence_state"] == UNKNOWN
    assert record["payment_proof_state"] == UNKNOWN
    assert record["verified_revenue"] == UNKNOWN


def test_synthetic_output_cannot_create_payment_state() -> None:
    run = WorkloadMeasurement(
        run_id="run-1",
        workload_id="rehearsal",
        agent_id="dealix-engineer",
        started_at="2026-08-29T08:00:00+00:00",
        completed_at="2026-08-29T08:01:00+00:00",
        payment_proof_refs=["synthetic-payment"],
        synthetic_output=True,
    )

    record = WorkloadEconomicsAttribution().measure(run).to_dict()

    assert record["payment_proof_state"] == UNKNOWN
    assert record["payment_proof_refs"] == []


def test_time_to_evidence_requires_an_output_ref_and_valid_window() -> None:
    run = WorkloadMeasurement(
        run_id="run-1",
        workload_id="bad-run",
        agent_id="dealix-engineer",
        started_at="2026-08-29T08:00:00+00:00",
        completed_at="2026-08-29T08:01:00+00:00",
        first_evidence_at="2026-08-29T08:00:30+00:00",
    )

    with pytest.raises(ValueError, match="output_evidence_refs"):
        WorkloadEconomicsAttribution().measure(run)


def test_report_is_stable_and_rejects_duplicate_runs() -> None:
    first = WorkloadMeasurement(
        run_id="run-2",
        workload_id="b",
        agent_id="agent",
        started_at="2026-08-29T08:00:00+00:00",
        completed_at="2026-08-29T08:02:00+00:00",
    )
    second = WorkloadMeasurement(
        run_id="run-1",
        workload_id="a",
        agent_id="agent",
        started_at="2026-08-29T08:00:00+00:00",
        completed_at="2026-08-29T08:01:00+00:00",
    )
    engine = WorkloadEconomicsAttribution()
    report = engine.summarize([first, second])
    reversed_report = engine.summarize([second, first])

    assert report.semantic_dict() == reversed_report.semantic_dict()
    assert [item["workload_id"] for item in report.workload_summaries] == ["a", "b"]

    with pytest.raises(ValueError, match="run_id must be unique"):
        engine.summarize([first, first])
