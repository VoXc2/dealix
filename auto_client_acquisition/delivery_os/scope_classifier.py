"""Scope classifier — deterministic rules for change requests (no LLM)."""

from __future__ import annotations

from auto_client_acquisition.delivery_os.change_request import ChangeRequestType


def forbidden_capability_requested(description: str) -> bool:
    blob = description.strip().lower()
    markers = (
        "scrape",
        "scraping",
        "cold whatsapp",
        "linkedin automation",
        "guaranteed sales",
        "ضمان مبيعات",
        "نضمن لك مبيعات",
    )
    return any(m in blob for m in markers)


def classify_scope_change(
    description: str,
    *,
    within_contract: bool,
    estimated_extra_hours: float,
    minor_adjustment_hour_cap: float = 1.5,
    requires_new_data_source: bool = False,
    requests_forbidden_capability: bool = False,
) -> tuple[ChangeRequestType, str]:
    """
    Return (classification, rationale).

    ``requests_forbidden_capability`` should be True when the client asks for
    scraping, cold WhatsApp automation, guaranteed sales, etc.
    """
    if requests_forbidden_capability or forbidden_capability_requested(description):
        return ChangeRequestType.REJECTED, "forbidden_capability_request"
    if not within_contract:
        return ChangeRequestType.NEW_SPRINT, "outside_original_contract_surface"
    if requires_new_data_source:
        return ChangeRequestType.PAID_ADD_ON, "new_source_or_passport_surface"
    if estimated_extra_hours <= 0:
        return ChangeRequestType.INCLUDED, "clarification_or_copy_edit"
    if estimated_extra_hours <= minor_adjustment_hour_cap:
        return ChangeRequestType.MINOR_ADJUSTMENT, "within_minor_adjustment_budget"
    if estimated_extra_hours <= 8:
        return ChangeRequestType.PAID_ADD_ON, "material_delivery_effort"
    return ChangeRequestType.RETAINER_BACKLOG, "ongoing_iteration_belongs_in_retainer"


__all__ = ["classify_scope_change", "forbidden_capability_requested"]
