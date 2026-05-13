"""Dealix Compliance & Trust Operations OS.

Companion doc: ``docs/compliance_trust_ops/COMPLIANCE_BY_DESIGN.md``.
"""

from __future__ import annotations

from auto_client_acquisition.compliance_trust_os.claim_compliance import (
    ClaimStatus,
    classify_claim_status,
)
from auto_client_acquisition.compliance_trust_os.compliance_report import (
    COMPLIANCE_REPORT_SECTIONS,
    ComplianceReport,
)

__all__ = [
    "ClaimStatus",
    "classify_claim_status",
    "COMPLIANCE_REPORT_SECTIONS",
    "ComplianceReport",
]
