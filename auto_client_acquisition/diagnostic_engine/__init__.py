"""Diagnostic Engine — bilingual brief composer.

Public API:
    from auto_client_acquisition.diagnostic_engine import (
        DiagnosticRequest, DiagnosticResult,
        generate_diagnostic, list_supported_sectors,
    )
"""
from auto_client_acquisition.diagnostic_engine.engine import (
    generate_diagnostic,
    list_supported_sectors,
)
from auto_client_acquisition.diagnostic_engine.opportunity_report import (
    AIOpportunity,
    AIOpportunityReport,
    generate_opportunity_report,
    list_opportunity_sectors,
)
from auto_client_acquisition.diagnostic_engine.schemas import (
    DiagnosticRequest,
    DiagnosticResult,
)

__all__ = [
    "AIOpportunity",
    "AIOpportunityReport",
    "DiagnosticRequest",
    "DiagnosticResult",
    "generate_diagnostic",
    "generate_opportunity_report",
    "list_opportunity_sectors",
    "list_supported_sectors",
]
