"""Delivery Kit — reusable factory for accepted engagements."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN"

class DeliveryStage(StrEnum):
    INTAKE = "intake"
    BASELINE = "baseline"
    SCOPE_LOCK = "scope_lock"
    IMPLEMENT = "implement"
    CUSTOMER_REVIEW = "customer_review"
    ACCEPTANCE = "acceptance"
    OUTCOME = "outcome"
    PROOF = "proof"
    HANDOVER = "handover"
    EXPANSION = "expansion"

class DeliveryKit(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kit_id: str
    cell_id: str
    scope: str = UNKNOWN
    owner: str = "dealix-delivery"
    customer_deps: list[str] = Field(default_factory=list)
    acceptance_criteria: str = UNKNOWN
    baseline: str = UNKNOWN
    target_metric: str = UNKNOWN
    delivery_effort_hours: float = 0.0
    actual_effort_hours: float = 0.0
    exceptions: list[str] = Field(default_factory=list)
    customer_feedback: str = UNKNOWN
    result: str = UNKNOWN
    proof_status: str = UNKNOWN
    stage: DeliveryStage = DeliveryStage.INTAKE
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    reusable_artifact_refs: list[str] = Field(default_factory=list)

    def advance(self, next_stage: DeliveryStage, notes: str = "") -> None:
        self.stage = next_stage
        if notes:
            self.exceptions.append(notes)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")

class DeliveryFactory:
    def __init__(self) -> None:
        self.kits: dict[str, DeliveryKit] = {}

    def create(self, kit: DeliveryKit) -> DeliveryKit:
        self.kits[kit.kit_id] = kit
        return kit

    def get(self, kit_id: str) -> DeliveryKit | None:
        return self.kits.get(kit_id)

__all__ = ["DeliveryKit", "DeliveryStage", "DeliveryFactory", "UNKNOWN"]
