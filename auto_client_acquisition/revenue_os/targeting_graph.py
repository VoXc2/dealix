"""V17 Targeting Graph — capability → pain → ICP → persona → signal → offer.

Deterministic graph derived from canonical commercial truth:

- ``data/commercial/capability_catalog.yaml``  (V17 capability records)
- ``data/commercial/pain_to_offer.yaml``      (pain -> offer mapping)
- ``data/commercial/icp_segments.yaml``       (ICP segments)
- ``auto_client_acquisition.service_catalog.registry`` (canonical offerings)

The graph answers: for a given account signal / pain / ICP segment, which
capabilities apply, what is the entry offer, the paid offer, and the
expansion path. It never invents edges: every pain and every ICP segment is
cross-validated against the canonical YAML sources; unknown values are
reported as validation errors rather than silently accepted.

Pure, deterministic, no I/O at import time (files are read lazily), no LLM,
no network, no DB.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from auto_client_acquisition.revenue_os.capability_catalog import (
    Capability,
    load_capability_catalog,
)

_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "commercial"

# Canonical pain ids from pain_to_offer.yaml primary_mapping.
_CANONICAL_PAINS: frozenset[str] = frozenset(
    {
        "lead_leakage",
        "follow_up_chaos",
        "crm_data_disorder",
        "proposal_delay",
        "weak_reporting",
        "sales_team_inconsistency",
        "support_overload",
        "no_proof_case_study_system",
        "slow_onboarding",
        "weak_renewal_upsell",
    }
)

# Canonical ICP segment ids from icp_segments.yaml.
_CANONICAL_ICP_SEGMENTS: frozenset[str] = frozenset(
    {
        "real_estate",
        "clinic",
        "logistics",
        "training",
        "marketing_agency",
        "b2b_services",
    }
)

# Canonical persona classes (from capability catalog buyer_persona fields).
_PERSONA_CANONICAL: frozenset[str] = frozenset(
    {
        "founder_or_gm_without_clear_priority",
        "founder_or_gm_with_identifiable_revenue_ops_pain",
        "sales_lead_with_messy_lead_data",
        "founder_or_ops_lead_wanting_ongoing_cadence",
        "customer_success_or_support_lead",
        "ceo_gm_needing_daily_visibility",
        "agency_or_consultancy_owner",
        "ceo_gm_of_20_200_person_company",
        "sales_lead_with_whatsapp_pipeline",
        "marketing_or_founder_owner",
        "ops_lead_with_repetitive_workflows",
        "customer_success_lead",
        "ops_lead_or_coo",
        "ceo_gm_or_board_owner",
        "compliance_or_trust_owner",
        "founder_or_cmo",
        "enterprise_owner_with_unique_workflows",
    }
)

# Persona → typical role titles used in outreach/message drafting.
PERSONA_ROLE_HINTS: dict[str, tuple[str, ...]] = {
    "founder_or_gm_without_clear_priority": ("Founder", "General Manager"),
    "founder_or_gm_with_identifiable_revenue_ops_pain": ("Founder", "GM", "Sales Director"),
    "sales_lead_with_messy_lead_data": ("Sales Manager", "BD Manager"),
    "founder_or_ops_lead_wanting_ongoing_cadence": ("Founder", "Operations Manager"),
    "customer_success_or_support_lead": ("Customer Success Manager", "Support Manager"),
    "ceo_gm_needing_daily_visibility": ("CEO", "GM", "COO"),
    "agency_or_consultancy_owner": ("Agency Owner", "Consultancy Partner"),
    "ceo_gm_of_20_200_person_company": ("CEO", "GM"),
    "sales_lead_with_whatsapp_pipeline": ("Sales Manager", "Sales Operations"),
    "marketing_or_founder_owner": ("CMO", "Marketing Manager", "Founder"),
    "ops_lead_with_repetitive_workflows": ("Operations Manager", "COO"),
    "customer_success_lead": ("Customer Success Lead"),
    "ops_lead_or_coo": ("COO", "Operations Director"),
    "ceo_gm_or_board_owner": ("CEO", "GM", "Board Member"),
    "compliance_or_trust_owner": ("Compliance Officer", "Risk Manager"),
    "founder_or_cmo": ("Founder", "CMO"),
    "enterprise_owner_with_unique_workflows": ("CEO", "COO", "Transformation Lead"),
}


class TargetingGraphError(ValueError):
    """Raised when the targeting graph cannot be built from canonical truth."""


@dataclass(frozen=True, slots=True)
class TargetingEdge:
    """One canonical targeting edge."""

    capability_id: str
    pain: str
    icp_segment: str
    persona: str
    entry_offer: str
    primary_paid_offer: str
    expansion_offers: tuple[str, ...]
    trigger_signals: tuple[str, ...]
    evidence_paths: tuple[str, ...]
    proof_gaps: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "pain": self.pain,
            "icp_segment": self.icp_segment,
            "persona": self.persona,
            "entry_offer": self.entry_offer,
            "primary_paid_offer": self.primary_paid_offer,
            "expansion_offers": list(self.expansion_offers),
            "trigger_signals": list(self.trigger_signals),
            "evidence_paths": list(self.evidence_paths),
            "proof_gaps": list(self.proof_gaps),
        }


def _load_pain_to_offer() -> dict[str, Any]:
    path = _DATA_DIR / "pain_to_offer.yaml"
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def _load_icp_segments() -> dict[str, Any]:
    path = _DATA_DIR / "icp_segments.yaml"
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def _load_product_catalog() -> dict[str, Any]:
    path = _DATA_DIR / "product_catalog.yaml"
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def canonical_pains() -> frozenset[str]:
    """Pain ids from the canonical pain_to_offer.yaml."""
    data = _load_pain_to_offer()
    pains = {str(p["pain"]) for p in data.get("primary_mapping", []) if isinstance(p, dict)}
    return frozenset(pains | _CANONICAL_PAINS)


def canonical_icp_segments() -> frozenset[str]:
    """ICP segment ids from the canonical icp_segments.yaml."""
    data = _load_icp_segments()
    segments = {str(s["id"]) for s in data.get("segments", []) if isinstance(s, dict)}
    return frozenset(segments | _CANONICAL_ICP_SEGMENTS)


def canonical_personas() -> frozenset[str]:
    return _PERSONA_CANONICAL


def build_targeting_graph(
    *,
    capabilities: list[Capability] | None = None,
) -> list[TargetingEdge]:
    """Build the full deterministic targeting graph.

    One edge per (capability, pain, ICP segment) combination found in the
    capability catalog. Every pain and ICP segment is validated against the
    canonical YAML sources; unknown values raise.
    """
    caps = capabilities if capabilities is not None else load_capability_catalog()
    known_pains = canonical_pains()
    known_icp = canonical_icp_segments()

    edges: list[TargetingEdge] = []
    for cap in caps:
        for pain in cap.buyer_pain:
            if pain not in known_pains:
                raise TargetingGraphError(
                    f"capability {cap.capability_id}: unknown pain {pain!r} "
                    f"(canonical pains: {sorted(known_pains)})"
                )
            for segment in cap.icp_segments:
                if segment not in known_icp:
                    raise TargetingGraphError(
                        f"capability {cap.capability_id}: unknown ICP segment {segment!r} "
                        f"(canonical segments: {sorted(known_icp)})"
                    )
                edges.append(
                    TargetingEdge(
                        capability_id=cap.capability_id,
                        pain=pain,
                        icp_segment=segment,
                        persona=cap.data.get("buyer_persona", "unknown"),
                        entry_offer=cap.entry_offer,
                        primary_paid_offer=cap.primary_paid_offer,
                        expansion_offers=tuple(cap.data.get("expansion_offer") or []),
                        trigger_signals=tuple(cap.trigger_signals),
                        evidence_paths=tuple(cap.evidence_paths),
                        proof_gaps=tuple(cap.proof_gaps),
                    )
                )
    return edges


def graph_for_signal(
    signal: str,
    *,
    capabilities: list[Capability] | None = None,
) -> list[TargetingEdge]:
    """Edges whose trigger_signals include ``signal``."""
    edges = build_targeting_graph(capabilities=capabilities)
    return [e for e in edges if signal in e.trigger_signals]


def graph_for_pain(
    pain: str,
    *,
    capabilities: list[Capability] | None = None,
) -> list[TargetingEdge]:
    """Edges for one pain id (validated)."""
    edges = build_targeting_graph(capabilities=capabilities)
    return [e for e in edges if e.pain == pain]


def graph_for_icp(
    segment: str,
    *,
    capabilities: list[Capability] | None = None,
) -> list[TargetingEdge]:
    """Edges for one ICP segment id (validated)."""
    edges = build_targeting_graph(capabilities=capabilities)
    return [e for e in edges if e.icp_segment == segment]


def offer_path_for_capability(
    capability_id: str,
    *,
    capabilities: list[Capability] | None = None,
) -> dict[str, Any] | None:
    """Return the canonical offer path for a capability, or None."""
    caps = capabilities if capabilities is not None else load_capability_catalog()
    for cap in caps:
        if cap.capability_id == capability_id:
            return {
                "capability_id": capability_id,
                "entry_offer": cap.entry_offer,
                "primary_paid_offer": cap.primary_paid_offer,
                "expansion_offers": cap.data.get("expansion_offer") or [],
            }
    return None


def graph_summary(*, capabilities: list[Capability] | None = None) -> dict[str, int]:
    """Deterministic summary counts for the targeting graph."""
    edges = build_targeting_graph(capabilities=capabilities)
    return {
        "edges": len(edges),
        "capabilities": len({e.capability_id for e in edges}),
        "pains": len({e.pain for e in edges}),
        "icp_segments": len({e.icp_segment for e in edges}),
        "personas": len({e.persona for e in edges}),
    }


__all__ = [
    "TargetingEdge",
    "TargetingGraphError",
    "build_targeting_graph",
    "canonical_icp_segments",
    "canonical_pains",
    "canonical_personas",
    "graph_for_icp",
    "graph_for_pain",
    "graph_for_signal",
    "graph_summary",
    "offer_path_for_capability",
]
