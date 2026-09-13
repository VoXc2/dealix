"""Comprehensive Omega V3 source-execution snapshot.

Sector/arm counts are observations of the canonical registries, never permanent
architecture targets. Runtime capacity is governed independently by the
ResourceGovernor and exact execution authority.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from dealix.commercial.expanded_launch_executor import ExpandedLaunchExecutor
from dealix.commercial.launch_readiness import check as check_launch
from dealix.commercial.saudi_market_radar import SaudiMarketRadar


class ComprehensiveLaunch:
    def launch(self) -> dict[str, Any]:
        readiness = check_launch()

        # Internal research signals only; they never imply a relationship,
        # qualification, consent, compliance defect, pipeline or revenue.
        radar = SaudiMarketRadar()
        radar.zatca_wave25_signal()
        radar.misa_invest_saudi_signal()
        radar.pdpl_signal()

        result = ExpandedLaunchExecutor().execute()
        return {
            # Compatibility keys consumed by existing internal callers.
            "sectors_launched": result["sectors_launched"],
            "arms_active": result["arms_active"],
            "tenants": result["tenants"],
            "cells": result["cells"],
            "readiness_overall": readiness.overall,
            "radar_signals": len(radar.signals),
            "radar_fresh": len(radar.list_fresh()),
            "generated_at": datetime.now(UTC).isoformat(),
            # Canonical truth additions.
            "sector_companies_observed": readiness.sector_companies,
            "active_arms_observed": readiness.arms_active,
            "logical_agents_observed": readiness.logical_agents,
            "arm_pods_observed": readiness.arm_pods,
            "resource_governor_dynamic": readiness.resource_governor_dynamic,
            "runtime_acceptance": readiness.runtime_acceptance,
            "deployed_release_identity": readiness.deployed_release_identity,
            "counts_are_architecture_authority": False,
            "market_control": "registry-derived sector/arm coverage + evidence-gated economic prioritization + ResourceGovernor-bounded execution",
        }


__all__ = ["ComprehensiveLaunch"]
