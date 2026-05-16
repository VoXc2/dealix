"""Sprint render endpoints — /api/v1/sprint/render/*."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

_BODY = {
    "engagement_id": "eng_render_1",
    "customer_id": "Acme Saudi",
    "raw_csv": (
        "company_name,sector,city,relationship_status\n"
        "Co,b2b_services,Riyadh,warm\n"
    ),
    "accounts": [
        {
            "company_name": "Co",
            "sector": "b2b_services",
            "city": "Riyadh",
            "relationship_status": "warm",
        }
    ],
    "problem_summary": "demo",
}


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "fr.jsonl"))
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "val.jsonl"))
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "cap.jsonl"))
    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    yield


def test_render_markdown_returns_bilingual_proof_pack():
    r = client.post("/api/v1/sprint/render/markdown", json=_BODY)
    assert r.status_code == 200, r.text
    assert "Dealix Proof Pack" in r.text
    assert "Acme Saudi" in r.text
    assert "النتائج التقديرية ليست نتائج مضمونة" in r.text


def test_render_pdf_or_markdown_fallback():
    r = client.post("/api/v1/sprint/render/pdf", json=_BODY)
    assert r.status_code == 200, r.text
    if "application/pdf" in r.headers.get("content-type", ""):
        assert r.content[:5] == b"%PDF-"
    else:
        assert r.headers.get("X-PDF-Renderer", "").startswith("unavailable")
        assert "Dealix Proof Pack" in r.text


def test_render_email_body():
    r = client.post("/api/v1/sprint/render/email-body", json=_BODY)
    assert r.status_code == 200, r.text
    assert "Subject" in r.text
    assert "Acme Saudi" in r.text
