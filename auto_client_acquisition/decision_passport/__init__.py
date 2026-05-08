"""
Decision Passport — يحوّل الـ lead من «اسم» إلى «قرار تجاري» موثّق.

Rule: No Decision Passport = No Action (enforced by product process; API returns passport with every pipeline run).
"""

from __future__ import annotations

from auto_client_acquisition.decision_passport.builder import build_from_pipeline_result
from auto_client_acquisition.decision_passport.schema import DecisionPassport

__all__ = ["SCHEMA_VERSION", "DecisionPassport", "build_from_pipeline_result"]

SCHEMA_VERSION = "1.0"
