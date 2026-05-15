"""System 33 — Human-AI Operating Model.

Delegation, escalation, explainability and a human oversight surface.
"""

from auto_client_acquisition.human_ai_os.core import (
    HumanAIError,
    HumanAIModel,
    get_human_ai_model,
    reset_human_ai_model,
)
from auto_client_acquisition.human_ai_os.schemas import (
    Delegation,
    Escalation,
    Explanation,
    OversightItem,
)

__all__ = [
    "Delegation",
    "Escalation",
    "Explanation",
    "HumanAIError",
    "HumanAIModel",
    "OversightItem",
    "get_human_ai_model",
    "reset_human_ai_model",
]
