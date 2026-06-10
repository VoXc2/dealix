"""CompanyBrain v6 — per-customer brain.

Composes a structured snapshot for a SPECIFIC CUSTOMER from a
``BuildRequest`` into a ``CompanyBrainV6``. Used by the diagnostic
workflow, founder dashboard, and offer builder.

Pure local composition. No LLM call. No external HTTP.

Public API:
    from auto_client_acquisition.company_brain_v6 import (
        CompanyBrainV6,
        BuildRequest,
        build_company_brain_v6,
        recommend_service,
        next_best_action,
    )
"""
from auto_client_acquisition.company_brain_v6.builder import build_company_brain_v6
from auto_client_acquisition.company_brain_v6.next_best_action import next_best_action
from auto_client_acquisition.company_brain_v6.schemas import BuildRequest, CompanyBrainV6
from auto_client_acquisition.company_brain_v6.service_matcher import recommend_service

__all__ = [
    "BuildRequest",
    "CompanyBrainV6",
    "build_company_brain_v6",
    "next_best_action",
    "recommend_service",
]
