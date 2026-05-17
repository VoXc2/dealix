"""Source-grounding guard: suggest_answer never answers without an
approved KB article (PR2)."""

from __future__ import annotations

import pytest

from auto_client_acquisition.knowledge.article_store import (
    KnowledgeArticle,
    get_default_article_store,
    reset_default_article_store,
)
from auto_client_acquisition.knowledge.gaps import (
    get_default_gap_store,
    reset_default_gap_store,
)
from auto_client_acquisition.knowledge.suggest import suggest_answer


@pytest.fixture
def kb_env(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_KNOWLEDGE_DIR", str(tmp_path / "kb"))
    reset_default_article_store()
    reset_default_gap_store()
    yield
    reset_default_article_store()
    reset_default_gap_store()


def test_no_match_returns_insufficient_evidence_and_records_gap(kb_env):
    result = suggest_answer("what is the refund policy for enterprise plans")
    assert result["found"] is False
    assert result["reason"] == "insufficient_evidence"
    assert len(get_default_gap_store().list(status="open")) == 1


def test_draft_articles_are_never_surfaced(kb_env):
    store = get_default_article_store()
    # A draft article that perfectly matches the query.
    store.create(
        KnowledgeArticle(
            slug="refund-policy",
            title_en="refund policy enterprise plans",
            body_en="Refunds are processed within 14 days.",
        )
    )
    result = suggest_answer("refund policy enterprise plans")
    assert result["found"] is False  # draft, not approved → not answerable


def test_approved_match_returns_grounded_answer(kb_env):
    store = get_default_article_store()
    art = store.create(
        KnowledgeArticle(
            slug="refund-policy",
            title_en="refund policy enterprise plans",
            body_en="Refunds are processed within 14 days.",
            body_ar="تتم معالجة المبالغ المستردة خلال 14 يوماً.",
        )
    )
    store.set_status(art.article_id, "approved")

    result = suggest_answer("refund policy enterprise plans")
    assert result["found"] is True
    assert result["article_id"] == art.article_id
    assert result["answer_en"].startswith("Refunds")
    assert result["confidence"] >= 0.34
    assert result["citations"][0]["article_id"] == art.article_id


def test_approved_match_does_not_record_a_gap(kb_env):
    store = get_default_article_store()
    art = store.create(
        KnowledgeArticle(slug="x", title_en="sprint pricing cost", body_en="499 SAR")
    )
    store.set_status(art.article_id, "approved")
    suggest_answer("sprint pricing cost")
    assert get_default_gap_store().list(status="open") == []
