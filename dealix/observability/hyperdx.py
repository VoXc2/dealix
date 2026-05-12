"""
HyperDX — OTLP-native observability (logs + traces + metrics in one UI).

HyperDX is an OpenTelemetry collector under the hood; we only need to
push the OTLP endpoint + headers via the existing `dealix.observability.otel`
setup. This module exposes a one-line `configure_hyperdx()` so the
ops team can flip the destination without code changes.

Reference: https://www.hyperdx.io/docs
"""

from __future__ import annotations

import os

from core.logging import get_logger

log = get_logger(__name__)


def is_configured() -> bool:
    return bool(os.getenv("HYPERDX_API_KEY", "").strip())


def configure_hyperdx() -> bool:
    """Wire OTel exporters to point at HyperDX. Idempotent + safe-when-disabled."""
    api_key = os.getenv("HYPERDX_API_KEY", "").strip()
    if not api_key:
        return False
    # HyperDX accepts OTLP/HTTP at this endpoint; tags route by service.
    endpoint = os.getenv(
        "HYPERDX_OTLP_ENDPOINT",
        "https://in-otel.hyperdx.io",
    ).rstrip("/")
    os.environ.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", endpoint)
    os.environ.setdefault(
        "OTEL_EXPORTER_OTLP_HEADERS",
        f"authorization={api_key}",
    )
    os.environ.setdefault("OTEL_SERVICE_NAME", "dealix-api")
    log.info("hyperdx_configured", endpoint=endpoint)
    return True
