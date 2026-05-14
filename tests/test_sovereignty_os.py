"""Tests for sovereignty_os."""

from __future__ import annotations

import pytest

from auto_client_acquisition.endgame_os.agent_control import AgentControlCard
from auto_client_acquisition.sovereignty_os import (
    AgentSovereigntyCard,
    CapitalSovereigntyMinimum,
    ModelRouterContext,
    SourcePassport,
    all_listed_dependencies_mitigated,
    can_make_retainer_push,
    capital_minimum_met,
    commercial_resilience_score,
    dependency_mitigated,
    enterprise_readiness_summary,
    proof_sections_complete,
    route_model_decision,
    source_passport_valid_for_ai,
    validate_agent_sovereignty,
)


def test_dependency_mitigated() -> None:
    assert dependency_mitigated(
        "single_llm_provider",
        frozenset({"llm_gateway_model_router"}),
    )


def test_all_mitigated() -> None:
    controls = frozenset({
        "llm_gateway_model_router",
        "delivery_os_checklists",
        "productized_offers",
        "source_passport",
        "governance_runtime",
        "partner_academy_distribution",
        "portfolio_strategy",
        "proof_pack_standard",
        "capital_ledger",
    })
    assert all_listed_dependencies_mitigated(controls)


def test_model_router_pii_high_risk() -> None:
    tier, tags = route_model_decision(
        ModelRouterContext(
            task_type="draft_outreach",
            risk_level="high",
            contains_pii=True,
            language="ar",
            required_quality="high",
        ),
    )
    assert tier == "rules_only"
    assert tags


def test_source_passport_blocks_bad_external_pii() -> None:
    ok, errs = source_passport_valid_for_ai(
        SourcePassport(
            source_id="SRC-1",
            source_type="client_upload",
            owner="client",
            allowed_use=frozenset({"internal_analysis"}),
            contains_pii=True,
            sensitivity="high",
            retention_policy="project_duration",
            ai_access_allowed=True,
            external_use_allowed=True,
        ),
    )
    assert not ok
    assert errs


def test_agent_sovereignty_mvp() -> None:
    base = AgentControlCard(
        agent_id="A1",
        name="R",
        owner="Dealix",
        purpose="x",
        autonomy_level=2,
        audit_required=True,
    )
    card = AgentSovereigntyCard(
        base=base,
        allowed_tools=frozenset({"internal_scorer"}),
        forbidden_actions_enumerated=frozenset({"send_messages"}),
        decommission_rule="on_unit_shutdown_archive",
    )
    ok, _ = validate_agent_sovereignty(card)
    assert ok


def test_agent_sovereignty_autonomy_cap() -> None:
    base = AgentControlCard(
        agent_id="A1",
        name="R",
        owner="Dealix",
        purpose="x",
        autonomy_level=5,
        audit_required=True,
    )
    card = AgentSovereigntyCard(
        base=base,
        allowed_tools=frozenset({"t"}),
        forbidden_actions_enumerated=frozenset(),
        decommission_rule="rule",
    )
    ok, errs = validate_agent_sovereignty(card)
    assert not ok
    assert "mvp_autonomy_exceeded" in errs


def test_proof_sections() -> None:
    full = frozenset(
        (
            "problem",
            "inputs",
            "work_completed",
            "metrics",
            "before_after",
            "ai_outputs",
            "governance_events",
            "business_value",
            "risks",
            "limitations",
            "recommended_next_step",
        ),
    )
    assert proof_sections_complete(full) is True


def test_capital_minimum() -> None:
    assert capital_minimum_met(CapitalSovereigntyMinimum(True, True, True))
    assert not capital_minimum_met(CapitalSovereigntyMinimum(True, False, True))


def test_commercial_resilience() -> None:
    assert commercial_resilience_score(frozenset({"sprints", "retainers"})) > 0


def test_enterprise_summary() -> None:
    lvl, tag = enterprise_readiness_summary(
        frozenset(
            {
                "data_handling_policy",
                "ai_usage_policy",
                "no_unsafe_automation_commitment",
                "proof_standard",
            },
        ),
    )
    assert lvl >= 1
    assert tag


def test_dependency_unknown() -> None:
    with pytest.raises(ValueError):
        dependency_mitigated("nope", frozenset())
