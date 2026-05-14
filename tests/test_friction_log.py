"""Friction log: emit/list, tenant isolation, aggregation, PII sanitization."""
from __future__ import annotations

import pytest

from auto_client_acquisition.friction_log.aggregator import (
    aggregate as aggregate_friction,
)
from auto_client_acquisition.friction_log.schemas import (
    FrictionKind,
    FrictionSeverity,
)
from auto_client_acquisition.friction_log.store import (
    clear_for_test as clear_friction,
)
from auto_client_acquisition.friction_log.store import (
    emit as emit_friction,
)
from auto_client_acquisition.friction_log.store import (
    list_events as list_friction,
)


@pytest.fixture(autouse=True)
def isolated_ledgers(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "friction.jsonl"))
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "value.jsonl"))
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "capital.jsonl"))
    try:
        clear_friction()
    except Exception:
        pass
    yield
    try:
        clear_friction()
    except Exception:
        pass


def test_emit_and_list_roundtrip() -> None:
    for _ in range(3):
        emit_friction(
            customer_id="A",
            kind=FrictionKind.GOVERNANCE_BLOCK,
            severity=FrictionSeverity.LOW,
        )
    events = list_friction(customer_id="A")
    assert len(events) == 3


def test_tenant_isolation() -> None:
    emit_friction(
        customer_id="A",
        kind=FrictionKind.GOVERNANCE_BLOCK,
        severity=FrictionSeverity.LOW,
    )
    events_b = list_friction(customer_id="B")
    assert events_b == []


def test_aggregator_kind_and_severity() -> None:
    emit_friction(customer_id="A", kind=FrictionKind.GOVERNANCE_BLOCK, severity="high")
    emit_friction(customer_id="A", kind=FrictionKind.APPROVAL_DELAY, severity="med")
    emit_friction(customer_id="A", kind=FrictionKind.APPROVAL_DELAY, severity="low")

    agg = aggregate_friction(customer_id="A", window_days=30)
    assert agg.by_kind.get("governance_block", 0) == 1
    assert agg.by_kind.get("approval_delay", 0) == 2
    assert agg.by_severity.get("high", 0) == 1
    assert agg.by_severity.get("med", 0) == 1
    assert agg.by_severity.get("low", 0) == 1


def test_aggregator_top_3_kinds_sorted_desc() -> None:
    for _ in range(4):
        emit_friction(customer_id="A", kind=FrictionKind.GOVERNANCE_BLOCK)
    for _ in range(2):
        emit_friction(customer_id="A", kind=FrictionKind.APPROVAL_DELAY)
    emit_friction(customer_id="A", kind=FrictionKind.SCHEMA_FAILURE)

    agg = aggregate_friction(customer_id="A", window_days=30)
    assert len(agg.top_3_kinds) <= 3
    counts = [c for _, c in agg.top_3_kinds]
    assert counts == sorted(counts, reverse=True)
    assert agg.top_3_kinds[0][1] == 4


def test_aggregator_total_cost_minutes() -> None:
    emit_friction(customer_id="A", kind=FrictionKind.RETRY, cost_minutes=5)
    emit_friction(customer_id="A", kind=FrictionKind.RETRY, cost_minutes=7)
    emit_friction(customer_id="A", kind=FrictionKind.SUPPORT_TICKET, cost_minutes=20)

    agg = aggregate_friction(customer_id="A", window_days=30)
    assert agg.total_cost_minutes == 32


def test_sanitizer_strips_email_from_notes() -> None:
    emit_friction(
        customer_id="A",
        kind=FrictionKind.SUPPORT_TICKET,
        notes="contact me at someone@example.com please",
    )
    events = list_friction(customer_id="A")
    assert events, "no events stored"
    assert "someone@example.com" not in events[0].notes


def test_sanitizer_strips_saudi_phone_from_notes() -> None:
    emit_friction(
        customer_id="A",
        kind=FrictionKind.SUPPORT_TICKET,
        notes="+966501234567 stuck on screen",
    )
    events = list_friction(customer_id="A")
    assert events, "no events stored"
    assert "+966501234567" not in events[0].notes


def test_rejects_empty_customer_id() -> None:
    with pytest.raises(ValueError):
        emit_friction(customer_id="", kind=FrictionKind.RETRY)
