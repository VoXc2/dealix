"""Full Ops 2.0 — GCC Governed AI Ops Pulse report."""
from __future__ import annotations

import json

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.media_os.gcc_pulse import build_gcc_pulse


def _records(n: int, **overrides) -> list[dict]:
    base = {
        "risk_category": "external_action",
        "workflow": "lead_reply_drafting",
        "has_evidence": True,
        "client_id": "client_x",
    }
    base.update(overrides)
    return [dict(base) for _ in range(n)]


# ── aggregation ──────────────────────────────────────────────────


def test_pulse_counts_risk_scores() -> None:
    pulse = build_gcc_pulse(_records(5), quarter="2026-Q2")
    assert pulse.risk_scores_count == 5
    assert pulse.quarter == "2026-Q2"


def test_pulse_most_frequent_risks() -> None:
    records = (
        _records(4, risk_category="external_action")
        + _records(3, risk_category="pii_exposure")
    )
    pulse = build_gcc_pulse(records, quarter="2026-Q2")
    top = pulse.most_frequent_risks
    assert top[0]["risk_category"] == "external_action"
    assert top[0]["count"] == 4


def test_pulse_most_requested_workflows() -> None:
    records = (
        _records(5, workflow="lead_reply_drafting")
        + _records(3, workflow="proof_pack_assembly")
    )
    pulse = build_gcc_pulse(records, quarter="2026-Q2")
    workflows = {w["workflow"]: w["count"] for w in pulse.most_requested_workflows}
    assert workflows["lead_reply_drafting"] == 5


def test_pulse_evidence_gaps() -> None:
    records = _records(3, workflow="auto_scoring", has_evidence=False)
    pulse = build_gcc_pulse(records, quarter="2026-Q2")
    gaps = {g["workflow"] for g in pulse.evidence_gaps}
    assert "auto_scoring" in gaps


def test_pulse_k_anonymity_withholds_small_groups() -> None:
    # Only 2 occurrences — below the default min_group_size of 3.
    records = _records(2, risk_category="rare_risk")
    pulse = build_gcc_pulse(records, quarter="2026-Q2")
    assert all(r["risk_category"] != "rare_risk" for r in pulse.most_frequent_risks)


def test_pulse_is_anonymized_no_client_ids_emitted() -> None:
    records = (
        _records(3, client_id="acme")
        + _records(3, client_id="beta")
    )
    pulse = build_gcc_pulse(records, quarter="2026-Q2")
    payload = pulse.to_dict()
    serialized = json.dumps(payload)
    # DOCTRINE — no client identifier leaks into the report body.
    assert "acme" not in serialized
    assert "beta" not in serialized
    assert pulse.distinct_clients == 2
    assert payload["anonymized"] is True


def test_pulse_includes_best_practices() -> None:
    pulse = build_gcc_pulse(_records(3), quarter="2026-Q2")
    assert len(pulse.best_practices) >= 3


# ── router ───────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_router_status() -> None:
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/media-os/status")
    assert r.status_code == 200
    assert r.json()["service"] == "media_os"


@pytest.mark.asyncio
async def test_router_gcc_pulse_aggregates_store(tmp_path, monkeypatch) -> None:
    from api.main import app

    path = tmp_path / "risk_scores.jsonl"
    rows = [
        json.dumps(
            {
                "risk_category": "external_action",
                "workflow": "lead_reply_drafting",
                "has_evidence": True,
                "client_id": "secret_client_abc",
            }
        )
        for _ in range(4)
    ]
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    monkeypatch.setenv("DEALIX_GOVERNANCE_RISK_SCORES_PATH", str(path))

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/media-os/gcc-pulse?quarter=2026-Q2")
    body = r.json()
    assert body["report"] == "gcc_governed_ai_ops_pulse"
    assert body["risk_scores_count"] == 4
    assert body["data_status"] == "live"
    # DOCTRINE — no client identifier in the response.
    assert "secret_client_abc" not in json.dumps(body)
    assert body["anonymized"] is True
