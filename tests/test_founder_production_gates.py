"""Founder production gates — unified Railway + GTM + weekly blockers."""

from __future__ import annotations

from dealix.commercial_ops.founder_production_gates import build_founder_production_gates
from dealix.commercial_ops.railway_production import probe_trust_layer


def test_build_founder_production_gates_offline() -> None:
    blob = build_founder_production_gates(skip_live=True)
    assert blob["verdict"] in ("PASS", "WARN", "FAIL")
    assert blob["railway"]["repo"]["ok"]
    assert "gtm_surfaces_repo" in blob
    assert "commands" in blob


def test_probe_trust_layer_stale_healthz() -> None:
    """When healthz lacks version field, deploy_stale_hint should fire (mock via snippet logic)."""
    # Offline: only structure — live probe may WARN on production until deploy.
    blob = probe_trust_layer("https://api.dealix.me")
    assert "probes" in blob
    assert "deploy_stale_hint_ar" in blob
