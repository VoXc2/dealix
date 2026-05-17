"""North-star and supporting metrics definitions."""

from __future__ import annotations

from typing import Any


def north_star_metrics() -> dict[str, Any]:
    return {
        "primary": "governed_value_decisions_created",
        "primary_definition": (
            "Count of revenue/operations decisions executed with source clarity, "
            "approval boundary, evidence trail, and measurable value signal."
        ),
        "secondary": "diagnostic_to_sprint_to_retainer_conversions",
        "guardrail": "blocked_external_actions_without_approval",
    }


def activation_metrics() -> dict[str, Any]:
    return {
        "proof_pack_requests_per_week": "target >= 5",
        "qualified_meetings_from_trust_outreach": "target >= 3 weekly",
        "time_to_first_governed_decision_days": "target <= 7",
    }


def retention_metrics() -> dict[str, Any]:
    return {
        "proof_pack_delivery_sla": "target 100% on committed date",
        "decision_passport_completeness": "target >= 95%",
        "retainer_upgrade_trigger": "repeat governed workflow confirmed by monthly evidence",
    }


def revenue_metrics() -> dict[str, Any]:
    return {
        "paid_diagnostics_count": "7-day diagnostic invoices paid",
        "sprint_conversion_rate": "diagnostic clients converted to sprint",
        "retainer_mrr_sar": "active governed ops retainers monthly recurring revenue",
    }


def ai_quality_metrics() -> dict[str, Any]:
    return {
        "source_coverage_rate": "claims with explicit source_ref / total claims",
        "approval_before_external_action_rate": "external actions approved before execution",
        "unsupported_claims_caught": "claims blocked by evidence gate before delivery",
        "agent_tool_boundary_violations": "must remain zero under policy runtime",
    }
