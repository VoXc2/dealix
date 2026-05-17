"""Tests for the support ticketing backend (PR3)."""

from __future__ import annotations

import pytest

from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.evidence_control_plane_os.event_store import (
    list_evidence_events,
    reset_default_evidence_ledger,
)
from auto_client_acquisition.knowledge.article_store import (
    KnowledgeArticle,
    get_default_article_store,
    reset_default_article_store,
)
from auto_client_acquisition.knowledge.gaps import reset_default_gap_store
from auto_client_acquisition.support import (
    create_ticket,
    draft_reply,
    request_send_reply,
    resolve_ticket,
)
from auto_client_acquisition.support.ticket_store import (
    get_default_ticket_store,
    reset_default_ticket_store,
)


@pytest.fixture
def support_env(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_SUPPORT_DIR", str(tmp_path / "support"))
    monkeypatch.setenv("DEALIX_KNOWLEDGE_DIR", str(tmp_path / "kb"))
    monkeypatch.setenv("DEALIX_EVIDENCE_LEDGER_DIR", str(tmp_path / "ev"))
    reset_default_ticket_store()
    reset_default_article_store()
    reset_default_gap_store()
    reset_default_evidence_ledger()
    get_default_approval_store().clear()
    yield
    reset_default_ticket_store()
    reset_default_article_store()
    reset_default_gap_store()
    reset_default_evidence_ledger()
    get_default_approval_store().clear()


def _approved_article(**kw):
    store = get_default_article_store()
    art = store.create(KnowledgeArticle(**kw))
    return store.set_status(art.article_id, "approved")


# ─── Create + classify ───────────────────────────────────────────


def test_create_ticket_persists_and_classifies(support_env):
    tkt = create_ticket(subject="Help", message="How do I get started onboarding?")
    assert get_default_ticket_store().get(tkt.ticket_id) is not None
    assert tkt.category != ""
    assert tkt.sla_due_at is not None


def test_create_ticket_writes_evidence(support_env):
    tkt = create_ticket(subject="x", message="how do I get started")
    events = list_evidence_events(entity_type="support_ticket", entity_id=tkt.ticket_id)
    assert any(e.event_type == "support_ticket_created" for e in events)


# ─── Draft from KB ───────────────────────────────────────────────


def test_draft_reply_uses_kb_for_low_risk(support_env):
    _approved_article(
        slug="getting-started",
        title_en="getting started onboarding guide",
        body_en="Start by completing the diagnostic form.",
    )
    tkt = create_ticket(subject="getting started",
                        message="how do I get started onboarding")
    result = draft_reply(tkt.ticket_id)
    assert result["drafted"] is True
    assert result["escalated"] is False
    assert result["kb_article_ids"]

    refreshed = get_default_ticket_store().get(tkt.ticket_id)
    assert refreshed.suggested_reply.startswith("Start by")


def test_draft_reply_escalates_when_kb_empty(support_env):
    tkt = create_ticket(subject="weird question",
                        message="how do I get started onboarding")
    result = draft_reply(tkt.ticket_id)
    assert result["drafted"] is False
    assert result["escalated"] is True
    assert get_default_ticket_store().get(tkt.ticket_id).status == "escalated"


# ─── Send reply is approval-gated ────────────────────────────────


def test_send_reply_requires_approval(support_env):
    tkt = create_ticket(subject="x", message="how do I get started")
    result = request_send_reply(tkt.ticket_id)
    assert result["sent"] is False
    assert result["approval_status"] == "approval_required"

    pending = get_default_approval_store().list_pending()
    assert any(p.object_id == tkt.ticket_id for p in pending)


# ─── Resolve ─────────────────────────────────────────────────────


def test_resolve_ticket(support_env):
    tkt = create_ticket(subject="x", message="how do I get started")
    resolved = resolve_ticket(tkt.ticket_id)
    assert resolved.status == "resolved"
    assert resolved.resolved_at is not None


# ─── Router ──────────────────────────────────────────────────────


async def test_support_router_full_flow(support_env, async_client):
    resp = await async_client.post(
        "/api/v1/support/tickets",
        json={"subject": "help", "message": "how do I get started onboarding"},
    )
    assert resp.status_code == 200
    ticket_id = resp.json()["ticket_id"]

    draft = await async_client.post(
        f"/api/v1/support/tickets/{ticket_id}/draft-response"
    )
    assert draft.status_code == 200

    send = await async_client.post(
        f"/api/v1/support/tickets/{ticket_id}/send-reply"
    )
    assert send.json()["approval_status"] == "approval_required"


async def test_support_router_status(support_env, async_client):
    resp = await async_client.get("/api/v1/support/tickets/status")
    assert resp.status_code == 200
    assert resp.json()["guardrails"]["support_never_sends"] is True
