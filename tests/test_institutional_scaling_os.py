"""Tests for institutional_scaling_os."""

from __future__ import annotations

from auto_client_acquisition.endgame_os.agent_control import AgentControlCard
from auto_client_acquisition.endgame_os.governance_product import GovernanceDecision
from auto_client_acquisition.institutional_scaling_os import (
    CONTROL_MEMO_SECTIONS,
    InstitutionalRisk,
    ScalingDisciplineSnapshot,
    agent_identity_mvp_ok,
    build_control_memo_markdown_skeleton,
    control_memo_complete,
    privacy_runtime_audit_payload,
    privacy_runtime_outcome,
    risk_register_entry_valid,
    scaling_discipline_blockers,
    trust_engine_coverage_score,
)
from auto_client_acquisition.institutional_scaling_os.risk_register import (
    RiskRegisterEntry,
)
from auto_client_acquisition.institutional_scaling_os.trust_engine import (
    TRUST_ENGINE_COMPONENTS,
)


def test_trust_engine_coverage() -> None:
    full = frozenset(TRUST_ENGINE_COMPONENTS)
    assert trust_engine_coverage_score(full) == 100
    assert trust_engine_coverage_score(frozenset()) == 0


def test_agent_identity_wraps_mvp() -> None:
    card = AgentControlCard("A", "n", "o", "p", 3, True)
    assert agent_identity_mvp_ok(card)[0]
    assert not agent_identity_mvp_ok(AgentControlCard("A", "n", "o", "p", 5, True))[0]


def test_privacy_runtime() -> None:
    r = privacy_runtime_outcome(
        input_contains_pii=True,
        allowed_use=frozenset({"internal_analysis", "draft_only"}),
        external_use_allowed=False,
    )
    assert r.decision == GovernanceDecision.DRAFT_ONLY
    assert "human_review" in r.required_action
    b = privacy_runtime_outcome(
        input_contains_pii=False,
        allowed_use=frozenset({"internal_analysis"}),
        external_use_allowed=False,
    )
    assert b.decision == GovernanceDecision.ALLOW


def test_scaling_discipline() -> None:
    good = ScalingDisciplineSnapshot(True, True, True, True)
    assert scaling_discipline_blockers(good) == ()
    bad = ScalingDisciplineSnapshot(False, True, True, True)
    assert "trust_metrics_weak_no_scale" in scaling_discipline_blockers(bad)


def test_control_memo() -> None:
    full = dict.fromkeys(CONTROL_MEMO_SECTIONS, "x")
    assert control_memo_complete(full) == (True, ())
    partial = dict(full)
    partial["proof"] = "   "
    ok, missing = control_memo_complete(partial)
    assert not ok and missing == ("proof",)


def test_risk_register() -> None:
    assert len(InstitutionalRisk) == 10
    entry = RiskRegisterEntry(
        risk_id="R1",
        owner="ceo",
        likelihood="med",
        impact="high",
        control="catalog",
        early_warning_signal="greenfield",
        response_plan="productize",
    )
    assert risk_register_entry_valid(entry)
    assert not risk_register_entry_valid(
        RiskRegisterEntry("", "a", "b", "c", "d", "e", "f"),
    )


def test_privacy_runtime_audit_payload_matches_doctrine_example() -> None:
    payload = privacy_runtime_audit_payload(
        input_contains_pii=True,
        allowed_use=frozenset({"internal_analysis", "draft_only"}),
        external_use_allowed=False,
    )
    assert payload["decision"] == "DRAFT_ONLY"
    assert payload["required_action"] == "human_review_before_any_external_use"
    assert payload["allowed_use"] == ["draft_only", "internal_analysis"]


def test_control_memo_skeleton_contains_ten_sections() -> None:
    md = build_control_memo_markdown_skeleton()
    assert "## 10. Strategic Bet" in md
    assert "Stop List" in md
