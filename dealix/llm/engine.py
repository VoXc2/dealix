"""Legacy Dealix three-gear compatibility surface.

Omega V3 owns model/provider/cost/data authority in the canonical broker and
Session Factory.  This module intentionally preserves historical task/gear
enums for callers that still import them, but it no longer mints model IDs or
provider authority.  Model-requiring callers must migrate to the governed
Company Operator -> Session Factory -> canonical broker execution path.
"""

from enum import Enum

from pydantic import BaseModel, Field


class LegacyModelAuthorityHold(RuntimeError):
    """Raised when legacy code attempts to select a model/provider directly."""


class Gear(str, Enum):
    """Historical compatibility gears; not model authority."""

    DAILY = "daily"
    POWER = "power"
    ARCHITECT = "architect"


class GearConfig(BaseModel):
    """Compatibility schema only; live configs come from the canonical broker."""

    gear: Gear
    model_id: str
    provider: str = "canonical_broker_required"
    timeout: int = Field(default=120, ge=30, le=300)
    max_tokens: int = Field(default=4096, ge=256, le=32768)
    cost_per_1m_input: float = 0.0
    cost_per_1m_output: float = 0.0
    use_for: list[str] = []
    risk_level: str = "unknown"


class TaskType(str, Enum):
    REFACTORING = "refactoring"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    SMALL_FIX = "small_fix"
    ENRICHMENT = "enrichment"
    CLASSIFICATION = "classification"
    FORMATTING = "formatting"
    NEW_FEATURE = "new_feature"
    PIPELINE_LOGIC = "pipeline_logic"
    AGENT_CODE = "agent_code"
    BUG_FIX = "bug_fix"
    API_ENDPOINT = "api_endpoint"
    DATA_MODEL = "data_model"
    SYSTEM_DESIGN = "system_design"
    POLICY_EVALUATION = "policy_evaluation"
    COMPLIANCE = "compliance"
    HARD_BUG = "hard_bug"
    ARCHITECTURE = "architecture"


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


_HOLD_MODEL = "HOLD_CANONICAL_BROKER_REQUIRED"


class DealixEngine:
    """Compatibility facade that fails closed instead of selecting a model."""

    @classmethod
    def _hold(cls, *, context: str) -> None:
        raise LegacyModelAuthorityHold(
            f"legacy_model_authority_disabled:{context}; "
            "use Company Operator -> Session Factory -> canonical broker"
        )

    @classmethod
    def get(cls, gear: Gear | None = None) -> GearConfig:
        cls._hold(context=f"gear={getattr(gear, 'value', gear) or 'active'}")

    @classmethod
    def get_for_task(cls, task: TaskType) -> GearConfig:
        cls._hold(context=f"task={task.value}")

    @classmethod
    def list_all(cls) -> dict[str, str]:
        return {gear.value: _HOLD_MODEL for gear in Gear}

    @classmethod
    def estimate_cost(cls, gear: Gear, input_tokens: int, output_tokens: int) -> float:
        _ = input_tokens, output_tokens
        cls._hold(context=f"cost_estimate_gear={gear.value}")


engine = DealixEngine()

__all__ = [
    "LegacyModelAuthorityHold",
    "Gear",
    "GearConfig",
    "TaskType",
    "TASK_GEAR_MAP",
    "DealixEngine",
    "engine",
]
