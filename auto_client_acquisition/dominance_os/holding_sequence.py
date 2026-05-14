"""Holding creation sequence tracking."""

from __future__ import annotations

HOLDING_SEQUENCE_STEP_IDS: tuple[str, ...] = (
    "prove_revenue_intelligence",
    "productize_data_revenue_proof",
    "convert_to_monthly_revops",
    "build_client_workspace",
    "add_company_brain_and_governance",
    "create_revenue_bu",
    "create_governance_bu",
    "launch_dealix_method_publicly",
    "build_partner_program",
    "launch_academy",
    "identify_vertical_venture",
    "launch_dealix_cloud_modules",
    "formalize_dealix_group",
)


def holding_sequence_progress(completed: set[str]) -> float:
    """Ratio 0-100 of completed holding steps."""
    unknown = completed - set(HOLDING_SEQUENCE_STEP_IDS)
    if unknown:
        raise ValueError(f"Unknown holding steps: {sorted(unknown)}")
    if not HOLDING_SEQUENCE_STEP_IDS:
        return 100.0
    return round(len(completed) / len(HOLDING_SEQUENCE_STEP_IDS) * 100.0, 2)
