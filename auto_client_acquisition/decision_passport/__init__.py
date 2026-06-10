"""
Decision Passport — يحوّل الـ lead من «اسم» إلى «قرار تجاري» موثّق.

Rule: No Decision Passport = No Action (enforced by product process; API returns passport with every pipeline run).
"""

from __future__ import annotations

from auto_client_acquisition.decision_passport.builder import build_from_pipeline_result
from auto_client_acquisition.decision_passport.schema import (
    ActionMode,
    DecisionPassport,
    Owner,
    PriorityBucket,
    ScoreBoard,
    ValidationFailure,
    validate_passport,
)

__all__ = [
    "SCHEMA_VERSION",
    "ActionMode",
    "DecisionPassport",
    "Owner",
    "PriorityBucket",
    "ScoreBoard",
    "ValidationFailure",
    "build_from_pipeline_result",
    "validate_passport",
]

# Wave 12 §32.3.4 — bumped from 1.0 → 1.1 (added owner / deadline / action_mode).
SCHEMA_VERSION = "1.1"
