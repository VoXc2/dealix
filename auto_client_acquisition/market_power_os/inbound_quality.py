"""Inbound quality — ICP + risk composite."""

from __future__ import annotations


def inbound_quality_score(*, icp_fit: int, client_risk: int) -> int:
    icp_c = max(0, min(100, icp_fit))
    risk_c = max(0, min(100, client_risk))
    return max(0, min(100, icp_c - risk_c // 2))


__all__ = ["inbound_quality_score"]
