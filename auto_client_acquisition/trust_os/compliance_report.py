"""Compliance report section contract (enterprise procurement)."""

from __future__ import annotations

from collections.abc import Mapping

COMPLIANCE_REPORT_SECTIONS: tuple[str, ...] = (
    "data_residency_summary",
    "access_control_summary",
    "subprocessors",
    "model_providers",
    "logging_and_pii_policy",
    "incident_response",
    "deletion_process",
    "customer_responsibilities",
)


def compliance_report_sections_complete(content: Mapping[str, str]) -> tuple[bool, tuple[str, ...]]:
    missing = [k for k in COMPLIANCE_REPORT_SECTIONS if not (content.get(k) or "").strip()]
    return not missing, tuple(missing)


__all__ = ["COMPLIANCE_REPORT_SECTIONS", "compliance_report_sections_complete"]
