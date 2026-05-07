"""Schemas for Executive Command Center (Phase 5)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

Cadence = Literal["snapshot", "daily", "weekly"]


class CommandCenterView(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_handle: str
    cadence: Cadence = "snapshot"
    executive_summary: dict[str, Any] = Field(default_factory=dict)
    full_ops_score: dict[str, Any] = Field(default_factory=dict)
    today_3_decisions: list[dict[str, Any]] = Field(default_factory=list)
    revenue_radar: dict[str, Any] = Field(default_factory=dict)
    sales_pipeline: dict[str, Any] = Field(default_factory=dict)
    growth_radar: dict[str, Any] = Field(default_factory=dict)
    partnership_radar: dict[str, Any] = Field(default_factory=dict)
    support_inbox: dict[str, Any] = Field(default_factory=dict)
    delivery_operations: dict[str, Any] = Field(default_factory=dict)
    finance_state: dict[str, Any] = Field(default_factory=dict)
    proof_ledger: dict[str, Any] = Field(default_factory=dict)
    risks_compliance: dict[str, Any] = Field(default_factory=dict)
    approval_center: dict[str, Any] = Field(default_factory=dict)
    whatsapp_decision_preview: dict[str, Any] = Field(default_factory=dict)
    degraded_sections: list[dict[str, Any]] = Field(default_factory=list)
    safety_summary: str = "no_fake_revenue_no_fake_proof_customer_safe_labels"
    built_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
