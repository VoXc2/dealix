"""Operating System domain router aggregator.

Bundles all /api/v1/ops/* routers.
"""

from __future__ import annotations

import importlib
import logging
import os

from fastapi import APIRouter

_ROUTER_MODULES = (
    "api.routers.ops_negotiation",
    "api.routers.ops_research",
    "api.routers.ops_knowledge",
    "api.routers.ops_communication",
    "api.routers.ops_collaboration",
    "api.routers.ops_sales",
    "api.routers.ops_growth",
    "api.routers.ops_customer_success",
    "api.routers.ops_health",
    "api.routers.ops_voice_ai",
)


def _strict_optional_routers() -> bool:
    return os.getenv("DEALIX_STRICT_OPTIONAL_ROUTERS", "").strip().lower() in {
        "1",
        "true",
        "yes",
    }


def _load_router(module_path: str) -> APIRouter | None:
    try:
        module = importlib.import_module(module_path)
        router = module.router
        if not isinstance(router, APIRouter):
            raise TypeError("module router is not an APIRouter")
        return router
    except Exception as exc:
        logging.getLogger(__name__).error(
            "ops_subrouter_skipped router=%s error_type=%s",
            module_path,
            type(exc).__name__,
        )
        if _strict_optional_routers():
            raise RuntimeError(
                f"Optional Ops subrouter failed to import: {module_path}"
            ) from exc
        return None


def get_routers() -> list[APIRouter]:
    """Load Ops subrouters independently so one degraded surface cannot drop all."""
    return [
        router
        for module_path in _ROUTER_MODULES
        if (router := _load_router(module_path)) is not None
    ]
