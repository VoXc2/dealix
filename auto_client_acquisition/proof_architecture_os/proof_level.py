"""Proof Levels 1..5 — Activity / Output / Quality / Business Value / Operating Capability."""

from __future__ import annotations

from enum import IntEnum


class ProofLevel(IntEnum):
    ACTIVITY = 1
    OUTPUT = 2
    QUALITY = 3
    BUSINESS_VALUE = 4
    OPERATING_CAPABILITY = 5


PROOF_LEVELS: tuple[ProofLevel, ...] = tuple(ProofLevel)
