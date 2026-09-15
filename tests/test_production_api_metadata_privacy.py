from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import patch

from api.routers import platform_meta
from scripts.server.verify_public_surfaces import SURFACES


def _settings(env: str):
    return SimpleNamespace(
        app_name="Dealix", app_version="3.0.0", app_env=env, git_sha="test-sha"
    )


def test_version_does_not_advertise_docs_in_production() -> None:
    with patch.object(platform_meta, "get_settings", return_value=_settings("production")), patch.object(
        platform_meta, "_deployment_git_sha", return_value="test-sha"
    ):
        body = asyncio.run(platform_meta.version())
    assert body["docs"] is None


def test_meta_does_not_advertise_openapi_in_production() -> None:
    with patch.object(platform_meta, "get_settings", return_value=_settings("production")), patch.object(
        platform_meta, "_deployment_git_sha", return_value="test-sha"
    ), patch.object(platform_meta, "build_gtm_public_surfaces_snapshot", return_value={}):
        body = asyncio.run(platform_meta.platform_meta())
    assert body["canonical_links"]["openapi"] is None


def test_schema_links_remain_available_outside_production() -> None:
    with patch.object(platform_meta, "get_settings", return_value=_settings("test")), patch.object(
        platform_meta, "_deployment_git_sha", return_value="test-sha"
    ), patch.object(platform_meta, "build_gtm_public_surfaces_snapshot", return_value={}):
        version_body = asyncio.run(platform_meta.version())
        meta_body = asyncio.run(platform_meta.platform_meta())
    assert version_body["docs"] == "/docs"
    assert meta_body["canonical_links"]["openapi"] == "/openapi.json"


def test_public_production_surface_registry_excludes_schema_endpoints() -> None:
    backend = SURFACES["backend"]
    assert "/docs" not in backend.values()
    assert "/openapi.json" not in backend.values()
    assert backend["version"] == "/version"
    assert backend["meta"] == "/api/v1/meta"
