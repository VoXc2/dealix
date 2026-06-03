"""degraded_section — emit a structured degradation marker.

Used by Wave 4 modules whenever a sub-section can't be composed.
The shape matches `DegradedSection` Pydantic schema.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.integration_upgrade.schemas import (
    DegradedSection,
    DegradeSeverity,
)


def degraded_section(
    *,
    section: str,
    reason_ar: str,
    reason_en: str,
    next_fix_ar: str = "",
    next_fix_en: str = "",
    severity: DegradeSeverity = "medium",
) -> dict[str, Any]:
    """Return a JSON-ready degraded-section dict (never raises)."""
    return DegradedSection(
        section=section,
        reason_ar=reason_ar,
        reason_en=reason_en,
        next_fix_ar=next_fix_ar,
        next_fix_en=next_fix_en,
        severity=severity,
    ).model_dump(mode="json")
