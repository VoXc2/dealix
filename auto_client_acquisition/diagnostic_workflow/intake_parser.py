"""Parse a warm-intro IntakeRequest into an anonymized IntakeRecord.

The parser ALWAYS overrides ``customer_handle`` with a derived public
placeholder built from the company name. Whatever the founder submits
in ``contact_handle`` is treated as opaque and never used as the
identifier.
"""
from __future__ import annotations

from uuid import uuid4

from auto_client_acquisition.diagnostic_workflow.schemas import (
    IntakeRecord,
    IntakeRequest,
)


def _safe_company_token(company: str) -> str:
    cleaned = "".join(ch for ch in company.strip() if ch.isalnum() or ch in (" ", "-", "_"))
    return cleaned.replace(" ", "-").upper() or "CUSTOMER"


def parse_intake(req: IntakeRequest) -> IntakeRecord:
    """Build the anonymized record stored downstream."""
    customer_handle = f"{_safe_company_token(req.company)}-PILOT-PLACEHOLDER"
    return IntakeRecord(
        company=req.company,
        sector=req.sector,
        region=req.region,
        # Re-anonymize: never echo whatever was submitted as a raw value.
        contact_handle="PLACEHOLDER-HANDLE",
        pipeline_state=req.pipeline_state,
        source=req.source,
        language_preference=req.language_preference,
        intake_id=f"intake_{uuid4().hex[:12]}",
        customer_handle=customer_handle,
        consent_recorded=False,
    )
