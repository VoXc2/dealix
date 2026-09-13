"""Expanded source-execution snapshot over canonical sector/arm registries.

This helper exercises in-memory/source components only. Counts in its output are
observations of the current registries, not permanent architecture authority and
not evidence of deployed Production Green.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
import tempfile
from typing import Any

from dealix.commercial.arm_registry import get_active_arms
from dealix.commercial.economic_cell_registry import EconomicCellRegistry
from dealix.commercial.launch_readiness import check as check_launch
from dealix.commercial.saas_foundation import SaaSControlPlane, TenantTier
from dealix.commercial.saas_onboarding import SaaSOnboardingEngine
from dealix.commercial.sector_company_factory import SectorCompanyFactory


class ExpandedLaunchExecutor:
    def execute(self) -> dict[str, Any]:
        readiness = check_launch()

        sector_companies = SectorCompanyFactory().build_all()
        control_plane = SaaSControlPlane()
        onboarding = SaaSOnboardingEngine(control_plane)
        launched: list[dict[str, Any]] = []
        for company in sector_companies:
            tenant = control_plane.create_tenant(
                f"Launch-{company.sector_name_en}",
                company.sector.value,
                TenantTier.STARTER,
            )
            session = onboarding.start(tenant.name, company.sector.value, TenantTier.STARTER)
            onboarding.complete_diagnostic(session.session_id)
            launched.append(
                {
                    "sector": company.sector.value,
                    "tenant": tenant.tenant_id,
                    "diagnostic": company.diagnostic_families[:2],
                }
            )

        active_arms = get_active_arms()

        # Bounded synthetic addressable-universe sample. The requested cap is a
        # test/sample size, not a claim that Dealix architecture has exactly 500 cells.
        registry = EconomicCellRegistry(storage_path=Path(tempfile.mktemp(suffix=".jsonl")))
        cells = registry.generate_addressable_universe(max_cells=500)

        # Keep historical keys for internal callers such as ComprehensiveLaunch,
        # but their values are current observations, not fixed architecture law.
        return {
            "sectors_launched": len(sector_companies),
            "arms_active": len(active_arms),
            "tenants": len(control_plane.tenants),
            "cells": len(cells),
            "readiness_overall": readiness.overall,
            "launched": launched[:3],
            "sector_companies_observed": len(sector_companies),
            "active_arms_observed": len(active_arms),
            "synthetic_tenants": len(control_plane.tenants),
            "addressable_cells_sampled": len(cells),
            "source_readiness_overall": readiness.overall,
            "runtime_acceptance": readiness.runtime_acceptance,
            "deployed_release_identity": readiness.deployed_release_identity,
            "counts_are_architecture_authority": False,
            "generated_at": datetime.now(UTC).isoformat(),
        }


__all__ = ["ExpandedLaunchExecutor"]
