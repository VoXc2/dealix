from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OPS = ROOT / "scripts" / "ops"
if str(OPS) not in sys.path:
    sys.path.insert(0, str(OPS))

import go_resource_broker as broker


CATALOG = [
    "opencode-go/deepseek-v4.1-flash",
    "opencode/nemotron-3-ultra-free",
]


def _clear_authority(monkeypatch) -> None:
    monkeypatch.delenv("DEALIX_OPENCODE_GO_USE_BALANCE", raising=False)
    monkeypatch.delenv("DEALIX_OPENCODE_GO_COST_AUTHORITY_REF", raising=False)


def test_unknown_provider_cost_authority_fails_closed_for_go_models(monkeypatch) -> None:
    _clear_authority(monkeypatch)
    authority = broker.provider_cost_authority()
    assert authority["state"] == broker.GO_COST_UNKNOWN
    model = broker.pick_model("R4_INCLUDED_HIGH", CATALOG, [], [])
    assert model == "opencode/nemotron-3-ultra-free"


def test_disabled_use_balance_with_evidence_allows_included_go(monkeypatch) -> None:
    _clear_authority(monkeypatch)
    monkeypatch.setenv("DEALIX_OPENCODE_GO_USE_BALANCE", "disabled")
    monkeypatch.setenv(
        "DEALIX_OPENCODE_GO_COST_AUTHORITY_REF",
        "provider-console-receipt:use-balance-disabled",
    )
    authority = broker.provider_cost_authority()
    assert authority["state"] == broker.GO_COST_VERIFIED_DISABLED
    assert authority["automatic_go_allowed"] is True
    assert broker.pick_model("R4_INCLUDED_HIGH", CATALOG, [], []) == (
        "opencode-go/deepseek-v4.1-flash"
    )


def test_enabled_use_balance_never_counts_as_zero_cost_authority(monkeypatch) -> None:
    _clear_authority(monkeypatch)
    monkeypatch.setenv("DEALIX_OPENCODE_GO_USE_BALANCE", "enabled")
    monkeypatch.setenv(
        "DEALIX_OPENCODE_GO_COST_AUTHORITY_REF",
        "provider-console-receipt:use-balance-enabled",
    )
    authority = broker.provider_cost_authority()
    assert authority["state"] == broker.GO_COST_VERIFIED_ENABLED
    assert authority["automatic_go_allowed"] is False
    assert broker.pick_model("R4_INCLUDED_HIGH", CATALOG, [], []) == (
        "opencode/nemotron-3-ultra-free"
    )


def test_unreferenced_local_flag_is_not_provider_evidence(monkeypatch) -> None:
    _clear_authority(monkeypatch)
    monkeypatch.setenv("DEALIX_OPENCODE_GO_USE_BALANCE", "disabled")
    authority = broker.provider_cost_authority()
    assert authority["state"] == broker.GO_COST_UNKNOWN
    assert authority["evidence_present"] is False


def test_local_daily_envelope_is_telemetry_not_subscription_authority() -> None:
    state = {
        "jobs": [
            {
                "recorded_at": "2026-09-12T00:00:00+00:00",
                "route": "R4_INCLUDED_HIGH",
            }
            for _ in range(broker.MAX_DAILY_INCLUDED_JOBS)
        ]
    }
    envelope = broker.daily_envelope(state)
    assert envelope["included_jobs_remaining"] == 0
    assert envelope["headroom_source"] == (
        "local_telemetry_only__provider_limits_are_authoritative"
    )


def test_status_reports_cost_authority_without_exposing_reference(monkeypatch) -> None:
    _clear_authority(monkeypatch)
    monkeypatch.setenv("DEALIX_OPENCODE_GO_USE_BALANCE", "disabled")
    monkeypatch.setenv("DEALIX_OPENCODE_GO_COST_AUTHORITY_REF", "sensitive-reference")
    monkeypatch.setattr(broker, "discover_opencode", lambda: {"binary": "UNKNOWN", "name": "UNKNOWN", "version": "UNKNOWN"})
    monkeypatch.setattr(broker, "discover_router_models", lambda: [])
    monkeypatch.setattr(broker, "discover_ollama_models", lambda: [])
    monkeypatch.setattr(broker, "load_state", lambda: {"jobs": []})
    status = broker.status_payload()
    authority = status["provider_cost_authority"]
    assert authority == {
        "state": broker.GO_COST_VERIFIED_DISABLED,
        "use_balance": "DISABLED",
        "evidence_present": True,
        "automatic_go_allowed": True,
    }
    assert "sensitive-reference" not in repr(status)
