"""Contracts for the deterministic OpenCode permission boundary audit."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _load(name: str) -> object:
    path = ROOT / "scripts" / "ops" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


audit = _load("audit_opencode_permissions")


def _sample_config() -> dict:
    return {
        "permission": {
            "edit": "allow",
            "read": "allow",
            "glob": "allow",
            "grep": "allow",
            "bash": {
                "*": "allow",
                "git push origin main": "deny",
                "git push --force*": "deny",
                "git push -f*": "deny",
                "gh pr merge*": "deny",
                "gh merge*": "deny",
                "railway up*": "deny",
                "railway redeploy*": "deny",
                "wrangler deploy*": "deny",
                "vercel*": "deny",
                "cat *secret*": "deny",
                "cat *.env": "deny",
                "printenv*SECRET*": "deny",
                "cat /proc/*/environ*": "deny",
                "rm -rf /*": "deny",
                "aws route53*": "deny",
                "gcloud dns*": "deny",
                "railway domain*": "deny",
                "alembic upgrade head*": "deny",
                "alembic downgrade*": "deny",
                "cloudflare*": "ask",
                "sudo*": "ask",
            },
        }
    }


def test_detect_version_parses_semver() -> None:
    assert audit.detect_version("1.18.30") == (1, 18, 30)
    assert audit.detect_version("no version") is None


def test_schema_family_detects_v1_permission_object() -> None:
    assert audit.schema_family({"permission": {}}) == "v1"
    assert audit.schema_family({"permissions": {}}) == "v2-unknown"
    assert audit.schema_family({}) == "unknown"


def test_classify_buckets_bash_rules() -> None:
    rules = audit.classify(_sample_config())
    assert "sudo*" in rules["ask"]
    assert "git push origin main" in rules["deny"]


def test_residual_ask_rules_fail_closed() -> None:
    payload = audit.audit_config(_sample_config(), version="1.18.30")
    assert payload["verdict"] == "FAIL"
    assert payload["auto_mode_safe"] is False
    assert "cloudflare*" in payload["residual_ask_rules"]
    assert "sudo*" in payload["residual_ask_rules"]


def test_harden_config_closes_every_ask_then_passes() -> None:
    hardened = audit.harden_config(_sample_config())
    assert not [value for value in hardened["permission"]["bash"].values() if value == "ask"]
    payload = audit.audit_config(hardened, version="1.18.30")
    assert payload["verdict"] == "PASS"
    assert payload["residual_ask_rules"] == []
    assert payload["hard_material_actions_fail_closed"] is True


def test_missing_hard_deny_is_detected() -> None:
    config = _sample_config()
    del config["permission"]["bash"]["railway up*"]
    payload = audit.audit_config(config, version="1.18.30")
    assert payload["verdict"] == "FAIL"
    assert "production_deploy" in payload["missing_hard_denies"]


def test_unsupported_major_version_fails() -> None:
    payload = audit.audit_config(_sample_config(), version="2.0.0")
    assert payload["version_supported"] is False
    assert payload["verdict"] == "FAIL"


def test_bare_permission_object_is_accepted() -> None:
    payload = audit.audit_config(_sample_config()["permission"], version="1.18.30")
    assert payload["schema_family"] == "v1"
    assert payload["deny_count"] > 0


def test_committed_autonomous_policy_passes() -> None:
    policy_path = ROOT / "config" / "opencode" / "autonomous-permissions.json"
    if not policy_path.is_file():
        return
    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    payload = audit.audit_config(policy, version="1.18.30")
    assert payload["verdict"] == "PASS"
    assert payload["residual_ask_rules"] == []


def test_load_config_file_preserves_urls_in_project_config() -> None:
    project = ROOT / "opencode.json"
    config = audit.load_config_file(project)
    assert config is not None
    assert config["provider"]["ollama"]["options"]["baseURL"].startswith("http")
    assert config["$schema"].startswith("https://")


def test_committed_project_config_passes_audit() -> None:
    project = ROOT / "opencode.json"
    config = audit.load_config_file(project)
    assert config is not None
    payload = audit.audit_config(config, version="1.18.30")
    assert payload["verdict"] == "PASS", payload
    assert payload["residual_ask_rules"] == []
