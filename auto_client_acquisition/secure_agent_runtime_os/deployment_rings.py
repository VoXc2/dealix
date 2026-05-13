"""Deployment Rings 0..5."""

from __future__ import annotations

from enum import IntEnum


class DeploymentRing(IntEnum):
    RING_0_LOCAL_SANDBOX = 0
    RING_1_INTERNAL_SYNTHETIC = 1
    RING_2_INTERNAL_NON_SENSITIVE = 2
    RING_3_CLIENT_DRAFT_ONLY = 3
    RING_4_RETAINER_WITH_APPROVAL = 4
    RING_5_ENTERPRISE_CONTROLLED = 5


DEPLOYMENT_RINGS: tuple[DeploymentRing, ...] = tuple(DeploymentRing)
