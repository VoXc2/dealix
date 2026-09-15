from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


def test_root_agents_uses_registry_derived_omega_v3_authority() -> None:
    text = _text("AGENTS.md")
    lowered = text.lower()
    assert "the 5 real sub-agents" not in lowered
    assert "5 real sub-agents" not in lowered
    assert "agentic holding" in lowered
    assert "resourcegovernor" in lowered
    assert "session factory" in lowered
    assert "legacy executor aliases" in lowered or "compatibility aliases" in lowered


def test_root_agents_allows_safe_autonomous_l0_l4_verification() -> None:
    text = _text("AGENTS.md").lower()
    assert "run/tests commands only when explicitly requested by the user" not in text
    assert "l0-l4" in text
    assert "isolated" in text and "worktree" in text
    assert "l5" in text and ("exact" in text or "specific" in text)


def test_agent_docs_no_longer_make_fixed_five_the_canonical_roster() -> None:
    for path in ("docs/agents/README.md", "docs/agents/AGENT_TEAM_REGISTRY.md"):
        text = _text(path).lower()
        assert "the 5 real sub-agents" not in text
        assert "5 real sub-agents" not in text
        assert "agentic holding" in text or "registry-derived" in text
        assert "compatibility" in text or "legacy" in text


def test_active_agent_registry_has_no_retired_seven_day_delivery_authority() -> None:
    text = _text("docs/agents/AGENT_TEAM_REGISTRY.md").lower()
    assert "7-day revenue intelligence sprint" not in text
    assert "7 day revenue intelligence sprint" not in text
    assert "free execution diagnostic" in text
    assert "customer-specific" in text


def test_agent_audit_is_registry_driven_and_rejects_fixed_five_authority() -> None:
    text = _text("scripts/audit_agent_team.py")
    lowered = text.lower()
    assert "build_current_registry" in text
    assert "orphan" in lowered
    assert "fixed_five_authority" in lowered or "fixed-five" in lowered
    assert "session factory" in lowered or "session_factory" in lowered
    assert "resourcegovernor" in lowered or "resource_governor" in lowered


def test_root_governance_preserves_current_model_and_commercial_law() -> None:
    text = _text("AGENTS.md").lower()
    assert "provider-neutral" in text and "no silent paid spill" in text
    assert "free" in text and "diagnostic" in text
    assert "qualified discovery" in text
    assert "customer-specific" in text
    assert "fixed public price" in text or "no public fixed" in text
