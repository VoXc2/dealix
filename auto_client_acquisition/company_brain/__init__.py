"""CompanyBrain v5 — single source of truth that composes existing signals
into a structured company snapshot.

Pure local composition. No LLM call. No external HTTP.

Public API:
    from auto_client_acquisition.company_brain import (
        CompanyBrain, build_company_brain,
    )
"""
from auto_client_acquisition.company_brain.brain import (
    CompanyBrain,
    build_company_brain,
)

__all__ = [
    "CompanyBrain",
    "build_company_brain",
]
