"""Message experiment — typed schema for tracking A/B variants.

This is a TEMPLATE for the founder to fill in manually. The runtime
does NOT execute experiments (no automated traffic split, no live
sends). The typed record exists so the founder's notes have a stable
shape that can later be aggregated into the weekly_growth_scorecard.
"""
from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.self_growth_os.safe_publishing_gate import check_text


class ExperimentStatus(StrEnum):
    DRAFT = "draft"
    APPROVED = "approved"
    RUNNING_MANUALLY = "running_manually"
    COMPLETE = "complete"
    BLOCKED = "blocked"


class MessageExperiment(BaseModel):
    """One experiment template — never executed automatically."""

    model_config = ConfigDict(use_enum_values=True, extra="forbid")

    id: str = Field(default_factory=lambda: f"exp_{uuid4().hex[:12]}")
    name: str
    hypothesis_ar: str
    hypothesis_en: str
    variant_a_ar: str
    variant_a_en: str
    variant_b_ar: str
    variant_b_en: str
    success_metric: str  # e.g. "reply_rate" | "diagnostic_request_count"
    target_audience: str
    expected_sample_size: int = 0  # 0 = unknown / manual
    channel_hint: str = "founder_warm_intro"
    forbidden_channels: list[str] = Field(default_factory=lambda: [
        "cold_whatsapp",
        "linkedin_automation",
        "purchased_lists",
    ])
    status: ExperimentStatus = ExperimentStatus.DRAFT
    safe_publishing_check: dict[str, Any] = Field(default_factory=dict)
    notes: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


def draft_experiment(
    *,
    name: str,
    hypothesis_ar: str,
    hypothesis_en: str,
    variant_a_ar: str,
    variant_a_en: str,
    variant_b_ar: str,
    variant_b_en: str,
    success_metric: str,
    target_audience: str,
    expected_sample_size: int = 0,
    channel_hint: str = "founder_warm_intro",
) -> MessageExperiment:
    """Build a new experiment, running both variants through the
    safe-publishing gate. If any variant fails the gate, the
    experiment status is BLOCKED with notes.
    """
    a_check = check_text(variant_a_ar)
    b_check = check_text(variant_b_ar)
    a_check_en = check_text(variant_a_en)
    b_check_en = check_text(variant_b_en)
    all_safe = all(c.decision == "allowed_draft" for c in (a_check, b_check, a_check_en, b_check_en))

    return MessageExperiment(
        name=name,
        hypothesis_ar=hypothesis_ar,
        hypothesis_en=hypothesis_en,
        variant_a_ar=variant_a_ar,
        variant_a_en=variant_a_en,
        variant_b_ar=variant_b_ar,
        variant_b_en=variant_b_en,
        success_metric=success_metric,
        target_audience=target_audience,
        expected_sample_size=expected_sample_size,
        channel_hint=channel_hint,
        status=(
            ExperimentStatus.DRAFT if all_safe else ExperimentStatus.BLOCKED
        ),
        safe_publishing_check={
            "variant_a_ar": a_check.decision,
            "variant_b_ar": b_check.decision,
            "variant_a_en": a_check_en.decision,
            "variant_b_en": b_check_en.decision,
            "all_safe": all_safe,
        },
        notes=(
            "All 4 variants passed safe_publishing_gate." if all_safe
            else "One or more variants contain forbidden vocabulary — rephrase before running."
        ),
    )
