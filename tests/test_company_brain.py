"""Phase D — schema-level guarantees for the CompanyBrain module.

The module is now shipped at ``auto_client_acquisition.company_brain``.
This file tests its public API: that the build function returns a
typed result, that no LLM/network call happens, and that the
canonical guardrails are advertised.
"""
from __future__ import annotations

import importlib

import pytest


def _module_exists(dotted_name: str) -> bool:
    try:
        importlib.import_module(dotted_name)
        return True
    except ModuleNotFoundError:
        return False


COMPANY_BRAIN_MODULES = [
    "auto_client_acquisition.company_brain",
    "auto_client_acquisition.self_growth_os.company_brain",
    "core.brain.company_brain",
    "dealix.brain.company_brain",
]


def _find_company_brain_module() -> str | None:
    for name in COMPANY_BRAIN_MODULES:
        if _module_exists(name):
            return name
    return None


def test_company_brain_module_is_present():
    """The module must now exist at one of the canonical paths."""
    module = _find_company_brain_module()
    assert module is not None, (
        "CompanyBrain module not found at any of: "
        + ", ".join(COMPANY_BRAIN_MODULES)
    )


def test_company_brain_exposes_required_public_api():
    """Either a CompanyBrain class or a build_company_brain factory."""
    module_name = _find_company_brain_module()
    assert module_name is not None
    mod = importlib.import_module(module_name)
    cls = getattr(mod, "CompanyBrain", None)
    factory = getattr(mod, "build_company_brain", None)
    assert cls is not None and factory is not None, (
        f"{module_name} must expose both CompanyBrain class AND "
        "build_company_brain factory"
    )


def test_build_company_brain_returns_full_structure():
    from auto_client_acquisition.company_brain import (
        CompanyBrain,
        build_company_brain,
    )
    brain = build_company_brain()
    assert isinstance(brain, CompanyBrain)
    assert brain.company_name == "Dealix"
    assert brain.mission_ar
    assert brain.mission_en
    assert isinstance(brain.services_summary, dict)
    assert isinstance(brain.agents_summary, dict)
    assert isinstance(brain.current_priorities, list)
    assert brain.health_overall in {"ok", "degraded", "unavailable", "unknown"}


def test_company_brain_guardrails_re_asserted():
    from auto_client_acquisition.company_brain import build_company_brain
    g = build_company_brain().guardrails
    assert g["no_live_send"] is True
    assert g["no_scraping"] is True
    assert g["no_cold_outreach"] is True
    assert g["approval_required_for_external_actions"] is True


def test_company_brain_no_external_calls_in_test_path(monkeypatch):
    """Schema-level instantiation must NOT trigger any network call.
    We patch httpx.Client to raise loudly if anyone calls it; the
    build must complete without touching it."""
    try:
        import httpx  # noqa: F401
    except ImportError:
        pytest.skip("httpx not available — no need to assert")

    import httpx

    def _exploding_request(*args, **kwargs):
        raise AssertionError("CompanyBrain attempted a network call")

    monkeypatch.setattr(httpx.Client, "request", _exploding_request)
    monkeypatch.setattr(
        httpx.AsyncClient, "request", _exploding_request, raising=False,
    )

    from auto_client_acquisition.company_brain import build_company_brain
    brain = build_company_brain()
    assert brain is not None


def test_company_brain_router_endpoint_returns_200():
    """The /api/v1/company-brain router must serve the brain."""
    from fastapi.testclient import TestClient
    from api.main import create_app

    client = TestClient(create_app())

    resp = client.get("/api/v1/company-brain/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["module"] == "company_brain"
    assert body["guardrails"]["no_llm_calls"] is True

    resp = client.get("/api/v1/company-brain/")
    assert resp.status_code == 200
    body = resp.json()
    assert body["company_name"] == "Dealix"
    assert "guardrails" in body
