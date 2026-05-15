"""AI control plane vocabulary and sample AI run payload shape."""

from __future__ import annotations

from typing import Any

CONTROL_PLANE_COMPONENTS: tuple[str, ...] = (
    "Agent Registry",
    "LLM Gateway",
    "Prompt Registry",
    "Model Router",
    "Cost Guard",
    "Eval Runner",
    "AI Run Ledger",
    "Policy Engine",
    "Approval Engine",
    "Kill Switch",
)


def example_ai_run_record() -> dict[str, Any]:
    return {
        "ai_run_id": "AIR-001",
        "agent": "RevenueAgent",
        "task": "score_accounts",
        "model_tier": "balanced",
        "prompt_version": "lead_scoring_v1",
        "inputs_redacted": True,
        "output_schema": "AccountScore",
        "governance_status": "approved_with_review",
        "qa_score": 91,
        "risk_level": "medium",
        "cost": 0.42,
    }
