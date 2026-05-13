"""Due Diligence Pack — 15-section checklist."""

from __future__ import annotations

from dataclasses import dataclass


DUE_DILIGENCE_SECTIONS: tuple[str, ...] = (
    "investment_thesis",
    "market_thesis",
    "productized_offers",
    "core_os_architecture",
    "governance_runtime",
    "agent_control_plane",
    "data_trust_architecture",
    "proof_pack_standard",
    "capital_ledger",
    "productization_ledger",
    "business_unit_model",
    "enterprise_trust_pack",
    "risk_register",
    "financial_model",
    "roadmap",
)


@dataclass(frozen=True)
class DueDiligencePack:
    sections_present: frozenset[str]


@dataclass(frozen=True)
class DueDiligenceResult:
    complete: bool
    missing: tuple[str, ...]


def evaluate_due_diligence_pack(pack: DueDiligencePack) -> DueDiligenceResult:
    missing = tuple(s for s in DUE_DILIGENCE_SECTIONS if s not in pack.sections_present)
    return DueDiligenceResult(complete=not missing, missing=missing)
