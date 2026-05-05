"""Pre-defined Proof Pack assembly workflow."""
from __future__ import annotations

from auto_client_acquisition.workflow_os_v10.schemas import WorkflowDefinition


PROOF_PACK_ASSEMBLY = WorkflowDefinition(
    workflow_id="wf_proof_pack_assembly",
    name="proof_pack_assembly",
    description_ar=(
        "تجميع Proof Pack من الأحداث المكتوبة — كل خطوة تحتاج مراجعة "
        "قبل النشر."
    ),
    description_en=(
        "Assemble a Proof Pack from logged events — each step requires "
        "manual review before publication."
    ),
    steps=[
        "collect_proof_events",
        "redact_pii",
        "draft_summary_bilingual",
        "request_consent",
        "qa_gate_check",
        "ready_for_send",
    ],
)
