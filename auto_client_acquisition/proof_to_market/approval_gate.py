"""Unified approval requirement flags."""
from __future__ import annotations

from typing import Any


def gate_for_public_use(*, has_written_approval: bool) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "public_snippet_allowed": has_written_approval,
        "case_study_allowed": has_written_approval,
        "logo_use_allowed": has_written_approval,
        "testimonial_allowed": has_written_approval,
        "blocked_until": None if has_written_approval else "written_customer_approval",
    }
