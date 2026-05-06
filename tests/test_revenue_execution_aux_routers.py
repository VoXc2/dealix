"""Auxiliary OS-mode routers wired in main."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app


def test_growth_os_mode_status() -> None:
    c = TestClient(create_app())
    r = c.get("/api/v1/growth-os/status")
    assert r.status_code == 200
    assert r.json()["delegate"] == "growth_v10"


def test_sales_os_pilot_draft() -> None:
    c = TestClient(create_app())
    r = c.post("/api/v1/sales-os/pilot-offer-draft", json={"sector": "b2b_services", "company": "TestCo"})
    assert r.status_code == 200
    assert r.json()["pilot_price_sar"] == 499


def test_partnership_fit_score() -> None:
    c = TestClient(create_app())
    r = c.post("/api/v1/partnership-os/fit-score", json={"partner_type": "agency"})
    assert r.status_code == 200
    assert r.json()["fit_score"] == 70


def test_executive_os_weekly_pack() -> None:
    c = TestClient(create_app())
    r = c.get("/api/v1/executive-os/weekly-pack")
    assert r.status_code == 200
    body = r.json()
    assert "week_label" in body
    assert "guardrails" in body


def test_self_improvement_weekly_learning_insufficient() -> None:
    c = TestClient(create_app())
    r = c.get("/api/v1/self-improvement-os/weekly-learning")
    assert r.status_code == 200
    assert r.json().get("status") in {"insufficient_data", "ok"}


def test_observability_v12_status() -> None:
    c = TestClient(create_app())
    r = c.get("/api/v1/observability-v12/status")
    assert r.status_code == 200
    assert r.json()["delegate"] == "observability_v10"


def test_customer_success_os_status() -> None:
    c = TestClient(create_app())
    r = c.get("/api/v1/customer-success/customer-success-os/status")
    assert r.status_code == 200
    assert r.json()["module"] == "customer_success_os"
