"""Readiness gates — delivery, AI, and production checklists (deterministic, no LLM)."""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.data_os.data_quality_score import summarize_table_quality
from auto_client_acquisition.strategy_os.ai_readiness import compute_ai_readiness


def check_delivery_readiness_gate(context: dict[str, Any]) -> dict[str, Any]:
    """Eight pre-sale / pre-build questions — all must be true to pass."""
    required = (
        "inputs_known",
        "outputs_known",
        "exclusions_known",
        "timeline_known",
        "report_template_ready",
        "qa_checklist_ready",
        "impact_metric_defined",
        "next_offer_defined",
    )
    blockers: list[str] = []
    for key in required:
        if not context.get(key):
            blockers.append(f"missing:{key}")
    return {"gate": "delivery", "passed": not blockers, "blockers": blockers}


def check_ai_readiness_gate(context: dict[str, Any]) -> dict[str, Any]:
    """Data + policy + optional table quality before AI implementation."""
    blockers: list[str] = []
    axes = context.get("axes")
    if not isinstance(axes, dict) or not axes:
        blockers.append("axes_required")

    sources = context.get("data_sources")
    if not isinstance(sources, list) or len(sources) == 0:
        blockers.append("data_sources_required")
    else:
        for i, s in enumerate(sources):
            if not isinstance(s, dict):
                blockers.append(f"data_sources[{i}]_not_object")
                continue
            if not str(s.get("id") or "").strip():
                blockers.append(f"data_sources[{i}]_missing_id")
            if not str(s.get("lawful_basis") or "").strip():
                blockers.append(f"data_sources[{i}]_missing_lawful_basis")

    rows = context.get("sample_rows")
    if isinstance(rows, list) and rows:
        q = summarize_table_quality(rows)
        if q.get("mean_completeness", 0) < 0.25:
            blockers.append("sample_data_completeness_too_low")

    if isinstance(axes, dict) and axes:
        ar = compute_ai_readiness(axes)
        if ar["readiness_score"] < 0.35:
            blockers.append("ai_readiness_score_below_threshold")

    return {"gate": "ai", "passed": not blockers, "blockers": blockers}


def check_production_readiness_gate(context: dict[str, Any]) -> dict[str, Any]:
    """Technical checklist — filled manually or by CI integration later."""
    required = (
        "has_tests",
        "has_logging",
        "has_audit_event",
        "has_output_schema",
        "pii_safe",
        "has_fallback",
        "documentation_linked",
    )
    blockers: list[str] = []
    for key in required:
        if not context.get(key):
            blockers.append(f"missing:{key}")
    uses_llm = bool(context.get("uses_llm"))
    if uses_llm and not context.get("has_cost_guard"):
        blockers.append("cost_guard_required_when_uses_llm")
    return {"gate": "production", "passed": not blockers, "blockers": blockers}


def check_readiness_gate(
    gate: str,
    context: dict[str, Any],
) -> dict[str, Any]:
    g = gate.lower().strip()
    if g == "delivery":
        return check_delivery_readiness_gate(context)
    if g == "ai":
        return check_ai_readiness_gate(context)
    if g == "production":
        return check_production_readiness_gate(context)
    return {
        "gate": gate,
        "passed": False,
        "blockers": [f"unknown_gate:{gate}"],
    }
