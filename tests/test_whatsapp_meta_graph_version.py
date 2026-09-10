from __future__ import annotations

from pathlib import Path

import pytest

from core.errors import IntegrationError
from integrations.whatsapp import (
    DEFAULT_GRAPH_API_VERSION,
    meta_graph_api_version,
    meta_graph_base_url,
)

ROOT = Path(__file__).resolve().parents[1]
META_CLIENT = ROOT / "integrations" / "whatsapp.py"
MULTI_PROVIDER = ROOT / "auto_client_acquisition" / "email" / "whatsapp_multi_provider.py"


def test_meta_graph_default_is_current_and_not_expiring_v20(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("WHATSAPP_GRAPH_API_VERSION", raising=False)
    assert DEFAULT_GRAPH_API_VERSION == "v26.0"
    assert meta_graph_api_version() == "v26.0"
    assert meta_graph_base_url() == "https://graph.facebook.com/v26.0"


def test_meta_graph_version_can_be_explicitly_overridden(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("WHATSAPP_GRAPH_API_VERSION", "v25.0")
    assert meta_graph_api_version() == "v25.0"
    assert meta_graph_base_url().endswith("/v25.0")


def test_meta_graph_version_rejects_malformed_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("WHATSAPP_GRAPH_API_VERSION", "latest")
    with pytest.raises(IntegrationError, match="must look like"):
        meta_graph_api_version()


def test_all_meta_whatsapp_paths_share_canonical_version_source() -> None:
    meta_text = META_CLIENT.read_text(encoding="utf-8")
    provider_text = MULTI_PROVIDER.read_text(encoding="utf-8")

    assert "graph.facebook.com/v20.0" not in meta_text
    assert "graph.facebook.com/v20.0" not in provider_text
    assert "meta_graph_base_url" in meta_text
    assert "from integrations.whatsapp import meta_graph_base_url" in provider_text
    assert 'WHATSAPP_GRAPH_API_VERSION' in meta_text
