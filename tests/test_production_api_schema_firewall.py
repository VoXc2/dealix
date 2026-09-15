from __future__ import annotations

from unittest.mock import patch

from api.main import create_app
from core.config.settings import get_settings


def _app_for_env(env: str):
    with patch.dict("os.environ", {"APP_ENV": env}, clear=False):
        get_settings.cache_clear()
        try:
            return create_app()
        finally:
            get_settings.cache_clear()


def test_production_does_not_mount_api_schema_surfaces() -> None:
    app = _app_for_env("production")
    assert app.docs_url is None
    assert app.redoc_url is None
    assert app.openapi_url is None


def test_test_environment_keeps_api_schema_surfaces() -> None:
    app = _app_for_env("test")
    assert app.docs_url == "/docs"
    assert app.redoc_url == "/redoc"
    assert app.openapi_url == "/openapi.json"
