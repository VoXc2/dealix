"""Dealix LLM Strategy - Fallback chains per task type."""

import os
from enum import Enum, StrEnum
from typing import Literal

from pydantic import BaseModel, Field


class ModelTier(StrEnum):
    PRIMARY = "primary"
    ARCHITECT = "architect"
    LIGHT = "light"
    FALLBACK = "fallback"


class TaskType(StrEnum):
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
        ModelTier.PRIMARY: os.getenv("GEAR2_MODEL", "minimax/minimax-m2.5"),
        ModelTier.ARCHITECT: os.getenv("GEAR3_MODEL", "minimax/minimax-m2.7"),
        ModelTier.LIGHT: os.getenv("GEAR1_MODEL", "deepseek/deepseek-chat"),
        ModelTier.FALLBACK: os.getenv("GEAR1_MODEL", "deepseek/deepseek-chat"),
    }

    _TIMEOUTS = {
        ModelTier.PRIMARY: int(os.getenv("GEAR2_TIMEOUT", "120")),
        ModelTier.ARCHITECT: int(os.getenv("GEAR3_TIMEOUT", "180")),
        ModelTier.LIGHT: int(os.getenv("GEAR1_TIMEOUT", "90")),
        ModelTier.FALLBACK: int(os.getenv("GEAR1_TIMEOUT", "90")),
    }

    def resolve(self, task: TaskType, prefer_cheap: bool = False):
        tiers = self._TASK_MAP.get(task, [ModelTier.PRIMARY, ModelTier.FALLBACK])
        if prefer_cheap:
            order = {ModelTier.LIGHT: 0, ModelTier.FALLBACK: 1, ModelTier.PRIMARY: 2, ModelTier.ARCHITECT: 3}
            tiers = sorted(tiers, key=lambda t: order[t])
        return [
            ModelConfig(
                model_id=self._MODEL_IDS[tier],
                timeout=self._TIMEOUTS[tier],
                reasoning_preserved=(tier != ModelTier.FALLBACK),
            )
            for tier in tiers
        ]


router = LLMStrategyRouter()
