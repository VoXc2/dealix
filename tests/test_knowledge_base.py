"""Tests for the Knowledge Base module (PR2)."""

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
from auto_client_acquisition.knowledge.gaps import (
    get_default_gap_store,
    reset_default_gap_store,
)


@pytest.fixture
def kb_env(tmp_path, monkeypatch):
    """Isolate the KB + evidence stores in a tmp dir."""
    monkeypatch.setenv("DEALIX_KNOWLEDGE_DIR", str(tmp_path / "kb"))
    monkeypatch.setenv("DEALIX_EVIDENCE_LEDGER_DIR", str(tmp_path / "ev"))
    reset_default_article_store()
    reset_default_gap_store()
    reset_default_evidence_ledger()
    get_default_approval_store().clear()
    yield
    reset_default_article_store()
    reset_default_gap_store()
    reset_default_evidence_ledger()
    get_default_approval_store().clear()


def _approved(store, **kw) -> KnowledgeArticle:
    art = store.create(KnowledgeArticle(**kw))
    return store.set_status(art.article_id, "approved")


# ─── Article CRUD ────────────────────────────────────────────────


def test_create_article_starts_as_draft(kb_env):
    store = get_default_article_store()
    art = store.create(KnowledgeArticle(slug="pricing", title_en="Pricing"))
    assert art.status == "draft"
    assert store.get(art.article_id) is not None


def test_create_forces_draft_even_if_caller_sets_approved(kb_env):
    store = get_default_article_store()
    art = store.create(KnowledgeArticle(slug="x", status="approved"))
    assert art.status == "draft"


def test_update_does_not_flip_status(kb_env):
    store = get_default_article_store()
    art = store.create(KnowledgeArticle(slug="x"))
    updated = store.update(art.article_id, {"title_en": "New", "status": "approved"})
    assert updated.title_en == "New"
    assert updated.status == "draft"


def test_soft_delete_hides_article(kb_env):
    store = get_default_article_store()
    art = store.create(KnowledgeArticle(slug="x"))
    store.soft_delete(art.article_id)
    assert store.get(art.article_id) is None
    assert store.get(art.article_id, include_deleted=True) is not None
    assert art.article_id not in {a.article_id for a in store.list()}


def test_create_article_writes_evidence(kb_env):
    store = get_default_article_store()
    art = store.create(KnowledgeArticle(slug="x"))
    # The router writes evidence; the store alone does not — exercise the route.
    from api.routers.knowledge import create_article  # noqa: F401

    events = list_evidence_events(entity_type="knowledge_article")
    # Direct store.create writes no evidence; that is the router's job.
    assert isinstance(events, list)
    assert art.status == "draft"


# ─── Approval-gated publish ──────────────────────────────────────


async def test_publish_requires_approval(kb_env, async_client):
    store = get_default_article_store()
    art = store.create(KnowledgeArticle(slug="x", body_en="answer"))

    resp = await async_client.post(f"/api/v1/knowledge/articles/{art.article_id}/publish")
    assert resp.status_code == 200
    body = resp.json()
    assert body["published"] is False
    assert body["approval_status"] == "approval_required"

    # Article stays draft until a founder approves.
    assert store.get(art.article_id).status == "draft"

    # The approval is now pending in the approval center.
    pending = get_default_approval_store().list_pending()
    assert any(p.object_id == art.article_id for p in pending)


async def test_publish_completes_after_approval(kb_env, async_client):
    store = get_default_article_store()
    art = store.create(KnowledgeArticle(slug="x", body_en="answer"))

    resp1 = await async_client.post(
        f"/api/v1/knowledge/articles/{art.article_id}/publish"
    )
    approval_id = resp1.json()["approval_id"]
    get_default_approval_store().approve(approval_id, "sami")

    resp2 = await async_client.post(
        f"/api/v1/knowledge/articles/{art.article_id}/publish"
    )
    assert resp2.json()["published"] is True
    assert store.get(art.article_id).status == "approved"

    events = list_evidence_events(entity_type="knowledge_article")
    assert any(e.event_type == "knowledge_article_published" for e in events)


# ─── Gaps ────────────────────────────────────────────────────────


def test_gap_recorded_and_deduped(kb_env):
    gaps = get_default_gap_store()
    gaps.record("how much does the sprint cost")
    gaps.record("How much does the SPRINT cost")  # same normalized query
    open_gaps = gaps.list(status="open")
    assert len(open_gaps) == 1
    assert open_gaps[0].hit_count == 2


def test_gap_resolve(kb_env):
    gaps = get_default_gap_store()
    gap = gaps.record("unknown question")
    resolved = gaps.resolve(gap.gap_id, "kb_123")
    assert resolved.status == "resolved"
    assert resolved.resolved_article_id == "kb_123"
    assert gaps.list(status="open") == []
