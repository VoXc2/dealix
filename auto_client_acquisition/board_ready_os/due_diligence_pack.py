"""Due diligence pack — artifact checklist for investor / enterprise review."""

from __future__ import annotations

DUE_DILIGENCE_ARTIFACTS: tuple[str, ...] = (
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


def due_diligence_pack_coverage_score(artifacts_present: frozenset[str]) -> int:
    if not DUE_DILIGENCE_ARTIFACTS:
        return 0
    n = sum(1 for a in DUE_DILIGENCE_ARTIFACTS if a in artifacts_present)
    return (n * 100) // len(DUE_DILIGENCE_ARTIFACTS)
