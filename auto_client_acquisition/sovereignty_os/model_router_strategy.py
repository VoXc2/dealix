"""Model Router Strategy — route AI requests to a model class by context.

See ``docs/sovereignty/MODEL_ROUTER_STRATEGY.md``. Pure decision logic;
the actual model invocation lives in ``llm_gateway``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ModelClass(str, Enum):
    CHEAP = "cheap_model"
    BALANCED = "balanced_model"
    PREMIUM = "premium_model"
    LOCAL_PRIVATE = "local_private_model"
    NO_MODEL = "no_model_rule_based"


@dataclass(frozen=True)
class ModelRouterRequest:
    task: str
    risk_level: str            # low | medium | high | critical
    contains_pii: bool
    language: str              # iso code, e.g. "ar", "en"
    required_quality: str      # low | medium | high
    cost_budget: str           # tight | moderate | loose
    latency_requirement: str   # low | medium | high
    sensitivity: str           # public | internal | confidential | restricted


@dataclass(frozen=True)
class ModelRouterDecision:
    model_class: ModelClass
    reasons: tuple[str, ...]
    requires_redaction: bool
    requires_human_review: bool


_HIGH_RISK = {"high", "critical"}


def route_request(request: ModelRouterRequest) -> ModelRouterDecision:
    """Apply the doctrine routing rules to a request.

    The function is intentionally deterministic and explainable; reasons
    accumulate so the decision can be audited.
    """

    reasons: list[str] = []

    # Confidential or restricted data prefers the private path when available.
    if request.sensitivity in {"confidential", "restricted"}:
        reasons.append("sensitivity_requires_private_or_premium")
        model = ModelClass.LOCAL_PRIVATE
    else:
        model = ModelClass.BALANCED

    # High-risk or high-quality demands escalate to premium.
    if request.risk_level in _HIGH_RISK or request.required_quality == "high":
        reasons.append("risk_or_quality_requires_premium")
        # Local-private wins over premium when sensitivity demands residency.
        if model is not ModelClass.LOCAL_PRIVATE:
            model = ModelClass.PREMIUM

    # Tight budgets and low-quality tasks may downgrade to cheap.
    if (
        request.cost_budget == "tight"
        and request.required_quality == "low"
        and request.risk_level not in _HIGH_RISK
        and model is not ModelClass.LOCAL_PRIVATE
    ):
        reasons.append("budget_and_quality_allow_cheap")
        model = ModelClass.CHEAP

    # Pure rule-based path when the task is deterministic and risk-free.
    if request.task in {"validate_email", "dedupe_records", "format_csv"}:
        reasons.append("deterministic_task_no_model_needed")
        model = ModelClass.NO_MODEL

    requires_redaction = request.contains_pii
    if requires_redaction:
        reasons.append("pii_present_requires_redaction")

    requires_human_review = (
        request.risk_level in _HIGH_RISK
        or request.contains_pii
        or request.sensitivity in {"confidential", "restricted"}
    )
    if requires_human_review:
        reasons.append("post_action_requires_human_review")

    return ModelRouterDecision(
        model_class=model,
        reasons=tuple(reasons),
        requires_redaction=requires_redaction,
        requires_human_review=requires_human_review,
    )
