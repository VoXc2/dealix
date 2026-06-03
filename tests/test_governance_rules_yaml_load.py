"""Governance rules YAML pack loads and declares ids."""

from __future__ import annotations

from auto_client_acquisition.governance_os.rules.loader import load_all_rules, rule_yaml_paths


def test_rule_files_exist() -> None:
    assert len(rule_yaml_paths()) >= 7


def test_each_rule_has_id_and_severity() -> None:
    for blob in load_all_rules():
        assert blob.get("id")
        assert blob.get("severity")
