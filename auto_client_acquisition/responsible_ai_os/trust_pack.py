"""Responsible AI Trust Pack — canonical section slugs for client deliverable."""

from __future__ import annotations

from collections.abc import Mapping

TRUST_PACK_SECTIONS: tuple[str, ...] = (
    "dealix_responsible_ai_standard",
    "what_dealix_refuses_to_build",
    "data_handling_model",
    "source_passport",
    "use_case_risk_classification",
    "ai_inventory",
    "human_oversight_model",
    "governance_runtime",
    "ai_run_ledger",
    "approval_engine",
    "proof_pack_standard",
    "incident_response",
    "client_responsibilities",
)


def trust_pack_sections_complete(
    content_by_section: Mapping[str, str],
) -> tuple[bool, tuple[str, ...]]:
    missing = [k for k in TRUST_PACK_SECTIONS if not (content_by_section.get(k) or "").strip()]
    return not missing, tuple(missing)
