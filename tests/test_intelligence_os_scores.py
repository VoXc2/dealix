"""Tests for intelligence_os pure scoring."""

from __future__ import annotations

from auto_client_acquisition.intelligence_os.capital_allocator import (
    PriorityBand,
    PriorityInputs,
    capital_priority_band,
    compute_capital_priority_score,
)
from auto_client_acquisition.intelligence_os.events_to_metrics import metric_family_for_event
from auto_client_acquisition.intelligence_os.venture_signal import (
    VentureInputs,
    VentureReadinessBand,
    classify_venture_readiness,
    compute_venture_readiness_score,
)


def test_capital_priority_score_mid() -> None:
    p = PriorityInputs(80, 80, 80, 80, 80, 80)
    assert compute_capital_priority_score(p) == 80.0


def test_capital_priority_bands() -> None:
    assert capital_priority_band(90) == PriorityBand.INVEST_SCALE
    assert capital_priority_band(75) == PriorityBand.BUILD_CAREFULLY
    assert capital_priority_band(60) == PriorityBand.PILOT_ONLY
    assert capital_priority_band(45) == PriorityBand.HOLD
    assert capital_priority_band(30) == PriorityBand.KILL


def test_venture_readiness_bands() -> None:
    v = VentureInputs(90, 90, 90, 90, 90, 90, 90)
    assert compute_venture_readiness_score(v) == 90.0
    assert classify_venture_readiness(90) == VentureReadinessBand.VENTURE_CANDIDATE
    assert classify_venture_readiness(75) == VentureReadinessBand.BUSINESS_UNIT
    assert classify_venture_readiness(60) == VentureReadinessBand.SERVICE_LINE
    assert classify_venture_readiness(40) == VentureReadinessBand.CORE_SERVICES


def test_metric_family_for_event() -> None:
    assert metric_family_for_event("proof_event_created") == "proof"
    assert metric_family_for_event("unknown_event") is None
