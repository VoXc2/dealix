"""Enterprise Control Plane — API import + router registration smoke.

Check #1 of the verify contract: the FastAPI app imports without error
and the control-plane-relevant routers are registered.
"""

from __future__ import annotations


def test_app_imports_without_error():
    from api.main import app

    assert app is not None
    assert len(app.routes) > 100


def test_control_plane_routers_registered():
    """The routers the Control Plane / proof flow depends on are wired."""
    from api.main import app

    paths = {getattr(r, "path", "") for r in app.routes}
    # Spot-check one path per relevant surface.
    expected_prefixes = (
        "/api/v1/agents",          # Agent OS
        "/api/v1/approvals",       # Approval Center
        "/api/v1/value",           # Value OS
        "/api/v1/data-os",         # Data OS (Source Passport gate)
        "/api/v1/self-improvement-os",  # Self-evolving (suggest-only)
    )
    for prefix in expected_prefixes:
        assert any(p.startswith(prefix) for p in paths), f"missing routes for {prefix}"


def test_runtime_decision_decide_importable():
    """``decide()`` — the runtime governance entrypoint — is importable."""
    from auto_client_acquisition.governance_os.runtime_decision import (
        RuntimeDecision,
        decide,
    )

    result = decide(action="read_internal_docs")
    assert isinstance(result, RuntimeDecision)
    assert result.decision.value == "ALLOW"
