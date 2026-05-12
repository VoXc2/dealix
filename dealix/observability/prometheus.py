"""
Prometheus exporter — exposes /metrics so Grafana scrapes us directly
without an OTel collector hop.

Uses `prometheus-fastapi-instrumentator` when installed; falls back to
a tiny in-process counter that still returns valid Prometheus text so
the scraper at least sees a healthy endpoint.
"""

from __future__ import annotations

from typing import Any

from core.logging import get_logger

log = get_logger(__name__)


def attach(app: Any) -> None:
    """Mount /metrics on the given FastAPI app. Best-effort."""
    try:
        from prometheus_fastapi_instrumentator import Instrumentator  # type: ignore

        Instrumentator(
            should_group_status_codes=True,
            should_ignore_untemplated=True,
            should_respect_env_var=False,
            should_instrument_requests_inprogress=True,
        ).instrument(app).expose(app, include_in_schema=False)
        log.info("prometheus_instrumentator_attached")
        return
    except ImportError:
        log.info(
            "prometheus_fastapi_instrumentator_not_installed; mounting tiny exporter"
        )

    # Tiny fallback so /metrics returns something parseable.
    from fastapi.responses import PlainTextResponse

    @app.get("/metrics", include_in_schema=False)
    async def _metrics() -> PlainTextResponse:
        text = (
            "# HELP dealix_up Service health.\n"
            "# TYPE dealix_up gauge\n"
            "dealix_up 1\n"
        )
        return PlainTextResponse(text, media_type="text/plain; version=0.0.4")
