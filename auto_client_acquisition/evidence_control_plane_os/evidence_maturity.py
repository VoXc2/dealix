"""Evidence Maturity Levels — L0..L5."""

from __future__ import annotations

from enum import IntEnum


class EvidenceMaturityLevel(IntEnum):
    L0_NO_EVIDENCE = 0
    L1_BASIC_LOGS = 1
    L2_GOVERNANCE_EVIDENCE = 2
    L3_APPROVAL_AND_PROOF = 3
    L4_ENTERPRISE_EVIDENCE_CONTROL_PLANE = 4
    L5_CONTINUOUS_TRUST_OS = 5


EVIDENCE_MATURITY_LEVELS: tuple[EvidenceMaturityLevel, ...] = tuple(EvidenceMaturityLevel)
