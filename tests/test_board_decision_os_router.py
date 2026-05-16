"""Board Decision OS router — smoke + contract tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.board_decision_os import (
    BOARD_MEMO_SECTIONS,
    RISK_REGISTER_CODES,
)

client = TestClient(app)


def test_overview_returns_taxonomy():
    r = client.get("/api/v1/board-decision-os/overview")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "board_decision_os"
    assert body["memo_section_count"] == len(BOARD_MEMO_SECTIONS)
    assert body["risk_count"] == len(RISK_REGISTER_CODES)
    assert body["capital_buckets"] == ["must_fund", "should_test", "hold", "kill"]
    assert body["hard_gates"]["no_live_send"] is True


def test_memo_flags_missing_sections():
    r = client.post(
        "/api/v1/board-decision-os/memo",
        json={"sections_present": ["executive_summary", "revenue_quality"]},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["complete"] is False
    assert "capital_allocation" in body["missing_sections"]


def test_memo_complete_when_all_sections_present():
    r = client.post(
        "/api/v1/board-decision-os/memo",
        json={"sections_present": list(BOARD_MEMO_SECTIONS)},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["complete"] is True
    assert body["missing_sections"] == []


def test_risks_maps_every_code_to_a_mitigation():
    r = client.get("/api/v1/board-decision-os/risks")
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == len(RISK_REGISTER_CODES)
    for row in body["risk_register"]:
        assert row["code"] in RISK_REGISTER_CODES
        assert row["mitigation_decision"], f"{row['code']} has no mitigation"


def test_capital_allocation_classifies_investments():
    r = client.get(
        "/api/v1/board-decision-os/capital-allocation",
        params={"investments": "proof_pack_generator,scraping_engine,unknown_thing"},
    )
    assert r.status_code == 200
    body = r.json()
    classified = {c["investment"]: c["bucket"] for c in body["classified"]}
    assert classified["proof_pack_generator"] == "must_fund"
    assert classified["scraping_engine"] == "kill"
    assert classified["unknown_thing"] is None


def test_capital_allocation_taxonomy_without_query():
    r = client.get("/api/v1/board-decision-os/capital-allocation")
    assert r.status_code == 200
    body = r.json()
    assert body["buckets"] == ["must_fund", "should_test", "hold", "kill"]
    assert body["classified"] == []
