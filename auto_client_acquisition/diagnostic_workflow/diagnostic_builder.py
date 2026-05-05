"""Diagnostic builder — combines CompanyBrainV6 + diagnostic engine.

Given an IntakeRecord, produces a DiagnosticBundle carrying both the
per-customer brain snapshot AND the bilingual diagnostic brief. The
output never contains the raw ``contact_handle`` — the brief is keyed
on ``company`` and the brain on ``company_handle``.
"""
from __future__ import annotations

from auto_client_acquisition.company_brain_v6 import (
    BuildRequest,
    build_company_brain_v6,
)
from auto_client_acquisition.diagnostic_engine import (
    DiagnosticRequest,
    generate_diagnostic,
)
from auto_client_acquisition.diagnostic_workflow.schemas import (
    DiagnosticBundle,
    IntakeRecord,
)


_DEFAULT_GAPS_AR_EN: tuple[str, ...] = (
    "no_structured_inbound_pipeline",
    "founder_bottleneck_after_hours",
    "no_written_proof_pack",
)


def build_diagnostic(record: IntakeRecord) -> DiagnosticBundle:
    """Compose a full diagnostic bundle from an anonymized intake."""
    brain = build_company_brain_v6(
        BuildRequest(
            company_handle=record.customer_handle,
            sector=record.sector,
            region=record.region,
            language_preference=record.language_preference,
        )
    )
    diag = generate_diagnostic(
        DiagnosticRequest(
            company=record.company,
            sector=record.sector,
            region=record.region,
            pipeline_state=record.pipeline_state,
        )
    )
    return DiagnosticBundle(
        company=record.company,
        recommended_bundle=diag.recommended_bundle,
        brain=brain,
        brief_markdown_ar_en=diag.markdown_ar_en,
        gaps=list(_DEFAULT_GAPS_AR_EN),
        approval_status="approval_required",
    )
