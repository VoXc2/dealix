"""Tier discipline checks for value measurement contracts.

Name kept for compatibility with enterprise hardening scripts.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.value_os.value_ledger import (
    ValueDisciplineError,
    add_event,
    clear_for_test,
    list_events,
    summarize,
)


@pytest.fixture(autouse=True)
def _isolated_value_ledger(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "value.jsonl"))
    clear_for_test()
    yield
    clear_for_test()


def test_verified_value_requires_source_ref() -> None:
    with pytest.raises(ValueDisciplineError):
        add_event(
            tenant_id="tenant-acme",
            customer_id="acme",
            kind="revenue_uplift",
            amount=1000.0,
            tier="verified",
            source_ref="",
        )


def test_client_confirmed_requires_both_source_and_confirmation_refs() -> None:
    with pytest.raises(ValueDisciplineError):
        add_event(
            tenant_id="tenant-acme",
            customer_id="acme",
            kind="revenue_uplift",
            amount=1000.0,
            tier="client_confirmed",
            source_ref="invoice#1",
            confirmation_ref="",
        )

    with pytest.raises(ValueDisciplineError):
        add_event(
            tenant_id="tenant-acme",
            customer_id="acme",
            kind="revenue_uplift",
            amount=1000.0,
            tier="client_confirmed",
            source_ref="",
            confirmation_ref="signed_doc#1",
        )


def test_summary_preserves_tier_totals_without_auto_promotion() -> None:
    add_event(
        tenant_id="tenant-acme",
        customer_id="acme",
        kind="revenue_uplift",
        amount=200.0,
        tier="estimated",
    )
    add_event(
        tenant_id="tenant-acme",
        customer_id="acme",
        kind="revenue_uplift",
        amount=500.0,
        tier="verified",
        source_ref="invoice#22",
    )

    rows = list_events(customer_id="acme")
    summary = summarize(customer_id="acme", period_days=30)

    assert len(rows) == 2
    assert summary["estimated"]["amount"] == 200.0
    assert summary["verified"]["amount"] == 500.0
    assert summary["tenant_id"] == "tenant-acme"
