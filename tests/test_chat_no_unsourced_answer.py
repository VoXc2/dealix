"""Non-negotiable guard: the chat widget never answers without an
approved KB source. No match → escalation only, never an improvised
answer (PR9)."""

from __future__ import annotations

import pytest

from auto_client_acquisition.chat import respond
from auto_client_acquisition.evidence_control_plane_os.event_store import (
    reset_default_evidence_ledger,
)
from auto_client_acquisition.knowledge.article_store import (
    KnowledgeArticle,
    get_default_article_store,
    reset_default_article_store,
)
from auto_client_acquisition.knowledge.gaps import reset_default_gap_store
from auto_client_acquisition.support.ticket_store import reset_default_ticket_store


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


def test_no_kb_means_no_answer(chat_env):
    """With an empty KB, every answer must be an escalation."""
    result = respond("what is your refund policy")
    assert result["answered"] is False
    assert "answer_en" not in result


def test_draft_article_does_not_produce_an_answer(chat_env):
    """A draft (unapproved) article must never be surfaced as an answer."""
    get_default_article_store().create(
        KnowledgeArticle(
            slug="refund",
            title_en="refund policy",
            body_en="Refunds in 14 days.",
        )
    )  # left as draft — not approved
    result = respond("what is your refund policy")
    assert result["answered"] is False
    assert result["escalated"] is True


def test_answered_response_always_carries_citations(chat_env):
    store = get_default_article_store()
    art = store.create(
        KnowledgeArticle(slug="x", title_en="onboarding steps guide",
                         body_en="Complete the form first.")
    )
    store.set_status(art.article_id, "approved")
    result = respond("onboarding steps guide")
    if result["answered"]:
        assert result["citations"], "an answered chat turn must cite its source"
