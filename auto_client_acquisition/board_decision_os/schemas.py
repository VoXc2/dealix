"""Pydantic schemas for Board Decision OS — read models + request bodies."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

DecisionBand = Literal["top", "strong", "mid", "low"]
StrategicBetType = Literal[
    "revenue",
    "product",
    "trust",
    "distribution",
    "enterprise",
    "venture",
]


class OfferScorecardInput(BaseModel):
    """Each field is 0–100 (already normalized score for that dimension)."""

    win_rate: float = Field(ge=0, le=100)
    gross_margin: float = Field(ge=0, le=100)
    proof_strength: float = Field(ge=0, le=100)
    retainer_conversion: float = Field(ge=0, le=100)
    repeatability: float = Field(ge=0, le=100)
    governance_safety: float = Field(ge=0, le=100)
    productization_signal: float = Field(ge=0, le=100, default=50.0)


class ClientScorecardInput(BaseModel):
    clear_pain: float = Field(ge=0, le=100)
    executive_sponsor: float = Field(ge=0, le=100)
    data_readiness: float = Field(ge=0, le=100)
    governance_alignment: float = Field(ge=0, le=100)
    adoption_score: float = Field(ge=0, le=100)
    proof_score: float = Field(ge=0, le=100)
    expansion_potential: float = Field(ge=0, le=100, default=50.0)


class ProductizationScorecardInput(BaseModel):
    repeated_pain: float = Field(ge=0, le=100)
    delivery_hours_saved: float = Field(ge=0, le=100)
    revenue_linkage: float = Field(ge=0, le=100)
    risk_reduction: float = Field(ge=0, le=100)
    client_pull: float = Field(ge=0, le=100)
    build_simplicity: float = Field(ge=0, le=100, default=50.0)


class ScorecardResult(BaseModel):
    total: float = Field(ge=0, le=100)
    band: DecisionBand
    board_read_ar: str
    board_read_en: str


class CEOSignals(BaseModel):
    """Compact signal payload for deterministic Top-N decisions (v1)."""

    proof_score: float = Field(ge=0, le=100, default=50.0)
    adoption_score: float = Field(ge=0, le=100, default=50.0)
    monthly_workflow_exists: bool = False
    approval_friction_clients: int = Field(ge=0, default=0)
    sprint_repeat_sales: int = Field(ge=0, default=0)
    sprint_avg_proof: float = Field(ge=0, le=100, default=0.0)
    cold_whatsapp_automation_request: bool = False
    repeated_sector_pattern: bool = False
    bad_revenue_unsafe_channel: bool = False


class CEOTopDecision(BaseModel):
    priority: int = Field(ge=1, le=10)
    decision: str
    target: str
    reason_ar: str
    reason_en: str


class StrategicBet(BaseModel):
    bet_type: StrategicBetType
    title: str = Field(min_length=3, max_length=200)
    rationale: str = Field(min_length=10, max_length=2000)


class StrategicBetsInput(BaseModel):
    month_label: str = Field(min_length=2, max_length=32)
    bets: list[StrategicBet] = Field(default_factory=list)


class AgentGateInput(BaseModel):
    purpose: str = Field(min_length=5)
    owner: str = Field(min_length=2)
    allowed_tools: list[str] = Field(min_length=1)
    forbidden_actions: list[str] = Field(min_length=1)
    autonomy_level: int = Field(ge=0, le=5)
    audit_required: bool = False
    decommission_rule: str = Field(min_length=5)


class AgentGateResult(BaseModel):
    approved: bool
    reasons_ar: list[str]
    reasons_en: list[str]


class BoardMemoMetrics(BaseModel):
    """Optional v1 metrics for memo body — all strings safe for Markdown."""

    executive_summary_ar: str = ""
    executive_summary_en: str = ""
    revenue_quality_ar: str = ""
    revenue_quality_en: str = ""
    proof_value_ar: str = ""
    proof_value_en: str = ""
    retainer_ar: str = ""
    retainer_en: str = ""
    governance_ar: str = ""
    governance_en: str = ""
    productization_ar: str = ""
    productization_en: str = ""
    client_health_ar: str = ""
    client_health_en: str = ""
    market_intel_ar: str = ""
    market_intel_en: str = ""
    bu_maturity_ar: str = ""
    bu_maturity_en: str = ""
    kill_list_ar: str = ""
    kill_list_en: str = ""
    capital_allocation_ar: str = ""
    capital_allocation_en: str = ""
    next_bets_ar: str = ""
    next_bets_en: str = ""
