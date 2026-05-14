"""Tests for wave-oriented execution modules (Trust MVP → Enterprise path)."""

from __future__ import annotations

import pytest

from auto_client_acquisition.adoption_os.retainer_readiness import wave2_retainer_eligibility
from auto_client_acquisition.agent_os.agent_card import AgentCard
from auto_client_acquisition.agent_os.agent_registry import clear_agent_registry_for_tests, register_agent
from auto_client_acquisition.agent_os.tool_permissions import tool_allowed_mvp
from auto_client_acquisition.auditability_os import AuditEvent, audit_event_valid
from auto_client_acquisition.capital_os import CapitalAssetType
from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.data_os.normalization import normalize_account_row_fields
from auto_client_acquisition.governance_os.claim_safety import audit_claim_safety
from auto_client_acquisition.proof_architecture_os.proof_pack_v2 import PROOF_PACK_V2_SECTIONS
from auto_client_acquisition.proof_os.proof_score import (
    proof_pack_completeness_score,
    proof_pack_score_with_governance_penalty,
    proof_strength_band,
)
from auto_client_acquisition.revenue_os.draft_pack import build_revenue_draft_pack
from auto_client_acquisition.secure_agent_runtime_os import (
    activate_kill_switch,
    evaluate_runtime_state,
    kill_switch_active,
    reset_kill_switch_for_tests,
)


@pytest.fixture(autouse=True)
def _reset_wave_side_effect_globals() -> None:
    clear_agent_registry_for_tests()
    reset_kill_switch_for_tests()
    yield
    clear_agent_registry_for_tests()
    reset_kill_switch_for_tests()


def test_claim_safety_blocks_guarantee() -> None:
    r = audit_claim_safety("نضمن لك مبيعات خلال أسبوع")
    assert r.suggested_decision == GovernanceDecision.BLOCK
    assert any("forbidden_claim:" in x for x in r.issues)


def test_proof_score_band() -> None:
    content = {k: "x" for k in PROOF_PACK_V2_SECTIONS}
    s = proof_pack_completeness_score(content)
    assert s == 100
    assert proof_strength_band(s) == "case_candidate"
    capped = proof_pack_score_with_governance_penalty(content, governance_blocked=True)
    assert capped <= 69


def test_normalize_account_row_lowercases_city() -> None:
    row = normalize_account_row_fields(
        {"company_name": "شركة  اختبار", "sector": "TECH", "city": " Riyadh ", "source": " CRM "},
    )
    assert row["city"] == "riyadh"
    assert row["sector"] == "tech"


def test_wave2_retainer_gate() -> None:
    ok, _ = wave2_retainer_eligibility(
        proof_score=85,
        adoption_score=75,
        workflow_owner_exists=True,
        monthly_workflow_exists=True,
        governance_risk_controlled=True,
    )
    assert ok
    ok2, reasons = wave2_retainer_eligibility(
        proof_score=70,
        adoption_score=75,
        workflow_owner_exists=True,
        monthly_workflow_exists=True,
        governance_risk_controlled=True,
    )
    assert not ok2
    assert "proof_score_below_80" in reasons


def test_draft_pack_has_linkedin_draft_only() -> None:
    pack = build_revenue_draft_pack({"company_name": "X"})
    assert "linkedin_draft_en" in pack
    assert "draft" in pack["linkedin_draft_en"].lower()


def test_audit_event_valid() -> None:
    e = AuditEvent(
        event_id="1",
        actor="system",
        source="revenue_intelligence",
        policy_checked="doctrine",
        matched_rule="no_cold_whatsapp",
        decision="BLOCK",
        approval_status="n/a",
        output_id="out-1",
        timestamp_iso="2026-05-14T00:00:00Z",
    )
    assert audit_event_valid(e)


def test_agent_registry_requires_identity() -> None:
    card = AgentCard(
        agent_id="AGT-REV-001",
        name="Revenue Intelligence Agent",
        owner="Revenue Owner",
        purpose="Score accounts and draft-only recommendations.",
        autonomy_level=2,
        status="active",
    )
    register_agent(card)
    assert tool_allowed_mvp("draft") is True
    assert tool_allowed_mvp("send_whatsapp") is False


def test_secure_runtime_kill_switch() -> None:
    assert evaluate_runtime_state("a1", forbidden_tool_attempt=False).value == "SAFE"
    activate_kill_switch()
    assert kill_switch_active()
    assert evaluate_runtime_state("a1", forbidden_tool_attempt=False).value == "KILLED"


def test_capital_asset_type_enum() -> None:
    assert CapitalAssetType.PROOF_EXAMPLE.value == "proof_example"
