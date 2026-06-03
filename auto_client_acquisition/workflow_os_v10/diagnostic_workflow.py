"""Pre-defined Mini Diagnostic workflow."""
from __future__ import annotations

from auto_client_acquisition.workflow_os_v10.schemas import WorkflowDefinition

MINI_DIAGNOSTIC = WorkflowDefinition(
    workflow_id="wf_mini_diagnostic",
    name="mini_diagnostic",
    description_ar=(
        "Diagnostic مصغّر للعميل — يولّد مسوّدة تشخيص بدون أيّ إرسال خارجي."
    ),
    description_en=(
        "Mini-diagnostic for a customer — produces a diagnostic draft, "
        "no external send."
    ),
    steps=[
        "intake_payload_parse",
        "icp_match_score",
        "pain_extract",
        "service_recommend",
        "diagnostic_draft_bilingual",
    ],
)
