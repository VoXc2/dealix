"""Fail-closed registration contract for the legacy autonomous router."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS_DOMAIN = (
    ROOT / "api" / "routers" / "domains" / "agents" / "__init__.py"
).read_text(encoding="utf-8")


def test_legacy_autonomous_router_is_not_production_registered() -> None:
    assert "    autonomous," not in AGENTS_DOMAIN
    assert "autonomous.router" not in AGENTS_DOMAIN
    assert "api.routers.autonomous remains deliberately unregistered" in AGENTS_DOMAIN
    assert "#1070" in AGENTS_DOMAIN


def test_registration_gate_names_the_required_evidence_boundaries() -> None:
    for boundary in ("authentication", "tenant", "policy", "evidence"):
        assert boundary in AGENTS_DOMAIN
