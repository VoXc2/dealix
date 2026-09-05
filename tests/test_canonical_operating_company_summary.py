from auto_client_acquisition.ai_workforce.canonical_delegation import CANONICAL_AGENTS
from auto_client_acquisition.orchestrator.canonical_operating_company import (
    build_canonical_operating_company_summary,
)


def test_operating_company_summary_exposes_five_canonical_agents_only() -> None:
    summary = build_canonical_operating_company_summary()
    assert summary["canonical_agents_total"] == 5
    assert set(summary["canonical_agents"]) == set(CANONICAL_AGENTS)
    assert summary["specialist_roles_total"] == 15
    assert summary["specialist_role_semantics"] == "BOUNDED_WORKLOAD_NOT_PERMANENT_AGENT"
    assert summary["legacy_agents_total_compatibility"] == 15
    assert summary["legacy_agents_total_authoritative"] is False
    assert "agents_total" not in summary
