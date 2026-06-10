"""Phase 2 doctrine — top-level governance assertions touching the API."""
from __future__ import annotations

import os
import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.friction_log.store import (
    clear_for_test as clear_friction,
)
from auto_client_acquisition.value_os.value_ledger import (
    clear_for_test as clear_value_for_test,
)

ALLOWLIST = [
    "api.openai.com",
    "api.anthropic.com",
    "graph.facebook.com",
    "graph.whatsapp.com",
    "api.hubspot.com",
    "login.salesforce.com",
    "www.googleapis.com",
    "api.notion.com",
    "api.zoho.com",
    "sandbox.payment.com",
    "api.moyasar.com",
]
_SUSPICIOUS_NAMES = ("scraper", "crawler", "harvest")


@pytest.fixture(autouse=True)
def isolated_ledgers(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "friction.jsonl"))
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "value.jsonl"))
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "capital.jsonl"))
    for cid in ("acme", "doctrine_cust", "friction_doctrine"):
        try:
            clear_friction()
        except Exception:
            pass
        try:
            clear_value_for_test(cid)
        except Exception:
            pass
    yield


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def test_workspace_endpoint_emits_governance_decision(client: TestClient) -> None:
    resp = client.get("/api/v1/customer-portal/acme/workspace")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert "governance_decision" in body
    assert body["governance_decision"]


def test_value_verified_without_source_raises_at_router(client: TestClient) -> None:
    """POST /api/v1/value/event/{cid} with tier=verified, source_ref="" → 4xx."""
    resp = client.post(
        "/api/v1/value/event/acme",
        json={
            "kind": "revenue_uplift",
            "amount": 1000.0,
            "tier": "verified",
            "source_ref": "",
        },
    )
    assert resp.status_code in (400, 422), resp.text


def test_friction_log_sanitizes_pii_via_router(client: TestClient) -> None:
    """POST event with email in notes → GET events shows email stripped."""
    payload = {
        "customer_id": "friction_doctrine",
        "kind": "support_ticket",
        "severity": "low",
        "notes": "please contact me at attacker@example.com asap",
    }
    resp = client.post("/api/v1/friction-log/event", json=payload)
    assert resp.status_code in (200, 201), resp.text

    resp2 = client.get("/api/v1/friction-log/friction_doctrine/events")
    assert resp2.status_code == 200, resp2.text
    body = resp2.json()
    serialized = repr(body)
    assert "attacker@example.com" not in serialized


def test_monthly_markdown_contains_disclaimer_via_router(client: TestClient) -> None:
    resp = client.get("/api/v1/value/doctrine_cust/report/monthly/markdown")
    assert resp.status_code == 200, resp.text
    body = resp.text
    assert "## Limitations" in body
    assert "Estimated value is not Verified value" in body


def test_no_scraper_in_tree() -> None:
    """Duplicate of test_no_scraping_engine — runs at governance level for fail-fast."""
    repo_root = Path(__file__).resolve().parents[2]
    root = repo_root / "auto_client_acquisition"
    offenders: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for fname in filenames:
            if not fname.endswith(".py"):
                continue
            lower = fname.lower()
            if not any(s in lower for s in _SUSPICIOUS_NAMES):
                continue
            path = Path(dirpath) / fname
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if "requests.get(" not in text:
                continue
            urls = re.findall(r"https?://([A-Za-z0-9.\-]+)", text)
            non_allowed = [u for u in urls if u not in ALLOWLIST]
            if non_allowed:
                offenders.append(f"{path} -> {non_allowed}")
    assert not offenders, (
        "Forbidden scraping-style modules found:\n" + "\n".join(offenders)
    )
