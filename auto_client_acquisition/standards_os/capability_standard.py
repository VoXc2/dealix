"""Capability Diagnostic Standard — re-exports the DCI surface."""

from __future__ import annotations

from auto_client_acquisition.global_grade_os.capability_index import (
    DCI_AXES,
    DCI_MATURITY_LABELS,
    DCIAxis,
    DCIMaturity,
    DCIReading,
    DCIReport,
)

__all__ = [
    "DCI_AXES",
    "DCI_MATURITY_LABELS",
    "DCIAxis",
    "DCIMaturity",
    "DCIReading",
    "DCIReport",
]
