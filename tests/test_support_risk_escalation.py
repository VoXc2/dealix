"""Guard: high-risk support categories always escalate and are never
auto-answered, even when the KB has a matching article (PR3)."""

from __future__ import annotations

import pytest

from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.knowledge.article_store import (
    KnowledgeArticle,
    get_default_article_store,
    reset_default_article_store,
)
from auto_client_acquisition.knowledge.gaps import reset_default_gap_store
from auto_client_acquisition.evidence_control_plane_os.event_store import (
    reset_default_evidence_ledger,
)
from auto_client_acquisition.support import create_ticket, draft_reply
from auto_client_acquisition.support.risk import (
    HIGH_RISK_CATEGORIES,
    is_auto_answerable,
    risk_level_for_category,
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


def test_high_risk_categories_are_never_auto_answerable():
    for category in HIGH_RISK_CATEGORIES:
        assert risk_level_for_category(category) == "high"
        assert is_auto_answerable(
            category=category, escalation_needed=False, kb_confidence=1.0
        ) is False


def test_refund_ticket_escalates_even_with_kb_article(support_env):
    # A perfectly matching approved article exists for the refund query.
    store = get_default_article_store()
    art = store.create(
        KnowledgeArticle(
            slug="refund",
            title_en="refund money back policy",
            body_en="Refunds take 14 days.",
        )
    )
    store.set_status(art.article_id, "approved")

    tkt = create_ticket(subject="refund", message="I want a refund, money back please")
    assert tkt.risk_level == "high"
    assert tkt.escalation_needed is True
    assert tkt.status == "escalated"

    result = draft_reply(tkt.ticket_id)
    # Even with a KB match, a refund ticket must escalate — never auto-draft.
    assert result["drafted"] is False
    assert result["escalated"] is True
    assert get_default_ticket_store().get(tkt.ticket_id).suggested_reply == ""


def test_escalation_needed_blocks_auto_answer():
    assert is_auto_answerable(
        category="onboarding", escalation_needed=True, kb_confidence=1.0
    ) is False
