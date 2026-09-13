"""Evidence-driven Dealix expansion planning.

Growth expands depth, proof and economic coverage first. New sectors/arms are added
only when fresh evidence justifies a canonical registry change; fixed doubling is
not a company objective.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from dealix.commercial.comprehensive_launch import ComprehensiveLaunch
from dealix.commercial.launch_readiness import check as check_launch


class NextExpansion:
    def execute(self) -> dict[str, Any]:
        readiness = check_launch()
        comprehensive = ComprehensiveLaunch().launch()

        current_sectors = readiness.sector_companies
        current_arms = readiness.arms_active
        return {
            "current_sectors": current_sectors,
            "current_arms": current_arms,
            # Compatibility keys remain numeric, but no arbitrary 2x target is minted.
            "next_sectors_target": current_sectors,
            "next_arms_target": current_arms,
            "readiness": readiness.overall,
            "comprehensive_sectors": comprehensive["sectors_launched"],
            "logical_agents": readiness.logical_agents,
            "arm_pods": readiness.arm_pods,
            "resource_governor_dynamic": readiness.resource_governor_dynamic,
            "runtime_acceptance": readiness.runtime_acceptance,
            "generated_at": datetime.now(UTC).isoformat(),
            "expansion_mode": "EVIDENCE_DRIVEN_REGISTRY_GROWTH",
            "next_action": (
                "Improve economic depth, proof, diagnostics, delivery and distribution across the current canonical registry; "
                "add a sector or arm only when fresh market/customer evidence justifies the canonical registry change; "
                "allocate runtime workers dynamically through ResourceGovernor."
            ),
        }


__all__ = ["NextExpansion"]
