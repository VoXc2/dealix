"""Feedback (NPS-style) model — comments are pre-redacted."""
from __future__ import annotations

from auto_client_acquisition.customer_data_plane.pii_redactor import redact_text
from auto_client_acquisition.growth_v10.schemas import FeedbackRecord


def record_feedback(customer_handle: str, score: int, comment: str) -> FeedbackRecord:
    """Build a FeedbackRecord with PII auto-redacted from the comment."""
    redacted = redact_text(comment) if isinstance(comment, str) else ""
    return FeedbackRecord(
        customer_handle=customer_handle,
        score=score,
        comment_redacted=redacted,
    )


def nps_band(score: int) -> str:
    if score >= 9:
        return "promoter"
    if score >= 7:
        return "passive"
    return "detractor"
