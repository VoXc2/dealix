"""Regression guard for OpenClaw memory remaining local and non-authoritative."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPAIR = ROOT / "scripts/ops/repair_dealix_openclaw_gateway.sh"


def test_openclaw_semantic_memory_uses_local_ollama_without_remote_key() -> None:
    text = REPAIR.read_text(encoding="utf-8")
    assert "config set memory.search.enabled true" in text
    assert "config set memory.search.provider ollama" in text
    assert "config set memory.search.model nomic-embed-text" in text
    assert "config set memory.search.fallback none" in text
    assert "config set memory.search.rememberAcrossConversations false" in text
    assert "OPENAI_API_KEY" not in text
    assert "models.providers.openai.apiKey" not in text


def test_openclaw_memory_does_not_weaken_founder_gateway_guards() -> None:
    text = REPAIR.read_text(encoding="utf-8")
    assert "gateway.bind loopback" in text
    assert "channels.telegram.dmPolicy pairing" in text
    assert "channels.telegram.groups '{}'" in text
    assert "channels.telegram.groupAllowFrom '[]'" in text
    assert 'tools.deny \'["group:runtime","group:fs","exec","process","write","edit","apply_patch"]\'' in text
    assert "OpenClaw memory is a local retrieval cache, not a second Company Brain" in text
