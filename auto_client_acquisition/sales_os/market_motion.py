"""Governed Market Motion OS for founder-led outreach.

Deterministic rules to classify outreach outcomes, tie them to evidence
levels (L4-L7), and produce board-level next-action decisions.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, StrEnum
from typing import Final, Iterable


class MarketEvidenceLevel(IntEnum):
    """External-market evidence ladder used by the sales motion."""

    L4_SENT_EXTERNAL_EXPOSURE = 4
    L5_USED_IN_MEETING = 5
    L6_MARKET_PULL = 6
    L7_REVENUE_CONFIRMED = 7


class ResponseEvent(StrEnum):
    """Canonical response classes for warm outreach."""

    SENT = "sent"
    REPLIED_INTERESTED = "replied_interested"
    SEND_MORE_INFO = "send_more_info"
    ASKS_FOR_CASE_STUDY = "asks_for_case_study"
    ASKS_FOR_PDF = "asks_for_pdf"
    ASKS_FOR_ENGLISH = "asks_for_english"
    ASKS_FOR_SCOPE = "asks_for_scope"
    MEETING_BOOKED = "meeting_booked"
    USED_IN_MEETING = "used_in_meeting"
    PILOT_INTRO_REQUESTED = "pilot_intro_requested"
    NO_RESPONSE_AFTER_FOLLOW_UP = "no_response_after_follow_up"
    INVOICE_SENT = "invoice_sent"
    INVOICE_PAID = "invoice_paid"


class BoardDecisionAction(StrEnum):
    """Allowed board recommendations after batch-level signals."""

    CONTINUE = "continue"
    REVISE_MESSAGE = "revise_message"
    TEST_BATCH_2 = "test_batch_2"
    BUILD_PDF = "build_pdf"
    PREPARE_SCOPE = "prepare_scope"


@dataclass(frozen=True, slots=True)
class ResponsePolicy:
    """Decision policy for one response event."""

    next_action: str
    evidence_level: int | None = None
    revenue_confirmed: bool = False
    l7_candidate: bool = False


@dataclass(frozen=True, slots=True)
class MarketMotionMetrics:
    """Minimal metrics for CEO scorecard + board intake."""

    sent_count: int
    reply_count: int
    reply_rate: float
    meeting_count: int
    meeting_rate: float
    l5_count: int
    l6_count: int
    invoice_sent_count: int
    invoice_paid_count: int
    asks_for_scope_count: int
    asks_for_pdf_count: int
    no_response_count: int


_REPLY_EVENTS: Final[set[ResponseEvent]] = {
    ResponseEvent.REPLIED_INTERESTED,
    ResponseEvent.SEND_MORE_INFO,
    ResponseEvent.ASKS_FOR_CASE_STUDY,
    ResponseEvent.ASKS_FOR_PDF,
    ResponseEvent.ASKS_FOR_ENGLISH,
    ResponseEvent.ASKS_FOR_SCOPE,
    ResponseEvent.MEETING_BOOKED,
    ResponseEvent.USED_IN_MEETING,
    ResponseEvent.PILOT_INTRO_REQUESTED,
    ResponseEvent.INVOICE_SENT,
    ResponseEvent.INVOICE_PAID,
}

_POLICY_BY_EVENT: Final[dict[ResponseEvent, ResponsePolicy]] = {
    ResponseEvent.SENT: ResponsePolicy(
        next_action="log_l4_external_exposure",
        evidence_level=int(MarketEvidenceLevel.L4_SENT_EXTERNAL_EXPOSURE),
    ),
    ResponseEvent.REPLIED_INTERESTED: ResponsePolicy(next_action="ask_for_meeting"),
    ResponseEvent.SEND_MORE_INFO: ResponsePolicy(next_action="offer_30_minute_framing"),
    ResponseEvent.ASKS_FOR_CASE_STUDY: ResponsePolicy(next_action="send_proof_stage_response"),
    ResponseEvent.ASKS_FOR_PDF: ResponsePolicy(next_action="send_mini_pdf_only"),
    ResponseEvent.ASKS_FOR_ENGLISH: ResponsePolicy(next_action="send_english_one_pager_only"),
    ResponseEvent.ASKS_FOR_SCOPE: ResponsePolicy(
        next_action="draft_diagnostic_scope",
        evidence_level=int(MarketEvidenceLevel.L6_MARKET_PULL),
    ),
    ResponseEvent.MEETING_BOOKED: ResponsePolicy(next_action="prepare_meeting_agenda"),
    ResponseEvent.USED_IN_MEETING: ResponsePolicy(
        next_action="log_l5_used_in_meeting",
        evidence_level=int(MarketEvidenceLevel.L5_USED_IN_MEETING),
    ),
    ResponseEvent.PILOT_INTRO_REQUESTED: ResponsePolicy(
        next_action="log_l6_market_pull_intro",
        evidence_level=int(MarketEvidenceLevel.L6_MARKET_PULL),
    ),
    ResponseEvent.NO_RESPONSE_AFTER_FOLLOW_UP: ResponsePolicy(
        next_action="move_to_batch_2"
    ),
    ResponseEvent.INVOICE_SENT: ResponsePolicy(
        next_action="mark_l7_candidate",
        l7_candidate=True,
    ),
    ResponseEvent.INVOICE_PAID: ResponsePolicy(
        next_action="mark_revenue_confirmed",
        evidence_level=int(MarketEvidenceLevel.L7_REVENUE_CONFIRMED),
        revenue_confirmed=True,
    ),
}


def classify_response_event(event: ResponseEvent) -> ResponsePolicy:
    """Return deterministic policy for a response event."""

    return _POLICY_BY_EVENT[event]


def highest_evidence_level(events: Iterable[ResponseEvent]) -> int | None:
    """Return highest achieved evidence level in the event stream."""

    levels = [
        policy.evidence_level
        for e in events
        if (policy := _POLICY_BY_EVENT.get(e)) and policy.evidence_level is not None
    ]
    return max(levels) if levels else None


def can_claim_traction(events: Iterable[ResponseEvent]) -> bool:
    """Traction claims require at least L5 evidence."""

    level = highest_evidence_level(events)
    return bool(level is not None and level >= int(MarketEvidenceLevel.L5_USED_IN_MEETING))


def can_claim_revenue(events: Iterable[ResponseEvent]) -> bool:
    """Revenue claims require confirmed invoice payment."""

    return any(e == ResponseEvent.INVOICE_PAID for e in events)


def build_market_motion_metrics(events: Iterable[ResponseEvent]) -> MarketMotionMetrics:
    """Aggregate core metrics from response events."""

    event_list = list(events)
    sent_count = sum(1 for e in event_list if e == ResponseEvent.SENT)
    reply_count = sum(1 for e in event_list if e in _REPLY_EVENTS)
    meeting_count = sum(1 for e in event_list if e == ResponseEvent.MEETING_BOOKED)
    l5_count = sum(1 for e in event_list if e == ResponseEvent.USED_IN_MEETING)
    l6_count = sum(
        1
        for e in event_list
        if e in {ResponseEvent.PILOT_INTRO_REQUESTED, ResponseEvent.ASKS_FOR_SCOPE}
    )
    invoice_sent_count = sum(1 for e in event_list if e == ResponseEvent.INVOICE_SENT)
    invoice_paid_count = sum(1 for e in event_list if e == ResponseEvent.INVOICE_PAID)
    asks_for_scope_count = sum(1 for e in event_list if e == ResponseEvent.ASKS_FOR_SCOPE)
    asks_for_pdf_count = sum(1 for e in event_list if e == ResponseEvent.ASKS_FOR_PDF)
    no_response_count = sum(
        1 for e in event_list if e == ResponseEvent.NO_RESPONSE_AFTER_FOLLOW_UP
    )

    reply_rate = (reply_count / sent_count) if sent_count else 0.0
    meeting_rate = (meeting_count / sent_count) if sent_count else 0.0

    return MarketMotionMetrics(
        sent_count=sent_count,
        reply_count=reply_count,
        reply_rate=reply_rate,
        meeting_count=meeting_count,
        meeting_rate=meeting_rate,
        l5_count=l5_count,
        l6_count=l6_count,
        invoice_sent_count=invoice_sent_count,
        invoice_paid_count=invoice_paid_count,
        asks_for_scope_count=asks_for_scope_count,
        asks_for_pdf_count=asks_for_pdf_count,
        no_response_count=no_response_count,
    )


def recommend_board_action(metrics: MarketMotionMetrics) -> BoardDecisionAction:
    """Map scorecard signals to one board-level decision."""

    if metrics.asks_for_scope_count > 0:
        return BoardDecisionAction.PREPARE_SCOPE
    if metrics.asks_for_pdf_count > 0:
        return BoardDecisionAction.BUILD_PDF
    if metrics.sent_count >= 5 and metrics.reply_count == 0 and metrics.no_response_count > 0:
        return BoardDecisionAction.REVISE_MESSAGE
    if metrics.sent_count >= 5 and metrics.reply_count == 0:
        return BoardDecisionAction.TEST_BATCH_2
    return BoardDecisionAction.CONTINUE


__all__ = [
    "BoardDecisionAction",
    "MarketEvidenceLevel",
    "MarketMotionMetrics",
    "ResponseEvent",
    "ResponsePolicy",
    "build_market_motion_metrics",
    "can_claim_revenue",
    "can_claim_traction",
    "classify_response_event",
    "highest_evidence_level",
    "recommend_board_action",
]
