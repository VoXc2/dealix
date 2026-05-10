"""Schemas for the Approval Command Center.

Every "approval_required" action across the platform — outbound draft
messages, invoice drafts, proof packs, partner intros, etc. — funnels
through these schemas. The store is in-memory / file-backed for now;
the Pydantic surface is what stays stable when we swap to Redis later.

Wave 12 §32.3.6 (Engine 6 hardening) extends ``ApprovalRequest`` with
6 backward-compatible optional fields that close the link to Engine 4
(Decision Passport) and Engine 7 (Delivery OS):

- ``action_id``    — separate from approval_id; identifies the underlying
                     action (one action can have N approvals over time)
- ``lead_id``      — links back to the originating Lead
- ``customer_id``  — for tenant isolation + per-customer audit
- ``due_date``     — when the action must complete (vs expires_at which
                     is when the approval window closes)
- ``audit_ref``    — back-pointer to the radar_events / audit log entry
- ``proof_target`` — what proof event this action should produce

Plus ``ActionType`` Literal enum (canonical 11 action types from plan
§32.3.6) replaces the free-form ``action_type: str``.
"""
from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class ApprovalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    BLOCKED = "blocked"


# Wave 12 §32.3.6 — canonical 11 action types. ``action_type`` field stays
# ``str`` for backward-compat (existing callers pass arbitrary strings),
# but new code should use ActionType Literal for type-checked values.
ActionType = Literal[
    "prepare_diagnostic",        # build a diagnostic report for a prospect
    "draft_email",               # compose an outbound email (draft_only)
    "draft_linkedin_manual",     # compose a manual LinkedIn message (NEVER auto-send)
    "call_script",               # generate a phone-call talk-track
    "follow_up_task",            # schedule a follow-up (with deadline)
    "support_reply_draft",       # draft a support ticket reply
    "payment_reminder",          # remind founder to confirm a payment
    "delivery_task",             # a delivery_session step requiring approval
    "proof_request",             # request proof event from delivery
    "upsell_recommendation",     # generate next-best-offer suggestion
    "partner_intro",             # introduce two parties (founder-mediated)
]


def is_canonical_action_type(value: str) -> bool:
    """Is ``value`` one of the 11 canonical Wave 12 action types?

    Returns True for Literal-valid values, False for legacy free-form
    strings (which remain accepted for backward compat).
    """
    return value in {
        "prepare_diagnostic", "draft_email", "draft_linkedin_manual",
        "call_script", "follow_up_task", "support_reply_draft",
        "payment_reminder", "delivery_task", "proof_request",
        "upsell_recommendation", "partner_intro",
    }


class ApprovalRequest(BaseModel):
    """A single approvable action awaiting human review.

    ``action_mode`` mirrors the platform-wide gate vocabulary:
      - ``draft_only``        → never sent live, kept as draft
      - ``approval_required`` → human must approve before any send
      - ``approved_execute``  → already approved upstream; recorded for audit
      - ``blocked``           → hard-stopped by policy; cannot be approved
    """

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    approval_id: str = Field(default_factory=lambda: f"apr_{uuid4().hex[:12]}")
    object_type: str
    object_id: str
    action_type: str
    action_mode: str = "approval_required"
    channel: str | None = None
    summary_ar: str = ""
    summary_en: str = ""
    risk_level: str = "low"
    proof_impact: str = ""
    expires_at: datetime | None = None
    status: ApprovalStatus = ApprovalStatus.PENDING
    edit_history: list[dict[str, Any]] = Field(default_factory=list)
    reject_reason: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # ─── Wave 12 §32.3.6 hardening fields (all optional for back-compat) ───
    action_id: str | None = None
    """Stable identifier for the underlying action (separate from approval_id).

    Use case: a single action may go through multiple approval cycles
    (e.g. customer rejects, founder revises, customer re-approves) — but
    it remains the same action_id throughout, while approval_id changes.
    """

    lead_id: str | None = None
    """Back-pointer to the originating Lead (links to Engine 2)."""

    customer_id: str | None = None
    """Customer/tenant scope (for RBAC + tenant isolation per Engine 12)."""

    due_date: datetime | None = None
    """When the action must complete (separate from ``expires_at``,
    which is when the approval window closes). Used by Engine 7 (Delivery
    OS) and the Founder Bottleneck Radar (§32.4A.2).
    """

    audit_ref: str | None = None
    """Back-pointer to the radar_events / audit log entry that records
    this approval's lifecycle (matches Engine 12 audit log linkage).
    """

    proof_target: str | None = None
    """The proof event this action should produce on success.

    Hard rule (Article 8 + plan §32.3.6): high-risk actions require a
    proof_target — without it, the action contributes no compounding value
    and should be blocked or downgraded to draft_only.
    """
