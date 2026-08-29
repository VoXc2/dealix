"""Fail-closed runtime switches for Dealix side-effect capabilities.

This module is deliberately *not* an authority engine. Commercial/Governance
contracts decide whether an action is authorized. Runtime flags may only reduce
that pre-existing authority. A missing SDK, missing provider, provider error, or
missing flag therefore returns ``False`` for the effective action.

OpenFeature is an optional adapter. The canonical Dealix authority/truth owners
remain unchanged, and this module creates no scheduler, service, database, or
remote control plane.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Final

SENSITIVE_SWITCHES: Final[tuple[str, ...]] = (
    "external_send",
    "public_publish",
    "paid_spend",
    "live_payment",
    "production_mutation",
    "connector_write",
    "cloud_model_route",
    "experimental_agent_workload",
    "personal_linkedin_automation",
    "whatsapp_outbound",
)

Evaluator = Callable[[str, bool], bool]


def _openfeature_boolean(flag_key: str, default: bool) -> bool:
    """Evaluate one OpenFeature flag, failing closed on every unavailable path."""

    try:
        from openfeature import api

        client = api.get_client(domain="dealix-runtime-controls")
        return bool(client.get_boolean_value(flag_key, default))
    except Exception:
        # Runtime controls are a safety layer. Provider/SDK failure may reduce
        # authority, never increase it.
        return False


@dataclass(frozen=True)
class RuntimeSwitchDecision:
    flag_key: str
    authority_allows: bool
    runtime_switch_allows: bool
    effective_allowed: bool
    reason: str


class RuntimeSwitchGate:
    """Combine canonical authority with a runtime-lowering switch.

    ``authority_allows`` MUST come from the canonical Commercial/Governance
    decision. A feature flag can never turn a denied action into an allowed one.
    """

    def __init__(self, evaluator: Evaluator | None = None) -> None:
        self._evaluator = evaluator or _openfeature_boolean

    def evaluate(self, flag_key: str, *, authority_allows: bool) -> RuntimeSwitchDecision:
        if flag_key not in SENSITIVE_SWITCHES:
            raise ValueError(f"unsupported Dealix runtime switch: {flag_key}")

        if not authority_allows:
            return RuntimeSwitchDecision(
                flag_key=flag_key,
                authority_allows=False,
                runtime_switch_allows=False,
                effective_allowed=False,
                reason="DENIED_BY_CANONICAL_AUTHORITY",
            )

        try:
            runtime_allows = bool(self._evaluator(flag_key, False))
        except Exception:
            runtime_allows = False

        return RuntimeSwitchDecision(
            flag_key=flag_key,
            authority_allows=True,
            runtime_switch_allows=runtime_allows,
            effective_allowed=runtime_allows,
            reason=("ALLOWED_BY_AUTHORITY_AND_RUNTIME_SWITCH" if runtime_allows else "LOWERED_BY_RUNTIME_SWITCH"),
        )

    def allowed(self, flag_key: str, *, authority_allows: bool) -> bool:
        return self.evaluate(flag_key, authority_allows=authority_allows).effective_allowed


__all__ = [
    "RuntimeSwitchDecision",
    "RuntimeSwitchGate",
    "SENSITIVE_SWITCHES",
]
