"""Enterprise Control Plane — value engine source discipline.

Check #8 of the verify contract: a measured (``verified``) value metric
is rejected unless it carries a ``source_ref``; ``client_confirmed``
also needs a ``confirmation_ref``. Estimated value never silently
becomes a verified claim.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.value_os.value_ledger import (
    ValueDisciplineError,
    add_event,
    clear_value_ledger_for_tests,
    list_events,
    validate_value_event,
)


@pytest.fixture(autouse=True)
def _isolated():
    clear_value_ledger_for_tests()
    yield
    clear_value_ledger_for_tests()


def test_verified_metric_requires_source_ref():
    with pytest.raises(ValueDisciplineError, match="verified_value_requires_source_ref"):
        add_event(customer_id="c1", kind="revenue_won", tier="verified", amount=10000)


def test_verified_metric_with_source_ref_is_accepted():
    event = add_event(
        customer_id="c1",
        kind="revenue_won",
        tier="verified",
        amount=10000,
        source_ref="crm:deal/4821",
    )
    assert event.tier == "verified"
    assert event.is_measured is True


def test_client_confirmed_requires_confirmation_ref():
    with pytest.raises(ValueDisciplineError, match="confirmation_ref"):
        add_event(
            customer_id="c1",
            kind="revenue_won",
            tier="client_confirmed",
            source_ref="crm:deal/4821",
        )


def test_estimated_metric_needs_no_source_ref():
    event = add_event(customer_id="c1", kind="time_saved", tier="estimated", amount=40)
    assert event.tier == "estimated"
    assert event.is_measured is False


def test_unknown_tier_is_rejected():
    with pytest.raises(ValueDisciplineError, match="unknown_value_tier"):
        validate_value_event(tier="guesstimate", source_ref="x")


def test_recorded_events_are_listable():
    add_event(customer_id="c1", kind="time_saved", tier="estimated", tenant_id="t1")
    add_event(
        customer_id="c1", kind="revenue_won", tier="verified",
        source_ref="crm:1", tenant_id="t1",
    )
    rows = list_events(customer_id="c1", tenant_id="t1")
    assert len(rows) == 2
    assert sum(1 for r in rows if r.is_measured) == 1
