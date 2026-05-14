"""Tests for the public /api/v1/dealix-promise endpoint."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.dealix_promise import router as dealix_promise_router


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(dealix_promise_router)
    return TestClient(app)


def test_dealix_promise_returns_eleven_commitments():
    r = _client().get("/api/v1/dealix-promise")
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 11
    assert len(body["commitments"]) == 11
    numbers = sorted(c["number"] for c in body["commitments"])
    assert numbers == list(range(1, 12))


def test_dealix_promise_each_commitment_links_to_a_test():
    body = _client().get("/api/v1/dealix-promise").json()
    for c in body["commitments"]:
        assert c["verified_by"], f"commitment {c['number']} missing verified_by"
        assert (
            c["verified_by"].startswith("tests/")
            or c["verified_by"].startswith("scripts/")
        )


def test_dealix_promise_has_expected_titles():
    body = _client().get("/api/v1/dealix-promise").json()
    titles = [c["title"] for c in body["commitments"]]
    assert "Source Passport before AI use" in titles
    assert "No scraping" in titles
    assert "No cold WhatsApp" in titles
    assert "Capital Asset registration before invoice" in titles
    assert "Verifiable, not merely trusted" in titles


def test_dealix_promise_exposes_verification_pointers():
    body = _client().get("/api/v1/dealix-promise").json()
    v = body["verification"]
    assert v["master_verifier"] == "scripts/verify_all_dealix.py"
    assert "verifier-report.json" in v["machine_readable_state"]


def test_dealix_promise_is_public_no_auth_required():
    # No Authorization header — should still succeed.
    r = _client().get("/api/v1/dealix-promise")
    assert r.status_code == 200
