from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCOPES = (
    ROOT / "dealix" / "AGENTS.md",
    ROOT / "scripts" / "AGENTS.md",
    ROOT / "apps" / "web" / "AGENTS.md",
    ROOT / "auto_client_acquisition" / "AGENTS.md",
    ROOT / "config" / "company" / "AGENTS.md",
    ROOT / "tests" / "AGENTS.md",
)


def test_scoped_agent_precedence_exists_for_authority_sensitive_paths() -> None:
    for path in SCOPES:
        assert path.is_file(), path


def test_scoped_instructions_reject_superseded_global_authority() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in SCOPES)
    assert "omega v3" in combined
    assert "resourcegovernor" in combined
    assert "provider-neutral" in combined or "provider neutral" in combined
    assert "fixed-five" in combined or "fixed five" in combined
    assert "compatibility" in combined
    assert "exact action-bound l5" in combined


def test_web_scope_preserves_governed_public_truth() -> None:
    text = (ROOT / "apps" / "web" / "AGENTS.md").read_text(encoding="utf-8").lower()
    assert "free execution diagnostic" in text
    assert "fixed price" in text
    assert "fixed five-agent" in text
    assert "http 200" in text


def test_company_brain_scope_preserves_truth_firewall() -> None:
    text = (ROOT / "auto_client_acquisition" / "AGENTS.md").read_text(encoding="utf-8").lower()
    assert "research != relationship" in text
    assert "draft != sent" in text
    assert "payment != verified revenue" in text
