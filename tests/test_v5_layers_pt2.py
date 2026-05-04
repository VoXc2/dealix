"""Tests for v5 layers part 2: agent_governance + reliability_os + vertical_playbooks."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.agent_governance import (
    AGENT_REGISTRY,
    AutonomyLevel,
    FORBIDDEN_TOOLS,
    ToolCategory,
    ToolPermission,
    evaluate_action,
    get_agent,
    list_agents,
)
from auto_client_acquisition.reliability_os import (
    HealthStatus,
    build_health_matrix,
)
from auto_client_acquisition.vertical_playbooks import (
    Vertical,
    get_playbook,
    list_playbooks,
    recommend_for,
)


# ════════════════════ agent_governance ════════════════════


def test_registry_has_core_agents():
    ids = set(list_agents())
    for required in {"prospecting", "personalization", "compliance", "outreach", "finance_assistant"}:
        assert required in ids, f"missing core agent: {required}"


def test_get_agent_unknown_raises():
    with pytest.raises(KeyError):
        get_agent("__not_a_real_agent__")


@pytest.mark.parametrize(
    "tool",
    [
        ToolCategory.SEND_WHATSAPP_LIVE,
        ToolCategory.LINKEDIN_AUTOMATION,
        ToolCategory.SCRAPE_WEB,
        ToolCategory.CHARGE_PAYMENT_LIVE,
        ToolCategory.SEND_EMAIL_LIVE,
    ],
)
def test_forbidden_tools_blocked_at_every_autonomy_level(tool: ToolCategory):
    """No autonomy level can override platform-level FORBIDDEN_TOOLS."""
    for level in AutonomyLevel:
        result = evaluate_action(
            agent_id="prospecting",
            tool=tool,
            autonomy_level=level,
            allowed_tools=[tool],  # even if explicitly allowed!
        )
        assert result.permitted is False
        assert result.permission == ToolPermission.FORBIDDEN.value


def test_l5_blocks_external_tool_but_allows_read_only():
    # Read-only tool at L5 → allowed
    ok = evaluate_action(
        agent_id="prospecting",
        tool=ToolCategory.READ_PUBLIC_WEB,
        autonomy_level=AutonomyLevel.L5_BLOCKED_FOR_EXTERNAL,
        allowed_tools=[ToolCategory.READ_PUBLIC_WEB],
    )
    assert ok.permitted is True
    # External-effect tool (draft_message — not even forbidden) at L5 → blocked
    blocked = evaluate_action(
        agent_id="prospecting",
        tool=ToolCategory.DRAFT_MESSAGE,
        autonomy_level=AutonomyLevel.L5_BLOCKED_FOR_EXTERNAL,
        allowed_tools=[ToolCategory.DRAFT_MESSAGE],
    )
    assert blocked.permitted is False


def test_tool_not_in_allowed_list_blocked():
    result = evaluate_action(
        agent_id="prospecting",
        tool=ToolCategory.DRAFT_EMAIL,
        autonomy_level=AutonomyLevel.L2_APPROVAL_REQUIRED,
        allowed_tools=[ToolCategory.READ_PUBLIC_WEB],
    )
    assert result.permitted is False
    assert "not in agent" in result.reason


def test_approval_required_tools_never_auto_execute():
    """Even at L3+, draft_message etc. require approval."""
    for level in (AutonomyLevel.L3_APPROVED_EXECUTE, AutonomyLevel.L4_INTERNAL_AUTOMATION_ONLY):
        result = evaluate_action(
            agent_id="personalization",
            tool=ToolCategory.DRAFT_MESSAGE,
            autonomy_level=level,
            allowed_tools=[ToolCategory.DRAFT_MESSAGE],
        )
        assert result.permitted is True
        assert result.permission == ToolPermission.REQUIRES_APPROVAL.value


def test_read_only_tools_allowed_at_l0():
    result = evaluate_action(
        agent_id="prospecting",
        tool=ToolCategory.READ_PUBLIC_WEB,
        autonomy_level=AutonomyLevel.L0_READ_ONLY,
        allowed_tools=[ToolCategory.READ_PUBLIC_WEB],
    )
    assert result.permitted is True
    assert result.permission == ToolPermission.ALLOWED.value


def test_default_l2_returns_requires_approval_for_neutral_tool():
    result = evaluate_action(
        agent_id="outreach",
        tool=ToolCategory.CREATE_INVOICE_DRAFT,
        autonomy_level=AutonomyLevel.L2_APPROVAL_REQUIRED,
        allowed_tools=[ToolCategory.CREATE_INVOICE_DRAFT],
    )
    assert result.permitted is True
    assert result.permission == ToolPermission.REQUIRES_APPROVAL.value


def test_safety_notes_always_present():
    result = evaluate_action(
        agent_id="prospecting",
        tool=ToolCategory.READ_PUBLIC_WEB,
        autonomy_level=AutonomyLevel.L1_DRAFT_ONLY,
        allowed_tools=[ToolCategory.READ_PUBLIC_WEB],
    )
    notes = result.safety_notes
    assert "no_cold_outreach" in notes
    assert "no_scraping" in notes
    assert "no_linkedin_automation" in notes


def test_every_registered_agent_forbids_a_dangerous_tool():
    """Defensive — none of the registered agents may have an empty
    forbidden_tools list while also allowing a sensitive tool."""
    for agent_id, spec in AGENT_REGISTRY.items():
        sensitive_allowed = any(
            t in spec.allowed_tools for t in (
                ToolCategory.DRAFT_WHATSAPP_REPLY,
                ToolCategory.DRAFT_EMAIL,
                ToolCategory.CREATE_INVOICE_DRAFT,
            )
        )
        if sensitive_allowed:
            assert spec.forbidden_tools, (
                f"agent {agent_id} allows sensitive tools but has no forbidden_tools"
            )


def test_forbidden_tools_set_includes_all_dangerous():
    expected = {
        ToolCategory.SEND_WHATSAPP_LIVE,
        ToolCategory.LINKEDIN_AUTOMATION,
        ToolCategory.SCRAPE_WEB,
        ToolCategory.CHARGE_PAYMENT_LIVE,
        ToolCategory.SEND_EMAIL_LIVE,
    }
    assert expected.issubset(FORBIDDEN_TOOLS)


# ════════════════════ reliability_os ════════════════════


def test_health_matrix_returns_typed_blocks():
    matrix = build_health_matrix()
    for key in ("schema_version", "generated_at", "overall_status",
                 "counts", "subsystems", "guardrails"):
        assert key in matrix
    assert matrix["overall_status"] in {s.value for s in HealthStatus}
    assert isinstance(matrix["subsystems"], list)
    assert len(matrix["subsystems"]) >= 5


def test_health_matrix_subsystem_records_have_name_status_dimension():
    matrix = build_health_matrix()
    for s in matrix["subsystems"]:
        assert "name" in s
        assert "status" in s
        assert "dimension" in s
        assert "description" in s


def test_health_matrix_includes_safety_subsystems():
    matrix = build_health_matrix()
    names = {s["name"] for s in matrix["subsystems"]}
    assert "safe_action_gateway" in names
    assert "live_action_gates" in names
    assert "safe_publishing_gate" in names


def test_health_matrix_safe_action_gateway_is_ok():
    matrix = build_health_matrix()
    safe = next(s for s in matrix["subsystems"] if s["name"] == "safe_action_gateway")
    assert safe["status"] == "ok"


def test_health_matrix_live_action_gates_is_ok():
    matrix = build_health_matrix()
    gates = next(s for s in matrix["subsystems"] if s["name"] == "live_action_gates")
    assert gates["status"] == "ok"


def test_health_matrix_guardrails_block_locked():
    matrix = build_health_matrix()
    g = matrix["guardrails"]
    assert g["no_live_send"] is True
    assert g["no_scraping"] is True
    assert g["no_cold_outreach"] is True


# ════════════════════ vertical_playbooks ════════════════════


def test_list_playbooks_returns_5():
    assert set(list_playbooks()) == {
        "agency", "b2b_services", "saas",
        "training_consulting", "local_services",
    }


@pytest.mark.parametrize("vertical", list(Vertical))
def test_every_playbook_has_arabic_and_english(vertical: Vertical):
    pb = get_playbook(vertical)
    assert pb["name_ar"] and pb["name_en"]
    assert pb["icp_ar"] and pb["icp_en"]
    assert pb["best_first_offer_ar"] and pb["best_first_offer_en"]
    assert pb["common_pains_ar"] and pb["common_pains_en"]
    assert pb["diagnostic_questions_ar"] and pb["diagnostic_questions_en"]


@pytest.mark.parametrize("vertical", list(Vertical))
def test_every_playbook_forbids_unsafe_channels(vertical: Vertical):
    pb = get_playbook(vertical)
    forbidden = pb["forbidden_channels"]
    # Each playbook must explicitly forbid cold WhatsApp.
    assert "cold_whatsapp" in forbidden, f"{vertical.value} doesn't forbid cold_whatsapp"


@pytest.mark.parametrize("vertical", list(Vertical))
def test_no_playbook_recommends_unsafe_action(vertical: Vertical):
    pb = get_playbook(vertical)
    text = " ".join([
        pb["best_first_offer_ar"], pb["best_first_offer_en"],
        pb["message_pattern_ar"], pb["message_pattern_en"],
        " ".join(pb["common_pains_ar"]), " ".join(pb["common_pains_en"]),
    ]).lower()
    for tok in ("blast", "scrape", "guaranteed", "auto-dm"):
        assert tok not in text, f"{vertical.value} mentions unsafe token {tok!r}"


def test_recommend_returns_saas_for_saas_hint():
    pb = recommend_for("Saudi SaaS B2B accounting tool")
    assert pb["vertical"] == "saas"


def test_recommend_returns_agency_for_marketing_hint():
    pb = recommend_for("performance marketing agency")
    assert pb["vertical"] == "agency"


def test_recommend_falls_back_to_b2b_services():
    pb = recommend_for("something completely unmapped")
    assert pb["vertical"] == "b2b_services"


def test_recommend_handles_empty_hint_safely():
    pb = recommend_for("")
    assert pb["vertical"] == "b2b_services"


# ════════════════════ API endpoint tests ════════════════════


@pytest.mark.asyncio
async def test_agent_governance_status_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/agent-governance/status")
    assert r.status_code == 200
    payload = r.json()
    assert payload["default_autonomy_level"] == "L2_approval_required"
    assert "send_whatsapp_live" in payload["forbidden_tools"]


@pytest.mark.asyncio
async def test_agent_governance_evaluate_endpoint_blocks_forbidden():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/agent-governance/evaluate",
            json={
                "agent_id": "prospecting",
                "tool": "send_whatsapp_live",
                "autonomy_level": "L3_approved_execute",
                "allowed_tools": ["send_whatsapp_live"],
            },
        )
    assert r.status_code == 200
    payload = r.json()
    assert payload["permitted"] is False
    assert payload["permission"] == "forbidden"


@pytest.mark.asyncio
async def test_agent_governance_get_one_agent():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/agent-governance/agents/personalization")
    assert r.status_code == 200
    assert r.json()["agent_id"] == "personalization"


@pytest.mark.asyncio
async def test_reliability_health_matrix_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/reliability/health-matrix")
    assert r.status_code == 200
    payload = r.json()
    assert "subsystems" in payload
    assert payload["overall_status"] in {"ok", "degraded", "unavailable", "unknown"}


@pytest.mark.asyncio
async def test_vertical_playbooks_list_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/vertical-playbooks/list")
    assert r.status_code == 200
    assert "saas" in r.json()["verticals"]


@pytest.mark.asyncio
async def test_vertical_playbooks_recommend_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/vertical-playbooks/recommend",
            json={"sector_hint": "Saudi SaaS company"},
        )
    assert r.status_code == 200
    assert r.json()["vertical"] == "saas"


@pytest.mark.asyncio
async def test_vertical_playbook_404_unknown():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/vertical-playbooks/__not_real__")
    assert r.status_code == 404
