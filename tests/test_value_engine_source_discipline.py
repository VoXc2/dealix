"""Value engine source evidence discipline."""

from __future__ import annotations

import pytest

from auto_client_acquisition.value_engine_os.repositories import (
    InMemoryValueEngineRepository,
    ValueEngineDisciplineError,
)


def test_measured_metric_requires_source_ref() -> None:
    repo = InMemoryValueEngineRepository()
    with pytest.raises(ValueEngineDisciplineError, match="source_ref"):
        repo.add_metric(
            tenant_id="tenant_a",
            run_id="run_1",
            metric_name="roi",
            metric_type="measured",
            value=1200,
            source_ref="",
        )


def test_roi_report_aggregates_estimated_and_measured() -> None:
    repo = InMemoryValueEngineRepository()
    repo.add_metric(
        tenant_id="tenant_a",
        run_id="run_1",
        metric_name="roi_est",
        metric_type="estimated",
        value=500,
    )
    repo.add_metric(
        tenant_id="tenant_a",
        run_id="run_1",
        metric_name="roi_real",
        metric_type="measured",
        value=320,
        source_ref="invoice#22",
    )
    report = repo.roi_report(tenant_id="tenant_a", run_id="run_1")
    assert report["estimated_total"] == 500
    assert report["measured_total"] == 320
