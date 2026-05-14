"""Locking test: the PUBLIC variant MUST NOT leak counts or rationale.

This is the doctrine moat for PR6. The public endpoint exists so a
prospect / partner / regulator can confirm Dealix's recommendation
without seeing internal operating data.
"""
from __future__ import annotations

import re

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.customer_readiness_gate import router as readiness_router


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(readiness_router)
    return TestClient(app)


# Field names that MUST NOT appear in the public response.
PUBLIC_FORBIDDEN = (
    "governance_decisions_7d",
    "proof_pack_count",
    "capital_asset_count",
    "rationale",
    "source_passport_status",
    "has_signed_scope",
)


def _flatten_keys(obj):
    keys = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            keys.append(str(k))
            keys.extend(_flatten_keys(v))
    elif isinstance(obj, list):
        for item in obj:
            keys.extend(_flatten_keys(item))
    return keys


def test_public_response_keys_are_minimal():
    body = _client().get("/api/v1/customer/demo-proceed/readiness/public").json()
    assert set(body.keys()) == {"handle", "recommendation", "as_of", "doctrine"}


def test_public_response_has_no_forbidden_field_names():
    body = _client().get("/api/v1/customer/demo-proceed/readiness/public").json()
    leaked = set(_flatten_keys(body)) & set(PUBLIC_FORBIDDEN)
    assert not leaked, f"public projection leaks: {leaked}"


def test_public_response_has_no_numeric_count_values():
    """The body text must not contain numeric strings that could be a
    count (1, 12, 42, etc.). We check that none of the small integers
    a real customer-state would emit appear in the response text.
    """
    body = _client().get("/api/v1/customer/demo-proceed/readiness/public").text
    # Strip the as_of timestamp (it contains digits legitimately).
    body_no_timestamp = re.sub(r'"as_of"\s*:\s*"[^"]+"', '"as_of":"<stripped>"', body)
    # Then no integers >= 0 should survive that aren't part of structure.
    assert not re.search(r"\b\d+\b", body_no_timestamp), (
        f"public response has bare integers (possible count leak):\n{body_no_timestamp}"
    )


def test_public_response_recommendation_matches_admin():
    """Recommendation in public response equals recommendation in admin."""
    admin = _client().get("/api/v1/customer/demo-hold-governance/readiness").json()
    public = _client().get("/api/v1/customer/demo-hold-governance/readiness/public").json()
    assert public["recommendation"] == admin["recommendation"]
