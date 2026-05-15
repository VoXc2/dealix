"""Value engine source discipline tests."""

from __future__ import annotations

import pytest

from auto_client_acquisition.value_engine_os import (
    ValueEngineRepository,
    WorkflowValueMetric,
)


def test_measured_metrics_require_source_ref() -> None:
    repo = ValueEngineRepository()
    with pytest.raises(ValueError):
        repo.record(
            WorkflowValueMetric(
                tenant_id="tenant-a",
                run_id="run-1",
                metric_name="pipeline_value",
                tier="measured",
                amount=100,
                source_ref="",
            ),
        )


def test_client_confirmed_requires_confirmation_ref() -> None:
    repo = ValueEngineRepository()
    with pytest.raises(ValueError):
        repo.record(
            WorkflowValueMetric(
                tenant_id="tenant-a",
                run_id="run-1",
                metric_name="pipeline_value",
                tier="client_confirmed",
                amount=100,
                source_ref="inv-1",
                confirmation_ref="",
            ),
        )


def test_roi_report_returns_expected_totals() -> None:
    repo = ValueEngineRepository()
    repo.record(
        WorkflowValueMetric(
            tenant_id="tenant-a",
            run_id="run-1",
            metric_name="pipeline_value",
            tier="estimated",
            amount=100,
        ),
    )
    repo.record(
        WorkflowValueMetric(
            tenant_id="tenant-a",
            run_id="run-1",
            metric_name="pipeline_value",
            tier="verified",
            amount=40,
            source_ref="invoice#12",
        ),
    )
    report = repo.roi_report(tenant_id="tenant-a", run_id="run-1")
    assert report["total_estimated_value"] == 140.0
    assert report["total_measured_value"] == 40.0
