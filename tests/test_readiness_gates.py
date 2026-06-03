"""Tests for readiness gates."""

from __future__ import annotations

from auto_client_acquisition.delivery_os.readiness_gates import (
    check_ai_readiness_gate,
    check_delivery_readiness_gate,
    check_production_readiness_gate,
    check_readiness_gate,
)


def test_delivery_gate_pass() -> None:
    ctx = dict.fromkeys(("inputs_known", "outputs_known", "exclusions_known", "timeline_known", "report_template_ready", "qa_checklist_ready", "impact_metric_defined", "next_offer_defined"), True)
    r = check_delivery_readiness_gate(ctx)
    assert r["passed"] is True
    assert r["blockers"] == []


def test_delivery_gate_blocks() -> None:
    r = check_delivery_readiness_gate({})
    assert r["passed"] is False
    assert "missing:inputs_known" in r["blockers"]


def test_ai_gate_pass_minimal() -> None:
    ctx = {
        "axes": {"data": 0.8, "process": 0.7, "governance": 0.8, "people": 0.5, "tech": 0.6},
        "data_sources": [{"id": "crm_export_1", "lawful_basis": "contract"}],
    }
    r = check_ai_readiness_gate(ctx)
    assert r["passed"] is True


def test_ai_gate_blocks_without_sources() -> None:
    r = check_ai_readiness_gate({"axes": {"data": 1.0}})
    assert r["passed"] is False
    assert "data_sources_required" in r["blockers"]


def test_production_gate_requires_cost_guard_with_llm() -> None:
    ctx = {
        "has_tests": True,
        "has_logging": True,
        "has_audit_event": True,
        "has_output_schema": True,
        "pii_safe": True,
        "has_fallback": True,
        "documentation_linked": True,
        "uses_llm": True,
        "has_cost_guard": False,
    }
    r = check_production_readiness_gate(ctx)
    assert r["passed"] is False
    assert "cost_guard_required_when_uses_llm" in r["blockers"]


def test_dispatch_unknown_gate() -> None:
    r = check_readiness_gate("unknown", {})
    assert r["passed"] is False
