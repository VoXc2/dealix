"""Bottleneck Radar schemas — Pydantic v2."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

BottleneckSeverity = Literal["clear", "watch", "blocking", "critical"]


class FounderBottleneck(BaseModel):
    """Single read-model of what's blocking revenue today.

    Replaces 100-card dashboard with 1 message + 1 single action.
    """

    model_config = ConfigDict(extra="forbid")

    customer_handle: str | None = None  # null = portfolio-wide founder view
    severity: BottleneckSeverity = "clear"

    # 5 counts (per plan §32.4A.2)
    blocking_approvals_count: int = Field(default=0, ge=0)
    pending_payment_confirmations: int = Field(default=0, ge=0)
    pending_proof_packs_to_send: int = Field(default=0, ge=0)
    overdue_followups: int = Field(default=0, ge=0)
    sla_at_risk_tickets: int = Field(default=0, ge=0)

    # Bilingual summary (single sentence each)
    bottleneck_summary_ar: str = ""
    bottleneck_summary_en: str = ""

    # Single most important action — 1 sentence (Article 11: focus)
    today_single_action_ar: str = ""
    today_single_action_en: str = ""

    is_estimate: bool = True
