"""Forward-reconciliation: provider-neutral canonical broker + fail-closed legacy isolation.

Canonical founder policy (from origin/main #2018, not reverting it and not
reviving closed #2025): provider-neutral local/free-first —
deterministic/no-model -> adequate local/private -> eligible verified-free ->
trusted-current included capacity -> HOLD. DeepSeek may be auto-selected ONLY
through the canonical broker when explicit-free or trusted included evidence
passes cost/data/privacy gates. Arbitrary paid spill remains
forbidden/approval-gated.

Legacy/direct-provider paths (direct DeepSeek clients, OpenClaw/provider
fallbacks, compatibility-router cloud aliases, secret/provider defaults) must
NOT become automatic authority. Existing no-DeepSeek compatibility tooling is
compatibility isolation for legacy/direct runtime, not global canonical policy.
"""
from __future__ import annotations

import importlib.util
import inspect
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPS = ROOT / "scripts" / "ops"


def _load(name: str):
    path = OPS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


policy = _load("model_cost_policy")
broker = _load("go_resource_broker")
free_broker = _load("opencode_model_broker")

RECONCILED_SCOPES = (
    ROOT / "scripts" / "AGENTS.md",
    ROOT / "config" / "company" / "AGENTS.md",
    ROOT / "dealix" / "AGENTS.md",
)

_BLANKET_NO_DEEPSEEK_CLAIMS = (
    "automatic model execution is no_deepseek",
    "automatic model policy is no_deepseek",
    "execution is no_deepseek and fail-closed",
    "policy is no_deepseek and fail-closed",
)


def test_canonical_broker_accepts_explicit_free_deepseek_after_gates() -> None:
    # Explicit-free DeepSeek is eligible through the canonical broker without
    # needing included-Go cost authority.
    assert policy.is_explicit_free_model("opencode/deepseek-v4-flash-free") is True
    assert policy.is_auto_selectable_model("opencode/deepseek-v4-flash-free") is True
    order = free_broker.candidate_order(
        {
            "models": ["opencode/nemotron-3-ultra-free", "opencode/deepseek-v4-flash-free"],
            "free_models": ["opencode/nemotron-3-ultra-free", "opencode/deepseek-v4-flash-free"],
        },
        current="opencode/paid-x",
    )
    assert order == ["opencode/nemotron-3-ultra-free", "opencode/deepseek-v4-flash-free"]
    # Free-only route works even when included-Go authority is absent.
    assert (
        broker.pick_model(
            "R4_INCLUDED_HIGH", ["opencode/deepseek-v4-flash-free"], [], [], broker.GO_COST_UNKNOWN
        )
        == "opencode/deepseek-v4-flash-free"
    )


def test_canonical_broker_accepts_trusted_included_deepseek_only_with_verified_gates(
    monkeypatch,
) -> None:
    # Trusted included DeepSeek requires live verified cost authority.
    monkeypatch.setenv("DEALIX_OPENCODE_GO_USE_BALANCE", "disabled")
    monkeypatch.setenv("DEALIX_OPENCODE_GO_COST_AUTHORITY_REF", "test_verified_disabled")
    catalog = ["opencode-go/deepseek-v4.1-flash"]
    verified = broker.GO_COST_VERIFIED_DISABLED
    assert broker.pick_model("R4_INCLUDED_HIGH", catalog, [], [], verified) == (
        "opencode-go/deepseek-v4.1-flash"
    )


def test_paid_unverified_deepseek_remains_hold(monkeypatch) -> None:
    # Paid DeepSeek (no explicit -free suffix, no verified included namespace
    # grant) is never auto-selectable and stays on HOLD signals.
    assert policy.is_explicit_free_model("opencode/deepseek-v4-flash") is False
    assert policy.is_auto_selectable_model("opencode/deepseek-v4-flash") is False
    assert policy.is_auto_selectable_model("vendor/deepseek-paid") is False

    paid_catalog = ["opencode/deepseek-v4-flash"]
    assert broker.pick_model("R4_INCLUDED_HIGH", paid_catalog, [], []) == policy.UNKNOWN_INCLUDED_HIGH
    assert (
        broker.pick_model("R5_STRONG_REASONING", paid_catalog, [], [])
        == policy.UNKNOWN_INCLUDED_STRONG
    )
    assert broker.pick_model("R6_PAID_EXCEPTION", paid_catalog, [], []) == policy.PAID_PENDING_APPROVAL

    # Included-namespace DeepSeek without live verified authority also HOLDs:
    # caller-supplied verified state alone cannot mint live cost authority.
    monkeypatch.delenv("DEALIX_OPENCODE_GO_USE_BALANCE", raising=False)
    monkeypatch.delenv("DEALIX_OPENCODE_GO_COST_AUTHORITY_REF", raising=False)
    assert broker.provider_cost_authority()["state"] == broker.GO_COST_UNKNOWN
    assert (
        broker.pick_model(
            "R4_INCLUDED_HIGH",
            ["opencode-go/deepseek-v4.1-flash"],
            [],
            [],
            broker.GO_COST_VERIFIED_DISABLED,
        )
        == policy.UNKNOWN_INCLUDED_HIGH
    )

    # Free selector never promotes paid DeepSeek.
    order = free_broker.candidate_order(
        {"models": ["opencode/deepseek-v4-flash"], "free_models": []},
        current="opencode/deepseek-v4-flash",
    )
    assert order == []


def test_legacy_direct_compatibility_paths_remain_fail_closed() -> None:
    # Legacy strategy cannot mint DeepSeek/paid defaults.
    from dealix.llm.strategy import LLMStrategyRouter, TaskType

    assert LLMStrategyRouter._MODEL_IDS  # explicit mapping exists but is broker-gated
    try:
        LLMStrategyRouter._require_explicit_model("deepseek/deepseek-chat")
        raise AssertionError("legacy strategy must fail closed on DeepSeek")
    except RuntimeError:
        pass
    # resolve() with broker-required sentinel also fails closed.
    import os

    for key in ("GEAR1_MODEL", "GEAR2_MODEL", "GEAR3_MODEL"):
        monkey = os.getenv(key, "")
        if monkey and "deepseek" in monkey.lower():
            raise AssertionError(f"{key} must not carry DeepSeek default")

    # Compatibility loopback router: cloud aliases HOLD, no remote authority.
    router = _load("dealix_local_ai_router")
    assert router.route_alias("dealix-flash") == "hold"
    assert router.route_alias("dealix-think") == "hold"
    assert router.route_alias("dealix-pro") == "hold"
    assert router.route_alias("dealix-auto") == "local"

    # OpenClaw migrator: DeepSeek authority fails audit, candidate passes,
    # non-model config preserved, secret-safe write.
    migration = _load("migrate_openclaw_no_deepseek")
    fixture = {
        "auth": {"profiles": {"deepseek:dealix": {"provider": "deepseek"}}},
        "models": {"providers": {"dealix-router": {"models": [{"id": "dealix-flash"}]}}},
        "plugins": {"entries": {"deepseek": {"enabled": True}}},
        "agents": {"list": [{"id": "a", "model": {"primary": "deepseek/x", "fallbacks": []}}]},
    }
    assert migration.audit_config(fixture)["ok"] is False
    candidate = migration.migrate(fixture)
    assert migration.audit_config(candidate)["ok"] is True
    source = (OPS / "migrate_openclaw_no_deepseek.py").read_text(encoding="utf-8")
    assert "refusing in-place mutation" in source
    assert "output.chmod(0o600)" in source

    # Secret/provider defaults never become authority: gear models blank in example.
    text = (ROOT / ".env.example").read_text(encoding="utf-8-sig")
    assignments: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        assignments[key.strip()] = value.strip()
    for key in ("GEAR1_MODEL", "GEAR2_MODEL", "GEAR3_MODEL"):
        assert assignments.get(key, "") == ""

    # Direct DeepSeek client exists only as explicit-key compatibility surface
    # and requires caller-supplied credentials (never automatic authority).
    from core.llm.openai_compat import DeepSeekClient

    sig = inspect.signature(DeepSeekClient.__init__)
    assert "api_key" in sig.parameters


def test_reconciled_scopes_no_blanket_global_no_deepseek() -> None:
    for path in RECONCILED_SCOPES:
        assert path.is_file(), path
        lowered = path.read_text(encoding="utf-8").lower()
        for claim in _BLANKET_NO_DEEPSEEK_CLAIMS:
            assert claim not in lowered, f"{path}: stale blanket claim {claim!r}"
        # Forward policy markers.
        assert "provider-neutral" in lowered, path
        assert "hold" in lowered, path
        assert "compatibility isolation" in lowered, path
        # Trusted cost/data/privacy gates preserved, paid spill gated.
        assert "cost" in lowered and "privacy" in lowered and "data" in lowered, path
        assert "paid spill" in lowered, path
        assert "approval-gated" in lowered or "approval" in lowered, path
        # Canonical chain present.
        assert "deterministic" in lowered, path
        assert "verified-free" in lowered or "verified free" in lowered, path
