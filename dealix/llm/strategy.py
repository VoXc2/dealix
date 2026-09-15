"""Dealix LLM Strategy compatibility surface.

Canonical unattended model/provider selection belongs to the Dealix model/cost/data
broker. This legacy strategy may organize task classes, but it must not mint provider
entitlement or silently default to DeepSeek/paid capacity.
"""

import os
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field

BROKER_REQUIRED_MODEL = "__dealix_canonical_broker_required__"


def _explicit_non_deepseek_model(env_name: str) -> str:
    value = (os.getenv(env_name) or "").strip()
    if not value or "deepseek" in value.lower():
        return BROKER_REQUIRED_MODEL
    return value


class ModelTier(str, Enum):
    PRIMARY = "primary"
    ARCHITECT = "architect"
    LIGHT = "light"
    FALLBACK = "fallback"


class TaskType(str, Enum):
    CODE_GENERATION = "code_generation"
    AGENT_REASONING = "agent_reasoning"
    POLICY_EVALUATION = "policy_evaluation"
    EVIDENCE_SYNTHESIS = "evidence_synthesis"
    DATA_ENRICHMENT = "data_enrichment"
    CONTENT_CREATION = "content_creation"
    COMPLIANCE_ANALYSIS = "compliance_analysis"
    CLASSIFICATION = "classification"


class ModelConfig(BaseModel):
    provider: Literal["openrouter"] = "openrouter"
    model_id: str
    timeout: int = Field(default=120, ge=30, le=300)
    max_retries: int = Field(default=2, ge=0, le=5)
    reasoning_preserved: bool = True


class LLMStrategyRouter:
    _TASK_MAP = {
        TaskType.CODE_GENERATION: [ModelTier.PRIMARY, ModelTier.ARCHITECT, ModelTier.FALLBACK],
        TaskType.AGENT_REASONING: [ModelTier.PRIMARY, ModelTier.ARCHITECT, ModelTier.FALLBACK],
        TaskType.POLICY_EVALUATION: [ModelTier.ARCHITECT, ModelTier.PRIMARY, ModelTier.FALLBACK],
        TaskType.EVIDENCE_SYNTHESIS: [ModelTier.ARCHITECT, ModelTier.PRIMARY, ModelTier.FALLBACK],
        TaskType.DATA_ENRICHMENT: [ModelTier.LIGHT, ModelTier.PRIMARY, ModelTier.FALLBACK],
        TaskType.CLASSIFICATION: [ModelTier.LIGHT, ModelTier.PRIMARY, ModelTier.FALLBACK],
        TaskType.CONTENT_CREATION: [ModelTier.PRIMARY, ModelTier.ARCHITECT, ModelTier.FALLBACK],
        TaskType.COMPLIANCE_ANALYSIS: [ModelTier.ARCHITECT, ModelTier.PRIMARY, ModelTier.FALLBACK],
    }

    _MODEL_IDS = {
        ModelTier.PRIMARY: _explicit_non_deepseek_model("GEAR2_MODEL"),
        ModelTier.ARCHITECT: _explicit_non_deepseek_model("GEAR3_MODEL"),
        ModelTier.LIGHT: _explicit_non_deepseek_model("GEAR1_MODEL"),
        ModelTier.FALLBACK: _explicit_non_deepseek_model("GEAR1_MODEL"),
    }

    _TIMEOUTS = {
        ModelTier.PRIMARY: int(os.getenv("GEAR2_TIMEOUT", "120")),
        ModelTier.ARCHITECT: int(os.getenv("GEAR3_TIMEOUT", "180")),
        ModelTier.LIGHT: int(os.getenv("GEAR1_TIMEOUT", "90")),
        ModelTier.FALLBACK: int(os.getenv("GEAR1_TIMEOUT", "90")),
    }

    @staticmethod
    def _require_explicit_model(model_id: str) -> str:
        if model_id == BROKER_REQUIRED_MODEL or "deepseek" in model_id.lower():
            raise RuntimeError(
                "Legacy strategy model selection is fail-closed. Use the canonical Dealix "
                "model/cost/data broker or an explicitly authorized non-DeepSeek model."
            )
        return model_id

    def resolve(self, task: TaskType, prefer_cheap: bool = False) -> list[ModelConfig]:
        tiers = self._TASK_MAP.get(task, [ModelTier.PRIMARY, ModelTier.FALLBACK])
        if prefer_cheap:
            order = {
                ModelTier.LIGHT: 0,
                ModelTier.FALLBACK: 1,
                ModelTier.PRIMARY: 2,
                ModelTier.ARCHITECT: 3,
            }
            tiers = sorted(tiers, key=lambda tier: order[tier])
        return [
            ModelConfig(
                model_id=self._require_explicit_model(self._MODEL_IDS[tier]),
                timeout=self._TIMEOUTS[tier],
                reasoning_preserved=(tier != ModelTier.FALLBACK),
            )
            for tier in tiers
        ]


router = LLMStrategyRouter()
