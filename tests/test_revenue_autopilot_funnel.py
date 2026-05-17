"""Revenue Autopilot funnel — transitions + the 3 hard rules."""
from __future__ import annotations

import pytest

from auto_client_acquisition.revenue_autopilot.funnel import (
    advance_stage,
    is_revenue_countable,
    valid_transitions,
)


def test_valid_forward_transition():
    assert advance_stage("new_lead", "qualified_A") == "qualified_A"
    assert advance_stage("qualified_A", "meeting_booked") == "meeting_booked"


def test_illegal_skip_is_rejected():
    with pytest.raises(ValueError):
        advance_stage("new_lead", "invoice_sent")


def test_hard_rule_no_invoice_sent_without_scope_sent():
    # invoice_sent's only non-terminal predecessor is scope_sent.
    with pytest.raises(ValueError):
        advance_stage("scope_requested", "invoice_sent")
    assert advance_stage("scope_sent", "invoice_sent") == "invoice_sent"


def test_hard_rule_no_delivery_started_without_invoice_paid():
    with pytest.raises(ValueError):
        advance_stage("invoice_sent", "delivery_started")
    assert advance_stage("invoice_paid", "delivery_started") == "delivery_started"


def test_hard_rule_revenue_not_countable_before_invoice_paid():
    for stage in ("new_lead", "qualified_A", "scope_sent", "invoice_sent"):
        assert is_revenue_countable(stage) is False
    for stage in ("invoice_paid", "delivery_started", "proof_pack_sent"):
        assert is_revenue_countable(stage) is True


def test_closed_lost_is_terminal():
    assert valid_transitions("closed_lost") == set()


def test_closed_lost_reachable_from_active_stages():
    for stage in ("new_lead", "qualified_A", "scope_sent", "delivery_started"):
        assert advance_stage(stage, "closed_lost") == "closed_lost"
