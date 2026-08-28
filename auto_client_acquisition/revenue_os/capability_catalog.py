"""V17 Repo Capability Miner — canonical capability catalog loader.

Loads ``data/commercial/capability_catalog.yaml`` and cross-validates every
record against the canonical 17-offering registry
(``auto_client_acquisition.service_catalog.registry``). A capability record
is only trusted when:

- ``capability_id`` exists in the canonical registry (or is an explicitly
  allowed non-offering entry, e.g. bundled sub-modules);
- every offer reference (entry_offer / primary_paid_offer / expansion_offer)
  resolves to a real registry id;
- ``claims_blocked`` contains the doctrine non-negotiables.

This module is pure and deterministic (no I/O beyond reading the YAML data
file, no LLM, no network, no DB). It never invents capabilities: a record
without executable evidence cannot be loaded.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from auto_client_acquisition.service_catalog.registry import (
    OFFERINGS,
    SERVICE_IDS,
    get_offering,
)

_CATALOG_PATH = Path(__file__).resolve().parents[2] / "data" / "commercial" / "capability_catalog.yaml"

# Non-negotiable claims every capability must block (mirrors safe_send_gateway
# doctrine + registry hard gates). These are the V17 red lines.
_REQUIRED_BLOCKED_CLAIMS = frozenset(
    {
        "guaranteed_revenue",
        "cold_whatsapp",
        "linkedin_automation",
    }
)

# Capability ids that are valid sub-module/bundle entries but not standalone
# registry offerings (bundles reference these; the loader tolerates them).
_ALLOWED_NON_OFFER_IDS = frozenset(
    {
        "proposal_factory",
        "proof_pack_factory",
        "weekly_revenue_command",
        "support_triage_draft_os",
        "data_pack",
        "revenue_ops",
        "diagnostic",
    }
)


class CapabilityCatalogError(ValueError):
    """Raised when the capability catalog fails validation."""


class Capability:
    """One validated capability record (read-only view)."""

    __slots__ = ("_data",)

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    @property
    def capability_id(self) -> str:
        return str(self._data["capability_id"])

    @property
    def name_en(self) -> str:
        return str(self._data.get("name_en", ""))

    @property
    def name_ar(self) -> str:
        return str(self._data.get("name_ar", ""))

    @property
    def primary_paid_offer(self) -> str:
        return str(self._data.get("primary_paid_offer", ""))

    @property
    def entry_offer(self) -> str:
        return str(self._data.get("entry_offer", ""))

    @property
    def buyer_pain(self) -> list[str]:
        raw = self._data.get("buyer_pain", [])
        return [raw] if isinstance(raw, str) else list(raw)

    @property
    def icp_segments(self) -> list[str]:
        raw = self._data.get("icp_segments", [])
        return list(raw)

    @property
    def trigger_signals(self) -> list[str]:
        raw = self._data.get("trigger_signals", [])
        return list(raw)

    @property
    def evidence_paths(self) -> list[str]:
        return list(self._data.get("evidence_paths", []))

    @property
    def proof_gaps(self) -> list[str]:
        return list(self._data.get("proof_gaps", []))

    @property
    def proof_available(self) -> list[str]:
        return list(self._data.get("proof_available", []))

    @property
    def claims_blocked(self) -> list[str]:
        return list(self._data.get("claims_blocked", []))

    @property
    def claims_allowed(self) -> list[str]:
        return list(self._data.get("claims_allowed", []))

    @property
    def productization_potential(self) -> str:
        return str(self._data.get("productization_potential", "low"))

    @property
    def data(self) -> dict[str, Any]:
        return dict(self._data)

    def to_dict(self) -> dict[str, Any]:
        return self._data


def _listify(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


def _validate(capabilities: list[dict[str, Any]]) -> list[str]:
    """Return a list of validation errors (empty when the catalog is valid)."""
    errors: list[str] = []
    seen: set[str] = set()
    for i, cap in enumerate(capabilities):
        cap_id = str(cap.get("capability_id") or "").strip()
        if not cap_id:
            errors.append(f"capability[{i}]: missing capability_id")
            continue
        if cap_id in seen:
            errors.append(f"capability[{i}]: duplicate capability_id {cap_id!r}")
        seen.add(cap_id)

        # 1. capability_id must exist in the canonical registry or be an allowed bundle id.
        if cap_id not in SERVICE_IDS and cap_id not in _ALLOWED_NON_OFFER_IDS:
            errors.append(
                f"capability_id {cap_id!r} is not a canonical registry offering "
                f"(registry ids: {sorted(SERVICE_IDS)})"
            )

        # 2. All offer references must resolve.
        for field in ("entry_offer", "primary_paid_offer"):
            offer = str(cap.get(field) or "").strip()
            if offer and offer not in SERVICE_IDS:
                errors.append(f"{cap_id}.{field}: unknown offer {offer!r}")
        for offer in _listify(cap.get("expansion_offer")):
            if offer and offer not in SERVICE_IDS:
                errors.append(f"{cap_id}.expansion_offer: unknown offer {offer!r}")

        # 3. Evidence paths must be non-empty — no capability without evidence.
        evidence = _listify(cap.get("evidence_paths"))
        if not evidence:
            errors.append(f"{cap_id}: no evidence_paths (capability cannot be loaded)")

        # 4. Doctrine non-negotiables must be blocked.
        blocked = {str(c).strip() for c in _listify(cap.get("claims_blocked"))}
        missing = _REQUIRED_BLOCKED_CLAIMS - blocked
        if missing:
            errors.append(f"{cap_id}: missing blocked claims {sorted(missing)}")

        # 5. Explicit proof gap honesty: no customer proof may be claimed.
        proof_available = {str(p) for p in _listify(cap.get("proof_available"))}
        for bad in ("customer_proof", "customer_case", "verified_customer"):
            if any(bad in p for p in proof_available):
                errors.append(
                    f"{cap_id}: proof_available must not claim customer proof ({bad!r})"
                )
    return errors


def load_capability_catalog(
    path: str | Path | None = None,
    *,
    _strict: bool = True,
) -> list[Capability]:
    """Load and validate the V17 capability catalog.

    Raises :class:`CapabilityCatalogError` on any validation failure so a
    broken catalog can never silently feed targeting or deal-desk logic.
    """
    p = Path(path) if path else _CATALOG_PATH
    if not p.exists():
        raise CapabilityCatalogError(f"capability catalog not found: {p}")
    with p.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    capabilities = data.get("capabilities") or []
    if not isinstance(capabilities, list):
        raise CapabilityCatalogError("capability catalog must contain a list under 'capabilities'")

    errors = _validate(capabilities)
    if errors and _strict:
        raise CapabilityCatalogError("capability catalog validation failed:\n- " + "\n- ".join(errors))
    return [Capability(c) for c in capabilities]


def get_capability(capability_id: str, *, catalog: list[Capability] | None = None) -> Capability | None:
    caps = catalog if catalog is not None else load_capability_catalog()
    for cap in caps:
        if cap.capability_id == capability_id:
            return cap
    return None


def capabilities_for_pain(pain: str, *, catalog: list[Capability] | None = None) -> list[Capability]:
    """All capabilities whose buyer_pain includes ``pain`` (deterministic)."""
    caps = catalog if catalog is not None else load_capability_catalog()
    return [c for c in caps if pain in c.buyer_pain]


def capabilities_for_icp(segment: str, *, catalog: list[Capability] | None = None) -> list[Capability]:
    """All capabilities whose ICP segments include ``segment`` (deterministic)."""
    caps = catalog if catalog is not None else load_capability_catalog()
    return [c for c in caps if segment in c.icp_segments]


def canonical_registry_ids() -> frozenset[str]:
    return SERVICE_IDS


def offering_summary(offer_id: str) -> dict[str, Any] | None:
    offering = get_offering(offer_id)
    if offering is None:
        return None
    return {
        "id": offering.id,
        "name_ar": offering.name_ar,
        "name_en": offering.name_en,
        "price_sar": offering.price_sar,
        "customer_journey_stage": offering.customer_journey_stage,
        "commercial_status": offering.commercial_status,
        "action_modes_used": list(offering.action_modes_used),
        "hard_gates": list(offering.hard_gates),
    }


__all__ = [
    "Capability",
    "CapabilityCatalogError",
    "canonical_registry_ids",
    "capabilities_for_icp",
    "capabilities_for_pain",
    "get_capability",
    "load_capability_catalog",
    "offering_summary",
]
