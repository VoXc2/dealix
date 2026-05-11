from __future__ import annotations

from saudi_ai_provider.go_live_sales import (
    build_go_live_sales_plan,
    evaluate_signature_readiness,
    render_go_live_sales_plan,
)


def test_build_go_live_sales_plan_for_enterprise() -> None:
    plan = build_go_live_sales_plan("enterprise")
    assert plan["segment"] == "enterprise"
    assert plan["priority_services"]
    assert plan["target_plays"]


def test_render_go_live_sales_plan_mentions_target_plays() -> None:
    text = render_go_live_sales_plan("mid_market", lang="ar")
    assert "Go-Live Sales Runbook" in text
    assert "Target Plays" in text


def test_signature_readiness_ready_case() -> None:
    verdict = evaluate_signature_readiness(
        stage="contract_ready",
        buyer_commitment="high",
        proof_level="L4",
        risk_status="low",
        governance_contract_accepted=True,
    )
    assert verdict.ready_to_ask_signature is True
    assert verdict.blockers == []


def test_signature_readiness_blocked_case() -> None:
    verdict = evaluate_signature_readiness(
        stage="proposal_sent",
        buyer_commitment="low",
        proof_level="L1",
        risk_status="high",
        governance_contract_accepted=False,
    )
    assert verdict.ready_to_ask_signature is False
    assert verdict.blockers
