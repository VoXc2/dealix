"""Proof strength score — deterministic readiness from canonical Proof Pack v2 sections."""

from __future__ import annotations

from collections.abc import Mapping

from auto_client_acquisition.proof_architecture_os.proof_pack_v2 import PROOF_PACK_V2_SECTIONS


def proof_pack_completeness_score(content_by_section: Mapping[str, str]) -> int:
    """0–100 from share of non-empty v2 sections (no LLM)."""
    if not PROOF_PACK_V2_SECTIONS:
        return 0
    filled = sum(1 for k in PROOF_PACK_V2_SECTIONS if (content_by_section.get(k) or "").strip())
    return round(100.0 * filled / len(PROOF_PACK_V2_SECTIONS))


def proof_strength_band(score: int) -> str:
    """Aligns with commercial proof ladder (internal sales / case gating)."""
    if score >= 85:
        return "case_candidate"
    if score >= 70:
        return "sales_support"
    if score >= 55:
        return "internal_learning"
    return "weak_proof"


def proof_pack_score_with_governance_penalty(
    content_by_section: Mapping[str, str],
    *,
    governance_blocked: bool,
) -> int:
    """If a governance BLOCK applies, cap score so weak proof cannot masquerade as case-ready."""
    base = proof_pack_completeness_score(content_by_section)
    if governance_blocked:
        return min(base, 69)
    return base


__all__ = [
    "proof_pack_completeness_score",
    "proof_pack_score_with_governance_penalty",
    "proof_strength_band",
]
