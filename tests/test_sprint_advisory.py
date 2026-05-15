"""Optional AI advisory layer for the Sprint — opt-in, governance-gated.

``route_task`` is monkeypatched to a fake — zero network calls. These tests
lock the doctrine: deterministic output is unchanged when advisory is OFF,
and every AI draft passes the governance gate.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.delivery_factory.delivery_sprint import run_sprint

client = TestClient(app)

_CSV = (
    "company_name,sector,city,relationship_status,last_interaction,notes\n"
    "شركة الواحة,b2b_services,Riyadh,warm,2026-04-12,clean fit\n"
    "Madar Logistics,logistics,Jeddah,warm,2026-04-22,past pilot\n"
)
_ACCOUNTS = [
    {
        "company_name": "Co1",
        "sector": "b2b_services",
        "city": "Riyadh",
        "relationship_status": "warm",
        "last_interaction": "2026-05",
        "notes": "fit",
    },
    {"company_name": "Co2", "sector": "logistics", "city": "Jeddah", "relationship_status": "cold"},
]
_PASSPORT = {
    "source_id": "SRC-ADV-1",
    "source_type": "client_upload",
    "owner": "client",
    "allowed_use": ("internal_analysis", "scoring"),
    "contains_pii": False,
    "sensitivity": "low",
    "ai_access_allowed": True,
    "external_use_allowed": False,
    "retention_policy": "project_duration",
}


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "fr.jsonl"))
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "val.jsonl"))
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "cap.jsonl"))
    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    monkeypatch.delenv("DEALIX_AI_ADVISORY", raising=False)
    yield


def _fake_decision(text: str, status: str = "ok_cloud"):
    return SimpleNamespace(
        status=status,
        text=text,
        confidence=SimpleNamespace(level="high", score=0.8),
        backend_used="cloud:anthropic",
        fallback_reasons=(),
        estimated_cost_usd=0.012,
    )


def _patch_route_task(monkeypatch, decision):
    monkeypatch.setattr(
        "auto_client_acquisition.intelligence.dealix_model_router.route_task",
        lambda task, **kw: decision,
    )


def _step(run, name):
    return next(s for s in run.steps if s.name == name)


def test_run_sprint_default_has_no_advisory():
    """Opt-in contract: with ai_advisory OFF, no advisory sub-object appears."""
    run = run_sprint(
        engagement_id="e1",
        customer_id="c1",
        source_passport=_PASSPORT,
        raw_csv=_CSV,
        accounts=_ACCOUNTS,
    )
    assert run.ai_advisory is False
    assert "advisory" not in _step(run, "account_scoring").output
    assert "advisory" not in _step(run, "draft_pack_outline").output


def test_advisory_on_attaches_governed_advisory(monkeypatch):
    _patch_route_task(
        monkeypatch,
        _fake_decision("فقرة تحليلية آمنة تشرح منطق الترتيب دون أي وعود."),
    )
    run = run_sprint(
        engagement_id="e2",
        customer_id="c2",
        source_passport=_PASSPORT,
        raw_csv=_CSV,
        accounts=_ACCOUNTS,
        ai_advisory=True,
    )
    assert run.ai_advisory is True

    s3_adv = _step(run, "account_scoring").output["advisory"]
    assert s3_adv["status"] == "advisory_draft"
    assert s3_adv["awaiting"] == "founder_approval"

    s4_adv = _step(run, "draft_pack_outline").output["advisory"]
    assert s4_adv["status"] == "advisory_draft"
    assert s4_adv["drafts"], "expected at least one advisory draft"
    for d in s4_adv["drafts"]:
        # Every advisory draft carries a governance verdict written by step 5.
        assert d["governance"] is not None
        assert d["surfaced"] is True  # benign text → allowed


def test_advisory_draft_with_forbidden_claim_not_surfaced(monkeypatch):
    """An AI draft with a guaranteed-revenue claim must be BLOCKed, not surfaced."""
    _patch_route_task(monkeypatch, _fake_decision("we guarantee 100% sales for you"))
    run = run_sprint(
        engagement_id="e3",
        customer_id="c3",
        source_passport=_PASSPORT,
        raw_csv=_CSV,
        accounts=_ACCOUNTS,
        ai_advisory=True,
    )
    s4_adv = _step(run, "draft_pack_outline").output["advisory"]
    for d in s4_adv["drafts"]:
        assert d["surfaced"] is False
        assert d["governance"]["decision"] == "BLOCK"
    # The rationale self-check also blocks the forbidden claim.
    assert _step(run, "account_scoring").output["advisory"]["status"] == "advisory_blocked"


def test_advisory_unavailable_when_router_degrades(monkeypatch):
    """Router degradation → advisory_unavailable; deterministic output intact."""
    _patch_route_task(monkeypatch, _fake_decision("", status="degraded_to_human"))
    run = run_sprint(
        engagement_id="e4",
        customer_id="c4",
        source_passport=_PASSPORT,
        raw_csv=_CSV,
        accounts=_ACCOUNTS,
        ai_advisory=True,
    )
    s3 = _step(run, "account_scoring").output
    assert s3["advisory"]["status"] == "advisory_unavailable"
    # Deterministic ranking is untouched — AI never reorders.
    assert [a["rank"] for a in s3["top_10"]] == list(range(1, len(s3["top_10"]) + 1))
    assert s3["top_10"][0]["company_name"] == "Co1"


def test_env_flag_forces_advisory_on(monkeypatch):
    monkeypatch.setenv("DEALIX_AI_ADVISORY", "1")
    _patch_route_task(monkeypatch, _fake_decision("فقرة آمنة."))
    run = run_sprint(
        engagement_id="e5",
        customer_id="c5",
        source_passport=_PASSPORT,
        raw_csv=_CSV,
        accounts=_ACCOUNTS,
    )
    assert run.ai_advisory is True
    assert "advisory" in _step(run, "account_scoring").output


def test_sprint_endpoint_ai_advisory_flag(monkeypatch):
    _patch_route_task(monkeypatch, _fake_decision("فقرة تحليلية آمنة."))
    resp = client.post(
        "/api/v1/sprint/run",
        json={
            "engagement_id": "eng_adv",
            "customer_id": "cust_adv",
            "raw_csv": _CSV,
            "accounts": [
                {
                    "company_name": "Co1",
                    "sector": "b2b_services",
                    "city": "Riyadh",
                    "relationship_status": "warm",
                },
            ],
            "ai_advisory": True,
        },
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["ai_advisory"] is True
    steps = {s["name"]: s for s in body["steps"]}
    assert "advisory" in steps["account_scoring"]["output"]
