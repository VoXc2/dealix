"""Tests for doctrine versioning + pinning endpoints."""
from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.doctrine import router as doctrine_router


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(doctrine_router)
    return TestClient(app)


def test_versions_endpoint_returns_versions_list():
    body = _client().get("/api/v1/doctrine/versions").json()
    assert "versions" in body
    assert isinstance(body["versions"], list)
    assert len(body["versions"]) >= 1
    v1 = next((v for v in body["versions"] if v["version"] == "v1.0.0"), None)
    assert v1 is not None
    assert v1["commit_sha"]
    assert v1["signed_by"]


def test_head_doctrine_includes_version_label():
    body = _client().get("/api/v1/doctrine").json()
    assert "version" in body
    # Should be the latest published version or "unversioned".
    assert body["version"]


def test_pinned_doctrine_returns_recorded_sha():
    body = _client().get("/api/v1/doctrine?version=v1.0.0").json()
    assert body["version"] == "v1.0.0"
    assert body["commit_sha"]
    assert "summary" in body
    assert "date" in body


def test_unknown_version_returns_404():
    r = _client().get("/api/v1/doctrine?version=v999.0.0")
    assert r.status_code == 404


def test_versions_file_is_valid_json_and_sorted():
    p = Path(__file__).resolve().parents[1] / "open-doctrine" / "doctrine_versions.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    versions = data["versions"]
    # Monotonic by semver.
    keys = [tuple(int(x) for x in v["version"].lstrip("v").split(".")) for v in versions]
    assert keys == sorted(keys)


def test_version_strings_match_semver_pattern():
    import re
    p = Path(__file__).resolve().parents[1] / "open-doctrine" / "doctrine_versions.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    rx = re.compile(r"^v\d+\.\d+\.\d+$")
    for v in data["versions"]:
        assert rx.match(v["version"]), f"bad version label: {v['version']}"
