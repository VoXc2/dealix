"""Tests for System 31 — runtime_safety_os."""

from __future__ import annotations

import pytest

from auto_client_acquisition.control_plane_os.ledger import (
    get_control_ledger,
    reset_control_ledger,
)
from auto_client_acquisition.runtime_safety_os import (
    get_safety_engine,
    reset_safety_engine,
)


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_control_ledger()
    get_control_ledger().clear_dir()
    reset_safety_engine()


def test_breaker_trips_at_threshold() -> None:
    engine = get_safety_engine()
    for _ in range(2):
        engine.record_failure("target1", threshold=3)
    assert engine.check(target="target1").allowed is True
    engine.record_failure("target1", threshold=3)
    verdict = engine.check(target="target1")
    assert verdict.allowed is False
    assert "circuit_open" in verdict.barriers_hit


def test_kill_switch_blocks_target() -> None:
    engine = get_safety_engine()
    engine.engage_kill_switch(target="wfX", reason="emergency")
    verdict = engine.check(target="wfX")
    assert verdict.allowed is False
    assert "kill_switch" in verdict.barriers_hit


def test_reset_breaker_clears_block() -> None:
    engine = get_safety_engine()
    for _ in range(3):
        engine.record_failure("t", threshold=3)
    engine.reset_breaker("t")
    assert engine.check(target="t").allowed is True
