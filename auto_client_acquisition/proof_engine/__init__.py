"""Proof Engine — مستويات الأدلة وحوكمة النشر."""

from __future__ import annotations

from auto_client_acquisition.proof_engine.evidence import (
    EVIDENCE_LEVEL_DESCRIPTIONS_AR,
    EVIDENCE_LEVEL_DESCRIPTIONS_EN,
    EvidenceLevel,
    assert_public_proof_allowed,
)

__all__ = [
    "EVIDENCE_LEVEL_DESCRIPTIONS_AR",
    "EVIDENCE_LEVEL_DESCRIPTIONS_EN",
    "EvidenceLevel",
    "assert_public_proof_allowed",
]
