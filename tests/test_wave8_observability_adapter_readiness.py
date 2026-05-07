"""Wave 8 — Observability Adapter Readiness tests."""
from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parent.parent
ADAPTERS_DIR = REPO_ROOT / "auto_client_acquisition" / "observability_adapters"


def test_adapters_dir_exists():
    assert ADAPTERS_DIR.exists()


def test_all_adapter_files_exist():
    required = ["__init__.py", "base.py", "otel_adapter.py", "langfuse_adapter.py", "redaction.py"]
    for f in required:
        assert (ADAPTERS_DIR / f).exists(), f"Missing: {f}"


def test_base_importable():
    import importlib
    import sys
    sys.path.insert(0, str(REPO_ROOT))
    mod = importlib.import_module("auto_client_acquisition.observability_adapters.base")
    assert hasattr(mod, "ObservabilityEvent")
    assert hasattr(mod, "NoopAdapter")
    assert hasattr(mod, "BaseObservabilityAdapter")


def test_noop_adapter_is_configured():
    from auto_client_acquisition.observability_adapters.base import NoopAdapter
    noop = NoopAdapter()
    assert noop.is_configured() is True


def test_noop_adapter_emit_does_not_raise():
    from auto_client_acquisition.observability_adapters.base import NoopAdapter, ObservabilityEvent
    noop = NoopAdapter()
    event = ObservabilityEvent(event_type="test_event", customer_handle="test-co")
    noop.emit(event)  # Must not raise


def test_noop_adapter_start_trace_returns_empty():
    from auto_client_acquisition.observability_adapters.base import NoopAdapter
    noop = NoopAdapter()
    trace_id = noop.start_trace("test_trace")
    assert trace_id == ""


def test_otel_adapter_without_credentials_is_not_configured():
    env = {k: v for k, v in os.environ.items()
           if k != "OTEL_EXPORTER_OTLP_ENDPOINT"}
    with patch.dict(os.environ, env, clear=True):
        from auto_client_acquisition.observability_adapters.otel_adapter import OtelAdapter
        adapter = OtelAdapter()
        assert not adapter.is_configured()


def test_langfuse_adapter_without_credentials_is_not_configured():
    env = {k: v for k, v in os.environ.items()
           if k not in ("LANGFUSE_SECRET_KEY", "LANGFUSE_PUBLIC_KEY")}
    with patch.dict(os.environ, env, clear=True):
        from auto_client_acquisition.observability_adapters.langfuse_adapter import LangfuseAdapter
        adapter = LangfuseAdapter()
        assert not adapter.is_configured()


def test_langfuse_adapter_emit_without_credentials_does_not_raise():
    from auto_client_acquisition.observability_adapters.base import ObservabilityEvent
    from auto_client_acquisition.observability_adapters.langfuse_adapter import LangfuseAdapter
    env = {k: v for k, v in os.environ.items()
           if k not in ("LANGFUSE_SECRET_KEY", "LANGFUSE_PUBLIC_KEY")}
    with patch.dict(os.environ, env, clear=True):
        adapter = LangfuseAdapter()
        event = ObservabilityEvent(event_type="llm_call", customer_handle="test")
        adapter.emit(event)  # Must not raise


def test_redaction_scrubs_phone():
    from auto_client_acquisition.observability_adapters.redaction import RedactionFilter
    result = RedactionFilter.scrub_string("Contact: +966512345678 for details")
    assert "+966512345678" not in result
    assert "REDACTED_PHONE" in result


def test_redaction_scrubs_email():
    from auto_client_acquisition.observability_adapters.redaction import RedactionFilter
    result = RedactionFilter.scrub_string("Email: customer@example.com")
    assert "customer@example.com" not in result
    assert "REDACTED_EMAIL" in result


def test_redaction_scrubs_api_key():
    from auto_client_acquisition.observability_adapters.redaction import RedactionFilter
    result = RedactionFilter.scrub_string("Key: sk_live_abcdefghijk12345")
    assert "sk_live_" not in result
    assert "REDACTED_KEY" in result


def test_redaction_scrubs_portal_token():
    from auto_client_acquisition.observability_adapters.redaction import RedactionFilter
    result = RedactionFilter.scrub_string("token=dealix-cust-abcdefghijklmnopqrst")
    assert "dealix-cust-" not in result
    assert "REDACTED_TOKEN" in result


def test_redaction_scrubs_dict_sensitive_keys():
    from auto_client_acquisition.observability_adapters.redaction import RedactionFilter
    data = {"customer_handle": "test", "token": "secret_value", "model": "gpt-4"}
    result = RedactionFilter.scrub_dict(data)
    assert result["token"] == "REDACTED"
    assert result["model"] == "gpt-4"
    assert result["customer_handle"] == "test"


def test_get_adapter_factory_returns_noop_on_error():
    from auto_client_acquisition.observability_adapters.base import get_adapter, NoopAdapter
    adapter = get_adapter("unknown_adapter_type")
    assert isinstance(adapter, NoopAdapter)
