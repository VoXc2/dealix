"""Pydantic schema for Decision Passport API responses.

Wave 12 §32.3.4 (Engine 4 hardening) extends v1.0 → v1.1 by adding three
fields that close the four hard rules from §32.3.4 ("No Owner =
Not Operational" etc.):

- ``owner``      — who's responsible for the next step
- ``deadline``   — when the action must complete (ISO 8601)
- ``action_mode`` — one of the canonical 5 modes (matches Engine 6)

Plus a runtime ``validate_passport()`` guard that hard-fails on:
- empty ``proof_target``
- empty ``owner``
- ``deadline`` in the past
- ``best_channel`` not in customer's ``allowed_channels`` (when supplied)

Backward compatibility: all 3 new fields have defaults so existing
v1.0 callers (builder.py, tests) keep working without code changes.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field

PriorityBucket = Literal["P0_NOW", "P1_THIS_WEEK", "P2_NURTURE", "P3_LOW_PRIORITY", "BLOCKED"]

# Canonical 5 action modes (matches Engine 6 + Wave 7.7 founder rules + safe_send_gateway).
# Code anywhere in the codebase that wants action-mode discipline should reuse this.
ActionMode = Literal[
    "suggest_only",       # internal hint to founder; no draft, no send
    "draft_only",         # draft generated; founder must edit/approve before manual send
    "approval_required",  # waiting on founder approval; live send still blocked
    "approved_manual",    # founder approved; founder copies + sends manually
    "blocked",            # safety gate refused; reason logged
]

# Canonical owner roles (matches RBAC roles + V14_FOUNDER_DAILY_OPS founder/csm split).
Owner = Literal[
    "founder",       # founder is responsible
    "csm",           # customer success manager (post-Hire)
    "sales_rep",     # sales-rep (post-Hire)
    "customer",      # customer must take the next step (e.g., upload CSV)
    "system_auto",   # automated step needs no human (rare; only for safe_auto agents)
]


class ScoreBoard(BaseModel):
    """Multi-dimensional scores (0–1 scale where applicable)."""

    fit_score: float = Field(ge=0.0, le=1.0)
    intent_score: float = Field(ge=0.0, le=1.0, description="Derived from pain + message strength")
    urgency_score: float = Field(ge=0.0, le=1.0)
    revenue_potential_score: float = Field(ge=0.0, le=1.0)
    engagement_score: float = Field(ge=0.0, le=1.0, description="Proxy: BANT progress + data depth")
    data_quality_score: float = Field(ge=0.0, le=1.0)
    warm_route_score: float = Field(ge=0.0, le=1.0, description="Higher = safer channels available")
    compliance_risk_score: float = Field(ge=0.0, le=1.0, description="Higher = more policy attention")
    deliverability_risk_score: float = Field(ge=0.0, le=1.0, description="Email/channel readiness risk")


class PassportApproval(BaseModel):
    """Explicit approval record attached to a Decision Passport.

    Governed Revenue: a passport carries who approved it and when —
    no source-less, no approval-less passports reach the store.
    """

    approver: str = Field(..., min_length=1)
    approved_at: datetime


class DecisionPassport(BaseModel):
    """جواز القرار — قرار تجاري واحد لكل lead.

    Schema v1.1 (Wave 12 §32.3.4): adds owner / deadline / action_mode.
    Governed Revenue extension: adds explicit source / approval /
    evidence_event_ids / measurable_impact.
    """

    schema_version: str = "1.1"
    lead_id: str
    company: str
    contact_name: str | None = None
    source: str
    locale: str = "ar"
    why_now_ar: str
    why_now_en: str
    icp_tier: str
    priority_bucket: PriorityBucket
    scores: ScoreBoard
    best_channel: str
    recommended_action: str
    recommended_action_ar: str
    blocked_actions: list[str] = Field(default_factory=list)
    proof_target: str
    proof_target_ar: str
    next_step_ar: str
    next_step_en: str
    bant_open_count: int = 0
    qualification_status: str | None = None
    # Wave 12 hardening fields — backward-compatible (defaults preserve v1.0 callers)
    owner: Owner = "founder"
    """Who's responsible for the next step. Hard rule: No Owner = Not Operational."""
    deadline: datetime | None = None
    """When the action must complete (ISO 8601). None = "today by EOD KSA"."""
    action_mode: ActionMode = "approval_required"
    """One of the canonical 5 modes. Hard rule: live send/charge always require approval."""
    # Governed Revenue & AI Ops fields — explicit governance trail.
    approval: PassportApproval | None = None
    """Explicit approver + timestamp. Required before a passport is persisted."""
    evidence_event_ids: list[str] = Field(default_factory=list)
    """Links to Evidence Events ledger ids (B1) — the source-of-truth trail."""
    measurable_impact: str = ""
    """The measurable commercial impact this passport targets (Article 8 framing)."""
    meta: dict[str, Any] = Field(default_factory=dict)


class ValidationFailure(Exception):
    """Raised by ``validate_passport()`` when a hard rule is violated.

    Attributes:
      ``rule``         — the violated hard rule (e.g. "no_proof_target")
      ``field``        — the offending field name
      ``message``      — bilingual human-readable reason (Arabic + English)
    """

    def __init__(self, rule: str, field: str, message: str) -> None:
        self.rule = rule
        self.field = field
        super().__init__(f"[{rule}] field={field}: {message}")


def validate_passport(
    p: DecisionPassport,
    *,
    allowed_channels: list[str] | None = None,
    now: datetime | None = None,
) -> None:
    """Runtime hard-rule guard. Raises ``ValidationFailure`` on violation.

    Hard rules (from plan §32.3.4):
      1. No Decision Passport = No Action  (callers must build one first)
      2. No Proof Target = No Action       (proof_target non-empty)
      3. No Owner = Not Operational         (owner non-empty + valid Literal)
      4. No Safe Channel = Blocked          (best_channel in allowed_channels)

    ``allowed_channels`` should be supplied from the customer's
    Company Brain (``CompanyBrainV6.allowed_channels``). When ``None``,
    the channel check is skipped (back-compat for callers that don't
    yet have a Company Brain).

    ``now`` is injectable for deterministic tests; default = UTC now.
    """
    # Rule 2: proof_target must be non-empty (whitespace-stripped)
    if not p.proof_target or not p.proof_target.strip():
        raise ValidationFailure(
            "no_proof_target",
            "proof_target",
            "بدون proof_target لا يُنفَّذ إجراء — every passport must have a measurable outcome target.",
        )

    # Rule 3: owner must be set (Literal validation already happened in pydantic;
    # but if someone bypassed pydantic by setting owner="" via dict, this catches it)
    if not p.owner or not str(p.owner).strip():
        raise ValidationFailure(
            "no_owner",
            "owner",
            "بدون owner لا يُعد passport جاهزًا للتنفيذ — every passport needs a named responsible party.",
        )

    # Rule 3b: deadline must not be in the past (None is allowed = "today EOD")
    if p.deadline is not None:
        ref = now if now is not None else datetime.now(timezone.utc)
        # Normalize naive deadlines to UTC (assumes UTC if no tz)
        if p.deadline.tzinfo is None:
            deadline_aware = p.deadline.replace(tzinfo=timezone.utc)
        else:
            deadline_aware = p.deadline
        if deadline_aware < ref:
            raise ValidationFailure(
                "deadline_in_past",
                "deadline",
                f"deadline {p.deadline.isoformat()} في الماضي — passport is stale; rebuild before action.",
            )

    # Rule 4: best_channel must be in allowed_channels (when supplied)
    if allowed_channels is not None:
        if p.best_channel not in allowed_channels:
            raise ValidationFailure(
                "channel_blocked",
                "best_channel",
                f"القناة '{p.best_channel}' ليست في القنوات المسموحة لهذا العميل: {allowed_channels}",
            )
