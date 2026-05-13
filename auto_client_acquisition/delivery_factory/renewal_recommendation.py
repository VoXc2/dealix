"""Renewal Recommendation — Stage 8 (Expand) next-step proposer.

توصية التوسّع في المرحلة الثامنة.

Reads the QA report + value-metric utilization signals and proposes the
single best next offer (Retainer / additional Sprint / Enterprise) — never
none. The Delivery Standard requires Stage 8 to open a conversation; a
documented "no" still counts.
"""
from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.delivery_factory.client_intake import StartingOffer


class NextOfferKind(StrEnum):
    RETAINER = "retainer"
    ADDITIONAL_SPRINT = "additional_sprint"
    ENTERPRISE = "enterprise"
    NO_NOW = "no_now"  # documented "no" with reason


class Recommendation(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    rec_id: str = Field(default_factory=lambda: f"rec_{uuid4().hex[:12]}")
    project_id: str
    next_offer: NextOfferKind
    name_ar: str
    name_en: str
    rationale_ar: str
    rationale_en: str
    estimated_price_sar: int | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def recommend(
    project_id: str,
    completed_offer: StartingOffer,
    quality_score: int,
    ships: bool,
    customer_signaled_volume: bool = False,
) -> Recommendation:
    """Pick the next best offer using simple, explainable heuristics."""
    if not ships:
        return Recommendation(
            project_id=project_id,
            next_offer=NextOfferKind.NO_NOW,
            name_ar="معالجة الجودة قبل أي توسّع",
            name_en="Resolve quality before any expansion",
            rationale_ar="درجة الجودة لم تتجاوز الحد الأدنى أو إحدى البوّابات فشلت.",
            rationale_en="Quality score below floor or one of the QA gates failed.",
            confidence=0.95,
        )

    if quality_score >= 90 and customer_signaled_volume:
        return Recommendation(
            project_id=project_id,
            next_offer=NextOfferKind.ENTERPRISE,
            name_ar="Enterprise AI OS Proposal",
            name_en="Enterprise AI OS Proposal",
            rationale_ar="جودة عالية + إشارة حجم — مرشّح لعرض Enterprise.",
            rationale_en="High quality + volume signal — qualified for Enterprise pitch.",
            estimated_price_sar=85_000,
            confidence=0.75,
        )

    if completed_offer == StartingOffer.REVENUE_INTELLIGENCE:
        return Recommendation(
            project_id=project_id,
            next_offer=NextOfferKind.RETAINER,
            name_ar="Monthly RevOps OS",
            name_en="Monthly RevOps OS",
            rationale_ar="بعد Sprint إيراد ناجح، Retainer شهري يحافظ على المخرجات.",
            rationale_en="Retainer sustains scoring, hygiene, and weekly outputs after a successful sprint.",
            estimated_price_sar=15_000,
            confidence=0.8,
        )

    if completed_offer == StartingOffer.AI_QUICK_WIN:
        return Recommendation(
            project_id=project_id,
            next_offer=NextOfferKind.ADDITIONAL_SPRINT,
            name_ar="Workflow Automation Sprint",
            name_en="Workflow Automation Sprint",
            rationale_ar="بعد Quick Win، الأتمتة الأكبر تحقّق ROI أوسع.",
            rationale_en="After a Quick Win, a broader Workflow Automation Sprint compounds the ROI.",
            estimated_price_sar=15_000,
            confidence=0.78,
        )

    return Recommendation(
        project_id=project_id,
        next_offer=NextOfferKind.RETAINER,
        name_ar="Monthly AI Ops Retainer",
        name_en="Monthly AI Ops Retainer",
        rationale_ar="بعد Company Brain، Retainer يحافظ على الحداثة وجودة الإجابات.",
        rationale_en="Retainer sustains freshness and answer quality after Company Brain.",
        estimated_price_sar=15_000,
        confidence=0.72,
    )
