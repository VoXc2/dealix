"""Omega5 — OpenObserve adapter (optional, disabled by default).

Reuses the existing observability_adapters contract. OpenObserve
accepts OTLP-compatible ingest, so this adapter emits only the
already-redacted ObservabilityEvent fields over HTTP when ALL of:

- OPENOBSERVE_ENABLED=1
- OPENOBSERVE_URL set (http(s) base URL, no credentials embedded)
- OPENOBSERVE_ORG + OPENOBSERVE_STREAM set
- OPENOBSERVE_TOKEN present (sent as Authorization header only)

Anything missing => noop (is_configured() False). Never sends raw
prompts, tool args/results, PII, or secrets: metadata is passed
through RedactionFilter.scrub_dict first. No service is deployed by
this module; enable only via the optional compose profile or docs.
"""
from __future__ import annotations

import logging
import os
from typing import Any

from auto_client_acquisition.observability_adapters.base import (
    BaseObservabilityAdapter,
    ObservabilityEvent,
)
from auto_client_acquisition.observability_adapters.redaction import RedactionFilter

logger = logging.getLogger(__name__)


def _enabled() -> bool:
    return os.environ.get("OPENOBSERVE_ENABLED", "0").strip() == "1"


class OpenObserveAdapter(BaseObservabilityAdapter):
    """Optional OpenObserve ingest adapter. Fail-safe; never raises."""

    adapter_name = "openobserve"

    def is_configured(self) -> bool:
        return bool(
            _enabled()
            and os.environ.get("OPENOBSERVE_URL", "").strip()
            and os.environ.get("OPENOBSERVE_TOKEN", "").strip()
            and os.environ.get("OPENOBSERVE_ORG", "").strip()
            and os.environ.get("OPENOBSERVE_STREAM", "").strip()
        )

    def emit(self, event: ObservabilityEvent) -> None:
        if not self.is_configured():
            return
        try:
            import json
            import urllib.request

            base = os.environ["OPENOBSERVE_URL"].rstrip("/")
            org = os.environ["OPENOBSERVE_ORG"].strip()
            stream = os.environ["OPENOBSERVE_STREAM"].strip()
            url = f"{base}/api/{org}/{stream}/_json"

            safe_meta = RedactionFilter.scrub_dict(dict(event.metadata or {}))
            body = json.dumps(
                [
                    {
                        "event_type": event.event_type,
                        "trace_id": event.trace_id,
                        "span_id": event.span_id,
                        "model": event.model,
                        "prompt_tokens": event.prompt_tokens,
                        "completion_tokens": event.completion_tokens,
                        "latency_ms": event.latency_ms,
                        "success": event.success,
                        "error_type": event.error_type,
                        "customer_handle": RedactionFilter.scrub_string(
                            event.customer_handle or ""
                        ),
                        **safe_meta,
                    }
                ]
            ).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=body,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Basic "
                    + os.environ["OPENOBSERVE_TOKEN"].strip(),
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                resp.read()
        except Exception as exc:
            logger.debug("OpenObserveAdapter.emit skipped: %s", type(exc).__name__)

    def start_trace(self, name: str, metadata: dict | None = None) -> str:
        return ""

    def end_trace(self, trace_id: str, success: bool = True, error_type: str = "") -> None:
        pass

    def flush(self) -> None:
        pass


__all__ = ["OpenObserveAdapter"]
