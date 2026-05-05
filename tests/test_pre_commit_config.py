"""Tests for .pre-commit-config.yaml hygiene.

Lock the policy hooks (verify-service-readiness-matrix +
export-service-readiness-json) so they cannot be silently dropped.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml


CONFIG = Path(__file__).resolve().parent.parent / ".pre-commit-config.yaml"


@pytest.fixture(scope="module")
def cfg() -> dict:
    return yaml.safe_load(CONFIG.read_text(encoding="utf-8"))


def test_pre_commit_config_exists_and_is_valid_yaml(cfg: dict):
    assert isinstance(cfg, dict)
    assert "repos" in cfg
    assert isinstance(cfg["repos"], list)


def _all_hook_ids(cfg: dict) -> set[str]:
    ids: set[str] = set()
    for repo in cfg["repos"]:
        for hook in repo.get("hooks") or []:
            hook_id = hook.get("id")
            if hook_id:
                ids.add(hook_id)
    return ids


def test_hygiene_hooks_present(cfg: dict):
    ids = _all_hook_ids(cfg)
    required = {
        "trailing-whitespace",
        "end-of-file-fixer",
        "check-yaml",
        "check-json",
        "check-merge-conflict",
    }
    missing = required - ids
    assert not missing, f"hygiene hooks missing: {missing}"


def test_policy_hooks_present(cfg: dict):
    """The two local hooks that enforce the YAML matrix invariant
    must stay wired."""
    ids = _all_hook_ids(cfg)
    assert "verify-service-readiness-matrix" in ids
    assert "export-service-readiness-json" in ids


def test_secrets_scanner_present(cfg: dict):
    """Gitleaks must always be wired — protects against accidental
    Stripe / API key commits."""
    ids = _all_hook_ids(cfg)
    assert "gitleaks" in ids


def test_pre_commit_setup_doc_exists():
    doc = Path(__file__).resolve().parent.parent / "docs" / "PRE_COMMIT_SETUP.md"
    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    assert "pre-commit install" in text
    assert "verify-service-readiness-matrix" in text
