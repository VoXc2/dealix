"""Enterprise Trust Engine — component coverage for institutional deals."""

from __future__ import annotations

TRUST_ENGINE_COMPONENTS: tuple[str, ...] = (
    "source_passport",
    "data_quality_score",
    "pii_detection",
    "allowed_use_registry",
    "llm_gateway",
    "agent_control_plane",
    "governance_runtime",
    "approval_engine",
    "audit_trail",
    "proof_pack",
    "incident_response",
)


def trust_engine_coverage_score(components_implemented: frozenset[str]) -> int:
    """Share of Trust Engine components present (0–100)."""
    if not TRUST_ENGINE_COMPONENTS:
        return 0
    n = sum(1 for c in TRUST_ENGINE_COMPONENTS if c in components_implemented)
    return (n * 100) // len(TRUST_ENGINE_COMPONENTS)
