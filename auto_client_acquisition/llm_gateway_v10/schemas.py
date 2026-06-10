"""Pydantic v2 schemas for the llm_gateway_v10 module.

Inspired by LiteLLM's router contract — but pure native: ZERO API
calls, ZERO external HTTP. The gateway is a deterministic routing
+ budgeting layer in front of model usage; live calls (if any)
happen elsewhere.
"""
from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ModelTier(StrEnum):
    """Four routing tiers — purpose-bound, vendor-neutral."""

    cheap_for_classification = "cheap_for_classification"
    balanced_for_drafts = "balanced_for_drafts"
    strong_for_strategy = "strong_for_strategy"
    local_no_model = "local_no_model"


class RoutingPolicy(BaseModel):
    """Inputs that drive a routing decision."""

    model_config = ConfigDict(extra="forbid")

    task_purpose: str = Field(min_length=1)
    language: Literal["ar", "en", "bilingual"]
    customer_handle: str = ""
    max_tokens: int = Field(default=4000, ge=1)
    max_iterations: int = Field(default=3, ge=1)


class BudgetPolicy(BaseModel):
    """Spending envelope evaluated by ``enforce_budget``."""

    model_config = ConfigDict(extra="forbid")

    per_run_budget_usd: float = 0.50
    per_customer_budget_usd: float = 5.00
    per_agent_budget_usd: float = 0.10
    monthly_founder_budget_usd: float = 50.0


class CostEstimate(BaseModel):
    """Pre-call estimate (token + USD) for one routed step."""

    model_config = ConfigDict(extra="forbid")

    tier: ModelTier
    estimated_input_tokens: int = Field(ge=0)
    estimated_output_tokens: int = Field(ge=0)
    estimated_usd: float = Field(ge=0.0)
    cache_key: str = ""
    stop_when_good_enough: bool = True
    human_review_when_budget_exceeded: bool = True


class RoutingDecision(BaseModel):
    """Final routing output — bilingual reason for founder review."""

    model_config = ConfigDict(extra="forbid")

    tier: ModelTier
    cost_estimate: CostEstimate
    action: Literal["proceed", "warn_founder", "pause_for_approval", "hard_stop"]
    reason_ar: str
    reason_en: str
