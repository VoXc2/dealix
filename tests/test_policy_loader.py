"""policy_config loader — malformed-input rejection + cache identity."""

from __future__ import annotations

import pytest

from auto_client_acquisition.policy_config import load_policy
from auto_client_acquisition.policy_config.loader import policy_path


def test_load_policy_returns_dict() -> None:
    data = load_policy("approval_policy")
    assert isinstance(data, dict)
    assert data["schema_version"] == "1.0"


def test_load_policy_is_cached() -> None:
    assert load_policy("claim_policy") is load_policy("claim_policy")


def test_non_dict_yaml_is_rejected(tmp_path, monkeypatch) -> None:
    bad = tmp_path / "broken.yaml"
    bad.write_text("- a\n- b\n", encoding="utf-8")
    monkeypatch.setenv("DEALIX_POLICY_DIR", str(tmp_path))
    with pytest.raises(ValueError, match="invalid_policy_yaml:broken"):
        load_policy("broken")


def test_env_override_changes_resolved_path(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DEALIX_POLICY_DIR", str(tmp_path))
    assert policy_path("approval_policy") == tmp_path / "approval_policy.yaml"


def test_all_shipped_policies_parse() -> None:
    for name in ("approval_policy", "claim_policy", "lead_scoring", "stage_transitions"):
        assert isinstance(load_policy(name), dict)
