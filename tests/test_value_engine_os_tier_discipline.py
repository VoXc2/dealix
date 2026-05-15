"""Non-negotiable: a `measured` value metric needs a verifiable source.

Guards `no_unverified_outcomes` / `no_fake_proof`.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.control_plane_os.ledger import (
    get_control_ledger,
    reset_control_ledger,
)
from auto_client_acquisition.value_engine_os import (
    ValueDisciplineError,
    ValueTier,
    get_value_engine,
    reset_value_engine,
)


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_control_ledger()
    get_control_ledger().clear_dir()
    reset_value_engine()


def test_measured_metric_without_source_ref_rejected() -> None:
    with pytest.raises(ValueDisciplineError):
        get_value_engine().record_metric(
            run_id="r1", workflow_id="wf1", tier=ValueTier.MEASURED
        )


def test_measured_metric_with_source_ref_accepted() -> None:
    metric = get_value_engine().record_metric(
        run_id="r1",
        workflow_id="wf1",
        revenue_impact_sar=5000.0,
        tier=ValueTier.MEASURED,
        source_ref="control-ledger#evt_123",
    )
    assert metric.tier == "measured"


def test_estimated_metric_needs_no_source_ref() -> None:
    metric = get_value_engine().record_metric(
        run_id="r1", workflow_id="wf1", tier=ValueTier.ESTIMATED
    )
    assert metric.tier == "estimated"


def test_roi_aggregates_recorded_metrics() -> None:
    engine = get_value_engine()
    engine.record_metric(run_id="r1", workflow_id="wf1", revenue_impact_sar=3000.0)
    engine.record_metric(run_id="r2", workflow_id="wf1", revenue_impact_sar=2000.0)
    report = engine.roi_for_workflow("wf1", cost_sar=1000.0)
    assert report.total_value_sar == 5000.0
    assert report.roi_ratio == 5.0
