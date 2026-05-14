"""The Dealix Promise — public manifesto endpoint (Wave 17)."""
from __future__ import annotations

import os
from pathlib import Path

from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.governance_os.non_negotiables import NON_NEGOTIABLES

client = TestClient(app)
REPO = Path(__file__).resolve().parent.parent


def test_manifesto_endpoint_is_public_no_admin_key_required():
    """The manifesto IS the marketing surface — must be reachable without
    an admin key. Mirrors the public commercial-map pattern."""
    resp = client.get("/api/v1/dealix-promise")
    assert resp.status_code == 200
    body = resp.json()
    assert body["governance_decision"] == "allow"
    assert body["is_estimate"] is False


def test_manifesto_returns_eleven_commitments_with_required_fields():
    body = client.get("/api/v1/dealix-promise").json()
    assert body["commitments_count"] == 11
    assert len(body["commitments"]) == 11
    required = {
        "id", "title_en", "title_ar",
        "promise_en", "promise_ar",
        "refusal_en", "refusal_ar",
        "enforced_by",
    }
    for c in body["commitments"]:
        missing = required - set(c.keys())
        assert not missing, f"{c.get('id')} missing fields: {missing}"
        assert c["enforced_by"], f"{c['id']} must list at least one enforcer"


def test_every_commitment_enforcer_path_exists_on_disk():
    """If we publish a commitment as 'enforced by tests/test_x.py', that
    file MUST exist. The manifesto cannot reference vapor."""
    for n in NON_NEGOTIABLES:
        for rel in n.enforced_by:
            path = REPO / rel
            assert path.exists(), (
                f"non-negotiable {n.id!r} claims enforcement by {rel!r} "
                f"but the file does not exist on disk"
            )


def test_markdown_endpoint_is_bilingual_and_lists_all_commitments():
    resp = client.get("/api/v1/dealix-promise/markdown")
    assert resp.status_code == 200
    body = resp.text
    # Bilingual title + footer disclaimer
    assert "The Dealix Promise" in body
    assert "وعد Dealix" in body
    assert "Estimated outcomes are not guaranteed outcomes" in body
    assert "النتائج التقديرية ليست نتائج مضمونة" in body
    # Every commitment id appears as a code-quoted Commitment ID line
    for n in NON_NEGOTIABLES:
        assert f"`{n.id}`" in body, f"markdown missing commitment_id={n.id}"


def test_manifesto_does_not_use_guarantee_language():
    """Article 8 self-test: the manifesto talks about commitments, not
    guarantees. Words like 'guaranteed' / 'نضمن' must not appear in the
    promise/refusal text. The `no_guaranteed_outcomes` commitment is the
    one allowed mention (the rule is literally about that token, used in
    explicit negation)."""
    body = client.get("/api/v1/dealix-promise").json()
    forbidden = ("guaranteed", "guarantees", "نضمن")
    for c in body["commitments"]:
        if c["id"] == "no_guaranteed_outcomes":
            continue
        for field in ("promise_en", "promise_ar", "refusal_en", "refusal_ar"):
            text = c[field].lower() if field.endswith("en") else c[field]
            for tok in forbidden:
                assert tok not in text, (
                    f"{c['id']}.{field} contains forbidden token {tok!r}"
                )
