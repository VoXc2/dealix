"""Wave 8 §10 — Langfuse Adapter.

Wraps the Langfuse SDK with graceful fallback when LANGFUSE_SECRET_KEY /
LANGFUSE_PUBLIC_KEY are not configured.
All operations are fail-safe. Never logs PII.
"""
from __future__ import annotations

import logging
import os
from typing import Any

from auto_client_acquisition.observability_adapters.base import (
    BaseObservabilityAdapter,
    ObservabilityEvent,
)

logger = logging.getLogger(__name__)

_LANGFUSE_AVAILABLE = False
try:
    from langfuse import Langfuse
    _LANGFUSE_AVAILABLE = True
except ImportError:
    pass


class LangfuseAdapter(BaseObservabilityAdapter):
    """Langfuse LLM observability adapter.

    Logs LLM calls (model, tokens, latency, success) to Langfuse for
    quality monitoring and cost tracking.

    Falls back gracefully when credentials missing.
    Never logs raw prompts/responses without explicit redaction.
    """

    adapter_name = "langfuse"

    def __init__(self) -> None:
        self._client: Any = None
        self._setup()

    def _setup(self) -> None:
        if not _LANGFUSE_AVAILABLE:
            logger.debug("LangfuseAdapter: langfuse SDK not installed")
            return

        secret_key = os.environ.get("LANGFUSE_SECRET_KEY", "")
        public_key = os.environ.get("LANGFUSE_PUBLIC_KEY", "")
        host = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com")

        if not (secret_key and public_key):
            logger.debug(
                "LangfuseAdapter: LANGFUSE_SECRET_KEY / LANGFUSE_PUBLIC_KEY not set; noop mode"
            )
            return

        try:
            self._client = Langfuse(
                secret_key=secret_key,
                public_key=public_key,
                host=host,
            )
            logger.info("LangfuseAdapter: connected to %s", host)
        except Exception as exc:
            logger.warning("LangfuseAdapter._setup failed: %s", exc)
            self._client = None

    def is_configured(self) -> bool:
        return (
            _LANGFUSE_AVAILABLE
            and bool(os.environ.get("LANGFUSE_SECRET_KEY"))
            and bool(os.environ.get("LANGFUSE_PUBLIC_KEY"))
        )

    def emit(self, event: ObservabilityEvent) -> None:
        if not self._client:
            return
        try:
            generation = self._client.generation(
                name=event.event_type,
                model=event.model or "unknown",
                usage={
                    "promptTokens": event.prompt_tokens,
                    "completionTokens": event.completion_tokens,
                },
                metadata={
                    "customer_handle": event.customer_handle,
                    "latency_ms": event.latency_ms,
                    "success": event.success,
                    "error_type": event.error_type,
                    **{k: v for k, v in event.metadata.items()
                       if not _is_sensitive_key(k)},
                },
            )
            if not event.success and event.error_type:
                generation.update(level="ERROR")
        except Exception as exc:
            logger.debug("LangfuseAdapter.emit failed (noop): %s", exc)

    def start_trace(self, name: str, metadata: dict | None = None) -> str:
        if not self._client:
            return ""
        try:
            safe_meta = {
                k: v for k, v in (metadata or {}).items()
                if not _is_sensitive_key(k)
            }
            trace = self._client.trace(name=name, metadata=safe_meta)
            return trace.id
        except Exception as exc:
            logger.debug("LangfuseAdapter.start_trace failed: %s", exc)
            return ""

    def end_trace(self, trace_id: str, success: bool = True, error_type: str = "") -> None:
        # Langfuse traces are auto-closed; this is a no-op
        pass

    def flush(self) -> None:
        if self._client:
            try:
                self._client.flush()
            except Exception as exc:
                logger.debug("LangfuseAdapter.flush failed: %s", exc)


def _is_sensitive_key(key: str) -> bool:
    """Return True if key likely contains PII or secrets."""
    sensitive = {
        "password", "token", "secret", "key", "phone", "email",
        "name", "address", "cr_number", "iban", "card",
    }
    key_lower = key.lower()
    return any(s in key_lower for s in sensitive)
