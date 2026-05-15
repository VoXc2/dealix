"""API import health gates for enterprise control plane hardening."""

from __future__ import annotations


def test_api_main_imports_cleanly() -> None:
    from api.main import app

    assert app is not None
    assert len(app.routes) > 0
