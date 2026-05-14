"""Locking test: the public capital-assets endpoint MUST NOT leak PII /
client / pricing / evidence fields.

If a future change adds a forbidden field to the response, this test
fails — and the failure is what stops the change from shipping.
"""
from __future__ import annotations

import json
import re
from typing import Any

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.capital_assets import (
    PUBLIC_FORBIDDEN_FIELDS,
    router as capital_assets_router,
)


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(capital_assets_router)
    return TestClient(app)


def _flatten_keys(obj: Any) -> list[str]:
    keys: list[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            keys.append(str(k))
            keys.extend(_flatten_keys(v))
    elif isinstance(obj, list):
        for item in obj:
            keys.extend(_flatten_keys(item))
    return keys


def test_public_response_has_no_forbidden_field_names():
    body = _client().get("/api/v1/capital-assets/public").json()
    keys = set(_flatten_keys(body))
    leaked = keys & PUBLIC_FORBIDDEN_FIELDS
    assert not leaked, f"forbidden fields leaked into public projection: {leaked}"


def test_public_response_strips_forbidden_fields_even_when_present_in_source(
    tmp_path, monkeypatch
):
    """Even if a raw entry contains forbidden fields, the projection drops them."""
    index = tmp_path / "idx.json"
    index.write_text(json.dumps({
        "entries": [
            {
                "asset_type": "proof_example",
                "title": "safe-title",
                # All of these MUST be stripped by the projection:
                "client_id": "CL-001",
                "client_name": "Bank of Saudi",
                "evidence": "raw evidence with PII",
                "description": "secret commercial details",
                "price_sar": 25000,
                "email": "private@example.com",
                "git_author": "founder <founder@dealix.sa>",
            }
        ]
    }))
    monkeypatch.setattr("api.routers.capital_assets.CAPITAL_ASSET_INDEX", index)

    body = _client().get("/api/v1/capital-assets/public").json()
    keys = set(_flatten_keys(body))
    leaked = keys & PUBLIC_FORBIDDEN_FIELDS
    assert not leaked, f"forbidden fields leaked: {leaked}"

    # The safe title is allowed.
    assert body["recent_titles_safe"][0]["title_safe"] == "safe-title"


def _has_pii_pattern(text: str) -> bool:
    """Heuristic: detect email / Saudi phone / SAR-amount patterns."""
    email_rx = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
    phone_rx = re.compile(r"\+?966\d{8,9}")
    money_rx = re.compile(r"\d+\s*SAR", re.IGNORECASE)
    return bool(email_rx.search(text) or phone_rx.search(text) or money_rx.search(text))


def test_public_response_body_has_no_pii_substrings(tmp_path, monkeypatch):
    index = tmp_path / "idx.json"
    index.write_text(json.dumps({
        "entries": [
            {
                "asset_type": "proof_example",
                "title": "safe label",
                "client_name": "Bank of Saudi",
                "email": "private@example.com",
                "price_sar": 25000,
            }
        ]
    }))
    monkeypatch.setattr("api.routers.capital_assets.CAPITAL_ASSET_INDEX", index)

    r = _client().get("/api/v1/capital-assets/public")
    body_text = r.text
    assert "Bank of Saudi" not in body_text
    assert "private@example.com" not in body_text
    assert not _has_pii_pattern(body_text), f"PII pattern in body: {body_text!r}"
