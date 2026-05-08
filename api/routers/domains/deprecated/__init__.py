"""
Deprecated versioned routers (v3/v6/v7/v10/v11).
These are kept for backward compatibility but will be removed in a future release.
موجهات الإصدارات المهجورة - تُحفظ للتوافق مع الإصدارات القديمة.
"""

from __future__ import annotations

from fastapi import APIRouter

from api.routers import (
    ai_workforce_v10,
    company_brain_v6,
    founder_v10,
    observability_v6,
    service_mapping_v7,
    v10_status,
    v11_status,
    v3,
)

# Wrap each deprecated router with a Deprecation response header middleware
_DEPRECATED_NOTE = "This endpoint group is deprecated and will be removed in v2.0."


def _mark_deprecated(router: APIRouter, sunset: str = "2025-12-31") -> APIRouter:
    """Return the router unchanged; deprecation header is injected globally."""
    return router


_ROUTERS = [
    _mark_deprecated(v3.router),
    _mark_deprecated(v10_status.router),
    _mark_deprecated(v11_status.router),
    _mark_deprecated(service_mapping_v7.router),
    _mark_deprecated(company_brain_v6.router),
    _mark_deprecated(ai_workforce_v10.router),
    _mark_deprecated(observability_v6.router),
    _mark_deprecated(founder_v10.router),
]

DEPRECATED_PREFIXES = {
    "/api/v1/v3/",
    "/api/v1/status/v10",
    "/api/v1/status/v11",
    "/api/v1/service-mapping/",
    "/api/v1/company-brain/v6/",
    "/api/v1/ai-workforce/v10/",
    "/api/v1/observability/v6/",
}


def get_routers() -> list[APIRouter]:
    """Return all deprecated routers (registered for backward compat)."""
    return _ROUTERS
