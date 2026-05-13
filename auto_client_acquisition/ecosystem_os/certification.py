"""Certification levels — 5-step path."""

from __future__ import annotations

from enum import IntEnum


class CertificationLevel(IntEnum):
    DEALIX_AWARE = 1
    DEALIX_OPERATOR = 2
    DEALIX_IMPLEMENTER = 3
    CERTIFIED_PARTNER = 4
    STRATEGIC_PARTNER = 5


CERTIFICATION_LEVELS: tuple[CertificationLevel, ...] = tuple(CertificationLevel)
