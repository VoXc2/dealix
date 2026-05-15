"""API import smoke checks for enterprise release gates."""

from __future__ import annotations


def test_api_main_imports_without_errors() -> None:
    from api.main import app

    assert app is not None
