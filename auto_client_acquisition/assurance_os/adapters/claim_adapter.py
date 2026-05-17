"""Adapter over the claim policy (claim_policy.yaml + trust doctrine)."""
from __future__ import annotations

from auto_client_acquisition.assurance_os.adapters.base import BaseAdapter
from auto_client_acquisition.assurance_os.config_loader import load_config
from auto_client_acquisition.assurance_os.models import AdapterResult


class ClaimAdapter(BaseAdapter):
    source = "assurance_os.config.claim_policy"

    def non_negotiables(self) -> AdapterResult:
        cfg = load_config()
        items = cfg.claim_policy.get("non_negotiables") or []
        if not items:
            return self.unknown("claim_policy.yaml not loaded")
        return self.ok(items, "claim_policy.non_negotiables")

    def forbidden_claims(self) -> AdapterResult:
        cfg = load_config()
        items = cfg.claim_policy.get("forbidden_claims") or []
        if not items:
            return self.unknown("claim_policy.yaml not loaded")
        return self.ok(items, "claim_policy.forbidden_claims")

    def escalation_triggers(self) -> AdapterResult:
        cfg = load_config()
        items = cfg.claim_policy.get("escalation_triggers") or []
        if not items:
            return self.unknown("claim_policy.yaml not loaded")
        return self.ok(items, "claim_policy.escalation_triggers")
