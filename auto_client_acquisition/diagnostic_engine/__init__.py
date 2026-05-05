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
from auto_client_acquisition.diagnostic_engine.schemas import (
    DiagnosticRequest,
    DiagnosticResult,
)

__all__ = [
    "DiagnosticRequest",
    "DiagnosticResult",
    "generate_diagnostic",
    "list_supported_sectors",
]
