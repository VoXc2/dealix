"""Grounding score API."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_grounding_score() -> None:
    resp = client.post(
        "/api/v1/intelligence/grounding-score",
        json={"answer": "value [source: test]", "source_refs": ["ref1", "ref2"]},
    )
    assert resp.status_code == 200
    assert resp.json()["grounding_score"] >= 50
