"""Canonical Data OS — Source Passport, Import Preview, Data Quality Score.

Composes existing repo facilities (customer_data_plane, consent_table,
enrichment_provider) into a single canonical entry point.
"""
from auto_client_acquisition.data_os.source_passport import (
    SourcePassport,
    ValidationResult,
    requires_approval,
    validate,
)
from auto_client_acquisition.data_os.import_preview import ImportPreview, preview
from auto_client_acquisition.data_os.data_quality_score import DQScore, compute_dq

__all__ = [
    "DQScore",
    "ImportPreview",
    "SourcePassport",
    "ValidationResult",
    "compute_dq",
    "preview",
    "requires_approval",
    "validate",
]
