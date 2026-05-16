"""Market-proof recording helpers.

Thin wrappers over `CommercialEngine` for the three highest-traffic commercial
transitions. Every send is guarded: `record_sent` refuses to record unless
`founder_confirmed=True` — nothing auto-sends.
"""

from __future__ import annotations

from typing import Literal

from auto_client_acquisition.commercial_os.engine import (
    CommercialEngine,
    RecordedTransition,
)

ReplyClassification = Literal["replied_interested", "silent", "not_interested"]


def record_prepared(
    engine: CommercialEngine,
    *,
    customer_id: str,
    subject_type: str,
    subject_id: str,
    actor: str = "system",
    payload: dict | None = None,
) -> RecordedTransition:
    """Record `commercial.prepared` (CEL2) — outreach drafted, nothing sent."""
    return engine.record_transition(
        customer_id=customer_id,
        subject_type=subject_type,
        subject_id=subject_id,
        next_state="prepared_not_sent",
        actor=actor,
        payload=payload,
    )


def record_sent(
    engine: CommercialEngine,
    *,
    customer_id: str,
    subject_type: str,
    subject_id: str,
    founder_confirmed: bool,
    actor: str = "system",
    payload: dict | None = None,
) -> RecordedTransition:
    """Record `commercial.sent` (CEL4).

    Raises `ValueError` if `founder_confirmed` is not `True` — hard rule 1.
    """
    if not founder_confirmed:
        raise ValueError("rule1_sent_requires_founder_confirmed")
    return engine.record_transition(
        customer_id=customer_id,
        subject_type=subject_type,
        subject_id=subject_id,
        next_state="sent",
        founder_confirmed=True,
        actor=actor,
        payload=payload,
    )


def record_reply_classified(
    engine: CommercialEngine,
    *,
    customer_id: str,
    subject_type: str,
    subject_id: str,
    classification: ReplyClassification,
    actor: str = "system",
    payload: dict | None = None,
) -> RecordedTransition:
    """Record `commercial.reply_classified` — every send gets a classification."""
    return engine.record_transition(
        customer_id=customer_id,
        subject_type=subject_type,
        subject_id=subject_id,
        next_state=classification,
        actor=actor,
        payload=payload,
    )


def record_meeting_used(
    engine: CommercialEngine,
    *,
    customer_id: str,
    subject_type: str,
    subject_id: str,
    actor: str = "system",
    payload: dict | None = None,
) -> RecordedTransition:
    """Record `commercial.meeting_used` (CEL5) — a Dealix artifact was used."""
    return engine.record_transition(
        customer_id=customer_id,
        subject_type=subject_type,
        subject_id=subject_id,
        next_state="used_in_meeting",
        used_in_meeting=True,
        actor=actor,
        payload=payload,
    )
