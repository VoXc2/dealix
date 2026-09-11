"""Proof → Asset — reusable asset from successful delivery."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN"

class AssetType(StrEnum):
    PLAYBOOK = "playbook"
    WORKFLOW = "workflow"
    CONNECTOR = "connector"
    AGENT_POLICY = "agent_policy"
    EVALUATION = "evaluation"
    CHECKLIST = "checklist"
    TEMPLATE = "template"
    DATA_MODEL = "data_model"
    PROMPT = "prompt"
    DIAGNOSTIC = "diagnostic"
    CALCULATOR = "calculator"
    API = "api"
    UI_COMPONENT = "ui_component"
    INTEGRATION = "integration"
    DELIVERY_KIT = "delivery_kit"
    CONTENT_SOURCE = "content_source"
    BENCHMARK = "benchmark"
    SECTOR_KNOWLEDGE = "sector_knowledge"
    AUTOMATION = "automation"
    TRAINING = "training"
    SAAS_MODULE = "saas_module"

class ProofAsset(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    asset_id: str
    source_delivery_id: str
    asset_type: AssetType
    title: str
    problem: str = UNKNOWN
    baseline: str = UNKNOWN
    intervention: str = UNKNOWN
    result: str = UNKNOWN
    evidence_ref: str = UNKNOWN
    reuse_count: int = 0
    reuse_value_sar: float = 0.0
    maintenance_cost_sar: float = 0.0
    privacy_class: str = "private_operational_proof"
    productization_candidate: bool = False
    distribution_candidate: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    def reuse(self, value_sar: float) -> "ProofAsset":
        return self.model_copy(update={"reuse_count": self.reuse_count + 1, "reuse_value_sar": self.reuse_value_sar + value_sar})

class ProofAssetFactory:
    def __init__(self) -> None:
        self.assets: dict[str, ProofAsset] = {}

    def create_from_delivery(self, delivery_id: str, asset_type: AssetType, title: str, evidence_ref: str) -> ProofAsset:
        asset_id = f"asset_{delivery_id}_{asset_type.value}"
        asset = ProofAsset(asset_id=asset_id, source_delivery_id=delivery_id, asset_type=asset_type, title=title, evidence_ref=evidence_ref)
        self.assets[asset_id] = asset
        return asset

    def to_dict(self) -> dict[str, Any]:
        return {"assets": [a.model_dump(mode="json") for a in self.assets.values()]}

__all__ = ["ProofAsset", "AssetType", "ProofAssetFactory", "UNKNOWN"]
