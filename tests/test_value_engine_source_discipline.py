"""Value engine source discipline tests."""

from __future__ import annotations

import pytest

from auto_client_acquisition.value_engine_os.repositories import (
    InMemoryValueEngineRepository,
    WorkflowValueMetric,
)


def test_measured_metric_requires_source_ref() -> None:
    repo = InMemoryValueEngineRepository()
    with pytest.raises(ValueError, match="measured metrics require source_ref"):
        repo.record_metric(
            WorkflowValueMetric(
                metric_id="m1",
                tenant_id="tenant-a",
                run_id="run-1",
                metric_name="new_revenue",
                metric_kind="measured",
                value=1200.0,
            )
        )

    measured = repo.record_metric(
        WorkflowValueMetric(
            metric_id="m2",
            tenant_id="tenant-a",
            run_id="run-1",
            metric_name="new_revenue",
            metric_kind="measured",
            value=1200.0,
            source_ref="invoice:INV-001",
        )
    )
    estimated = repo.record_metric(
        WorkflowValueMetric(
            metric_id="m3",
            tenant_id="tenant-a",
            run_id="run-1",
            metric_name="new_revenue_forecast",
            metric_kind="estimated",
            value=1000.0,
        )
    )
    assert measured.source_ref == "invoice:INV-001"
    assert estimated.metric_kind == "estimated"
    roi = repo.roi_summary(tenant_id="tenant-a")
    assert roi == {"estimated_total": 1000.0, "measured_total": 1200.0, "delta": 200.0}
