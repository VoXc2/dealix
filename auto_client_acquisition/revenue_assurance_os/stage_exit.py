"""Stage Exit Criteria — every pipeline stage is a proof state, not a label.

A deal may not leave a stage until its exit criteria carry evidence.
"""

from __future__ import annotations

from enum import StrEnum


class PipelineStage(StrEnum):
    LEAD = "lead"
    QUALIFIED = "qualified"
    MEETING_BOOKED = "meeting_booked"
    MEETING_DONE = "meeting_done"
    SCOPE_REQUESTED = "scope_requested"
    SCOPE_SENT = "scope_sent"
    INVOICE_SENT = "invoice_sent"
    PAID = "paid"
    DELIVERY_STARTED = "delivery_started"
    PROOF_DELIVERED = "proof_delivered"
    UPSELL_CANDIDATE = "upsell_candidate"


STAGE_EXIT_CRITERIA: dict[PipelineStage, tuple[str, ...]] = {
    PipelineStage.LEAD: ("company_identified", "source_exists"),
    PipelineStage.QUALIFIED: ("icp_fit", "pain", "likely_budget", "owner"),
    PipelineStage.MEETING_BOOKED: ("calendar_or_confirmed_time",),
    PipelineStage.MEETING_DONE: ("notes", "pain_confirmed_or_rejected"),
    PipelineStage.SCOPE_REQUESTED: ("client_requested_scope",),
    PipelineStage.SCOPE_SENT: ("approved_scope", "price", "timeline", "exclusions"),
    PipelineStage.INVOICE_SENT: ("approved_invoice", "approved_scope"),
    PipelineStage.PAID: ("payment_proof_or_signed_commitment",),
    PipelineStage.DELIVERY_STARTED: ("invoice_paid_evidence",),
    PipelineStage.PROOF_DELIVERED: ("proof_pack_sent", "review_call_done"),
    PipelineStage.UPSELL_CANDIDATE: ("value_confirmed", "next_workflow_identified"),
}


def stage_exit_check(
    stage: PipelineStage | str,
    evidence_present: set[str] | frozenset[str],
) -> tuple[bool, tuple[str, ...]]:
    """Return ``(ok, missing_criteria)`` for a stage.

    ``ok`` is True only when every exit criterion has evidence.
    """
    stage = PipelineStage(stage) if not isinstance(stage, PipelineStage) else stage
    required = STAGE_EXIT_CRITERIA[stage]
    missing = tuple(c for c in required if c not in evidence_present)
    return (not missing, missing)


__all__ = [
    "STAGE_EXIT_CRITERIA",
    "PipelineStage",
    "stage_exit_check",
]
