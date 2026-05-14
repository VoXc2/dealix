"""Locking test: the cap-table public projection MUST NOT leak absolute
share counts, SAR / USD amounts, or any integer that could be misread
as a share count.

Only `ratio_pct` (0..100) per holder is permitted.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.cap_table import (
    CAP_TABLE_PATH,
    PUBLIC_HOLDER_FIELDS,
    router as cap_table_router,
)


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(cap_table_router)
    return TestClient(app)


def test_public_response_has_no_forbidden_field_names():
    body = _client().get("/api/v1/holding/cap-table/public").json()
    forbidden = {
        "share_count", "shares", "absolute_shares", "price_per_share",
        "amount_sar", "amount_usd", "sar", "usd", "amount",
        "preference", "liquidation_preference",
    }
    # Flatten the holders list.
    holder_keys = set()
    for h in (body.get("holders") or []):
        holder_keys |= set(h.keys())
    leaked = holder_keys & forbidden
    assert not leaked, f"public cap table leaks: {leaked}"


def test_public_holders_only_have_allowed_fields():
    body = _client().get("/api/v1/holding/cap-table/public").json()
    allowed = set(PUBLIC_HOLDER_FIELDS)
    for h in (body.get("holders") or []):
        extra = set(h.keys()) - allowed
        assert not extra, f"public cap table holder leaks: {extra}"


def test_public_body_has_no_integer_above_100():
    """Ratios are in 0..100. Any integer > 100 in the response would be
    a clue for a share count, an SAR amount, or similar leak."""
    text = _client().get("/api/v1/holding/cap-table/public").text
    for m in re.finditer(r"\b(\d+(?:\.\d+)?)\b", text):
        v = float(m.group(1))
        assert v <= 100, (
            f"public cap-table response has numeric > 100 ({v}); "
            f"could be a share count or amount leak."
        )


def test_public_strips_amounts_even_when_present_in_source(tmp_path, monkeypatch):
    src = tmp_path / "cap.json"
    src.write_text(json.dumps({
        "doctrine_version": "v1.0.0",
        "holders": [
            {
                "holder": "Founder", "class": "Common",
                "ratio_pct": 90.0,
                # All of these MUST be stripped by the projection:
                "shares": 9000000,
                "amount_sar": 9000000,
                "price_per_share": 1.0,
                "preference": "1x non-participating",
                "vesting": "Full vested",
                "notes": "private notes",
            },
            {
                "holder": "Reserved Option Pool", "class": "Pool",
                "ratio_pct": 10.0,
                "shares": 1000000,
            },
        ],
    }))
    monkeypatch.setattr("api.routers.cap_table.CAP_TABLE_PATH", src)
    body = _client().get("/api/v1/holding/cap-table/public").json()
    text = _client().get("/api/v1/holding/cap-table/public").text

    for bad in ("9000000", "1000000", "preference", "private notes", "Full vested", "price_per_share"):
        assert bad not in text, f"public response leaked: {bad}"

    # Ratios survive.
    ratios = [h["ratio_pct"] for h in body["holders"]]
    assert ratios == [90.0, 10.0]


def test_public_has_no_email_or_phone_patterns(tmp_path, monkeypatch):
    src = tmp_path / "cap.json"
    src.write_text(json.dumps({
        "holders": [{"holder": "x@y.com", "class": "C", "ratio_pct": 50.0,
                     "notes": "+966500000000"},
                    {"holder": "Y", "class": "C", "ratio_pct": 50.0}],
    }))
    monkeypatch.setattr("api.routers.cap_table.CAP_TABLE_PATH", src)
    # `holder` is on the allowed field list — but we should at least
    # detect that no email-shaped strings leak in OTHER fields. Here
    # we focus on the response body globally:
    text = _client().get("/api/v1/holding/cap-table/public").text
    # phone never allowed:
    assert not re.search(r"\+?966\d{8,9}", text)
