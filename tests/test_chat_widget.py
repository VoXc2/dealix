"""Tests for the customer-facing chat widget (PR9)."""

from __future__ import annotations

import pytest

from auto_client_acquisition.chat import respond
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
from auto_client_acquisition.support.ticket_store import (
    get_default_ticket_store,
    reset_default_ticket_store,
)


@pytest.fixture
def chat_env(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_KNOWLEDGE_DIR", str(tmp_path / "kb"))
    monkeypatch.setenv("DEALIX_SUPPORT_DIR", str(tmp_path / "support"))
    monkeypatch.setenv("DEALIX_EVIDENCE_LEDGER_DIR", str(tmp_path / "ev"))
    reset_default_article_store()
    reset_default_gap_store()
    reset_default_ticket_store()
    reset_default_evidence_ledger()
    yield
    reset_default_article_store()
    reset_default_gap_store()
    reset_default_ticket_store()
    reset_default_evidence_ledger()


def _approved(**kw):
    store = get_default_article_store()
    art = store.create(KnowledgeArticle(**kw))
    return store.set_status(art.article_id, "approved")


def test_chat_answers_from_approved_kb(chat_env):
    _approved(
        slug="pricing",
        title_en="sprint pricing cost",
        body_en="The Revenue Intelligence Sprint costs 499 SAR.",
    )
    result = respond("what is the sprint pricing cost")
    assert result["answered"] is True
    assert result["escalated"] is False
    assert "499" in result["answer_en"]
    assert result["citations"]


def test_chat_escalates_when_no_kb_match(chat_env):
    result = respond("can you integrate with our legacy mainframe system")
    assert result["answered"] is False
    assert result["escalated"] is True
    assert result["ticket_id"].startswith("tkt_")

    # A real support ticket must have been created.
    assert get_default_ticket_store().get(result["ticket_id"]) is not None


def test_chat_writes_evidence(chat_env):
    respond("a question with no answer in the kb")
    events = list_evidence_events(entity_type="chat")
    assert any(e.event_type == "chat_escalated" for e in events)


async def test_public_chat_endpoint(chat_env, async_client):
    resp = await async_client.post(
        "/api/v1/public/chat/message", json={"message": "how does this work"}
    )
    assert resp.status_code == 200
    assert "answered" in resp.json()


async def test_public_chat_requires_message(chat_env, async_client):
    resp = await async_client.post("/api/v1/public/chat/message", json={})
    assert resp.status_code == 422
