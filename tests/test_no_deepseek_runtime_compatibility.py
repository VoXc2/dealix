from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_source_managed_compat_router_is_loopback_only_and_has_no_cloud_credentials() -> None:
    text = (ROOT / "scripts/ops/dealix_local_ai_router.py").read_text(encoding="utf-8").lower()
    assert "api.deepseek.com" not in text
    assert "deepseek.key" not in text
    assert "authorization" not in text
    assert "https://" not in text
    assert 'host = "127.0.0.1"' in text
    assert 'ollama = "http://127.0.0.1:11434/api/chat"' in text


def test_historical_cloud_aliases_hold_instead_of_selecting_remote_models() -> None:
    router = load_module("dealix_local_ai_router", "scripts/ops/dealix_local_ai_router.py")
    assert router.route_alias("dealix-auto") == "local"
    assert router.route_alias("dealix-local") == "local"
    for alias in ("dealix-flash", "dealix-think", "dealix-pro"):
        assert router.route_alias(alias) == "hold"
    assert router.route_alias("unknown-provider/model") == "invalid"


def test_router_health_does_not_claim_inference_ready_from_process_liveness(monkeypatch) -> None:
    router = load_module("dealix_local_ai_router_health", "scripts/ops/dealix_local_ai_router.py")
    monkeypatch.setattr(
        router,
        "request_json",
        lambda *_args, **_kwargs: {"models": [{"name": f"{router.LOCAL_MODEL}:latest"}]},
    )
    state = router.local_availability()
    assert state["ollama_reachable"] is True
    assert state["local_model_present"] is True
    assert state["local_inference_ready"] == "NOT_PROVEN_BY_HEALTH"


def openclaw_fixture() -> dict:
    return {
        "auth": {"profiles": {"deepseek:dealix": {"provider": "deepseek", "mode": "api_key"}}},
        "models": {
            "providers": {
                "ollama": {"models": [{"id": "qwen3:4b-instruct-2507-q4_K_M"}]},
                "dealix-router": {"models": [{"id": "dealix-flash", "name": "Dealix Flash"}]},
            }
        },
        "plugins": {"entries": {"deepseek": {"enabled": True}, "ollama": {"enabled": True}}},
        "agents": {
            "list": [
                {
                    "id": "founder-president",
                    "model": {
                        "primary": "ollama/qwen3:4b-instruct-2507-q4_K_M",
                        "fallbacks": ["dealix-router/dealix-flash"],
                    },
                },
                {
                    "id": "engineering-verifier",
                    "model": {
                        "primary": "ollama/qwen3:4b-instruct-2507-q4_K_M",
                        "fallbacks": ["deepseek/deepseek-v4-flash", "deepseek/deepseek-v4-pro"],
                    },
                },
            ]
        },
    }


def test_openclaw_candidate_migration_removes_all_automatic_deepseek_authority() -> None:
    migration = load_module("migrate_openclaw_no_deepseek", "scripts/ops/migrate_openclaw_no_deepseek.py")
    before = openclaw_fixture()
    assert migration.audit_config(before)["ok"] is False
    candidate = migration.migrate(before)
    audit = migration.audit_config(candidate)
    assert audit["ok"] is True
    assert audit["deepseek_auth_profiles"] == []
    assert audit["deepseek_model_providers"] == []
    assert audit["deepseek_plugin_enabled"] is False
    assert audit["agent_violations"] == []
    assert audit["forbidden_router_alias_present"] is False
    assert audit["dealix_router_models"] == ["dealix-local"]


def test_openclaw_migration_preserves_non_model_configuration() -> None:
    migration = load_module("migrate_openclaw_preserve", "scripts/ops/migrate_openclaw_no_deepseek.py")
    before = openclaw_fixture()
    before["channels"] = {"telegram": {"enabled": True, "dmPolicy": "allowlist"}}
    candidate = migration.migrate(before)
    assert candidate["channels"] == before["channels"]


def test_cutover_script_is_action_bound_and_resets_router_credential_binding() -> None:
    text = (ROOT / "scripts/ops/dealix_no_deepseek_runtime_cutover.sh").read_text(encoding="utf-8")
    approval = 'DEALIX_L5_APPROVAL_ACTION:-}'
    mutation = 'install -o dealix -g dealix -m 0750 "$ROUTER_SOURCE" "$ROUTER_RUNTIME"'
    assert "dealix-no-deepseek-runtime-cutover-v1" in text
    assert approval in text
    assert "BLOCKED_L5" in text
    assert "LoadCredential=" in text
    assert text.index(approval) < text.index(mutation)


def test_openclaw_candidate_files_are_written_secret_safe() -> None:
    text = (ROOT / "scripts/ops/migrate_openclaw_no_deepseek.py").read_text(encoding="utf-8")
    assert "output.chmod(0o600)" in text
    assert "refusing in-place mutation" in text
