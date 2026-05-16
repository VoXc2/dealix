"""Tests for governed market motion OS rules."""

from __future__ import annotations

from auto_client_acquisition.sales_os.market_motion import (
    BoardDecisionAction,
    ResponseEvent,
    build_market_motion_metrics,
    can_claim_revenue,
    can_claim_traction,
    classify_response_event,
    highest_evidence_level,
    recommend_board_action,
)


def test_event_classification_for_scope_and_invoice() -> None:
    scope_policy = classify_response_event(ResponseEvent.ASKS_FOR_SCOPE)
    assert scope_policy.next_action == "draft_diagnostic_scope"
    assert scope_policy.evidence_level == 6

    invoice_policy = classify_response_event(ResponseEvent.INVOICE_SENT)
    assert invoice_policy.l7_candidate is True
    assert invoice_policy.evidence_level is None

    paid_policy = classify_response_event(ResponseEvent.INVOICE_PAID)
    assert paid_policy.revenue_confirmed is True
    assert paid_policy.evidence_level == 7


def test_evidence_claim_guards() -> None:
    events = [ResponseEvent.SENT, ResponseEvent.MEETING_BOOKED]
    assert highest_evidence_level(events) == 4
    assert can_claim_traction(events) is False
    assert can_claim_revenue(events) is False

    events.append(ResponseEvent.USED_IN_MEETING)
    assert highest_evidence_level(events) == 5
    assert can_claim_traction(events) is True

    events.append(ResponseEvent.INVOICE_PAID)
    assert can_claim_revenue(events) is True


def test_metrics_and_board_decision_flow() -> None:
    events = [
        ResponseEvent.SENT,
        ResponseEvent.SENT,
        ResponseEvent.SENT,
        ResponseEvent.SENT,
        ResponseEvent.SENT,
        ResponseEvent.REPLIED_INTERESTED,
        ResponseEvent.ASKS_FOR_PDF,
        ResponseEvent.MEETING_BOOKED,
        ResponseEvent.USED_IN_MEETING,
        ResponseEvent.ASKS_FOR_SCOPE,
        ResponseEvent.INVOICE_SENT,
    ]
    metrics = build_market_motion_metrics(events)
    assert metrics.sent_count == 5
    assert metrics.reply_count == 6
    assert metrics.l5_count == 1
    assert metrics.l6_count == 1
    assert metrics.invoice_sent_count == 1
    assert metrics.invoice_paid_count == 0
    assert metrics.reply_rate == 6 / 5
    assert metrics.meeting_rate == 1 / 5
    assert recommend_board_action(metrics) == BoardDecisionAction.PREPARE_SCOPE


def test_board_decision_for_zero_reply_after_batch() -> None:
    events = [
        ResponseEvent.SENT,
        ResponseEvent.SENT,
        ResponseEvent.SENT,
        ResponseEvent.SENT,
        ResponseEvent.SENT,
    ]
    metrics = build_market_motion_metrics(events)
    assert recommend_board_action(metrics) == BoardDecisionAction.TEST_BATCH_2

    with_followup = events + [ResponseEvent.NO_RESPONSE_AFTER_FOLLOW_UP]
    metrics_followup = build_market_motion_metrics(with_followup)
    assert recommend_board_action(metrics_followup) == BoardDecisionAction.REVISE_MESSAGE
