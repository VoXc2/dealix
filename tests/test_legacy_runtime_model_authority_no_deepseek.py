from __future__ import annotations

import inspect
from pathlib import Path

import core.config.models as models
from core.config.models import Provider, Task
from core.llm.router import ModelRouter

ROOT = Path(__file__).resolve().parents[1]


def test_static_task_routes_fail_closed_instead_of_selecting_providers() -> None:
    assert set(models.TASK_ROUTING.values()) == {Provider.HOLD}
    for fallbacks in models.FALLBACK_CHAIN.values():
        assert fallbacks == []


def test_smart_route_fails_closed_for_every_task() -> None:
    for task in Task:
        probes = (
            dict(text_sample="", est_tokens=0, critical=False),
            dict(text_sample="short", est_tokens=128, critical=False),
            dict(text_sample="نص عربي للاختبار", est_tokens=128, critical=False),
            dict(text_sample="critical", est_tokens=8192, critical=True),
        )
        for kwargs in probes:
            assert models.smart_route(task, **kwargs).provider == Provider.HOLD


def test_legacy_router_has_no_automatic_deepseek_client_or_local_fallback() -> None:
    init_source = inspect.getsource(ModelRouter.__init__)
    build_source = inspect.getsource(ModelRouter._build_clients)
    run_source = inspect.getsource(ModelRouter.run)
    assert "_build_deepseek_local_fallback" not in init_source
    assert "self._clients[Provider.DEEPSEEK]" not in build_source
    assert "_try_deepseek_local_fallback" not in run_source
    assert "LegacyModelAuthorityHold" in run_source


def test_application_inference_cannot_choose_from_configured_provider_order() -> None:
    source = (ROOT / "core" / "llm" / "inference.py").read_text(encoding="utf-8")
    assert "Provider.DEEPSEEK" in source
    assert "Provider.HOLD" in source
    assert "providers[0]" not in source
    assert "preferred_provider=" not in source


def test_windows_helpers_have_no_model_switching_defaults_or_config_mutation() -> None:
    for relative in ("scripts/run-aider.ps1", "scripts/watchdog.ps1", "scripts/switch-gear.ps1"):
        source = (ROOT / relative).read_text(encoding="utf-8-sig").lower()
        assert "deepseek/deepseek-chat" not in source
        assert "daily (deepseek)" not in source
    switch_source = (ROOT / "scripts" / "switch-gear.ps1").read_text(encoding="utf-8-sig").lower()
    assert "set-content" not in switch_source
    assert ".aider.conf.yml" not in switch_source


def test_legacy_gear_engine_cannot_mint_model_defaults() -> None:
    source = (ROOT / "dealix" / "llm" / "engine.py").read_text(encoding="utf-8").lower()
    assert "deepseek/deepseek-chat" not in source
    assert "gear 1: deepseek" not in source
    assert "hold_canonical_broker_required" in source


def test_legacy_strategy_has_no_implicit_deepseek_or_paid_model_defaults() -> None:
    source = (ROOT / "dealix" / "llm" / "strategy.py").read_text(encoding="utf-8").lower()
    assert '"deepseek/deepseek-chat"' not in source
    assert '"minimax/minimax-m2.5"' not in source
    assert '"minimax/minimax-m2.7"' not in source
    assert "broker_required_model" in source
    assert "_explicit_non_deepseek_model" in source


def test_env_example_is_model_neutral_for_legacy_gears() -> None:
    text = (ROOT / ".env.example").read_text(encoding="utf-8-sig")
    assignments: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        assignments[key.strip()] = value.strip()

    for key in ("GEAR1_MODEL", "GEAR2_MODEL", "GEAR3_MODEL"):
        assert assignments.get(key, "") == ""
    assert "Founder unattended policy is NO_DEEPSEEK" in text
    assert "NEVER automatic model or cost authority" in text
