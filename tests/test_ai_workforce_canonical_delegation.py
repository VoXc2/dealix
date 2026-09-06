from __future__ import annotations

from pathlib import Path

from auto_client_acquisition.ai_workforce import (
    AGENT_REGISTRY,
    CANONICAL_AGENTS,
    REVENUE_SPECIALIST_DELEGATION,
    RUNTIME_SPECIALIST_DELEGATION,
    WorkforceGoal,
    build_revenue_factory_blueprint,
    run_workforce_goal,
)

ROOT = Path(__file__).resolve().parents[1]
AGENT_CONTRACTS_SOURCE = ROOT / "auto_client_acquisition/ai_workforce/agent_contracts.py"
ORCHESTRATOR_SOURCE = ROOT / "auto_client_acquisition/ai_workforce/orchestrator.py"
SCHEMAS_SOURCE = ROOT / "auto_client_acquisition/ai_workforce/schemas.py"


def test_all_runtime_specialist_roles_delegate_to_five_canonical_agents() -> None:
    assert set(AGENT_REGISTRY) == set(RUNTIME_SPECIALIST_DELEGATION)
    assert set(RUNTIME_SPECIALIST_DELEGATION.values()) <= set(CANONICAL_AGENTS)
    assert len(CANONICAL_AGENTS) == 5


def test_revenue_factory_specialists_delegate_without_losing_automation_plays() -> None:
    blueprint = build_revenue_factory_blueprint()
    role_ids = {item["agent_id"] for item in blueprint["agent_contracts"]}
    assert role_ids == set(REVENUE_SPECIALIST_DELEGATION)
    assert blueprint["canonical_agents_total"] == 5
    assert blueprint["specialist_roles_total"] == 15
    assert len(blueprint["automation_plays"]) == 30
    assert all(
        item["canonical_owner"] in CANONICAL_AGENTS
        for item in blueprint["agent_contracts"]
    )
    assert all(
        slot["canonical_owner"] in CANONICAL_AGENTS
        for slot in blueprint["daily_schedule"]
    )


def test_workforce_run_emits_canonical_ownership_and_safe_entry_offer() -> None:
    goal = WorkforceGoal(
        company_handle="dealix-canonical-acceptance",
        goal_en="Prepare governed revenue next actions",
        desired_outcome="qualified evidence-backed opportunity",
        approved_channels=[],
        blocked_channels=["cold_whatsapp", "linkedin_automation"],
        language_preference="en",
    )
    run = run_workforce_goal(goal)
    assert run.recommended_service == "free_mini_diagnostic"
    assert run.specialist_roles_used == run.assigned_agents
    assert set(run.canonical_agents_used) <= set(CANONICAL_AGENTS)
    assert run.canonical_agents_used
    assert all(task.canonical_owner in CANONICAL_AGENTS for task in run.task_plan)
    assert all(
        request["canonical_owner"] in CANONICAL_AGENTS
        for request in run.approval_requests
    )


def test_finance_and_delivery_never_create_autonomous_price_or_payment() -> None:
    goal = WorkforceGoal(company_handle="dealix-finance-gate")
    run = run_workforce_goal(goal)
    by_role = {task.agent_id: task for task in run.task_plan}

    finance = by_role["FinanceAgent"].output
    assert finance["amount_sar"] is None
    assert finance["customer_specific_quote_only"] is True
    assert finance["invoice_draft_status"] == "blocked_until_approved_customer_specific_quote"
    assert finance["live_charge_enabled"] is False
    assert finance["payment_execution_enabled"] is False
    assert finance["payment_verification_required"] is True

    delivery = by_role["DeliveryAgent"].output
    assert delivery["service_id"] == "revenue_command_pilot_30d"
    assert delivery["release_status"] == "blocked_until_customer_specific_quote_and_verified_payment_or_start_authority"
    assert delivery["public_fixed_price"] is False


def test_active_ai_workforce_sources_cannot_recreate_retired_commercial_motion() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (AGENT_CONTRACTS_SOURCE, ORCHESTRATOR_SOURCE, SCHEMAS_SOURCE)
    )
    for forbidden in (
        "499 SAR Pilot invoice draft prepared",
        "مسوّدة فاتورة 499 ريال",
        'tier_id="growth_starter_pilot"',
        'return "growth_starter"',
        'recommended_service: str = "growth_starter"',
        "7-Day Revenue Command Room Sprint",
        "7-Day Operating Diagnostic",
    ):
        assert forbidden not in source

    for required in (
        "free_mini_diagnostic",
        "revenue_command_pilot_30d",
        "customer_specific_quote",
        "verified_payment",
        "customer_validated_proof",
        "canonical_owner",
    ):
        assert required in source
