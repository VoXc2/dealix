"""Map canonical event types to metric families (documentation + lookup)."""

from __future__ import annotations

from typing import Final

# event_type -> metric_family
EVENT_METRIC_FAMILY: Final[dict[str, str]] = {
    "project_created": "delivery",
    "client_intake_completed": "delivery",
    "data_source_registered": "data",
    "dataset_uploaded": "data",
    "data_quality_scored": "data",
    "pii_detected": "governance",
    "governance_checked": "governance",
    "ai_run_completed": "ai_run",
    "account_scored": "revenue",
    "draft_generated": "delivery",
    "approval_required": "governance",
    "approval_granted": "governance",
    "proof_event_created": "proof",
    "report_delivered": "proof",
    "capital_asset_created": "capital",
    "feature_candidate_created": "productization",
    "retainer_recommended": "commercial",
    "retainer_won": "commercial",
    "playbook_updated": "capital",
    "partner_lead_created": "partner",
    "venture_signal_detected": "venture",
}


def metric_family_for_event(event_type: str) -> str | None:
    return EVENT_METRIC_FAMILY.get(event_type)
