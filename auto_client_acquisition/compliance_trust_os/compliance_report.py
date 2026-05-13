"""Compliance Report — 12-section monthly artifact per engagement."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ComplianceReportSection(str, Enum):
    DATA_SOURCES_USED = "data_sources_used"
    SOURCE_PASSPORT_STATUS = "source_passport_status"
    PII_DETECTED = "pii_detected"
    REDACTIONS_APPLIED = "redactions_applied"
    AI_RUNS_LOGGED = "ai_runs_logged"
    GOVERNANCE_DECISIONS = "governance_decisions"
    APPROVALS_REQUESTED = "approvals_requested"
    APPROVALS_COMPLETED = "approvals_completed"
    EXTERNAL_ACTIONS = "external_actions"
    CLAIMS_SUPPORTED_BY_PROOF = "claims_supported_by_proof"
    INCIDENTS = "incidents"
    RECOMMENDATIONS = "recommendations"


COMPLIANCE_REPORT_SECTIONS: tuple[ComplianceReportSection, ...] = tuple(
    ComplianceReportSection
)


@dataclass(frozen=True)
class ComplianceReport:
    engagement_id: str
    period: str
    sections: dict[ComplianceReportSection, str]

    def __post_init__(self) -> None:
        missing = set(COMPLIANCE_REPORT_SECTIONS) - set(self.sections)
        if missing:
            raise ValueError(
                "missing_compliance_sections:"
                + ",".join(sorted(s.value for s in missing))
            )
