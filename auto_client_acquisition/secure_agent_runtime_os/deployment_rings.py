"""Deployment rings — progressive exposure (docs-aligned)."""

from __future__ import annotations

from enum import StrEnum


class DeploymentRing(StrEnum):
    DEV = "dev"
    STAGING = "staging"
    PRODUCTION = "production"


def production_requires_full_card(ring: DeploymentRing) -> bool:
    return ring == DeploymentRing.PRODUCTION


__all__ = ["DeploymentRing", "production_requires_full_card"]
