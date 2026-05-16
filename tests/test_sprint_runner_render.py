"""Sprint render endpoints — /api/v1/sprint/render/*.

The render routes are pure formatting: they take the Proof Pack from a prior
/run response and never execute the Sprint again.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

_RUN_BODY = {
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


def _proof_pack() -> dict:
    """Run the Sprint once and return its Proof Pack for rendering."""
    run = client.post("/api/v1/sprint/run", json=_RUN_BODY)
    assert run.status_code == 200, run.text
    return run.json()["proof_pack"]


def test_render_markdown_returns_bilingual_proof_pack():
    r = client.post(
        "/api/v1/sprint/render/markdown",
        json={"customer_handle": "Acme Saudi", "proof_pack": _proof_pack()},
    )
    assert r.status_code == 200, r.text
    assert "Dealix Proof Pack" in r.text
    assert "Acme Saudi" in r.text
    assert "النتائج التقديرية ليست نتائج مضمونة" in r.text


def test_render_pdf_or_markdown_fallback():
    r = client.post(
        "/api/v1/sprint/render/pdf",
        json={"customer_handle": "Acme Saudi", "proof_pack": _proof_pack()},
    )
    assert r.status_code == 200, r.text
    if "application/pdf" in r.headers.get("content-type", ""):
        assert r.content[:5] == b"%PDF-"
    else:
        assert r.headers.get("X-PDF-Renderer", "").startswith("unavailable")
        assert "Dealix Proof Pack" in r.text


def test_render_email_body():
    r = client.post(
        "/api/v1/sprint/render/email-body",
        json={"customer_handle": "Acme Saudi", "proof_pack": _proof_pack()},
    )
    assert r.status_code == 200, r.text
    assert "Subject" in r.text
    assert "Acme Saudi" in r.text


def test_render_accepts_whole_run_response():
    """The full /run response can be posted back via the `run` field."""
    run = client.post("/api/v1/sprint/run", json=_RUN_BODY)
    assert run.status_code == 200
    r = client.post(
        "/api/v1/sprint/render/markdown",
        json={"customer_handle": "Acme Saudi", "run": run.json()},
    )
    assert r.status_code == 200, r.text
    assert "Dealix Proof Pack" in r.text


def test_render_empty_pack_is_honest_not_generated_notice():
    r = client.post(
        "/api/v1/sprint/render/markdown",
        json={"customer_handle": "Acme Saudi", "proof_pack": {}},
    )
    assert r.status_code == 200
    assert "not yet generated" in r.text.lower()


def test_render_pdf_sanitizes_engagement_id_in_header():
    """A CR/LF-bearing engagement_id must not inject extra response headers."""
    r = client.post(
        "/api/v1/sprint/render/pdf",
        json={
            "customer_handle": "Acme",
            "engagement_id": "evil\r\nX-Injected: 1",
            "proof_pack": _proof_pack(),
        },
    )
    assert r.status_code == 200
    cd = r.headers.get("content-disposition", "")
    assert "\r" not in cd and "\n" not in cd
    assert "x-injected" not in {k.lower() for k in r.headers}
