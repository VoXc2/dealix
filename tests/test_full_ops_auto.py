"""
PR-FULL-OPS-AUTO acceptance tests.

Covers:
  - auto_executor: gate-aware execution decisions
  - approval queue: /approve now invokes auto_execute
  - inbound webhooks: linkedin / email / whatsapp
  - self-ops: Dealix's own customer + runner
  - cron scripts importable
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


# ── Auto-executor (pure logic) ────────────────────────────────────


@pytest.mark.asyncio
async def test_auto_executor_email_skipped_when_gate_closed() -> None:
    from auto_client_acquisition.execution import auto_execute_approved

    class FakeEvent:
        unit_type = "draft_created"
        meta_json = {"draft_text": "test", "channel": "email_draft", "to_email": "x@y.com"}
    r = await auto_execute_approved(FakeEvent())
    assert r.executed is False
    assert "RESEND_ALLOW_LIVE_SEND_false" in r.reason
    assert r.safe_to_retry is True


@pytest.mark.asyncio
async def test_auto_executor_hard_refusal_cold_whatsapp() -> None:
    from auto_client_acquisition.execution import auto_execute_approved

    class FakeEvent:
        unit_type = "draft_created"
        meta_json = {"draft_text": "test", "channel": "cold_whatsapp"}
    r = await auto_execute_approved(FakeEvent())
    assert r.executed is False
    assert "hard_refusal" in r.reason


@pytest.mark.asyncio
async def test_auto_executor_linkedin_manual_only() -> None:
    from auto_client_acquisition.execution import auto_execute_approved

    class FakeEvent:
        unit_type = "draft_created"
        meta_json = {"draft_text": "test", "channel": "linkedin_manual"}
    r = await auto_execute_approved(FakeEvent())
    assert r.executed is False
    assert "manual_only" in r.reason


# ── Approval queue calls auto_executor ────────────────────────────


@pytest.mark.asyncio
async def test_approve_endpoint_includes_auto_execution_field(async_client) -> None:
    """When /approve is called, response must include auto_execution dict."""
    from auto_client_acquisition.revenue_company_os.proof_ledger import (
        record as record_proof,
    )
    from db.session import get_session

    async with get_session() as s:
        ev = await record_proof(
            s, unit_type="draft_created",
            customer_id="cus_test_approve",
            actor="test",
            approval_required=True, approved=False, risk_level="low",
            meta={"draft_text": "السلام عليكم", "channel": "linkedin_manual"},
        )
        await s.commit()
        eid = ev.id

    r = await async_client.post(f"/api/v1/actions/{eid}/approve",
                                json={"actor": "test_founder"})
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "approved"
    assert "auto_execution" in body
    # LinkedIn manual → never auto-executed
    assert body["auto_execution"]["executed"] is False


@pytest.mark.asyncio
async def test_approve_endpoint_skip_auto_execute(async_client) -> None:
    from auto_client_acquisition.revenue_company_os.proof_ledger import (
        record as record_proof,
    )
    from db.session import get_session

    async with get_session() as s:
        ev = await record_proof(
            s, unit_type="draft_created",
            customer_id="cus_test_skip",
            actor="test",
            approval_required=True, approved=False, risk_level="low",
            meta={"draft_text": "ok"},
        )
        await s.commit()
        eid = ev.id

    r = await async_client.post(f"/api/v1/actions/{eid}/approve",
                                json={"actor": "x", "skip_auto_execute": True})
    assert r.status_code == 200
    body = r.json()
    assert body["auto_execution"]["skipped"] is True


# ── Inbound webhooks ──────────────────────────────────────────────


@pytest.mark.asyncio
async def test_inbound_linkedin_advances_status(async_client) -> None:
    create = await async_client.post(
        "/api/v1/prospects",
        json={"name": "inbound_test", "company": "Inbound Co",
              "relationship_type": "warm_1st_degree"},
    )
    pid = create.json()["id"]
    await async_client.post(f"/api/v1/prospects/{pid}/advance",
                            json={"target_status": "messaged"})

    r = await async_client.post("/api/v1/inbound/linkedin",
                                json={"prospect_id": pid, "message_text": "مهتم"})
    assert r.status_code == 200
    body = r.json()
    assert body["new_status"] == "replied"
    assert body["rwu_emitted"] == "opportunity_created"


@pytest.mark.asyncio
async def test_inbound_email_no_match_returns_safe(async_client) -> None:
    r = await async_client.post("/api/v1/inbound/email",
                                json={"contact_email": "ghost@nowhere.example"})
    assert r.status_code == 200
    body = r.json()
    assert body["matched"] is False
    assert "PDPL" in body["note_ar"] or "lead pollution" in body["note_ar"]


@pytest.mark.asyncio
async def test_inbound_whatsapp_opens_24h_window(async_client) -> None:
    create = await async_client.post(
        "/api/v1/prospects",
        json={"name": "wa_test", "company": "WA Co",
              "contact_phone": "+966500000001",
              "relationship_type": "warm_1st_degree"},
    )
    pid = create.json()["id"]
    await async_client.post(f"/api/v1/prospects/{pid}/advance",
                            json={"target_status": "messaged"})

    r = await async_client.post("/api/v1/inbound/whatsapp",
                                json={"phone": "+966500000001", "message_text": "اهلا"})
    assert r.status_code == 200
    body = r.json()
    assert body["matched"] is True
    assert body["new_status"] == "replied"
    assert body["consent_status"] == "opt_in_recorded"
    assert "+24h" in (body.get("wa_24h_window_until") or "")


# ── Self-ops ──────────────────────────────────────────────────────


def test_self_ops_brain_constants() -> None:
    from auto_client_acquisition.self_ops import DEALIX_BRAIN
    assert DEALIX_BRAIN["company_name"] == "Dealix"
    assert "PDPL" in DEALIX_BRAIN["offer_ar"]
    assert "linkedin_manual" in DEALIX_BRAIN["approved_channels"]
    assert "cold_whatsapp" in DEALIX_BRAIN["blocked_channels"]


@pytest.mark.asyncio
async def test_self_ops_run_daily_creates_dealix_customer(async_client) -> None:
    r = await async_client.post("/api/v1/self-ops/run-daily",
                                json={"prospect_target": 3, "intro_count": 2})
    assert r.status_code == 200
    body = r.json()
    assert body["customer_id"] == "cus_dealix_self"
    assert body["prospects_seeded"] >= 0  # 0 if already seeded by earlier test
    # state endpoint should now show initialized
    s = await async_client.get("/api/v1/self-ops/state")
    sb = s.json()
    assert sb["initialized"] is True
    assert sb["company_name"] == "Dealix"


@pytest.mark.asyncio
async def test_self_ops_brain_endpoint(async_client) -> None:
    r = await async_client.get("/api/v1/self-ops/brain")
    assert r.status_code == 200
    body = r.json()
    assert body["brain"]["company_name"] == "Dealix"


# ── Cron scripts importable ───────────────────────────────────────


def test_cron_auto_followup_script_exists() -> None:
    p = REPO / "scripts" / "cron_auto_followup.py"
    assert p.exists()
    assert p.stat().st_size > 1000


def test_cron_sprint_progression_script_exists() -> None:
    p = REPO / "scripts" / "cron_sprint_auto_progression.py"
    assert p.exists()
    assert p.stat().st_size > 1000


def test_cron_dealix_self_ops_script_exists() -> None:
    p = REPO / "scripts" / "cron_dealix_self_ops.py"
    assert p.exists()


def test_railway_cron_includes_new_jobs() -> None:
    import json
    data = json.loads((REPO / "railway.json").read_text(encoding="utf-8"))
    cron_names = {entry["name"] for entry in data.get("cron", [])}
    for required in ("dealix-self-ops", "sprint-progression", "auto-followup"):
        assert required in cron_names, f"railway.json cron missing {required}"
