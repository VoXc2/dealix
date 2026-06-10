"""Weekly cross-OS snapshot — merges finance, delivery risk, flywheel, reliability drill posture."""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.delivery_os.control_tower import (
    DeliveryRisk,
    compute_delivery_risk_score,
    delivery_risk_band,
)
from auto_client_acquisition.operating_finance_os.lifecycle_unit_economics import (
    LifecycleEconomicsInputs,
    compute_lifecycle_economics,
)
from auto_client_acquisition.reliability_os.mission_critical_program import (
    DrillResult,
    compute_mission_critical_score,
)
from auto_client_acquisition.revenue_os.data_flywheel import FlywheelInputs, compute_flywheel_score


@dataclass(frozen=True, slots=True)
class WeeklyCrossOsSnapshot:
    """Structured inputs for weekly executive review (GTM + finance + delivery + platform signals)."""

    gross_margin_pct: float
    contribution_margin_sar: float
    ltv_sar: float
    cac_payback_months: float
    delivery_risk_score: int
    delivery_risk_band: str
    flywheel_overall: float
    flywheel_band: str
    reliability_posture_score: float
    reliability_posture_status: str
    gtm_discovery_to_pilot_conversion_pct: float


def weekly_cross_os_snapshot(
    *,
    economics: LifecycleEconomicsInputs | None = None,
    delivery_risk: DeliveryRisk | None = None,
    flywheel: FlywheelInputs | None = None,
    drills: tuple[DrillResult, ...] | None = None,
    slo_breaches_open: int = 0,
    gtm_discovery_to_pilot_conversion_pct: float = 0.0,
) -> WeeklyCrossOsSnapshot:
    """Build a deterministic weekly snapshot from operational inputs (defaults are placeholders until telemetry wires in)."""
    econ = economics or LifecycleEconomicsInputs(
        monthly_revenue_sar=15000.0,
        monthly_delivery_cost_sar=8500.0,
        acquisition_cost_sar=12000.0,
        retention_months=10.0,
        expansion_revenue_sar=6000.0,
    )
    snap_econ = compute_lifecycle_economics(econ)

    risk = delivery_risk or DeliveryRisk(
        engagement_id="weekly_aggregate",
        blocker_count=1,
        quality_exceptions=0,
        governance_exceptions=0,
        schedule_delay_days=2,
    )
    dr_score = compute_delivery_risk_score(risk)
    dr_band = delivery_risk_band(dr_score)

    fw = flywheel or FlywheelInputs(
        source_reliability=82.0,
        dedupe_precision=86.0,
        signal_freshness=80.0,
        actionability_precision=78.0,
        outcome_conversion=70.0,
        learning_adoption=74.0,
    )
    fw_score = compute_flywheel_score(fw)

    drill_tuple = drills or (
        DrillResult("rollback", True),
        DrillResult("kill_switch", True),
        DrillResult("approval_center", True),
    )
    mission = compute_mission_critical_score(drill_tuple, slo_breaches_open=slo_breaches_open)

    return WeeklyCrossOsSnapshot(
        gross_margin_pct=snap_econ.gross_margin_pct,
        contribution_margin_sar=snap_econ.contribution_margin_sar,
        ltv_sar=snap_econ.ltv_sar,
        cac_payback_months=snap_econ.cac_payback_months,
        delivery_risk_score=dr_score,
        delivery_risk_band=dr_band,
        flywheel_overall=fw_score.overall,
        flywheel_band=fw_score.band,
        reliability_posture_score=mission.score,
        reliability_posture_status=mission.status,
        gtm_discovery_to_pilot_conversion_pct=float(gtm_discovery_to_pilot_conversion_pct),
    )


__all__ = ["WeeklyCrossOsSnapshot", "weekly_cross_os_snapshot"]
