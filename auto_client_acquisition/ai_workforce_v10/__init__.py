"""AI Workforce v10 — extends ai_workforce/ with Reviewer + Planner.

Pure local composition: NO LLM, NO external HTTP. Inspired by
AutoGen's reviewer + planner patterns. Memory NEVER crosses customer
boundaries.
"""
from auto_client_acquisition.ai_workforce_v10.extended_orchestrator import (
    run_workforce_v10,
)
from auto_client_acquisition.ai_workforce_v10.memory_store import (
    list_memory,
    recall_memory,
    record_memory,
    reset_memory,
)
from auto_client_acquisition.ai_workforce_v10.planner_agent import run_planner
from auto_client_acquisition.ai_workforce_v10.reviewer_agent import run_reviewer
from auto_client_acquisition.ai_workforce_v10.schemas import (
    PlannerOutput,
    ReviewerOutput,
    ReviewerVerdict,
    WorkforceMemoryEntry,
)

__all__ = [
    "PlannerOutput",
    "ReviewerOutput",
    "ReviewerVerdict",
    "WorkforceMemoryEntry",
    "list_memory",
    "recall_memory",
    "record_memory",
    "reset_memory",
    "run_planner",
    "run_reviewer",
    "run_workforce_v10",
]
