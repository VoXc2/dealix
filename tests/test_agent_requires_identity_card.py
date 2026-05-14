"""Doctrine commitment #9: no agent without identity.

Every AI agent in Dealix has a documented identity card listing its
owner, allowed tools, and kill switch. This test asserts that the agent
runtime infrastructure is on disk and that the doctrine source declares
the rule.
"""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_agent_os_module_exists():
    candidates = [
        REPO_ROOT / "auto_client_acquisition" / "agent_os",
        REPO_ROOT / "auto_client_acquisition" / "agents",
    ]
    assert any(p.exists() and p.is_dir() for p in candidates), (
        "Agent OS module missing — commitment #9 (no agent without identity) "
        "has no infrastructure to enforce it."
    )


def test_secure_agent_runtime_module_exists():
    p = REPO_ROOT / "auto_client_acquisition" / "secure_agent_runtime_os"
    assert p.exists() and p.is_dir(), (
        "secure_agent_runtime_os module missing — kill-switch / sandboxing "
        "infrastructure required for commitment #9."
    )


def test_doctrine_source_declares_identity_rule():
    p = REPO_ROOT / "open-doctrine" / "11_NON_NEGOTIABLES.md"
    assert p.exists()
    text = p.read_text(encoding="utf-8")
    assert "No agent without identity" in text, (
        "open-doctrine/11_NON_NEGOTIABLES.md must declare commitment #9 "
        "exactly as 'No agent without identity'"
    )
    # The commitment language should mention what an identity card needs.
    lower = text.lower()
    assert "owner" in lower
    assert "kill switch" in lower or "kill-switch" in lower
