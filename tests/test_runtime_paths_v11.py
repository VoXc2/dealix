"""V11 Phase 3 — runtime path resolver tests."""
from __future__ import annotations

import os
from pathlib import Path

import pytest

from auto_client_acquisition.runtime_paths import (
    registry_dir_exists,
    resolve_phase_e_dir,
    resolve_proof_events_dir,
    resolve_registry_dir,
    resolve_repo_root,
    resolve_seo_audit_report,
)


def test_resolve_repo_root_returns_real_dir() -> None:
    root = resolve_repo_root()
    assert isinstance(root, Path)
    assert root.is_dir()
    # The repo root must contain pyproject.toml + api/ + auto_client_acquisition/
    assert (root / "pyproject.toml").exists()
    assert (root / "api").is_dir()


def test_resolve_registry_dir_default() -> None:
    # No env override → repo-relative
    os.environ.pop("DEALIX_REGISTRY_DIR", None)
    p = resolve_registry_dir()
    assert p == resolve_repo_root() / "docs" / "registry"


def test_resolve_registry_dir_respects_env_override(tmp_path: Path) -> None:
    custom = tmp_path / "custom_registry"
    custom.mkdir()
    os.environ["DEALIX_REGISTRY_DIR"] = str(custom)
    try:
        p = resolve_registry_dir()
        assert p == custom
        assert registry_dir_exists()
    finally:
        os.environ.pop("DEALIX_REGISTRY_DIR", None)


def test_registry_dir_exists_for_real_repo() -> None:
    os.environ.pop("DEALIX_REGISTRY_DIR", None)
    # The real repo ships docs/registry — this must be true on CI + local
    assert registry_dir_exists() is True


def test_registry_dir_missing_returns_false_with_bogus_override() -> None:
    os.environ["DEALIX_REGISTRY_DIR"] = "/this/path/does/not/exist/anywhere/v11"
    try:
        assert registry_dir_exists() is False
    finally:
        os.environ.pop("DEALIX_REGISTRY_DIR", None)


def test_phase_e_and_proof_events_paths() -> None:
    pe = resolve_phase_e_dir()
    pr = resolve_proof_events_dir()
    seo = resolve_seo_audit_report()
    assert pe == resolve_repo_root() / "docs" / "phase-e"
    assert pr == resolve_repo_root() / "docs" / "proof-events"
    assert seo == resolve_repo_root() / "docs" / "SEO_AUDIT_REPORT.json"
