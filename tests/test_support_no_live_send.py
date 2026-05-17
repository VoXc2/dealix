"""Non-negotiable guard: support never sends a live message.

The support module must contain no live-send call, and the only
reply-sending path must route through the approval center.
"""

from __future__ import annotations

import pathlib

import pytest

from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.evidence_control_plane_os.event_store import (
    reset_default_evidence_ledger,
)
from auto_client_acquisition.knowledge.article_store import reset_default_article_store
from auto_client_acquisition.knowledge.gaps import reset_default_gap_store
from auto_client_acquisition.support import create_ticket, request_send_reply
from auto_client_acquisition.support.ticket_store import reset_default_ticket_store

_SUPPORT_DIR = (
    pathlib.Path(__file__).resolve().parents[1]
    / "auto_client_acquisition"
    / "support"
)

# Tokens that would indicate a live external send from inside support code.
_FORBIDDEN = (
    "send_whatsapp",
    "send_email",
    "send_sms",
    "smtp",
    "twilio",
    "requests.post",
    "httpx.post",
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


def test_support_module_has_no_live_send_call():
    hits: list[str] = []
    for path in _SUPPORT_DIR.glob("*.py"):
        text = path.read_text(encoding="utf-8").lower()
        for token in _FORBIDDEN:
            if token in text:
                hits.append(f"{path.name}: {token}")
    assert not hits, f"forbidden live-send tokens in support module: {hits}"


def test_send_reply_never_sends_directly(support_env):
    tkt = create_ticket(subject="x", message="how do I get started")
    result = request_send_reply(tkt.ticket_id)
    assert result["sent"] is False
    assert result["approval_status"] == "approval_required"
    assert result["approval_id"]
