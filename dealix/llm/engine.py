"""
Dealix LLM Engine - Three Gear System v3.0
The brain that selects the right model for the right job.
"""

import os
from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, Field


class Gear(str, Enum):
    """Three gear system for cost-optimized LLM routing."""
    DAILY = "daily"           # Gear 1: DeepSeek - cheap and fast
    POWER = "power"           # Gear 2: Minimax M2.5 - strong coding
    ARCHITECT = "architect"   # Gear 3: Minimax M2.7 - deep reasoning


class GearConfig(BaseModel):
    """Configuration for a single gear."""
    gear: Gear
    model_id: str
    provider: Literal["openrouter"] = "openrouter"
    timeout: int = Field(default=120, ge=30, le=300)
    max_tokens: int = Field(default=4096, ge=256, le=32768)
    cost_per_1m_input: float = 0.0
    cost_per_1m_output: float = 0.0
    use_for: list[str] = []
    risk_level: str = "low"  # low, medium, high


class TaskType(str, Enum):
    """Dealix task classifications for smart gear selection."""
    # Gear 1 tasks (cheap, fast)
    REFACTORING = "refactoring"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    SMALL_FIX = "small_fix"
    ENRICHMENT = "enrichment"
    CLASSIFICATION = "classification"
    FORMATTING = "formatting"
    # Gear 2 tasks (strong, balanced)
    NEW_FEATURE = "new_feature"
    PIPELINE_LOGIC = "pipeline_logic"
    AGENT_CODE = "agent_code"
    BUG_FIX = "bug_fix"
    API_ENDPOINT = "api_endpoint"
    DATA_MODEL = "data_model"
    # Gear 3 tasks (expensive, deep)
    SYSTEM_DESIGN = "system_design"
    POLICY_EVALUATION = "policy_evaluation"
    COMPLIANCE = "compliance"
    HARD_BUG = "hard_bug"
    ARCHITECTURE = "architecture"


# Map tasks to recommended gears
TASK_GEAR_MAP: dict[TaskType, Gear] = {
    TaskType.REFACTORING: Gear.DAILY,
    TaskType.TESTING: Gear.DAILY,
    TaskType.DOCUMENTATION: Gear.DAILY,
    TaskType.SMALL_FIX: Gear.DAILY,
    TaskType.ENRICHMENT: Gear.DAILY,
    TaskType.CLASSIFICATION: Gear.DAILY,
    TaskType.FORMATTING: Gear.DAILY,
    TaskType.NEW_FEATURE: Gear.POWER,
    TaskType.PIPELINE_LOGIC: Gear.POWER,
    TaskType.AGENT_CODE: Gear.POWER,
    TaskType.BUG_FIX: Gear.POWER,
    TaskType.API_ENDPOINT: Gear.POWER,
    TaskType.DATA_MODEL: Gear.POWER,
    TaskType.SYSTEM_DESIGN: Gear.ARCHITECT,
    TaskType.POLICY_EVALUATION: Gear.ARCHITECT,
    TaskType.COMPLIANCE: Gear.ARCHITECT,
    TaskType.HARD_BUG: Gear.ARCHITECT,
    TaskType.ARCHITECTURE: Gear.ARCHITECT,
}


class DealixEngine:
    """
    The brain that selects the right model for the right job.

    Three Gear System:
    - Gear 1 (Daily): DeepSeek - $0.02/$0.10 per 1M tokens
    - Gear 2 (Power): Minimax M2.5 - $0.15/$1.15 per 1M tokens
    - Gear 3 (Architect): Minimax M2.7 - $0.279/$1.20 per 1M tokens

    Cost savings: 80-90% vs using Architect mode for all tasks.
    """

    _GEARS: dict[Gear, GearConfig] = {
        Gear.DAILY: GearConfig(
            gear=Gear.DAILY,
            model_id=os.getenv("GEAR1_MODEL", "deepseek/deepseek-chat"),
            timeout=int(os.getenv("GEAR1_TIMEOUT", "90")),
            max_tokens=int(os.getenv("GEAR1_MAX_TOKENS", "4096")),
            cost_per_1m_input=0.02,
            cost_per_1m_output=0.10,
            use_for=["refactoring", "tests", "docs", "small fixes", "enrichment", "classification", "formatting"],
            risk_level="low",
        ),
        Gear.POWER: GearConfig(
            gear=Gear.POWER,
            model_id=os.getenv("GEAR2_MODEL", "minimax/minimax-m2.5"),
            timeout=int(os.getenv("GEAR2_TIMEOUT", "120")),
            max_tokens=int(os.getenv("GEAR2_MAX_TOKENS", "8192")),
            cost_per_1m_input=0.15,
            cost_per_1m_output=1.15,
            use_for=["new features", "pipeline logic", "agent code", "bug fixes", "API endpoints", "data models"],
            risk_level="medium",
        ),
        Gear.ARCHITECT: GearConfig(
            gear=Gear.ARCHITECT,
            model_id=os.getenv("GEAR3_MODEL", "minimax/minimax-m2.7"),
            timeout=int(os.getenv("GEAR3_TIMEOUT", "180")),
            max_tokens=int(os.getenv("GEAR3_MAX_TOKENS", "16384")),
            cost_per_1m_input=0.279,
            cost_per_1m_output=1.20,
            use_for=["system design", "policy", "compliance", "hard bugs", "architecture decisions"],
            risk_level="high",
        ),
    }

    @classmethod
    def get(cls, gear: Gear | None = None) -> GearConfig:
        """Get config for a specific gear, or the active gear from env."""
        if gear is None:
            active = int(os.getenv("ACTIVE_GEAR", "1"))
            gear_map = {1: Gear.DAILY, 2: Gear.POWER, 3: Gear.ARCHITECT}
            gear = gear_map.get(active, Gear.DAILY)
        return cls._GEARS[gear]

    @classmethod
    def get_for_task(cls, task: TaskType) -> GearConfig:
        """Smart gear selection based on task type."""
        gear = TASK_GEAR_MAP.get(task, Gear.DAILY)
        return cls._GEARS[gear]

    @classmethod
    def list_all(cls) -> dict:
        """List all gears and their model IDs."""
        return {g.value: cfg.model_id for g, cfg in cls._GEARS.items()}

    @classmethod
    def estimate_cost(cls, gear: Gear, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost in USD for a request."""
        cfg = cls._GEARS[gear]
        cost = (input_tokens / 1_000_000 * cfg.cost_per_1m_input +
                output_tokens / 1_000_000 * cfg.cost_per_1m_output)
        return round(cost, 6)


# Singleton instance
engine = DealixEngine()
