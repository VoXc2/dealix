"""Renewal scheduler — JSONL store + due lookup + cycle confirmation."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from auto_client_acquisition.payment_ops.renewal_scheduler import (
    RenewalStatus,
    clear_for_test,
    list_by_customer,
    list_due,
    mark_confirmed,
    schedule_renewal,
)


@pytest.fixture(autouse=True)
def _isolated_ledger(tmp_path, monkeypatch):
    monkeypatch.setenv(
        "DEALIX_RENEWAL_SCHEDULE_PATH", str(tmp_path / "renewal.jsonl")
    )
    clear_for_test()
    yield
    clear_for_test()


def test_schedule_renewal_returns_awaiting_founder():
    s = schedule_renewal(
        customer_id="acme",
        plan="managed_revenue_ops_starter",
        amount_sar=2999,
        cadence_days=30,
    )
    assert s.status == RenewalStatus.AWAITING_FOUNDER.value
    assert s.cadence_days == 30
    assert s.amount_sar == 2999
    assert s.cycle_count == 0


def test_list_by_customer_returns_persisted_record():
    schedule_renewal(
        customer_id="acme", plan="managed_revenue_ops_starter", amount_sar=2999
    )
    schedule_renewal(
        customer_id="acme", plan="managed_revenue_ops_growth", amount_sar=4999
    )
    schedule_renewal(
        customer_id="beta", plan="managed_revenue_ops_starter", amount_sar=2999
    )
    items = list_by_customer("acme")
    assert len(items) == 2
    assert all(s.customer_id == "acme" for s in items)


def test_mark_confirmed_increments_cycle():
    s = schedule_renewal(
        customer_id="acme", plan="managed_revenue_ops_starter", amount_sar=2999
    )
    assert mark_confirmed(s.schedule_id) is True
    items = list_by_customer("acme")
    assert items[0].cycle_count == 1
    assert items[0].status == RenewalStatus.CONFIRMED.value


def test_auto_charge_eligible_after_three_cycles():
    s = schedule_renewal(
        customer_id="acme", plan="managed_revenue_ops_starter", amount_sar=2999
    )
    for _ in range(3):
        assert mark_confirmed(s.schedule_id) is True
    items = list_by_customer("acme")
    assert items[0].cycle_count == 3
    assert items[0].auto_charge_eligible is True


def test_list_due_excludes_future():
    schedule_renewal(
        customer_id="acme",
        plan="managed_revenue_ops_starter",
        amount_sar=2999,
        last_paid_at=datetime.now(timezone.utc).isoformat(),
    )
    due = list_due()
    assert due == []


def test_list_due_includes_past():
    past = (datetime.now(timezone.utc) - timedelta(days=40)).isoformat()
    schedule_renewal(
        customer_id="acme",
        plan="managed_revenue_ops_starter",
        amount_sar=2999,
        last_paid_at=past,
        cadence_days=30,
    )
    due = list_due()
    assert len(due) == 1
    assert due[0].customer_id == "acme"
